"""LangChain Provider

!!! note "Additional Dependency Required"

    To use this module, you must have the `trulens-providers-langchain` package installed.

    ```bash
    pip install trulens-providers-langchain
    ```

!!! note
    LangChain provider cannot be used in `deferred` mode due to inconsistent serialization capabilities of LangChain apps.
"""

from importlib.metadata import version

from trulens.providers.langchain.provider import Langchain

__version__ = version(__package__ or __name__)

__all__ = [
    "Langchain",
]