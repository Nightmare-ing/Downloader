import sys
import os
from urllib.parse import urlparse
import csv  # Import CSV module
import argparse

def extract_file_name(url):
    """
    Extract the file name from the given URL.
    """
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def main():
    input_file = "inputs/links.src"
    output_dir = "inputs"
    gen_csv_with_links(input_file, output_dir)
            

def gen_csv_with_links(links_src, folder):
    """
    Generate CSV file with file names and links from the given src file which only contain links
    """
    # get the name of the file links_src without extension
    file_name = os.path.splitext(os.path.basename(links_src))[0] + ".csv"
    csv_file = os.path.join(folder, file_name)
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(links_src, "r") as source_file, open(csv_file, "w", newline="") as csv_file:
        lines = source_file.readlines()
        writer = csv.writer(csv_file)
        writer.writerow(["File Name", "Link"])  # Write CSV header

        for line in lines:
            url = line.strip()
            file_name = extract_file_name(url)
            writer.writerow([file_name, url])  # Write file name and link to CSV
            print(f"Added to CSV: {file_name}, {url}")


if __name__ == "__main__":
    main()
