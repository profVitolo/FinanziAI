import subprocess
import sys
import webbrowser


def main():
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