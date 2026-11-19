<!--
SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later
-->

# AGENTS.md — QFlashlight

## Overview

C++/Qt6 port of the former Python/PyQt5 qflashlight. No Python remains.

Upstream history is preserved; the port commits replace the Python
implementation with an equivalent C++ one.

## Layout

```
src/
  main.cpp                 CLI (QCommandLineParser)
  application.{hpp,cpp}    Orchestration, dialogs, context menu
  flashlight_model.*       Colors, font, text + change signal
  flashlight_widget.*      Painting, input events
  text_generator.*         QProcess + QTimer for -C/-n
CMakeLists.txt
flake.nix
data/qflashlight.svg
qflashlight.desktop
```

## Rules

- Feature parity with the Python version at the rebase base.
- Qt6, C++17, CMake, Nix flake.
- GPLv3+, SPDX headers.
- Grok Web only: deliver git bundles; document in TODO.md. Other agents
  (e.g. Claude Code) commit directly.
