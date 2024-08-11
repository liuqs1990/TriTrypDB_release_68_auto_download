import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

# Base URL of the website
base_url = "https://tritrypdb.org/common/downloads/release-68/"

# Create a session
session = requests.Session()


# Function to download a file and preserve directory structure
def download_file(file_url, local_dir):
    file_name = os.path.basename(unquote(file_url))
    local_path = os.path.join(local_dir, file_name)

    # Create local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    # Download and save the file
    print(f"Downloading {file_url} to {local_path}")
    response = session.get(file_url)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download {file_url}, Status Code: {response.status_code}")


# Function to recursively scrape directories and download files
def scrape_directory(url, local_root):
    print(f"Scraping directory: {url}")
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}, Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Skip invalid links and parent directory links
        if "?" in href or "&" in href or href.startswith("..") or href.startswith("/"):
            print(f"Skipping invalid link: {href}")
            continue

        full_url = urljoin(url, href)
        local_dir = os.path.join(local_root, unquote(href).strip("/"))

        if href.endswith("/"):
            # If the link is a directory, recurse into it
            scrape_directory(full_url, os.path.join(local_root, href.strip("/")))
        else:
            # If the link is a file, download it
            download_file(full_url, local_root)


# Create the local root directory
local_root = "tritrypdb_downloads"

# Start scraping from the base URL
scrape_directory(base_url, local_root)
