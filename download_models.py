import os
import requests

def downloadModel(url, write_path):
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    filename = os.path.basename(url)
    with open(os.path.join(write_path, filename), "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {filename}")


downloadModel("https://github.com/NYUAD-CRC/riskHPC/releases/download/v1.0/ClassFier_LGBM_alldata.joblib", "./classification_model/models")
downloadModel("https://github.com/NYUAD-CRC/riskHPC/releases/download/v1.0/RandomForest_balanced_all_ComputeTimewithsampling.joblib", "./ComputeTimewithsampling/models")
downloadModel("https://github.com/NYUAD-CRC/riskHPC/releases/download/v1.0/RandomForest_balanced_all_MEMwithsampling.joblib", "./MEMwithsampling/models")