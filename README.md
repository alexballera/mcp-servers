# 🤖 Ollama MCP Server

Sistema integrado de IA para desarrollo con **Ollama local** + **GitHub** + **Model Context Protocol**.

Un agente de IA **completamente GRATIS**, **privado** y **sin límites** para desarrollo de software.

> 🌟 **Nuevo**: Repositorio optimizado para instalación directa desde GitHub

## 🚀 Instalación Rápida desde GitHub

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/mcp-servers.git
cd mcp-servers

# 2. Configurar entorno
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. Configurar GitHub token
cp .env.example .env
# Editar .env con tu GitHub token

# 4. Configurar terminal (opcional - ajustar ruta según tu instalación)
cat .bashrc.example >> ~/.bashrc
source ~/.bashrc

# 5. Instalar modelos de Ollama
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b

# ¡Listo!
python ollama_mcp_server.py  # Modo interactivo
# o usar comandos directos si configuraste .bashrc
```

## ✨ Características Principales

- 🚀 **Ollama local**: Chat y asistencia de código sin límites ni costos
- 📁 **GitHub integration**: Buscar repos, analizar código, obtener archivos  
- 🔍 **Análisis de código**: Revisión y optimización con IA especializada
- 💬 **Modo dual**: Servidor interactivo Y comandos directos
- 🔒 **Privado y seguro**: Todo funciona localmente
- ⚡ **Desde cualquier proyecto**: Usa el agente desde cualquier directorio

## 🏗️ Instalación Rápida

### Requisitos Previos

- **Ollama** instalado: [https://ollama.ai/](https://ollama.ai/)
- **Python 3.8+**
- **Git**

### Instalación

```bash
# 1. Clonar y configurar
git clone <tu-repo> mcp-servers
cd mcp-servers

# 2. Configurar entorno
python3 -m venv .venv
.venv/bin/pip install requests python-dotenv PyGithub

# 3. Configurar GitHub token
cp .env.example .env
# Editar .env con tu GitHub token

# 4. Configurar terminal
cat .bashrc.example >> ~/.bashrc
source ~/.bashrc

# 5. Instalar modelos recomendados
ollama pull llama3.1:8b
ollama pull deepseek-coder:6.7b

# ¡Listo!
mcp start
```

## 🔧 Configuración de VS Code MCP

Para usar el servidor con VS Code y GitHub Copilot:

### 1. Instalar Extensión MCP
- Instala la extensión "Model Context Protocol" en VS Code

### 2. Configurar settings.json
```json
{
  "mcp": {
    "servers": {
      "ollama-mcp": {
        "command": "python3",
        "args": [
          "/ruta/completa/a/mcp-servers/ollama_mcp_protocol.py"
        ],
        "cwd": "/ruta/completa/a/mcp-servers",
        "env": {
          "PATH": "/ruta/completa/a/mcp-servers/.venv/bin:${PATH}",
          "VIRTUAL_ENV": "/ruta/completa/a/mcp-servers/.venv"
        }
      }
    }
  }
}
```

### 3. Herramientas Disponibles
- `chat` - Chat general con Llama
- `code_assist` - Asistencia de código especializada  
- `github_search` - Buscar repositorios en GitHub
- `analyze_code` - Análisis de código con IA

**Importante:** Asegúrate de que tu `GITHUB_TOKEN` esté en el archivo `.env`

## 🎯 Modos de Uso

### 🖥️ MODO 1: Servidor Interactivo

```bash
mcp start
# Te lleva a: 🤖 MCP> donde escribes comandos interactivos
```

**Comandos disponibles en el servidor:**

```bash
🤖 MCP> help                    # Ver todos los comandos
🤖 MCP> chat Hola, ¿cómo estás? # Chat general con Llama
🤖 MCP> code Crear una API REST  # Asistencia de código con DeepSeek
🤖 MCP> github_search python ML # Buscar repositorios
🤖 MCP> github_repo microsoft/vscode # Info de repositorio
🤖 MCP> analyze_code <código>    # Analizar código
🤖 MCP> review_code <código>     # Revisar código
🤖 MCP> quit                    # Salir
```

### 🚀 MODO 2: Comandos Directos (Agente)

```bash
# Desde cualquier directorio/proyecto:
mcp chat "¿Cómo optimizar este código Python?"
mcp code "Crear una API REST con FastAPI"
mcp github "machine learning python"

# Aliases más cortos:
ai-chat "explícame async/await"
ai-code "mejores prácticas Python"
ai-github "react hooks examples"

# Análisis de archivos:
analyze mi_script.py
review src/app.js
```

## 🔧 Configuración

### GitHub Token (REQUERIDO)

1. Ve a [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Genera token con permisos: `repo`, `public_repo`, `read:org`
3. Agrega a `.env`: `GITHUB_TOKEN=tu_token_aqui`

### Modelos Recomendados

```bash
# Modelos especializados (instalación automática con install.py)
ollama pull deepseek-coder:6.7b     # Mejor para código
ollama pull qwen2.5-coder:7b        # Alternativa rápida
ollama pull llama3.2:3b             # Liviano y eficiente

# Ver modelos instalados
mcp models
```

## 📊 Comandos Disponibles

### Comandos de Sistema
```bash
mcp start       # Iniciar servidor interactivo
mcp status      # Estado del sistema
mcp models      # Ver modelos de Ollama
mcp pull <modelo> # Instalar nuevo modelo
mcp install     # Reinstalar/configurar
mcp help        # Ayuda completa
```

### Comandos de Agente (Directos)
```bash
mcp chat <mensaje>      # Chat con Llama
mcp code <consulta>     # Asistencia de código
mcp github <búsqueda>   # Buscar en GitHub
analyze <archivo>       # Analizar código de archivo
review <archivo>        # Revisar código de archivo
```

## 💡 Ejemplos Prácticos

### Workflow Típico de Desarrollo
```bash
# 1. Estás en tu proyecto
cd ~/mi-proyecto/

# 2. Buscar inspiración
mcp github "fastapi postgresql example"

# 3. Pedir ayuda con código
mcp code "Cómo conectar FastAPI con PostgreSQL usando SQLAlchemy"

# 4. Analizar tu código
analyze src/main.py

# 5. Revisar antes del commit
review components/Header.jsx

# 6. Chat general
mcp chat "¿Cuáles son las mejores prácticas para APIs REST?"
```

### Casos de Uso Específicos
```bash
# Aprendizaje
mcp chat "Explícame el patrón Observer en JavaScript"
mcp code "Ejemplo de Factory Pattern en Python"

# Debugging
mcp code "Por qué mi función async no funciona: <tu_código>"
analyze error.log

# Investigación
mcp github "microservices kubernetes python"
mcp github "machine learning tensorflow examples"

# Code Review
review pull_request.diff
mcp code "Optimiza esta función: <función>"
```

## 🏗️ Arquitectura del Sistema

```
mcp-servers/
├── .env                    # Configuración (GitHub token, etc.)
├── .env.example           # Plantilla de configuración
├── .bashrc.example        # Configuración para ~/.bashrc
├── .venv/                 # Entorno virtual Python
├── requirements.txt       # Dependencias mínimas
├── install.py            # Instalador automático
├── ollama_mcp_server.py  # Servidor MCP interactivo
├── mcp_direct.py         # Comandos directos/agente
├── sync_bashrc.sh        # 🔄 Auto-sync .bashrc → .bashrc.example
├── sync_bashrc.py        # 🔄 Auto-sync (versión Python)
├── help.sh               # 📋 Comandos de ayuda rápida
├── SYNC_SCRIPTS.md       # 📚 Documentación de sincronización
└── README.md             # Esta documentación
```

### Componentes Principales

1. **ollama_mcp_server.py**: Servidor interactivo principal
2. **mcp_direct.py**: Comandos directos para uso como agente
3. **install.py**: Instalación y configuración automática
4. **.bashrc.example**: Configuración de terminal optimizada
5. **sync_bashrc.sh/py**: Scripts de sincronización automática

## 🔄 Scripts de Sincronización

**Mantén tu configuración sincronizada automáticamente:**

```bash
# Ver estado de sincronización
./sync_bashrc.sh --status

# Sincronización única
./sync_bashrc.sh --once

# Monitoreo continuo (auto-sync cuando cambies ~/.bashrc)
./sync_bashrc.sh

# Ayuda rápida
./help.sh
```

**Características:**
- ✅ **Auto-detección** de cambios en `~/.bashrc`
- ✅ **Limpieza automática** de tokens y rutas específicas
- ✅ **Git automation** - commit y push automático
- ✅ **Sin dependencias** (versión Bash) o Python puro
- ✅ **Documentación completa** en `SYNC_SCRIPTS.md`

## 🔄 Flujo de Datos

```
Usuario → Terminal → .bashrc (función mcp) → mcp_direct.py → Ollama/GitHub API → Respuesta
                  ↘ ollama_mcp_server.py → Servidor interactivo
```

## 🛠️ Troubleshooting

### Ollama no responde
```bash
ollama serve              # Iniciar Ollama
ollama list              # Ver modelos instalados
mcp models               # Ver estado desde MCP
```

### Error de dependencias

```bash
cd mcp-servers
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### GitHub no funciona
- Verificar token en `.env`
- Comprobar permisos del token
- `mcp status` para ver configuración

### Comandos no reconocidos
```bash
source ~/.bashrc         # Recargar configuración
mcp help                # Ver comandos disponibles
```

## 🎉 Ventajas del Sistema

### vs ChatGPT/Claude
- ✅ **GRATIS**: Sin suscripciones ni límites
- ✅ **Privado**: Tu código nunca sale de tu máquina
- ✅ **Sin límites**: Usa cuanto quieras
- ✅ **Especializado**: Modelos optimizados para código

### vs GitHub Copilot
- ✅ **Más funciones**: Chat, búsqueda, análisis completo
- ✅ **Sin dependencias**: No necesita IDE específico
- ✅ **Flexible**: Modo interactivo Y comandos directos
- ✅ **Transparente**: Sabes exactamente qué hace

### vs Otras Soluciones
- ✅ **Todo en uno**: IA + Git + Análisis + Chat
- ✅ **Portátil**: Funciona en cualquier máquina
- ✅ **Customizable**: Agrega tus propios modelos/funciones
- ✅ **Sin vendor lock-in**: Es tuyo para siempre

## 📈 Próximas Funciones

- [ ] Integración con más Git providers
- [ ] Análisis de repositorios completos
- [ ] Generación automática de documentación
- [ ] Integración con bases de datos
- [ ] Workflow de CI/CD
- [ ] Soporte para más lenguajes

## 📄 Licencia

MIT License - Úsalo libremente para cualquier propósito.

---

**¡Tu asistente de IA local, gratis y sin límites!** 🚀

Para soporte o contribuciones, abre un issue en el repositorio.
