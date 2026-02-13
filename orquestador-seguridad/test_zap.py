from app.scanners.zap import run_zap

def main():
    result = run_zap(
        target_url="http://dvwa:80",
        output_dir="output/raw"
    )

    print("Archivo JSON generado en:", result["output_file"])
    print("stdout:\n", result["stdout"])
    print("stderr:\n", result["stderr"])

if __name__ == "__main__":
    main()
