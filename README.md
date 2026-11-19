<!--
SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later
-->

# QFlashlight

Simple Qt application that fills the screen (or a window) with a solid
color. Optionally displays scaled centered text, either static or the
live output of a command (watch-like).

This is a pure **C++ / Qt6** port of the original Python/PyQt5 application.
All Python has been removed.

## Features

- Solid background color (CLI or interactive picker)
- Optional centered, aspect-preserving scaled text
- Text color and font selection
- Static text (`-t`), file / stdin, or command output (`-C`) with optional refresh (`-n`)
- Fullscreen / windowed / borderless
- Hide mouse cursor
- Geometry (`WxH+X+Y`)
- Context menu and keyboard shortcuts

### Keyboard

| Key | Action              |
|-----|---------------------|
| Esc / Q | Quit            |
| F   | Toggle fullscreen   |
| M   | Toggle cursor       |
| B   | Toggle borderless   |
| C   | Background color    |
| T   | Text color          |
| E   | Edit text           |

## Build

### Nix (recommended)

```bash
nix build
./result/bin/qflashlight
```

Development shell:

```bash
nix develop
cmake -B build -G Ninja
cmake --build build
./build/qflashlight
```

### CMake + system Qt6

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
sudo cmake --install build
```

## Usage

```
qflashlight [options] [FILE]

Style:
  -c, --color COLOR         Background color (default: black)
  -T, --text-color COLOR    Text color (default: white)
  -F, --font FONT           Font for text

Content:
  -t, --text TEXT           Static text
  -C, --command CMD         Run CMD and show output
  -n, --interval SECONDS    Refresh interval for -C

Window:
  -f, --fullscreen          Start fullscreen
  -w, --window              Start windowed (default)
  -m, --hide-cursor
  -b, --borderless
  -g, --geometry WxH+X+Y
```

Example (live clock):

```bash
qflashlight -C date -n 1 -c black -T lime
```

## License

GPL-3.0-or-later. See [LICENSES/GPL-3.0-or-later.txt](LICENSES/GPL-3.0-or-later.txt).

Copyright (C) 2017–2026 Ingo Ruhnke <grumbel@gmail.com>
