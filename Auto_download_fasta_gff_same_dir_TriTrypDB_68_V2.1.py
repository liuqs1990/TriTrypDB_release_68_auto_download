import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL
base_url = "https://tritrypdb.org/common/downloads/release-68/"

# Create a session
session = requests.Session()


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


# Function to parse the main page and get all species subfolders
def get_species_folders(base_url):
    response = session.get(base_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve main page. Status code: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, "html.parser")
    subfolders = [
        a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith("/")
    ]
    subfolders = [folder for folder in subfolders if folder != "../"]
    return subfolders


# Main script logic
species_folders = get_species_folders(base_url)

for species in species_folders:
    species_name = species.strip("/")

    # Define the relative URLs for the fasta and gff files
    fasta_relative_url = (
        f"{species_name}/fasta/data/TriTrypDB-68_{species_name}_Genome.fasta"
    )
    gff_relative_url = f"{species_name}/gff/data/TriTrypDB-68_{species_name}.gff"

    # Download the fasta file and maintain directory structure
    download_file(base_url, fasta_relative_url, f"{species_name}/fasta/data")

    # Download the gff file and maintain directory structure
    download_file(base_url, gff_relative_url, f"{species_name}/gff/data")
