import os
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


# Function to download a specific file and maintain directory structure
def download_file(base_url, relative_url, local_dir):
    file_url = urljoin(base_url, relative_url)
    local_path = os.path.join(local_dir, os.path.basename(relative_url))

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


# Iterate over each subfolder and download the specific files
for subfolder in subfolders:
    subfolder_name = subfolder.strip(
        "/"
    )  # Extract the subfolder name (e.g., 'AdeanaiCavalhoATCCPRA-265')

    # Define the files to download for each subfolder
    fasta_file = (
        f"{subfolder_name}/fasta/data/TriTrypDB-68_{subfolder_name}_Genome.fasta"
    )
    gff_file = f"{subfolder_name}/gff/data/TriTrypDB-68_{subfolder_name}.gff"

    # Download the fasta file
    download_file(base_url, fasta_file, os.path.join(subfolder_name, "fasta/data"))

    # Download the gff file, excluding Orf50.gff
    download_file(base_url, gff_file, os.path.join(subfolder_name, "gff/data"))
