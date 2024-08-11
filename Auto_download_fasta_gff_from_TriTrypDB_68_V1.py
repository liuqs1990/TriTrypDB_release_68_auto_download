import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL
base_url = "https://tritrypdb.org/common/downloads/release-68/"

# Create a session
session = requests.Session()

# Fetch the main page content
response = session.get(base_url)
if response.status_code == 200:
    main_page = response.text
else:
    raise Exception(
        f"Failed to retrieve main page. Status code: {response.status_code}"
    )

# Parse the main page content
soup = BeautifulSoup(main_page, "html.parser")

# Find all subfolder links
subfolders = [
    a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith("/")
]

# Filter out non-subfolder links (like parent directory links)
subfolders = [folder for folder in subfolders if folder != "../"]


# Helper function to check for specific files in a subfolder
def download_file_if_exists(base_url, folder_name, file_extension, exclude=None):
    folder_url = urljoin(base_url, folder_name)
    response = session.get(folder_url)
    if response.status_code != 200:
        print(f"Failed to access {folder_url}, Status Code: {response.status_code}")
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    files = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].endswith(file_extension)
    ]
    for file in files:
        if exclude and exclude in file:
            continue
        file_url = urljoin(folder_url, file)
        print(f"Downloading {file_url}")
        file_content = session.get(file_url).content
        with open(file, "wb") as f:
            f.write(file_content)
        return True
    return False


# Check each subfolder for the required subfolders and download the files
for subfolder in subfolders:
    subfolder_url = urljoin(base_url, subfolder)
    print(f"Processing subfolder: {subfolder_url}")

    # Check for fasta/data/ subfolder
    fasta_downloaded = download_file_if_exists(subfolder_url, "fasta/data/", ".fasta")
    if not fasta_downloaded:
        print(f"Genome Not Found for {subfolder}")

    # Check for gff/data/ subfolder and exclude Orf50.gff
    gff_downloaded = download_file_if_exists(
        subfolder_url, "gff/data/", ".gff", exclude="Orf50.gff"
    )
    if not gff_downloaded:
        print(f"Annotation Not Found for {subfolder}")
