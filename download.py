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
from colorama import Fore, init  # Import colorama
import logging  # Import logging module


def main():
    init(autoreset=True)  # Initialize colorama with auto-reset
    setup_logging()  # Set up logging
    args = parse_args()
    QCoreApplication.setApplicationName("Link Downloader")
    app = QApplication(sys.argv)
    login_url = args.url  # Get the login URL from command line arguments
    links_file = args.file # Get the file containing links from command line arguments
    browser = BrowserWindow(login_url)
    browser.show()

    browser.cookies_ready.connect(lambda cookies: download_with_cookies(cookies, links_file))  # Connect the signal to the handler
    sys.exit(app.exec_())


def setup_logging():
    """
    Set up logging to log messages to both a file and the console.
    """
    log_file = "outputs/download.log"
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
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the CSV file containing links.')
    parser.add_argument('-u', '--url', type=str, required=True, help='Login URL for authentication.')
    return parser.parse_args()
    

def download_with_cookies(cookies, links_file):
    """
    Use cookies to download protected data.
    """
    download_dir = "outputs"
    os.makedirs(download_dir, exist_ok=True)
    
    with open(links_file, "r", newline='') as links_file:
        reader = csv.reader(links_file)
        next(reader, None)  # Skip the header row
        for row in reader:
            target_name = row[0]
            target_link = row[1]
            logging.info(Fore.CYAN + f"Processing {target_name} with link {target_link}")

            if target_name and target_link:
                response = requests.get(target_link, cookies=cookies)
                if response.status_code == 200:
                    target = os.path.join(download_dir, os.path.basename(target_name))
                    with open(target, "wb") as f:
                        f.write(response.content)
                    logging.info(Fore.GREEN + f"Downloaded {target_name}")
                else:
                    logging.error(Fore.RED + f"Failed to download {target_name}: {response.status_code}")

                # Add a random delay between 1 and 5 seconds
                delay = random.uniform(1, 5)
                logging.info(Fore.YELLOW + f"Waiting for {delay:.2f} seconds before the next request...")
                time.sleep(delay)

    # Create a zip file of the downloaded files
    logging.info(Fore.MAGENTA + "Finish Downloading All the Files! Creating a zip file...")
    shutil.make_archive(download_dir, 'zip', download_dir)
    logging.info(Fore.BLUE + "Thank you for downloading the files! Have a great day!")


if __name__ == '__main__':
    main()