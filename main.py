import subprocess
import sys
import webbrowser

from advisor_engine.download_model import ensure_model


def bootstrap():
    print("Checking local AI model...")
    ensure_model()

def main():
    bootstrap()

    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.app:app"])
    webbrowser.open("http://127.0.0.1:8000")

    try:
        input("\nPremi INVIO per terminare...\n")
    finally:
        print("Chiusura backend...")
        server.terminate()
        server.wait()
        print("FinanziAI terminato.")


if __name__ == "__main__":
    main()