"""Setup configuration for Agent Skill Library."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="agent-skill-library",
    version="0.1.0",
    author="Agent Skill Library Contributors",
    description="A modular, extensible framework for building AI agent capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ymngkhtd/Skill-library",
    packages=find_packages(exclude=["examples", "examples.*"]),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="agent skills ai framework modular extensible",
    project_urls={
        "Documentation": "https://github.com/ymngkhtd/Skill-library/blob/main/ARCHITECTURE.md",
        "Source": "https://github.com/ymngkhtd/Skill-library",
    },
)
