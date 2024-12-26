import subprocess

def ejecutar_scripts():
    scripts = ["src/00_data_download.py", "src/01_data_analysis.py", "scripts/src/02_data_results.py"]
    
    for script in scripts:
        print(f"Executing {script}...")
        result = subprocess.run(["python", script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error in {script}:\n{result.stderr}")
            return
        print(f"Output of {script}:\n{result.stdout}")

if __name__ == "__main__":
    ejecutar_scripts()
