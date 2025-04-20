{
  description = "Hack Davis 2025";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        pkgs.uv
        pkgs.yt-dlp
        pkgs.ffmpeg_6
        pkgs.libGL
        pkgs.python312Packages.opencv4
      ];

      shellHook = ''
        echo Activated FFL shell
      '';
    };
  };
}
