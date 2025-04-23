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
    args = parse_args()
    input_file = args.file
    output_dir = "inputs"
    gen_csv_with_src(input_file, output_dir)
            

def parse_args():
    """
    Parse command line arguments.
    """
    if len(sys.argv) < 3:
        print("Usage: python csv-gen.py --file <links.src>")
        sys.exit(1)
    
    # check the extension of the file
    if not sys.argv[2].endswith(".src"):
        print("The file must have a .src extension.")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Generate CSV containing file name and links" \
    "from links in src file")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the SRC file containing links')
    return parser.parse_args()


def gen_csv_with_src(links_src, folder):
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
            # Skip comments and empty lines
            if line.startswith("#") or line.strip() == "":
                continue
            url = line.strip()
            file_name = extract_file_name(url)
            writer.writerow([file_name, url])  # Write file name and link to CSV
            print(f"Added to CSV: {file_name}, {url}")


if __name__ == "__main__":
    main()
