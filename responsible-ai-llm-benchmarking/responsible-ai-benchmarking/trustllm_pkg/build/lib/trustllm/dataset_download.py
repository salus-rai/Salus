import requests
import os
import zipfile
import logging

log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
def download_dataset(save_path=None):
    """
    Download a dataset from Hugging Face and save it locally.

    Args:
    - save_path (str, optional): The local path to save the dataset. If None, uses default path.

    Returns:
    - None
    """
    repo = 'HowieHwong/TrustLLM'
    branch = 'main'
    folder_path = 'dataset'
    # Ensure the output directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # GitHub API endpoint for contents of the repository
    api_url = f"https://api.github.com/repos/{repo}/contents/{folder_path}?ref={branch}"

    response = requests.get(api_url)
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item['type'] == 'file':
                log.info(f"Downloading {item['name']}...")
                file_response = requests.get(item['download_url'])
                if file_response.status_code == 200:
                    with open(os.path.join(save_path, item['name']), 'wb') as file:
                        file.write(file_response.content)
                else:
                    log.info(f"Failed to download {item['name']}")
            else:
                log.info(f"Skipping {item['name']}, as it's not a file.")
    else:
        log.info("Failed to fetch repository data.")
        

    zip_path = os.path.join(save_path, "dataset.zip")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)

    # Delete the ZIP file after extraction
    os.remove(zip_path)

    

