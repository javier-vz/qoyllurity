#!/usr/bin/env bash
# Script de inicio — Qoyllur Rit'i Explorer Offline
# Generado por instalar_rpi5.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activar entorno virtual
source "$SCRIPT_DIR/.venv/bin/activate"

# Iniciar Ollama si no está corriendo
if ! pgrep -x "ollama" > /dev/null; then
    echo "Iniciando Ollama..."
    ollama serve &>/dev/null &
    sleep 2
fi

# Iniciar Streamlit
echo "Iniciando Qoyllur Rit'i Explorer..."
echo "Abre tu navegador en: http://localhost:8501"
echo "(En red local: http://$(hostname -I | awk '{print $1}'):8501)"
echo ""
streamlit run app_offline.py     --server.port 8501     --server.address 0.0.0.0     --server.headless true     --browser.gatherUsageStats false
