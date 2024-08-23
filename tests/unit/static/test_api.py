"""API tests.

These make sure components considered high or low level API are accessible.
"""

import inspect
import sys
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple
from unittest import main
from unittest import skipIf

from jsondiff import SymmetricJsonDiffSyntax
from jsondiff import diff
from jsondiff.symbols import Symbol
from trulens.core.utils.imports import is_dummy
from trulens.core.utils.serial import Lens
import yaml

from tests.test import JSONTestCase
from tests.test import optional_test
from tests.utils import Member
from tests.utils import get_class_members
from tests.utils import get_module_members
from tests.utils import get_submodule_names
from tests.utils import type_str


class TestAPI(JSONTestCase):
    """API Tests."""

    def setUp(self):
        self.pyversion = ".".join(map(str, sys.version_info[0:2]))

    def get_members(
        self, mod, aliases_are_defs: bool = False
    ) -> Dict[str, Dict[str, Member]]:
        """Get the API members of the trulens_eval module."""
        # TODEP: Deprecate after trulens_eval is removed.

        objects = {}

        classes = set()

        # Enumerate mod and all submodules.
        for modname in get_submodule_names(mod):
            mod = get_module_members(modname, aliases_are_defs=aliases_are_defs)
            if mod is None:
                continue

            highs = {}
            lows = {}

            for mem in mod.api_highs:
                if inspect.isclass(mem.val):
                    classes.add(mem.val)

                highs[mem.name] = type_str(mem.typ)

            for mem in mod.api_lows:
                if inspect.isclass(mem.val):
                    classes.add(mem.val)

                lows[mem.name] = type_str(mem.typ)

            k = modname  # + "(" + type_str(type(mod.obj)) + ")"

            objects[k] = {
                "highs": highs,
                "lows": lows,
                "__class__": type_str(type(mod.obj)),
            }
            if mod.version is not None:
                objects[k]["__version__"] = mod.version

        # Enumerate all public classes found in the prior step.
        for class_ in classes:
            if is_dummy(class_):
                with self.subTest(class_=class_.__name__):
                    self.fail(
                        f"Dummy class found in classes: {str(class_)}. Make sure all optional modules are installed before running this test."
                    )
                # Record this as a test issue but continue to the next class.
                continue

            members = get_class_members(
                class_, class_api_level="low"
            )  # api level is arbitrary

            attrs = {}

            for mem in members.api_lows:  # because of "low" above
                attrs[mem.name] = type_str(mem.typ)

            k = type_str(class_)  # + "(" + type_str(type(class_)) + ")"

            info = {
                "__class__": type_str(type(members.obj)),
                "__bases__": [type_str(base) for base in members.obj.__bases__],
                "attributes": attrs,
            }

            # if k in objects:
            #    self.assertJSONEqual(info, objects[k], path=Lens()[k])
            print(f"duplicate {k}")

            objects[k] = info

        return objects

    def get_members_trulens_eval(
        self, aliases_are_defs: bool = False
    ) -> Dict[str, Dict[str, Member]]:
        """Get the API members of the trulens_eval module."""
        # TODEP: Deprecate after trulens_eval is removed.

        import trulens_eval

        return self.get_members(trulens_eval, aliases_are_defs=aliases_are_defs)

    def get_members_trulens(self) -> Dict[str, Dict[str, Member]]:
        """Get the API members of the trulens_eval module."""

        import trulens

        return self.get_members(trulens)

    def _flatten(
        self, val: Any, lens: Optional[Lens] = None
    ) -> Iterable[Tuple[Lens, Any]]:
        """Flatten the API diff for easier comparison."""

        if lens is None:
            lens = Lens()

        if len(lens) > 1 or isinstance(val, (str, int, float, bool)):
            yield (lens, val)
        elif isinstance(val, dict):
            for k, v in val.items():
                yield from self._flatten(val=v, lens=lens[k])
        elif isinstance(val, Sequence):
            for i, v in enumerate(val):
                yield from self._flatten(val=v, lens=lens[i])
        else:
            raise ValueError(f"Unexpected type {type(val)}")

    def _flatten_api_diff(
        self, diff_value: Any, lens: Optional[Lens] = None
    ) -> Iterable[Tuple[Symbol, Lens, Any]]:
        """Flatten the API diff for easier comparison."""

        if lens is None:
            lens = Lens()

        if isinstance(diff_value, dict):
            for k, v in diff_value.items():
                if isinstance(k, Symbol):
                    for sublens, subval in self._flatten(val=v, lens=lens):
                        yield (k, sublens, subval)
                else:
                    yield from self._flatten_api_diff(
                        diff_value=v, lens=lens[k]
                    )

    # @skip("Compat not ready.")
    @skipIf(sys.version_info[0:2] != (3, 11), "Only run on Python 3.11")
    @optional_test
    def test_api_trulens_eval_compat(self):
        """Check that the trulens_eval API members are still present.

        To regenerate golden file, run `make test-write-api`.
        """
        # TODEP: Deprecate after trulens_eval is removed.

        golden_file = f"api.trulens_eval.{self.pyversion}.yaml"

        members = self.get_members_trulens_eval(aliases_are_defs=True)

        with open("current.yaml", mode="w") as fh:
            yaml.dump(members, fh, indent=2)

        self.write_golden(
            path=golden_file, data=members
        )  # will raise exception if golden file is written

        expected = self.load_golden(golden_file)

        jdiff = diff(expected, members, syntax=SymmetricJsonDiffSyntax())

        flat_diffs = list(self._flatten_api_diff(jdiff))
        flat_diffs_dump = list(
            map(
                lambda x: {str(x[1]): [str(x[0]), x[2]]},
                filter(lambda x: x[0] != Symbol.Insert, flat_diffs),
            )
        )

        with open("api.diff", "w") as fh:
            yaml.dump(flat_diffs_dump, fh, indent=2)

        if flat_diffs:
            for diff_type, diff_lens, diff_value in flat_diffs:
                if diff_type == Symbol.Insert:
                    # ignore additions
                    continue
                if repr(diff_lens.path[-1]) == ".__bases__":
                    # Ignore __bases__ differences.
                    continue
                if isinstance(diff_value, dict) and len(diff_value) == 0:
                    # Ignore empty dicts in diffs.
                    continue
                with self.subTest(api=str(diff_lens)):
                    self.fail(
                        f"trulens_eval compatibility API mismatch: {diff_type} at {diff_lens} value {diff_value}"
                    )

    @skipIf(sys.version_info[0:2] != (3, 11), "Only run on Python 3.11")
    @optional_test
    def test_api_trulens(self):
        """Check that the trulens API members are still present.

        To regenerate golden file, run `make test-write-api`.
        """

        golden_file = f"api.trulens.{self.pyversion}.yaml"

        members = self.get_members_trulens()

        self.write_golden(
            path=golden_file, data=members
        )  # will raise exception if golden file is written

        expected = self.load_golden(golden_file)

        jdiff = diff(expected, members, syntax=SymmetricJsonDiffSyntax())
        flat_diffs = self._flatten_api_diff(jdiff)

        if flat_diffs:
            for diff_type, diff_lens, diff_value in flat_diffs:
                with self.subTest(api=str(diff_lens)):
                    self.fail(
                        f"API mismatch: {diff_type} at {diff_lens} value {diff_value}"
                    )


if __name__ == "__main__":
    main()
