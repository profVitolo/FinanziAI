from pathlib import Path
import shutil
import subprocess
import sys
import os
from test_utils import  *

env = dict(os.environ)
env["FINANZIAI_TEST_RUNNER"] = "1"

ROOT_DIR = Path(__file__).parent.parent
TEST_DIR = Path(__file__).parent

DB_PATH = ROOT_DIR / "database" / "vault.db"
BACKUP_PATH = ROOT_DIR / "database" / "vault.db.bk"

server = None

tests = sorted(f for f in TEST_DIR.glob("*_test_*.py")
    if f.name != "start_test.py"
    and not f.name.endswith("test_utils.py")
)

try:
    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.app:app"])

    if not wait_for_server():
        print("Server non raggiungibile")
        sys.exit(1)

    print("Server pronto")

    print("\n=== TESTS ===\n")
    print("0. Esegui tutti i test")

    for index, test_file in enumerate(tests, start=1):
        print(f"{index}. {test_file.stem}")

    choice = input("\nSeleziona test: ")

    # Tutti - default
    if choice == "0":
        if DB_PATH.exists():
                print("\nBackup database...")

                shutil.copy2(DB_PATH, BACKUP_PATH )

        for test_file in tests:
            print(f"\n{'=' * 60}")
            print(f"Avvio {test_file.name}")
            print(f"{'=' * 60}\n")

            result = subprocess.run(
                [sys.executable, str(test_file.relative_to(ROOT_DIR))],
                cwd=ROOT_DIR,
                env=env
            )

            if result.returncode != 0:
                print(f"\nTest fallito: {test_file.name}")
                sys.exit(result.returncode)

        print("\nTutti i test completati.")
        
    else:
        selected = tests[int(choice) - 1]
        print(f"\nAvvio {selected.name}\n")
        subprocess.run([sys.executable, str(selected.relative_to(ROOT_DIR))], cwd=ROOT_DIR, env=env)
    
finally:
    stop_server(server)
    time.sleep(3)
    
    if BACKUP_PATH.exists():
        print("\nRipristino database...")

        if DB_PATH.exists():
            DB_PATH.unlink()

        shutil.move(BACKUP_PATH, DB_PATH)
