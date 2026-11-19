<!--
SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later
-->

# TODO / Handoff

## Current tip

`a09ad66` — Polish text rendering and file input to match upstream behaviour

Work-line base: `d7659bf` (github.com/grumbel/qflashlight tip at start of this sequence)

## Done

- [x] Full feature port from Python/PyQt5 (at d7659bf) to C++/Qt6
  - model, widget, application, text generator (QProcess)
  - color/text dialogs, context menu, all CLI flags
  - keyboard shortcuts (Esc/Q/F/M/E/C/T/B)
- [x] Remove all Python sources and packaging
- [x] CMakeLists.txt
- [x] Nix flake (qt6.wrapQtAppsHook)
- [x] README, AGENTS.md, TODO.md
- [x] Multi-line text sizing + trailing newline strip matched to upstream

## Feature parity checklist (vs d7659bf Python)

| Feature | Status |
|---------|--------|
| -c / --color | yes |
| -T / --text-color | yes |
| -F / --font | yes |
| -t / --text | yes |
| -C / --command | yes (sh -c) |
| -n / --interval | yes |
| FILE / stdin (-) | yes |
| -f fullscreen / -w window (default window) | yes |
| -m hide-cursor | yes |
| -b borderless (only when not FS) | yes |
| -g geometry | yes |
| Double-click FS toggle | yes |
| Drag move | yes |
| Context menu (FS/cursor/border/color/text/exit) | yes |
| Keys Esc Q F M E C T B | yes |
| Scaled centered text (multi-line) | yes |
| Color dialogs (live preview + cancel restore) | yes |
| Text dialog (live + cancel restore) | yes |

## Open

- [ ] Optional: unit tests / CI
- [ ] Optional: AppStream metainfo
- [ ] Smoke-test under real compositor

## Notes

- First attempt was based on the ancient PyPI 0.2.0 wheel; discarded.
- This history is rebased on the real GitHub tip `d7659bf`.
- Command execution uses `sh -c` to match `subprocess.getoutput`.
