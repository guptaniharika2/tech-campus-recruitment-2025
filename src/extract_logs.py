import sys
import os

def extract_logs(log_file, target_date, output_dir="output"):
    """
    Extracts logs for a specific date from a large log file efficiently.
    
    Args:
        log_file (str): Path to the log file.
        target_date (str): Date in YYYY-MM-DD format to filter logs.
        output_dir (str, optional): Directory to save the output file. Defaults to "output".
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{target_date}.txt")

    try:
        with open(log_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                if line.startswith(target_date):
                    outfile.write(line)
        print(f"Logs for {target_date} saved in {output_file}")
    except FileNotFoundError:
        print(f"Error: File {log_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_logs.py <log_file_path> <YYYY-MM-DD>")
        sys.exit(1)

    log_file = sys.argv[1]
    target_date = sys.argv[2]
    extract_logs(log_file, target_date)
