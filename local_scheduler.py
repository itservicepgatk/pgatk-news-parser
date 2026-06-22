import time
import subprocess
import sys

def run_parser():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting telegram_parser.py...")
    try:
        # Run telegram_parser.py using the current Python interpreter
        subprocess.run([sys.executable, "telegram_parser.py"], check=True)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] telegram_parser.py finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error running telegram_parser.py: {e}", file=sys.stderr)

if __name__ == "__main__":
    print("Starting local news parser scheduler. Press Ctrl+C to exit.")
    print("Will run telegram_parser.py every 30 minutes.")
    try:
        while True:
            run_parser()
            print("Sleeping for 30 minutes...")
            time.sleep(1800)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
