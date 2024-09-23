#!/bin/bash

pip install azure-identity azure-mgmt-network azure-mgmt-compute azure-mgmt-network
nano step_1_provision_vm.py
export AZURE_SUBSCRIPTION_ID="aee8556f-d2fd-4efd-a6bd-f341a90fa76e"
python step_1_provision_vm.py