import os
import sys
import urllib.request, urllib.error

def main():
    url = os.getenv("HEALTHCHECK_URL", "http://localhost:8000/health/ready")
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            sys.exit(0 if response.status == 200 else 1)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()

