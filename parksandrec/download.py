import gdown 
from pathlib import Path

def get_tract_lui_data():
    """
    Downloads a pickle file from a Google Drive link.

    The file being downloaded is the land use inventory data linked to 
    census tract IDs.
    """
    
    current_filepath = Path(__file__).resolve()
    output_filepath = str(current_filepath.parents[0] / "data/parcel_tract_linked.pkl")
    print(output_filepath)
    file_id = "1Hbweu2_StECH6L4ZhOZ1TUtJYCEtRDxh"
    gdrive_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(gdrive_url, output_filepath, quiet = False)

# Run this script to download the data for the app
if __name__ == "__main__":
    get_tract_lui_data()