---
icon: lucide/database
---

### What each tool does

| Tool     | Explanation                                                                                   |
| -------- | --------------------------------------------------------------------------------------------- |
| Python   | A programming language that we will use in later sessions to work with data                   |
| Positron | The application where you open projects, notebooks, data, and results                         |
| `uv`     | A tool that installs Python versions and packages and keeps a project's environment organised |

### Step 1: install Positron

1. Open the official [Positron download page](https://positron.posit.co/download).
2. Download the installer for your operating system.
3. Install and open Positron.

### Step 2: check or install `uv`

=== "Mac/Linux"

    Open the **Terminal** application and paste:

    ``` sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows PowerShell"

    Open the **PowerShell** application and paste:

    ``` powershell
    irm https://astral.sh/uv/install.ps1 | iex
    ```

To verify it's actually installed:

1. In Positron, open **View > Terminal**.
2. Type the command below and press Enter.

```text
uv --version
```

If a version number appears, `uv` is ready.

The [official `uv` installation page](https://docs.astral.sh/uv/getting-started/installation/) lists alternative installation methods.

!!! note "If installation is restricted"

    You do not need administrator rights for every installation method. If your network blocks the installer, continue with a neighbour and tell the instructor.

### Step 3: create a project environment

The Positron menus may look slightly different across versions, but the workflow is the same.

1. In Positron, choose **New > New Folder from Template**.
2. Select **Python Project**.
3. Choose a location such as your Documents folder and name the project `indigo-data`.
4. When asked, create a `pyproject.toml` file.
5. Choose **Create a new virtual environment**.
6. Choose **`uv`** as the environment provider (default).
7. Name the environment `.venv` (default).
8. Choose the latest stable Python version offered by Positron, then select **Create**.

Positron may download Python through `uv` if Python is not already installed. This is expected. A new `.venv` folder should appear in the project, along with a `pyproject.toml` file.

### Step 4: install one package and verify it can be used

We will install `polars`, a common package for working with tables.

1. Make sure the Positron terminal is open in the `indigo-data` project.
2. Go to **Terminal**:

```sh
uv add polars
```

The command adds the package to the project and updates the project's environment. It should also record the dependency in `pyproject.toml`.

3. Go to **Console**.
4. Copy the following code block, paste it, and press Enter:

```python
import sys
import polars as pd

print(sys.executable)
print(sys.version)
print(pd.__version__)
```

You have succeeded when the cell prints a Python path, a Python version, and a polars version without errors.

??? info "Troubleshooting"

    **`uv` is not found:** close and reopen the terminal, then try `uv --version` again. If it still fails, use the official `uv` installation page or ask for help.

    **The `.venv` environment does not appear:** open the Command Palette and run **Interpreter: Discover All Interpreters**, then select the `.venv` environment.

    **The notebook uses the wrong environment:** click the kernel selector at the top of the notebook and choose the interpreter inside your project's `.venv` folder.

    **The package installation fails:** check your internet connection and the spelling of `uv add polars`. If the computer is managed by your school or company, ask the instructor rather than changing security settings yourself.

    For more detail, see Positron's [Python installation and environment guide](https://positron.posit.co/python-installations.html) and [first Python notebook tutorial](https://positron.posit.co/tutorial-get-started-ipynb.html).
