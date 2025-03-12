import gdown 
from parksandrec import app 


def get_tract_lui_data():
    """
    Downloads a pickle file from a Google Drive link.

    The file being downloaded is the land use inventory data linked to 
    census tract IDs.
    """
    file_id = "1Hbweu2_StECH6L4ZhOZ1TUtJYCEtRDxh"
    gdrive_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(gdrive_url, "data/parcel_tract_linked.pkl", quiet = False)

if __name__ == '__main__':
    get_tract_lui_data()
    app.run_server(debug=True)