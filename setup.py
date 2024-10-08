import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

reqs = ["discord.py~=2.3"]

extras_require = {
    "hook": ["pre-commit~=4.0"],
    "lint": ["black~=24.1", "ruff~=0.1"],
    "docs": ["mkdocs-material~=9.0", "mkdocstrings[python]~=0.18", "mike~=2.0"],
}
extras_require["all"] = sum(extras_require.values(), [])
extras_require["dev"] = extras_require["hook"] + extras_require["lint"]

setuptools.setup(
    name="discord_interactive",
    version="5.0.0.dev0",
    author="Nicolas REMOND",
    author_email="remondnicola@gmail.com",
    license="MIT",
    description="A package allowing you to display interactive help in Discord easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astariul/discord_interactive_help",
    packages=setuptools.find_packages(),
    keywords=["Discord", "Interactive", "Help"],
    install_requires=reqs,
    extras_require=extras_require,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
