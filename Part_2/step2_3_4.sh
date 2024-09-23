#!/bin/bash

# Step 2&3&4
pip install azure-identity azure-storage-blob pandas
nano step2_3_4_data_analysis.py
python step2_3_4_data_analysis.py

# Download to VM
# Generate ssh key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/mysshkey

az vm user update \
  --resource-group Data_Engineer \
  -- name VM-ZhengWang \
  -- username zhengwang \
  --ssh-key-value ~/.ssh/mysshkey.pub

# Connect to VM
ssh zhengwang@4.180.128.244

# go to home directory
cd ..

# download file
az storage blob download \
  --container-name zheng-wang \
  --name Zheng-Wang/Zheng-Wang.csv \
  --file result-ZhengWang.csv \
  --account-name dataengineerv1 \
  --account-key replace-account-key