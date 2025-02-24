from setuptools import setup, find_packages

setup(
    name="askai",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'ask=askai.cli:ask',
        ],
    },
)