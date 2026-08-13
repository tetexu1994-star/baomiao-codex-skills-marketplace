"""Compatibility shim for Python environments with pre-PEP 660 pip."""

from setuptools import find_packages, setup


setup(
    name="baomiao-codex-skills-marketplace",
    version="0.1.0",
    packages=find_packages(include=("scripts", "scripts.*")),
    install_requires=["jsonschema>=4.23,<5"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "baomiao-validate=scripts.validate_catalog:main",
            "baomiao-build=scripts.build:main",
            "baomiao-sync=scripts.sync_candidates:main",
        ]
    },
)

