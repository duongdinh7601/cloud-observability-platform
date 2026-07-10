import os
import sys
import urllib.error
import urllib.request


def main():
    # Optional override for non-default deployments
    url = os.getenv("HEALTHCHECK_URL", "http://localhost:8000/health/ready")
    try:
        # Sends HTTP request to url
        # If success, stores HTTP response in "response"
        with urllib.request.urlopen(url, timeout=2) as response:
            sys.exit(0 if response.status == 200 else 1)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
