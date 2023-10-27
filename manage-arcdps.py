#!/usr/bin/env python3
from os import symlink, unlink
from sys import stderr
from pathlib import Path
from hashlib import md5
from argparse import ArgumentParser
import requests


def update_arcdps(game_path):
    dll = requests.get("https://www.deltaconnected.com/arcdps/x64/d3d11.dll")
    checksum = requests.get(
        "https://www.deltaconnected.com/arcdps/x64/d3d11.dll.md5sum"
    )

    if not dll.ok or not checksum.ok:
        print("Something went wrong with the download of files", file=stderr)
        exit(1)

    md5sum = checksum.text.split()[0]
    if not md5sum == md5(dll.content).hexdigest():
        print("Digest does not match dll. Download might be faulty", file=stderr)

    with open(f"{game_path}/arcdps.dll", "wb+") as f:
        f.write(dll.content)


def enable_arcdps(game_path):
    dll_path = f"{game_path}/arcdps.dll"
    dx11_path = f"{game_path}/d3d11.dll"

    try:
        symlink(dll_path, dx11_path)
    except FileExistsError:
        pass


def disable_arcdps(game_path):
    dx11_path = f"{game_path}/d3d11.dll"
    unlink(dx11_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("command", choices=["enable", "disable", "update"])
    default_game_path = (
        f"{Path.home()}/Games/guild-wars-2/drive_c/Program Files/Guild Wars 2"
    )
    parser.add_argument(
        "--game-path",
        default=default_game_path,
        help=f"Absolute Path ot Game Path. Defaults to {default_game_path}",
    )
    args = parser.parse_args()

    locals()[f"{args.command}_arcdps"](args.game_path)
