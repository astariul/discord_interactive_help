# Discord Interactive Help

## Introduction

Welcome to the documentation of the `discord_interactive` package.

`discord_interactive` helps you build an interactive help for your Discord bot easily.

This is an alternative way to engage with a Discord bot, offering a more intuitive approach than the traditional command message method.

![](https://user-images.githubusercontent.com/22237185/53283254-da5a3100-3786-11e9-95cd-cd4dd4859bd2.gif)

Users can interact with the bot using reactions, making it a more natural way to read multiple pages (for a help manual for example).


## Installation

### Latest version

You can install the latest version of the package directly from PyPi with :

```bash
pip install discord-interactive
```

!!! hint
    If you want to install directly from Github, run :
    ```bash
    pip install git+https://github.com/astariul/discord_interactive_help.git
    ```

### Specific version

You can install a specific version of the package (`3.0.0` in this example) from PyPi with :

```bash
pip install discord-interactive==3.0.0
```

!!! hint
    If you want to install directly from Github, run :
    ```bash
    pip install git+https://github.com/astariul/discord_interactive_help.git@v3.0.0
    ```

### Local

You can also clone the repository locally and install it manually :

```bash
git clone https://github.com/astariul/discord_interactive_help.git
cd pytere
pip install -e .
```

### Extra dependencies

You can also install extras dependencies, for example :

```bash
pip install -e .[docs]
```

Will install necessary dependencies for building the docs.

!!! hint
    If you installed the package directly from github, run :
    ```bash
    pip install "discord-interactive[docs] @ https://github.com/astariul/discord_interactive_help.git"
    ```

---

List of extra dependencies :

* **`hook`** : Dependencies for running pre-commit hooks.
* **`lint`** : Dependencies for running linters and formatters.
* **`docs`** : Dependencies for building the documentation.
* **`dev`** : `hook` + `lint` + `docs`.
* **`all`** : All extra dependencies.

## Contribute

To contribute, install the package locally (see [Installation](#local)), create your own branch, add your code (and documentation), and open a PR !

### Pre-commit hooks

Pre-commit hooks are set to check the code added whenever you commit something.

When you try to commit your code, hooks are automatically run, and if you code does not meet the quality required by linters, it will not be committed. You then have to fix your code and try to commit again !

!!! important
    If you never ran the hooks before, install it with :
    ```bash
    pre-commit install
    ```

!!! info
    You can manually run the pre-commit hooks with :
    ```bash
    pre-commit run --all-files
    ```

### Documentation

When you contribute, make sure to keep the documentation up-to-date.

You can visualize the documentation locally by running :

```bash
mkdocs serve
```
