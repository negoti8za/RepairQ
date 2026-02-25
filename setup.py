"""
setup.py - Build configuration for RepairQ Windows application
"""

from setuptools import setup, find_packages

setup(
    name="RepairQ",
    version="1.0.0",
    description="Professional Repair Shop Management Application",
    author="RepairQ",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.7.0",
    ],
    entry_points={
        "gui_scripts": [
            "repairq=main:main",
        ]
    },
    include_package_data=True,
)
