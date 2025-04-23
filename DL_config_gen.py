import sys
import os
from urllib.parse import urlparse
import csv  # Import CSV module
import argparse
import yaml

def extract_file_name(url):
    """
    Extract the file name from the given URL.
    """
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def main():
    args = parse_args()
    input_file = args.file
    if args.type == "csv":
        gen_csv_with_src(input_file, args.output_dir)
    elif args.type == "yml":
        gen_yml_with_src(input_file, args.output_dir)
            

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
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='Path to the output folder')
    parser.add_argument('-t', '--type', type=str, choices=['csv', 'yml'], required=True, help='Type of output file (csv or yml)')
    return parser.parse_args()


def gen_csv_with_src(links_src, folder):
    """
    Generate CSV file with file names and links from the given src file
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

def gen_yml_with_src(links_src, folder):
    """
    Generate YAML file with file names and links from the given src file
    """
    # get the name of the file links_src without extension
    file_name = os.path.splitext(os.path.basename(links_src))[0] + ".yml"
    yml_file = os.path.join(folder, file_name)
    os.makedirs(os.path.dirname(yml_file), exist_ok=True)

    with open(links_src, "r") as source_file, open(yml_file, "w") as yml_file:
        lines = source_file.readlines()
        data = []
        group = {"group name": "default", "pairs": []}
        group_count = 0

        for line in lines:
            # Skip comments and empty lines
            if line.startswith("# ") or line.strip() == "":
                continue
            # Start new group if line starts with "#! "
            if line.startswith("#! "):
                group_name = line[3:].strip('\n')
                if group_name:
                    group["group name"] = group_name
                    group["pairs"] = []
                    group_count += 1
                print(f"New group: {group_name}")
                if group_count > 1:
                    data.append(group.copy())
                continue
            url = line.strip()
            file_name = extract_file_name(url)
            group["pairs"].append({"file name": file_name, "link": url})
            print(f"Added to YAML: {file_name}, {url}")
        yaml.dump(data, yml_file)

if __name__ == "__main__":
    main()
