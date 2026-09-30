import shutil
import subprocess
import sys
import zipfile

from pathlib import Path


# =========================================================
# CONFIG
# =========================================================

APP_NAME = "Luso"
VERSION = "0.1.0-alpha"

ROOT = Path(__file__).resolve().parent

DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"

OUTPUT_DIR = DIST_DIR / APP_NAME

ZIP_NAME = f"{APP_NAME}-v{VERSION}.zip"
ZIP_PATH = DIST_DIR / ZIP_NAME


# =========================================================
# UTILS
# =========================================================

def remove(path):
    if not path.exists():
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_folder(source, destination):
    if not source.exists():
        print(f"[WARNING] Dossier introuvable : {source}")
        return

    print(
        f"[COPY] {source.name}"
    )

    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True
    )


# =========================================================
# CLEAN
# =========================================================

def clean():
    print()
    print("========================================")
    print(" CLEAN")
    print("========================================")

    remove(
        BUILD_DIR / APP_NAME
    )

    remove(
        OUTPUT_DIR
    )

    remove(
        ZIP_PATH
    )


# =========================================================
# PYINSTALLER
# =========================================================

def build_exe():

    print()
    print("========================================")
    print(" BUILD PYINSTALLER")
    print("========================================")

    command = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--noconfirm",
        "--clean",
        "--onedir",

        "--name",
        APP_NAME,

        "--exclude-module",
        "admin",

        str(
            ROOT / "main.py"
        )
    ]

    result = subprocess.run(
        command,
        cwd=ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            "PyInstaller a échoué."
        )


# =========================================================
# COPY ASSETS
# =========================================================

def copy_assets():

    print()
    print("========================================")
    print(" COPY ASSETS")
    print("========================================")

    copy_folder(
        ROOT / "assets",
        OUTPUT_DIR / "assets"
    )


# =========================================================
# DATA
# =========================================================

def create_data_folder():

    print(
        "[CREATE] data/"
    )

    data_dir = (
        OUTPUT_DIR
        / "data"
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # IMPORTANT :
    # on ne copie PAS ton stats.json personnel.


# =========================================================
# OPTIONAL FILES
# =========================================================

def copy_optional_files():

    files = [
        "README.txt",
        "LICENSE.txt"
    ]

    for filename in files:

        source = ROOT / filename

        if source.exists():

            shutil.copy2(
                source,
                OUTPUT_DIR / filename
            )

            print(
                f"[COPY] {filename}"
            )


# =========================================================
# ZIP
# =========================================================

def create_zip():

    print()
    print("========================================")
    print(" CREATE ZIP")
    print("========================================")

    with zipfile.ZipFile(
        ZIP_PATH,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        for file_path in (
            OUTPUT_DIR.rglob("*")
        ):

            if not file_path.is_file():
                continue

            relative = (
                file_path.relative_to(
                    DIST_DIR
                )
            )

            archive.write(
                file_path,
                relative
            )

    print(
        f"[ZIP] {ZIP_NAME}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("========================================")
    print(f" {APP_NAME} BUILD TOOL")
    print(f" VERSION {VERSION}")
    print("========================================")

    try:

        clean()

        build_exe()

        copy_assets()

        create_data_folder()

        copy_optional_files()

        create_zip()

    except Exception as error:

        print()
        print("========================================")
        print(" BUILD FAILED")
        print("========================================")

        print(
            error
        )

        input(
            "\nAppuie sur Entrée..."
        )

        return

    print()
    print("========================================")
    print(" BUILD SUCCESS")
    print("========================================")

    print()
    print(
        f"EXE : {OUTPUT_DIR}"
    )

    print(
        f"ZIP : {ZIP_PATH}"
    )

    input(
        "\nAppuie sur Entrée pour fermer..."
    )


if __name__ == "__main__":
    main()