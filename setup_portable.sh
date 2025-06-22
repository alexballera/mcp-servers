#!/bin/bash
# 🚀 Setup automático para MCP Servers - Portátil
# Configura el proyecto en cualquier dispositivo

echo "🚀 Configurando MCP Servers..."

# Detectar ubicación actual del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "� Proyecto detectado en: $PROJECT_DIR"

# Verificar que estamos en el directorio correcto
if [ ! -f "$PROJECT_DIR/groq_mcp_fast.py" ]; then
    echo "❌ Error: No se encontraron los archivos MCP"
    echo "   Ejecuta este script desde el directorio mcp-servers"
    exit 1
fi

# Configurar entorno virtual
echo "🐍 Configurando entorno Python..."
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    python3 -m venv "$PROJECT_DIR/.venv"
fi

source "$PROJECT_DIR/.venv/bin/activate"
pip install -r "$PROJECT_DIR/requirements.txt"

# Configurar archivo .env si no existe
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo "� Archivo .env creado - configura tus API keys"
fi

# Dar permisos a comandos de terminal
chmod +x "$PROJECT_DIR"/{mcpai,mcpask,mcpcode,mcpgroq}

# Actualizar shebangs para usar el entorno virtual local
for cmd in mcpai mcpask mcpcode mcpgroq; do
    if [ -f "$PROJECT_DIR/$cmd" ]; then
        sed -i "1s|.*|#!$PROJECT_DIR/.venv/bin/python3|" "$PROJECT_DIR/$cmd"
    fi
done

echo ""
echo "✅ Setup completado!"
echo ""
echo "📋 Comandos disponibles:"
echo "  ./mcpask \"pregunta rápida\""
echo "  ./mcpcode \"problema de código\""
echo "  ./mcpai chat \"conversación\""
echo "  ./mcpgroq \"chat directo\""
echo ""
echo "📝 Próximos pasos:"
echo "1. Edita $PROJECT_DIR/.env con tus API keys"
echo "2. Opcionalmente, agrega al PATH:"
echo "   export PATH=\"\$PATH:$PROJECT_DIR\""
echo "3. Para VS Code, usa esta configuración en settings.json:"
echo ""
echo "{"
echo "  \"mcp\": {"
echo "    \"servers\": {"
echo "      \"groq-agent\": {"
echo "        \"command\": \"$PROJECT_DIR/.venv/bin/python3\","
echo "        \"args\": [\"$PROJECT_DIR/groq_mcp_fast.py\"]"
echo "      },"
echo "      \"git-python\": {"
echo "        \"command\": \"$PROJECT_DIR/.venv/bin/python3\","
echo "        \"args\": [\"$PROJECT_DIR/git_mcp_server.py\"]"
echo "      },"
echo "      \"github-python\": {"
echo "        \"command\": \"$PROJECT_DIR/.venv/bin/python3\","
echo "        \"args\": [\"$PROJECT_DIR/github_mcp_server.py\"],"
echo "        \"env\": { \"GITHUB_TOKEN\": \"tu_token_aqui\" }"
echo "      }"
echo "    }"
echo "  }"
echo "}"
