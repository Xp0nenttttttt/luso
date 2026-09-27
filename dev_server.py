import subprocess
import sys
import time
from pathlib import Path


# Dossiers surveillés
WATCH_PATHS = [
    Path("server"),
    Path("games/uno"),
]

CHECK_INTERVAL = 0.5


def get_files_state():
    state = {}

    for folder in WATCH_PATHS:

        if not folder.exists():
            continue

        for path in folder.rglob("*.py"):

            # Ignore __pycache__
            if "__pycache__" in path.parts:
                continue

            try:
                state[path] = path.stat().st_mtime
            except FileNotFoundError:
                pass

    return state


def start_server():

    print()
    print("=" * 45)
    print("Démarrage du serveur...")
    print("=" * 45)

    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "server.server"
        ]
    )


def stop_server(process):

    if process is None:
        return

    if process.poll() is not None:
        return

    print()
    print("Arrêt du serveur...")

    process.terminate()

    try:
        process.wait(
            timeout=3
        )

    except subprocess.TimeoutExpired:

        print(
            "Le serveur ne répond pas, fermeture forcée."
        )

        process.kill()

        process.wait()


def main():

    print(
        "======================================"
    )

    print(
        " HUB DEV SERVER - AUTO RELOAD"
    )

    print(
        "======================================"
    )

    print(
        "Dossiers surveillés :"
    )

    for folder in WATCH_PATHS:
        print(
            f" - {folder}"
        )

    print()
    print(
        "Sauvegarde un fichier .py pour redémarrer."
    )

    print(
        "CTRL+C pour quitter."
    )


    previous_state = (
        get_files_state()
    )

    process = start_server()


    try:

        while True:

            time.sleep(
                CHECK_INTERVAL
            )

            current_state = (
                get_files_state()
            )

            if (
                current_state
                != previous_state
            ):

                print()
                print(
                    "♻ Modification détectée !"
                )

                stop_server(
                    process
                )

                time.sleep(
                    0.3
                )

                process = (
                    start_server()
                )

                previous_state = (
                    current_state
                )


            # Si le serveur crash,
            # on ne le relance pas en boucle.
            # Il redémarrera au prochain save.
            if (
                process.poll()
                is not None
            ):

                pass


    except KeyboardInterrupt:

        print()
        print(
            "Fermeture du dev server..."
        )

        stop_server(
            process
        )


if __name__ == "__main__":
    main()