# PacmanTui

A lightweight Terminal User Interface (TUI) to manage packages on Arch Linux using Python and `textual`.

## Features
- Search packages using `yay`
- Install packages interactively
- Uninstall packages with configuration cleanup
- Perform full system upgrades (`yay -Syu`)
- Filter packages (update 1.1)

## Installation

You can install it locally using `pip`:

```bash
git clone https://github.com/toast-jpg/pacmantui.git
cd pacmantui
pip install .
```

Make sure `~/.local/bin` is in your `PATH` environment variable.

## Usage
Simply run:
```bash
pacmantui
```
