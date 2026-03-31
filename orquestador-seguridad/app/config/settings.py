import os

# Base directory of the app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Target Configurations
TARGET_URL = os.getenv("TARGET_URL", "http://dvwa")

# ZAP Configurations
ZAP_HOST = os.getenv("ZAP_HOST", "zap")
ZAP_PORT = int(os.getenv("ZAP_PORT", 8090))
ZAP_API_KEY = os.getenv("ZAP_API_KEY", "12345")

# FFUF Configurations
# We resolve the path relative to the base directory to avoid FileNotFoundError
WORDLIST_PATH = os.getenv("WORDLIST_PATH", os.path.join(BASE_DIR, "worldlists", "wordlist.txt"))

# SQLMap Configurations
SQLMAP_PATH = os.getenv("SQLMAP_PATH", "/opt/sqlmap/sqlmap.py")
SQLMAP_TIMEOUT = int(os.getenv("SQLMAP_TIMEOUT", 300)) # Timeout in seconds

# Result & Reporting Configurations
# Path relative to project root
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.abspath(os.path.join(BASE_DIR, "..", "output", "raw")))
REPORTS_DIR = os.getenv("REPORTS_DIR", os.path.abspath(os.path.join(BASE_DIR, "..", "output", "reports")))
FINAL_REPORT_FILE = "resultado.json"
