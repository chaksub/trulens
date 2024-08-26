from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'tqdm',
        'opensearch-py',
        'certifi'
    ],
    entry_points={
        'console_scripts': [
            'my_package=embedding:main',
        ],
    },
)