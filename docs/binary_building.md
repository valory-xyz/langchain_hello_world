# Building Agent Binaries

This document explains how the agent is packaged into standalone executables and how to produce them locally or via CI.

## Overview

The agent is compiled into a single-file binary using [PyInstaller](https://pyinstaller.org). The binary bundles the Python interpreter and all dependencies, so no Python installation is required on the target machine.

Binaries follow the naming convention:

```
agent_runner_{os_name}_{arch}[.exe]
```

| `os_name` | `arch` | Example |
|-----------|--------|---------|
| `linux`   | `x64`  | `agent_runner_linux_x64` |
| `linux`   | `arm64`| `agent_runner_linux_arm64` |
| `macos`   | `x64`  | `agent_runner_macos_x64` |
| `macos`   | `arm64`| `agent_runner_macos_arm64` |
| `windows` | `x64`  | `agent_runner_windows_x64.exe` |

> **Important:** PyInstaller produces a binary for the OS and CPU architecture it runs on. To build for a different target, you must build natively on that platform — cross-compilation is not supported.

---

## Automated builds (CI)

Binaries are built and published automatically by the [Release Binaries workflow](../.github/workflows/release.yaml) whenever a GitHub release is published.

The workflow runs six parallel jobs — one per OS/arch combination — using GitHub-hosted runners:

| OS | Arch | Runner |
|----|------|--------|
| Linux | x64 | `ubuntu-latest` |
| Linux | arm64 | `ubuntu-24.04-arm` |
| macOS | x64 | `macos-13` (Intel) |
| macOS | arm64 | `macos-latest` (Apple Silicon) |
| Windows | x64 | `windows-latest` |

Each job:
1. Installs Python 3.10 and Poetry 1.8.4
2. Installs project dependencies via `poetry install`
3. Installs PyInstaller into the Poetry virtualenv
4. Runs PyInstaller to produce the binary under `dist/`
5. Uploads the binary to the release as an artifact using `gh release upload`

To trigger the workflow, [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) on GitHub. The binaries will appear as downloadable assets on the release page once all jobs finish.

---

## Building locally

Follow these steps to produce a binary on your own machine.

### Prerequisites

- Python 3.10
- [Poetry](https://python-poetry.org/docs/#installation) 1.8.4+

### Steps

```bash
# 1. Install project dependencies
poetry install --no-interaction --no-root

# 2. Install PyInstaller
poetry run pip install pyinstaller

# 3. Build the binary (replace <os_name> and <arch> with your platform values)
poetry run pyinstaller \
  --onefile \
  --name agent_runner_<os_name>_<arch> \
  langchain_hello_world/main.py
```

The resulting binary is placed in the `dist/` directory:

```
dist/
└── agent_runner_<os_name>_<arch>[.exe]
```

### Example — Linux x64

```bash
poetry install --no-interaction --no-root
poetry run pip install pyinstaller
poetry run pyinstaller --onefile --name agent_runner_linux_x64 langchain_hello_world/main.py
./dist/agent_runner_linux_x64
```

### Example — Windows x64 (PowerShell)

```powershell
poetry install --no-interaction --no-root
poetry run pip install pyinstaller
poetry run pyinstaller --onefile --name agent_runner_windows_x64 langchain_hello_world/main.py
.\dist\agent_runner_windows_x64.exe
```

---

## Runtime requirements

The binary is self-contained, but the agent still needs the following **environment variables** set at runtime:

| Variable | Description |
|----------|-------------|
| `CONNECTION_CONFIGS_CONFIG_TAVILY_API_KEY` | Tavily search API key |
| `CONNECTION_CONFIGS_CONFIG_OPENAI_API_KEY` | OpenAI API key |
| `CONNECTION_LEDGER_CONFIG_LEDGER_APIS_GNOSIS_ADDRESS` | Gnosis RPC endpoint |

These can be supplied via a `.env` file in the working directory or exported in the shell before running the binary.
