#!/bin/bash
# 🚀 Generador automático de instrucciones IA para proyectos MCP
# Uso: ./generate-mcp-instructions.sh

set -e

# Detectar ubicación del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"

echo "🚀 Generando instrucciones IA para proyecto MCP: $PROJECT_NAME"
echo "📁 Ubicación: $PROJECT_DIR"

# Verificar si es un proyecto MCP
if [[ ! -f "$PROJECT_DIR/groq_mcp_fast.py" && ! -f "$PROJECT_DIR/requirements.txt" ]]; then
    echo "❌ Error: No parece ser un proyecto MCP válido"
    echo "   Se esperan archivos como groq_mcp_fast.py o requirements.txt"
    exit 1
fi

# Crear directorio .github si no existe
mkdir -p "$PROJECT_DIR/.github"

# Generar fecha actual
CURRENT_DATE=$(date +"%B %Y")

# Detectar tipo de proyecto MCP
MCP_TYPE="MCP Servers"
if [[ -f "$PROJECT_DIR/groq_mcp_fast.py" ]]; then
    MCP_TYPE="MCP Servers con Groq"
elif [[ -f "$PROJECT_DIR/git_mcp_server.py" ]]; then
    MCP_TYPE="MCP Git Server"
fi

# Detectar comandos disponibles
AVAILABLE_COMMANDS=""
for cmd in mcpai mcpask mcpcode mcpgroq; do
    if [[ -f "$PROJECT_DIR/$cmd" ]]; then
        AVAILABLE_COMMANDS="$AVAILABLE_COMMANDS\n- ✅ \`$cmd\` - Comando MCP disponible"
    fi
done

# Detectar configuración de .env
ENV_CONFIG=""
if [[ -f "$PROJECT_DIR/.env.example" ]]; then
    ENV_CONFIG=$(grep "=" "$PROJECT_DIR/.env.example" | head -5 | sed 's/^/# /')
fi

# Generar archivo de instrucciones principal
cat > "$PROJECT_DIR/.github/copilot-instructions.md" << EOF
# Instrucciones para Agentes de IA - $PROJECT_NAME

## 🚨 **CONTEXTO CRÍTICO - LEE ESTO PRIMERO**

### **Ubicación y Ambiente**
- **Directorio de trabajo**: \`$PROJECT_DIR\`
- **Sistema**: Linux (bash shell)
- **Ambiente principal**: **Python 3 con entorno virtual aislado**
- **Idioma**: **SIEMPRE responder en ESPAÑOL**
- **Tipo de proyecto**: **$MCP_TYPE**

### **Estado Actual del Proyecto ($CURRENT_DATE)**
- ✅ **Proyecto MCP**: Detectado y configurado
- ✅ **Entorno Python**: Entorno virtual en .venv
- ✅ **Comandos MCP**: Scripts ejecutables disponibles
- 🔴 **NUNCA** asumir instalaciones globales
- 🔴 **SIEMPRE** usar comandos con \`./\` desde el directorio del proyecto

### **Comandos Disponibles**
$AVAILABLE_COMMANDS

### **Flujo de Trabajo Obligatorio**
1. **ANTES de cualquier acción**: verificar que estamos en \`$PROJECT_DIR\`
2. **Para setup inicial**: SIEMPRE usar \`./setup_portable.sh\`
3. **Para comandos MCP**: SIEMPRE usar \`./comando\` con prefijo
4. **Para debugging**: activar entorno virtual primero
5. **Antes de commits**: verificar que .env no se incluya

### **Comandos que NUNCA debes sugerir**
- ❌ \`pip install\` global (usar entorno virtual .venv)
- ❌ Comandos MCP sin \`./\` (no están en PATH global)
- ❌ \`npm install\` o Node.js (este es proyecto Python puro)
- ❌ Modificaciones del PATH del sistema

### **Comandos que SÍ debes usar siempre**
- ✅ \`./setup_portable.sh\` - configuración inicial automática
- ✅ \`source .venv/bin/activate\` - activar entorno virtual
- ✅ \`echo \$GROQ_API_KEY\` - verificar configuración
- ✅ \`./mcpask "pregunta"\` - preguntas rápidas (si existe)
- ✅ \`python3 groq_mcp_fast.py\` - test directo del servidor

## 🏗️ Arquitectura del Proyecto

Proyecto **$MCP_TYPE** optimizado para velocidad y portabilidad:

\`\`\`
📁 $PROJECT_NAME/
$(find "$PROJECT_DIR" -maxdepth 1 -type f -name "*.py" -o -name "mcp*" -o -name "setup*" -o -name "requirements.txt" | head -10 | sed "s|$PROJECT_DIR/||" | sed 's/^/├── /')
└── .venv/               # Entorno virtual Python
\`\`\`

## 🛠️ Flujos de Trabajo Esenciales

### Setup Inicial Automático
\`\`\`bash
# Configuración completa del proyecto MCP
cd $PROJECT_DIR
chmod +x setup_portable.sh
./setup_portable.sh
nano .env  # Configurar API keys necesarias
\`\`\`

### Comandos de Verificación
\`\`\`bash
# Verificar configuración
echo \$GROQ_API_KEY
ls -la .venv/
source .venv/bin/activate
pip list
\`\`\`

### Debugging de Servidores MCP
\`\`\`bash
# Test directo del servidor principal
source .venv/bin/activate
python3 groq_mcp_fast.py

# Verificar logs si algo falla
ls -la logs/ 2>/dev/null || echo "No hay directorio de logs"
\`\`\`

## 🔧 Configuración Específica

### Variables de Entorno (.env)
\`\`\`bash
$ENV_CONFIG
\`\`\`

### Integración con .bashrc del Usuario
El usuario ya tiene configurado:
- ✅ PATH que incluye proyectos MCP
- ✅ Auto-activación de entornos virtuales Python
- ✅ Aliases para GitHub Copilot CLI
- ✅ Prompt Git avanzado con colores

## 🚨 Errores Comunes en Proyectos MCP

### "Comando no encontrado"
- **Causa**: No usar \`./\` antes del comando MCP
- **Solución**: \`./mcpask\` en lugar de \`mcpask\`

### "ModuleNotFoundError"
- **Causa**: No activar entorno virtual
- **Solución**: \`source .venv/bin/activate\` primero

### "API key not found"
- **Causa**: Archivo .env no configurado
- **Solución**: \`cp .env.example .env\` y configurar keys

### "Permission denied"
- **Causa**: Scripts sin permisos de ejecución
- **Solución**: \`chmod +x setup_portable.sh mcpai mcpask mcpcode mcpgroq\`

## 🎯 **REGLAS DE ORO PARA AGENTES**

### **SIEMPRE hacer esto ANTES de responder:**
1. **Responder en ESPAÑOL** - preferencia crítica del usuario
2. Verificar que estamos en el directorio correcto del proyecto
3. Recordar que es un proyecto Python MCP, no Node.js
4. Usar comandos con \`./\` para scripts del proyecto
5. Verificar entorno virtual antes de operaciones Python

### **NUNCA sugerir:**
- Instalaciones globales de Python (usar .venv)
- Comandos MCP sin \`./\` (no están en PATH)
- Dependencias Node.js (proyecto Python puro)
- **Responder en inglés** (solo español)

### **Contexto del usuario:**
- Sistema Linux con bash optimizado
- .bashrc con prompt Git y auto-activación de entornos virtuales
- GitHub Copilot CLI configurado
- Aliases Docker y Git optimizados

---
**🚀 Ready MCP** | **⚡ Python nativo** | **🔧 Setup automático**
EOF

# Generar archivo de contexto rápido
cat > "$PROJECT_DIR/CONTEXTO_RAPIDO.md" << EOF
# CONTEXTO RÁPIDO - $PROJECT_NAME

## 🚨 ESPAÑOL OBLIGATORIO
**Responder SIEMPRE en español - preferencia crítica del usuario**

## 📁 Ubicación
- **Directorio**: \`$PROJECT_DIR\`
- **Sistema**: Linux + bash + Python 3
- **Tipo**: $MCP_TYPE

## ⚡ Comandos Esenciales
\`\`\`bash
# Setup inicial (solo una vez)
./setup_portable.sh

# Comandos MCP (usar con ./)
$AVAILABLE_COMMANDS

# Verificación
echo \$GROQ_API_KEY
source .venv/bin/activate
python3 groq_mcp_fast.py
\`\`\`

## 🔧 Configuración Clave
- **API keys**: En archivo .env (nunca commitear)
- **Entorno**: Todo en .venv (nunca global)
- **Scripts**: Usar \`./comando\` siempre

## 🚨 Soluciones Rápidas
- "Command not found" → Usar \`./comando\`
- "API key not found" → Configurar .env
- "Module not found" → \`source .venv/bin/activate\`
- "Permission denied" → \`chmod +x\` a los scripts

**🎯 Proyecto MCP ultra-rápido** | **Python puro** | **Setup automático**
EOF

echo "✅ Instrucciones generadas:"
echo "   📄 .github/copilot-instructions.md"
echo "   📄 CONTEXTO_RAPIDO.md"
echo ""
echo "🎯 Listo para usar con agentes IA en español"
echo "💡 Los agentes detectarán automáticamente el contexto MCP"
