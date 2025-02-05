#!/bin/bash

# Ativar o ambiente virtual se necessário
# source /path/to/venv/bin/activate

# Inicia ngrok em background
ngrok http 5006 > /dev/null 2>&1 &

# Aguarda alguns segundos para o ngrok inicializar
sleep 3

# Obtém a URL de forwarding do ngrok via API (sem usar jq)
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4 | sed 's|https://||')

# Verifica se obteve a URL
if [ -z "$NGROK_URL" ]; then
    echo "Erro: Não foi possível obter a URL do ngrok"
    exit 1
fi

echo "Ngrok URL: $NGROK_URL"

# Inicia o Panel com a URL do ngrok
panel serve src/bigbets_origination_crews/main.py \
    --static-dirs /output=output \
    --allow-websocket-origin=$NGROK_URL

# Mata o processo ngrok ao encerrar
trap "pkill ngrok" EXIT