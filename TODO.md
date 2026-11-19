# TODO / Handoff

## Current tip

C++/Qt6 port rebased on upstream `d7659bf` (github.com/grumbel/qflashlight).

Work-line base: `d7659bf`

## Done

- [x] Full feature port from Python/PyQt5 to C++/Qt6
  - model, widget, application, text generator (QProcess)
  - color/text dialogs, context menu, all CLI flags
  - keyboard shortcuts (Esc/Q/F/M/E/C/T/B)
- [x] Remove all Python sources and packaging
- [x] CMakeLists.txt
- [x] Nix flake (qt6.wrapQtAppsHook)
- [x] README, AGENTS.md, TODO.md

## Open

- [ ] Optional: unit tests / CI
- [ ] Optional: AppStream metainfo
- [ ] Smoke-test under real compositor

## Notes

- Default is window mode (matches current Python upstream).
- Command execution uses `sh -c` to match `subprocess.getoutput`.
- Borderless flag only applied when not fullscreen (avoids flicker).
