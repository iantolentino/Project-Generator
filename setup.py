from setuptools import setup, find_packages

setup(
    name="project-gen",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "questionary>=1.10.0",
        "Jinja2>=3.1.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "project-gen=project_gen.cli:main",
        ],
    },
)