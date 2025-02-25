import sys
import os
import zipfile
from datetime import datetime, timedelta

CHUNK_SIZE = 1024 * 1024  # 1 MB

def binary_search_date(zip_file, log_file, target_date, file_size):
    left, right = 0, file_size - 1
    while left <= right:
        mid = (left + right) // 2
        zip_file.seek(max(0, mid - CHUNK_SIZE))
        chunk = zip_file.read(CHUNK_SIZE * 2).decode('utf-8', errors='ignore')
        lines = chunk.split('\n')
        
        # Debugging print statement:
        print(f"Searching for {target_date}, left: {left}, right: {right}, mid: {mid}, chunk_start: {zip_file.tell() - len(chunk.encode('utf-8'))}") 
        
        if len(lines) < 2:
            return mid
        
        first_full_line = lines[1] if mid > 0 else lines[0]
        date_str = first_full_line[:10]
        
        if date_str < target_date:
            left = mid + CHUNK_SIZE
        elif date_str > target_date:
            right = mid - CHUNK_SIZE
        else:
            while mid > 0 and chunk.startswith(target_date):
                mid -= CHUNK_SIZE
                zip_file.seek(max(0, mid - CHUNK_SIZE))
                chunk = zip_file.read(CHUNK_SIZE).decode('utf-8', errors='ignore')
            return zip_file.tell()
    
    return -1

def extract_logs(zip_path, target_date, output_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Delete the output file if it already exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        log_files = [f for f in zip_file.namelist() if f.endswith('.log')]
        if not log_files:
            print("No log files found in the zip archive.")
            return
        
        log_file = log_files[0]  # Assume the first log file is the one we want
        file_size = zip_file.getinfo(log_file).file_size
        
        with zip_file.open(log_file, 'r') as f, open(output_file, 'w', encoding='utf-8') as out:
            start_pos = binary_search_date(f, log_file, target_date, file_size)
            if start_pos == -1:
                print(f"No logs found for date {target_date}")
                return
            
            f.seek(start_pos)
            next_date = (datetime.strptime(target_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                
                chunk = chunk.decode('utf-8', errors='ignore')
                lines = chunk.split('\n')
                for line in lines:
                    if line.startswith(next_date):
                        return
                    if line.startswith(target_date):
                        out.write(line + '\n')
    
    print(f"Logs for {target_date} have been extracted to {output_file}")

if __name__ == "__main__":
    target_date = "2024-12-01"  # Replace with your desired date
    zip_path = "/content/logs_2024.log.zip"  
    output_file = f"output_logs/output_{target_date}.txt"  
    
    extract_logs(zip_path, target_date, output_file)
