import os
from urllib.parse import urlparse
import csv  # Import CSV module

def extract_file_name(url):
    """
    Extract the file name from the given URL.
    """
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def main():
    input_file = "inputs/links"
    output_csv = "inputs/links.csv"
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)  # Ensure output directory exists

    with open(input_file, "r") as file, open(output_csv, "w", newline="") as csv_file:
        lines = file.readlines()
        writer = csv.writer(csv_file)
        writer.writerow(["File Name", "Link"])  # Write CSV header

        for line in lines:
            url = line.strip()
            file_name = extract_file_name(url)
            writer.writerow([file_name, url])  # Write file name and link to CSV
            print(f"Added to CSV: {file_name}, {url}")

if __name__ == "__main__":
    main()
