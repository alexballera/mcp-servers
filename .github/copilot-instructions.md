# Instrucciones para Agentes de IA - MCP Servers

## 🚨 **CONTEXTO CRÍTICO - LEE ESTO PRIMERO**

### **Ubicación y Ambiente**
- **Directorio de trabajo**: `/home/alexballera/mcp-servers`
- **Sistema**: Linux (bash shell)
- **Ambiente principal**: **Python 3 con entorno virtual aislado**
- **Idioma**: **SIEMPRE responder en ESPAÑOL**
- **NO usar Python global** - todo funciona dentro del entorno virtual `.venv`

### **Estado Actual del Proyecto (Julio 2025)**
- ✅ **Servidores MCP**: Completamente funcionales y optimizados
- ✅ **Comandos Terminal**: mcpai, mcpask, mcpcode, mcpgroq operativos
- ✅ **Integración VS Code**: Configurado automáticamente con `${env:HOME}`
- 🔴 **NUNCA** asumir que algo está "instalado globalmente"
- 🔴 **SIEMPRE** usar comandos con `./` desde el directorio del proyecto

### **Flujo de Trabajo Obligatorio**
1. **ANTES de cualquier acción**: verificar que estamos en `/home/alexballera/mcp-servers`
2. **Para setup inicial**: SIEMPRE usar `./setup_portable.sh`
3. **Para comandos**: SIEMPRE usar `./mcpask`, `./mcpcode`, etc.
4. **Para debugging**: usar `python3 groq_mcp_fast.py` con entorno virtual activado
5. **Antes de commits**: verificar que `.env` no se incluya

### **Comandos que NUNCA debes sugerir**
- ❌ `pip install` global (usar el entorno virtual `.venv`)
- ❌ `npm install` o Node.js (este proyecto es Python puro)
- ❌ `mcpask` sin `./` (no está en PATH por defecto)
- ❌ Modificaciones del PATH global del sistema

### **Comandos que SÍ debes usar siempre**
- ✅ `./setup_portable.sh` - setup inicial completo
- ✅ `./mcpask "pregunta"` - preguntas rápidas (0.4-0.8s)
- ✅ `./mcpcode "problema"` - asistencia de código (1.0-1.5s)
- ✅ `./mcpgroq "chat"` - chat ultra-rápido (0.5-1.0s)
- ✅ `source .venv/bin/activate` - activar entorno virtual
- ✅ `echo $GROQ_API_KEY` - verificar configuración

## 🏗️ Arquitectura del Proyecto

Este es un **ecosistema MCP (Model Context Protocol)** optimizado para **velocidad extrema** con múltiples interfaces:

```
📁 mcp-servers/
├── groq_mcp_fast.py     # 🤖 Servidor MCP principal (Groq API)
├── git_mcp_server.py    # 🔧 Operaciones Git via MCP
├── github_mcp_server.py # 🐙 API GitHub via MCP
├── mcpai                # 💬 Agente terminal completo
├── mcpask               # ❓ Preguntas rápidas
├── mcpcode              # 💻 Asistente de código
├── mcpgroq              # ⚡ Chat ultra-rápido
├── setup_portable.sh    # 🚀 Setup automático
├── requirements.txt     # 📦 Dependencias Python
├── .env                 # 🔑 API keys (NUNCA commitear)
└── .venv/               # 🐍 Entorno virtual aislado
```

### Componentes Clave
- **Rendimiento crítico**: Todas las respuestas deben ser <2 segundos
- **Portabilidad**: Funciona en múltiples dispositivos con `${env:HOME}`
- **Python nativo**: Sin Node.js, solo Python + entorno virtual
- **APIs requeridas**: Groq (obligatorio), GitHub (opcional)
├── groq_mcp_fast.py     # 🤖 Servidor MCP con Groq (respuestas <2s)
├── git_mcp_server.py    # 🔧 Operaciones Git via MCP
├── github_mcp_server.py # 🐙 API GitHub via MCP
├── mcpai                # 💬 Agente terminal completo
├── mcpask               # ❓ Preguntas rápidas (0.4-0.8s)
├── mcpcode              # 💻 Asistente de código (1.0-1.5s)
├── mcpgroq              # ⚡ Chat ultra-rápido (0.5-1.0s)
├── setup_portable.sh    # 🚀 Setup automático y portable
├── requirements.txt     # 📦 Dependencias Python
├── .env.example         # ⚙️ Template configuración
└── .venv/               # 🐍 Entorno virtual aislado
```

### Componentes Clave
- **Rendimiento crítico**: Todas las respuestas deben ser <2 segundos
- **Portabilidad**: Funciona en múltiples dispositivos con `${env:HOME}`
- **Python nativo**: Sin Node.js, solo Python + entorno virtual
- **APIs requeridas**: Groq (obligatorio), GitHub (opcional)

## 🛠️ Flujos de Trabajo Esenciales

### Setup Inicial Automático
```bash
# Configuración completa en 2 minutos
git clone [repo] ~/mcp-servers
cd ~/mcp-servers
chmod +x setup_portable.sh
./setup_portable.sh
nano .env  # Agregar GROQ_API_KEY
```

### Comandos Diarios
```bash
# Preguntas rápidas (0.4-0.8s)
./mcpask "¿cómo optimizar esta función Python?"

# Asistencia de código (1.0-1.5s)
./mcpcode "tengo un error en mi API Flask"

# Chat conversacional (0.5-1.0s)
./mcpgroq "explícame los microservicios"

# Agente completo (0.8-1.2s)
./mcpai chat "analiza este código y sugiere mejoras"
```

### Debugging y Mantenimiento
```bash
# Verificar configuración
echo $GROQ_API_KEY

# Test directo del servidor MCP
source .venv/bin/activate
python3 groq_mcp_fast.py

# Reinstalar dependencias
source .venv/bin/activate
pip install -r requirements.txt
```

## 🎯 Patrones de Performance Críticos

### Objetivos de Velocidad
| Comando | Target | Estado Actual |
|---------|--------|---------------|
| mcpask | 0.4-0.8s | ✅ Operativo |
| mcpcode | 1.0-1.5s | ✅ Operativo |
| mcpgroq | 0.5-1.0s | ✅ Operativo |
| mcpai | 0.8-1.2s | ✅ Operativo |
| MCP Git | Instantáneo | ✅ Operativo |
| MCP GitHub | 1-3s | ✅ Operativo |

### Optimizaciones Implementadas
- **Python puro**: Sin dependencias Node.js
- **Entorno virtual aislado**: Sin conflictos de versiones
- **API Groq optimizada**: Llama-3.1 ultra-rápido
- **Portabilidad con `${env:HOME}`**: Funciona en múltiples dispositivos

## 🔧 Configuración de VS Code

### Configuración MCP Automática
El proyecto está diseñado para detectarse automáticamente en VS Code:

```json
{
  "mcp": {
    "servers": {
      "groq-agent": {
        "command": "${env:HOME}/mcp-servers/.venv/bin/python3",
        "args": ["${env:HOME}/mcp-servers/groq_mcp_fast.py"]
      },
      "git-python": {
        "command": "${env:HOME}/mcp-servers/.venv/bin/python3", 
        "args": ["${env:HOME}/mcp-servers/git_mcp_server.py"]
      },
      "github-python": {
        "command": "${env:HOME}/mcp-servers/.venv/bin/python3",
        "args": ["${env:HOME}/mcp-servers/github_mcp_server.py"],
        "env": {
          "GITHUB_TOKEN": "tu_github_token_aqui"
        }
      }
    }
  }
}
```

### Integración con .bashrc del Usuario
El usuario ya tiene configurado:
- ✅ `PATH="$HOME/mcp-servers:$PATH"` - Comandos accesibles globalmente
- ✅ `MCP_PATH="$HOME/mcp-servers"` - Variable de referencia
- ✅ GitHub Copilot CLI aliases (`ask`, `explain`, `cpl`)
- ✅ Prompt Git avanzado con estado de repositorio
- ✅ Auto-activación de entornos virtuales Python
- ✅ Node.js dockerizado dinámico por .nvmrc/package.json

## 📁 Convenciones de Archivos

### Variables de Entorno (.env)
```bash
GROQ_API_KEY=gsk_...           # OBLIGATORIO - console.groq.com
GITHUB_TOKEN=ghp_...           # OPCIONAL - github.com/settings/tokens
```

### Scripts Ejecutables
- **setup_portable.sh**: Setup automático, debe tener permisos +x
- **mcpai, mcpask, mcpcode, mcpgroq**: Comandos ejecutables sin extensión

### Portabilidad
- **Ubicación estándar**: `~/mcp-servers` en todos los dispositivos
- **Variables de entorno**: `${env:HOME}` para rutas portátiles
- **Sin dependencias globales**: Todo aislado en `.venv`

## 🧹 Gestión de Estado

### Archivos que NUNCA commitear
- `.env` - Contiene API keys sensibles
- `.venv/` - Entorno virtual (se regenera automáticamente)
- `__pycache__/` - Cache de Python

### Reset Completo
```bash
# Si algo falla, reset completo
rm -rf .venv
./setup_portable.sh
nano .env  # Volver a configurar API keys
```

## 🎯 Patrones de Desarrollo

### Flujo Típico de Usuario
1. **Setup inicial**: `./setup_portable.sh` (una sola vez)
2. **Uso diario**: Comandos `./mcpask`, `./mcpcode` según necesidad
3. **VS Code**: Integración automática con Copilot
4. **Debugging**: `python3 groq_mcp_fast.py` para testing directo

### Casos de Uso Comunes
- **Consultas rápidas**: `./mcpask "¿cómo hacer X?"`
- **Errores de código**: `./mcpcode "tengo este error: [error]"`
- **Chat conversacional**: `./mcpgroq "explícame este concepto"`
- **Operaciones Git**: Integración automática vía MCP en VS Code

## 🚨 Errores Comunes

### "Comando no encontrado"
- **Causa**: No usar `./` antes del comando
- **Solución**: `./mcpask` en lugar de `mcpask`

### "No such file groq_mcp_fast.py"
- **Causa**: No estar en el directorio correcto
- **Solución**: `cd ~/mcp-servers` primero

### "API key not found"
- **Causa**: `.env` no configurado o sin GROQ_API_KEY
- **Solución**: `nano .env` y agregar la API key

### "Permission denied"
- **Causa**: Scripts sin permisos de ejecución
- **Solución**: `chmod +x setup_portable.sh mcpai mcpask mcpcode mcpgroq`

## 🎯 **REGLAS DE ORO PARA AGENTES**

### **SIEMPRE hacer esto ANTES de responder:**
1. **Responder en ESPAÑOL** - el usuario es hispanohablante
2. Verificar que estamos en `/home/alexballera/mcp-servers`
3. Recordar que TODO funciona con Python + entorno virtual
4. Usar comandos con `./` como primera opción
5. Verificar configuración con `echo $GROQ_API_KEY` si hay dudas

### **NUNCA sugerir:**
- Instalaciones globales de Python packages
- Comandos sin `./` para los scripts MCP
- Node.js o npm (este proyecto es Python puro)
- Modificar PATH del sistema
- **Responder en inglés** (solo español)

### **SIEMPRE preguntar si no estás seguro de:**
- Si el usuario tiene configurado GROQ_API_KEY
- Si está en el directorio correcto
- Si necesita setup inicial o ya está configurado

### **Respuestas típicas que debes dar:**
- Usuario: "No funciona mcpask" → "Usa `./mcpask` desde el directorio mcp-servers. ¿Ya configuraste GROQ_API_KEY?"
- Usuario: "Instala numpy" → "Este proyecto usa Groq API, no necesita numpy. ¿Qué quieres hacer específicamente?"
- Usuario: "Error de permisos" → "Ejecuta `chmod +x setup_portable.sh mcpai mcpask mcpcode mcpgroq`"
- **Todas las respuestas en español, con comandos específicos y explicaciones claras**

### **Contexto adicional del usuario:**
El usuario ya tiene su `.bashrc` optimizado con:
- Prompt Git avanzado con estado de repositorio y colores
- Aliases para GitHub Copilot CLI (`ask`, `explain`, `cpl`)
- PATH configurado para mcp-servers (`$HOME/mcp-servers`)
- Función de auto-activación de entornos virtuales Python
- Aliases de Docker y Git optimizados
- Node.js dockerizado dinámico basado en .nvmrc/package.json
- Variables de entorno cargadas desde ~/.env

---
**🚀 Ready to use en <2 minutos** | **⚡ Respuestas en <2 segundos** | **🔧 Python puro, sin Node.js**
