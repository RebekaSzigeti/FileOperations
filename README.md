# FileOperations

A modular command-line file management tool written in Python.

`fileops` is a CLI application that helps you organize, search, and delete files efficiently from the terminal.

---

## Features

- Organize files by extension
- Search files by name (with optional recursion)
- Delete files by name pattern
- Dry-run mode
- Force mode (skip confirmation)
- Logging support
- Installable as a Python package
- Unit tested (pytest)
- Verbose mode

---

## Usage

### Organize files

```bash
fileops organize --path ./downloads
```

**Options:**

- `--dry-run`     # simulate without moving files
- `--verbose`     # detailed output
- `--config`      # custom config file

---

### Search files

```bash
fileops search --path ./documents --name report
```

**Options:**

- `--recursive`
- `--dry-run`
- `--verbose`

---

### Delete files

```bash
fileops delete --path ./temp --name test
```

**Options:**

- `--force`       # skip confirmation
- `--dry-run`
- `--verbose`
- `--recursive`



## Installation

### 1. Clone the repository

If you downloaded the ZIP file, extract it and navigate into the project folder.

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

---

### 3. Activate the virtual environment

**Windows (PowerShell):**

```bash
.\venv\Scripts\Activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal.

---

### 4. Install the package

```bash
pip install -e .
```

---

### 5. Verify installation

```bash
fileops --help
```

If the help message appears, the installation was successful.






