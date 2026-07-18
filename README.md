# riskHPC
# To run the test pipeline
Step 1 cd riskHPC
Step 2 conda env create -f environment.yml
Step 2 conda activate riskHPC
Step 3 pip install -r requirements.txt
Step 4 python download_models.py
Step 5 python test.py