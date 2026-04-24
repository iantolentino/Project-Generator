from setuptools import setup, find_packages

setup(
    name="project-gen",
    version="2.0.0",
    description="Full-stack project scaffolding in seconds",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "questionary>=1.10.0",
        "colorama>=0.4.6",
        "flask>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "project-gen=project_gen.cli:main",
            "project-gen-web=project_gen.server:run_server",
        ],
    },
)
