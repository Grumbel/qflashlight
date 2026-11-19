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
      in {
        packages = rec {
          default = qflashlight;

          qflashlight = pkgs.stdenv.mkDerivation rec {
            pname = "qflashlight";
            version = "0.3.0";

            src = ./.;

            nativeBuildInputs = with pkgs; [
              cmake
              qt6.wrapQtAppsHook
            ];

            buildInputs = with pkgs; [
              qt6.qtbase
            ];

            cmakeFlags = [ "-DCMAKE_BUILD_TYPE=Release" ];

            meta = with pkgs.lib; {
              description = "Simple Qt-based fullscreen flashlight";
              homepage = "https://github.com/grumbel/qflashlight";
              license = licenses.gpl3Plus;
              platforms = platforms.linux;
              mainProgram = "qflashlight";
            };
          };
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
