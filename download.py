import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from browser import BrowserWindow
import os
import csv
import requests
import shutil
import argparse
import time
import random
from colorama import Fore, init, Style  # Import colorama
import logging  # Import logging module
import yaml
from google_drive_downloader import create_service, get_file_id, download_docs_with_id, download_file_with_id


def main():
    download_dir = "outputs"
    # remove the old directory if it exists
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir, exist_ok=True)

    init(autoreset=True)  # Initialize colorama with auto-reset
    setup_logging()  # Set up logging
    args = parse_args()
    QCoreApplication.setApplicationName("Link Downloader")
    app = QApplication(sys.argv)
    login_url = args.url  # Get the login URL from command line arguments
    browser = BrowserWindow(login_url)
    browser.show()

    config_file_src = args.file
    if os.path.isdir(config_file_src):
        file_batches_dir = config_file_src
        browser.cookies_ready.connect(lambda cookies: batch_download(cookies, file_batches_dir, download_dir))
    else:
        links_file = config_file_src
        browser.cookies_ready.connect(lambda cookies: single_download(cookies, links_file, download_dir))
    sys.exit(app.exec_())


def setup_logging():
    """
    Set up logging to log messages to both a file and the console.
    """
    log_file = "outputs/download.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True) # create the file if not exist
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Log to a file
            logging.StreamHandler()        # Log to the console
        ]
    )
    logging.info("Logging initialized. Messages will be logged to both the terminal and the log file.")


def parse_args():
    """
    Parse command line arguments.
    """
    if len(sys.argv) < 5:
        print("Usage: python download.py --file <links.csv> --url <login_url>")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Download files using cookies.")
    parser.add_argument('-u', '--url', type=str, required=True, help='Login URL for authentication.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the CSV or YML file containing links, or path to the dir containing bathes of CSV or YML files')
    return parser.parse_args()
    

def single_download(cookies, links_file, download_dir):
    """
    Use cookies to download protected data described in a CSV or YML file.
    :param cookies: The cookies to use for the download.
    :param links_file: The path to the CSV or YML file.
    :param download_dir: The directory to save all the downloaded things described in CSV or YML file.
    """
    if links_file.endswith(".csv"):
        parse_csv(cookies, links_file, download_dir)
    elif links_file.endswith(".yml") or links_file.endswith(".yaml"):
        parse_yml(cookies, links_file, download_dir)
    else:
        logging.error(Fore.RED + "Unsupported file format. Please provide a CSV or YML file." + Style.RESET_ALL)
        sys.exit(1)
    after_download()

    
def batch_download(cookies, input_dir, output_dir):
    """
    Download according to all files in the input directory and save them to the output directory.
    :param cookies: The cookies use for downloading.
    :param input_dir: The directory containing the csv or yml files used for downloading.
    :param output_dir: The root directory to save all the downloaded things.
    """
    for conifg_file in os.listdir(input_dir):
        if conifg_file.endswith(".csv") or conifg_file.endswith(".yml") or conifg_file.endswith(".yaml"):
            config_file_path = os.path.join(input_dir, conifg_file)
            if conifg_file.endswith(".csv"):
                parse_csv(cookies, config_file_path, output_dir)
            else:
                config_file_name = os.path.splitext(conifg_file)[0]
                download_dir = os.path.join(output_dir, config_file_name)
                parse_yml(cookies, config_file_path, download_dir)
    after_download()


def parse_csv(cookies, csv, download_dir):
    """
    Use cookies to download protected data described in a CSV file.
    :param cookies: The cookies to use for the download.
    :param csv: The path to the CSV file.
    :param download_dir: The directory to save all the downloaded things described in CSV file.
    """
    with open(csv, "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        name_with_links = [(row[0], row[1]) for row in reader if row]
    for pair in name_with_links:
        target_name = pair[0]
        target_link = pair[1]
        download_file_with_lnk(download_dir, target_name, target_link, cookies)


def parse_yml(service, creds, cookies, yml, download_dir):
    """
    Use cookies to download protected data described in a YAML file.
    :param cookies: The cookies to use for the download.
    :param file_path: The path to the YAML file.
    :param download_dir: The directory to save all the downloaded things described in YAML file.
    :return: None
    """
    with open(yml, "r") as ymlfile:
        data = yaml.safe_load(ymlfile)
    for group in data:
        if group["pairs"] == []:
            continue
        sub_dir_path = os.path.join(download_dir, group["group name"])
        os.makedirs(sub_dir_path, exist_ok=True)
        logging.info(Fore.CYAN + f"Creating group: {group['group name']}" + Style.RESET_ALL)
        for pair in group["pairs"]:
            target_name = pair["file name"]
            target_link = pair["link"]
            if "google.com" in target_link:
                file_id = get_file_id(target_link)
                if "presentation" in target_link:
                    download_docs_with_id(sub_dir_path, file_id, service, types=["pptx", "pdf"])
                elif "document" in target_link:
                    download_docs_with_id(sub_dir_path, file_id, service, types=["docx", "pdf"])
                elif "drive.google.com" in target_link:
                    download_file_with_id(sub_dir_path, file_id, creds, "pdf")
                else:
                    logging.error(Fore.RED + f"Unsupported Google Drive link: {target_link}" + Style.RESET_ALL)
                    continue
            else:
                download_file_with_lnk(sub_dir_path, target_name, target_link, cookies)


def after_download():
    """
    Perform any actions needed after the download is complete.
    """
    logging.info(Fore.MAGENTA + "Finish Downloading All the Files! Creating a zip file..." + Style.RESET_ALL)
    shutil.make_archive("outputs", 'zip', "outputs")
    logging.info(Fore.BLUE + "Thank you for downloading the files! Have a great day!" + Style.RESET_ALL)


def download_file_with_lnk(folder, file, link, cookies):
    """
    Download a file using the provided link and cookies.
    :param folder: The folder to save the downloaded file.
    :param file: The name of the file to save.
    :param link: The link to download the file from.
    :param cookies: The cookies to use for the download.
    :return: None
    """
    logging.info(Fore.CYAN + f"Processing {file} with link {link}" + Style.RESET_ALL)
    if file and link:
        response = requests.get(link, cookies=cookies)
        if response.status_code == 200:
            target = os.path.join(folder, os.path.basename(file))
            with open(target, "wb") as f:
                f.write(response.content)
            logging.info(Fore.GREEN + f"Downloaded {file}" + Style.RESET_ALL)
        else:
            logging.error(Fore.RED + f"Failed to download {file}: {response.status_code}" + Style.RESET_ALL)
        
        # Add a random delay between 1 and 5 seconds
        delay = random.uniform(1, 5)
        logging.info(Fore.YELLOW + f"Waiting for {delay:.2f} seconds before the next request..." + Style.RESET_ALL)
        time.sleep(delay)
    if link and "google.com" in link:
        file_id = get_file_id(link)
        creds, service = create_service()
        download_docs_with_id(file_id, service, types=["pptx", "pdf"])





if __name__ == '__main__':
    main()