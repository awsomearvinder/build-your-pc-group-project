# Setup
In order to setup this project, you need a few pre-requisites:
- Python (I use 3.12, I'd make sure it's atleast later then 3.10 since it released nice features)
  - Installing Python can be done with: `winget install Python.Python.3.12` in your terminal.
- Poetry (this is used to install dependencies)
    - Installing Poetry can be done with: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -` in powershell.
      If you get an error where it says Python is not found, restart your terminal.

Once `poetry` is installed, and you open this repo in vscode, run `poetry config virtualenvs.in-project true`. This option creates a `.venv` folder in the
current folder which vscode can be aware of. This is needed so that you can do things like autocomplete libraries. Afterwards, run `poetry install` to install
dependencies.

Now, `poetry run python build-your-pc/main.py` in order to run it.
