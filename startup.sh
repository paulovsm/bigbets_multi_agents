#!/bin/bash

# Ativar o ambiente virtual se necessário
# source /path/to/venv/bin/activate

# Inicia o Panel com a URL do ngrok
panel serve src/bigbets_origination_crews/main.py \
    --static-dirs /output=output