from pathlib import Path
import shutil
import subprocess
import sys

ROOT_DIR = Path(__file__).parent.parent
TEST_DIR = Path(__file__).parent

DB_PATH = ROOT_DIR / "database" / "vault.db"
BACKUP_PATH = ROOT_DIR / "database" / "vault.db.bk"

tests = sorted(
    [
        f
        for f in TEST_DIR.glob("*_test_*.py")
        if f.name != "start_test.py"
    ]
)

print("\n=== TESTS ===\n")
print("0. Esegui tutti i test")

for index, test_file in enumerate(tests, start=1):
    print(f"{index}. {test_file.stem}")

choice = input("\nSeleziona test: ")

# Tutti - default
if choice == "0":
    try:
        if DB_PATH.exists():
                print("\nBackup database...")

                shutil.copy2(DB_PATH, BACKUP_PATH )

        for test_file in tests:
            print(f"\n{'=' * 60}")
            print(f"Avvio {test_file.name}")
            print(f"{'=' * 60}\n")

            result = subprocess.run(
                [sys.executable, str(test_file.relative_to(ROOT_DIR))],
                cwd=ROOT_DIR
            )

            if result.returncode != 0:
                print(f"\nTest fallito: {test_file.name}")
                sys.exit(result.returncode)

        print("\nTutti i test completati.")
    
    finally:

        if BACKUP_PATH.exists():
            print("\nRipristino database...")

            if DB_PATH.exists():
                DB_PATH.unlink()

            shutil.move(BACKUP_PATH, DB_PATH)
    sys.exit(0)
    
try:
    selected = tests[int(choice) - 1]
except (ValueError, IndexError):
    print("Scelta non valida")
    sys.exit(1)

print(f"\nAvvio {selected.name}\n")

subprocess.run([sys.executable, str(test_file.relative_to(ROOT_DIR))], cwd=ROOT_DIR)