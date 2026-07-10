---
name: jupyter-notebook-ops
description: Guides Claude through setting up, running, converting, and troubleshooting Jupyter notebook environments and .ipynb files from the command line, for use whenever a task involves executing notebooks, managing kernels, or exporting notebooks to other formats.
---

# Jupyter Notebook Operations

## Purpose

This skill helps Claude work with Jupyter notebooks and Jupyter environments from the command line: installing and verifying a Jupyter setup, listing and managing kernels, executing notebooks non-interactively, converting notebooks to other formats (scripts, HTML, PDF, Markdown), and diagnosing common environment problems (missing kernel, mismatched Python environment, stale outputs).

Apply this skill when a task involves:
- A `.ipynb` file that needs to be run, re-executed, or have its outputs regenerated.
- Converting a notebook to a script, HTML report, PDF, or Markdown document.
- Setting up or repairing a Jupyter installation (classic notebook, JupyterLab, or the `jupyter` metapackage) in a project.
- Registering, listing, or removing Jupyter kernels (e.g. a project-specific virtualenv/conda kernel).
- Debugging why a notebook fails to run, uses the wrong Python interpreter, or can't find an installed package.

Do not use this skill for editing notebook cell content directly (use the dedicated notebook-editing tool for that) — this skill is about the surrounding tooling: installation, execution, conversion, and kernel management.

## Step-by-step guidance

### 1. Confirm what's installed before assuming a fix

Before troubleshooting or suggesting installs, check what's actually present:
- Check for a Jupyter installation: look for a `jupyter` executable on PATH or in the active virtual environment, and check `pip show jupyter` / `pip show jupyterlab` / `pip show notebook` output.
- Check installed kernels: run `jupyter kernelspec list` to see which kernels are registered and where they point.
- Check the Python environment a notebook actually depends on: read the notebook's `metadata.kernelspec` field inside the `.ipynb` JSON, not just what's active in the shell.

Never assume Jupyter is missing or misconfigured without checking first — a failing notebook is often a kernel mismatch, not a missing install.

### 2. Installing or repairing Jupyter

- The `jupyter` package is a metapackage: installing it (`pip install jupyter`) pulls in the notebook server, JupyterLab, IPython kernel, and core utilities as a bundle. Prefer this metapackage for a general-purpose setup; install `jupyterlab` or `notebook` alone only if the user specifically wants just the server component.
- If a project uses a virtual environment or conda environment, install Jupyter (or at minimum `ipykernel`) inside that environment, then register a kernel pointing at it, rather than relying on a globally installed Jupyter to somehow pick up project dependencies.
- To register a project environment as a selectable kernel: run `python -m ipykernel install --user --name <project-name> --display-name "<Human Readable Name>"` from within the activated project environment.
- To remove a stale or duplicate kernel: run `jupyter kernelspec remove <kernel-name>`.

### 3. Executing notebooks non-interactively

When a notebook needs to be run end-to-end without a human clicking through cells:
- Use `jupyter nbconvert --to notebook --execute <notebook>.ipynb --output <output>.ipynb` to run all cells and write a new notebook with fresh outputs, leaving the original untouched.
- Add `--ExecutePreprocessor.timeout=<seconds>` if the notebook has long-running cells, so execution isn't killed prematurely.
- If the notebook must run under a specific kernel rather than the default, pass `--ExecutePreprocessor.kernel_name=<kernel-name>` (matching a name from `jupyter kernelspec list`).
- For parameterized re-runs (same notebook, different input values), prefer a papermill-style parameter injection approach if the tool is available in the environment, rather than manually editing cell source.

### 4. Converting notebooks to other formats

Use `jupyter nbconvert --to <format> <notebook>.ipynb` for one-off exports:
- `--to script` produces a plain `.py` file with cell code concatenated in order — useful for extracting reusable logic out of a notebook.
- `--to html` or `--to html --template lab` produces a shareable static report including outputs.
- `--to pdf` produces a PDF (requires a LaTeX installation on the system; if it fails, fall back to `--to html` and note the missing LaTeX dependency rather than silently failing).
- `--to markdown` produces a Markdown version, useful for embedding notebook content into documentation.

Always confirm the target format's dependencies are present (e.g. LaTeX for PDF) before running the conversion, and report a clear error if a dependency is missing rather than retrying blindly.

### 5. Common failure diagnosis

- "Kernel not found" errors mean the notebook's `metadata.kernelspec.name` doesn't match any kernel in `jupyter kernelspec list` — either register the missing kernel or update the notebook's kernelspec metadata to point at an existing one.
- "Module not found" during execution usually means the notebook is running under a different Python environment than the one where the package is installed — verify with `jupyter kernelspec list` which environment the selected kernel actually points to, and reinstall the missing package there.
- Stale or missing outputs after a manual edit mean the notebook needs re-execution (step 3) rather than the outputs being hand-edited into the JSON.
- If `nbconvert` reports a timeout, increase `--ExecutePreprocessor.timeout` rather than assuming the notebook itself is broken.
