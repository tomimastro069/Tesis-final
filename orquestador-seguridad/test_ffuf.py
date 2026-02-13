from app.scanners.ffuf import run_ffuf

def main():
    result = run_ffuf(
        target_url="http://dvwa",
        wordlist_path="worldlists/small.txt",  # <-- CORRECTO
        output_dir="output/raw"
    )

    print("Archivo JSON generado en:", result["output_file"])
    print("stdout:\n", result["stdout"])
    print("stderr:\n", result["stderr"])

if __name__ == "__main__":
    main()
