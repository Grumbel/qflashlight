# SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

{
  description = "QFlashlight - Simple Qt-based fullscreen flashlight (C++/Qt6)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        versionBase = nixpkgs.lib.fileContents ./VERSION;
        gitRev = "${self.shortRev or self.dirtyShortRev or "dirty"}";
        isDev = nixpkgs.lib.strings.hasInfix "-dev" versionBase;
        version =
          if isDev then
            "${versionBase}.${toString (self.revCount or 0)}+g${gitRev}"
          else
            versionBase;
      in {
        packages = rec {
          default = qflashlight;

          qflashlight = pkgs.stdenv.mkDerivation {
            pname = "qflashlight";
            inherit version;

            src = ./.;

            nativeBuildInputs = with pkgs; [
              cmake
              qt6.wrapQtAppsHook
            ];

            buildInputs = with pkgs; [
              qt6.qtbase
            ];

            cmakeFlags = [
              "-DCMAKE_BUILD_TYPE=Release"
              "-DPROJECT_VERSION_FULL=${version}"
            ];

            meta = with pkgs.lib; {
              description = "Simple Qt-based fullscreen flashlight";
              homepage = "https://github.com/grumbel/qflashlight";
              license = licenses.gpl3Plus;
              platforms = platforms.linux;
              mainProgram = "qflashlight";
            };
          };
        };

        checks = {
          qflashlight = self.packages.${system}.qflashlight;

          reuse = pkgs.runCommand "qflashlight-reuse-lint" {
            nativeBuildInputs = [ pkgs.reuse ];
          } ''
            cd ${self}
            reuse lint
            touch $out
          '';
        };

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/qflashlight";
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.qflashlight ];
          packages = with pkgs; [ cmake clang-tools gdb ];
        };
      }
    );
}
