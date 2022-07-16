{
  description = "An app that fills the whole screen with a color";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python310Packages;
       in rec {
         packages = flake-utils.lib.flattenTree rec {
           PyQt5-stubs = pythonPackages.buildPythonPackage rec {
             pname = "PyQt5-stubs";
             version = "5.15.6.0";
             src = pythonPackages.fetchPypi {
               inherit pname version;
               sha256 = "sha256-kScKwj6/OKHcBM2XqoUs0Ir4Lcg5EA5Tla8UR+Pplwc=";
             };
           };

          qflashlight = pythonPackages.buildPythonPackage rec {
            name = "qflashlight";
            src = self;
            nativeBuildInputs = [ pkgs.qt5.wrapQtAppsHook ];
            makeWrapperArgs = [
              "\${qtWrapperArgs[@]}"

              "--set" "LIBGL_DRIVERS_PATH" "${pkgs.mesa.drivers}/lib/dri"
              "--prefix" "LD_LIBRARY_PATH" ":" "${pkgs.mesa.drivers}/lib"
            ];
            preCheck = ''
              export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt5.qtbase.bin}/lib/qt-${pkgs.qt5.qtbase.version}/plugins";
            '';
            propagatedBuildInputs = with pythonPackages; [
              setuptools
              pyqt5
              pyxdg
            ];
            checkInputs = (with pkgs; [
              pyright
            ]) ++ (with pythonPackages; [
              flake8
              mypy
              pylint
              types-setuptools
            ]) ++ [
              PyQt5-stubs
            ];
          };

          qflashlight-nocheck = qflashlight.override {
            doCheck = false;
          };

          default = qflashlight;
        };

        devShells = rec {
          qflashlight-dev = pkgs.mkShell {
            inputsFrom = [ packages.qflashlight ];
            shellHook = packages.qflashlight.preCheck + ''
              # runHook setuptoolsShellHook
            '';
          };
        };

        apps = rec {
          qflashlight = flake-utils.lib.mkApp {
            drv = packages.qflashlight;
            exePath = "/bin/qflashlight";
          };
          default = qflashlight;
        };
       }
    );
}
