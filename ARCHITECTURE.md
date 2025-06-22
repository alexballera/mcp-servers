# 📚 Documentación Técnica - Ollama MCP Server

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO / TERMINAL                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                 ~/.bashrc (función mcp)                    │
│  • mcp start    → Servidor interactivo                     │
│  • mcp chat     → Comando directo                          │
│  • mcp code     → Comando directo                          │
│  • mcp github   → Comando directo                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├── MODO INTERACTIVO
                  │   ▼
                  │ ┌───────────────────────────────────────┐
                  │ │      ollama_mcp_server.py             │
                  │ │   • Servidor loop interactivo         │
                  │ │   • Parse de comandos                 │
                  │ │   • Interfaz "🤖 MCP>"                │
                  │ └───────────────────────────────────────┘
                  │
                  └── MODO DIRECTO
                      ▼
                    ┌───────────────────────────────────────┐
                    │         mcp_direct.py                 │
                    │   • Comandos one-shot                 │
                    │   • Sin interfaz persistente          │
                    │   • Retorno directo al terminal       │
                    └───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICIOS EXTERNOS                      │
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐               │
│  │   OLLAMA LOCAL  │    │   GITHUB API    │               │
│  │ • llama3.1:8b   │    │ • Repos search  │               │
│  │ • deepseek-coder│    │ • File content  │               │
│  │ • qwen2.5-coder │    │ • Repo info     │               │
│  └─────────────────┘    └─────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

#### Modo Interactivo (mcp start)
```
Terminal → .bashrc → ollama_mcp_server.py → [LOOP] → Input → Parse → API → Response → Output
```

#### Modo Directo (mcp chat/code/github)
```
Terminal → .bashrc → mcp_direct.py → API → Response → Terminal
```

## 🔧 Componentes Detallados

### 1. ollama_mcp_server.py

**Propósito**: Servidor interactivo principal
**Dependencias**: requests, python-dotenv, asyncio

```python
class OllamaMCPServer:
    def __init__(self):
        # Configuración de modelos y APIs
        self.default_model = "llama3.1:8b"
        self.coding_model = "deepseek-coder:6.7b"
        self.github_token = os.getenv('GITHUB_TOKEN')
        
    async def run(self):
        # Loop principal interactivo
        while True:
            user_input = input("🤖 MCP> ")
            result = await self.handle_request(parsed_command)
            print(formatted_output)
```

**Funciones principales**:
- `chat()`: Chat general con Llama
- `code_assist()`: Asistencia de código con DeepSeek
- `github_search()`: Búsqueda en GitHub
- `github_repo_info()`: Info detallada de repos
- `analyze_code()`: Análisis de código
- `review_code()`: Revisión de código

### 2. mcp_direct.py

**Propósito**: Comandos directos sin servidor persistente
**Dependencias**: requests, python-dotenv

```python
class MCPDirect:
    def chat(self, message: str) -> str:
        # Chat directo con timeout
        
    def code_assist(self, query: str) -> str:
        # Código directo con system prompt
        
    def github_search(self, query: str) -> str:
        # Búsqueda directa en GitHub
```

**Ventajas del modo directo**:
- ✅ Sin overhead de servidor
- ✅ Uso desde cualquier directorio
- ✅ Integración fácil en scripts
- ✅ Respuesta inmediata

### 3. install.py

**Propósito**: Instalación y configuración automática

```python
def main():
    check_ollama()           # Verificar Ollama
    setup_venv()             # Crear entorno virtual
    install_dependencies()   # Instalar paquetes
    setup_env_file()         # Configurar .env
    install_models()         # Modelos de Ollama (opcional)
    update_bashrc()          # Configurar aliases
```

### 4. .bashrc Configuration

**Propósito**: Interfaz de usuario en terminal

```bash
mcp() {
    case "$1" in
        start)   # Modo interactivo
        chat)    # Modo directo - chat
        code)    # Modo directo - código
        github)  # Modo directo - GitHub
        *)       # Ayuda y otros comandos
    esac
}
```

## 🔄 Estados del Sistema

### Estados de Ollama
1. **No instalado**: `install.py` detecta y avisa
2. **Instalado pero no corriendo**: Error de conexión
3. **Corriendo sin modelos**: Lista vacía
4. **Completamente funcional**: ✅

### Estados de GitHub
1. **Sin token**: Error en todas las funciones GitHub
2. **Token inválido**: Error 401
3. **Token sin permisos**: Error 403  
4. **Completamente funcional**: ✅

### Estados del MCP
1. **Sin configurar**: Falta .env o dependencias
2. **Parcialmente funcional**: Solo algunas funciones
3. **Completamente funcional**: ✅

## 🛡️ Manejo de Errores

### Patrones Implementados

```python
# Timeout para evitar cuelgues
response = requests.post(url, json=data, timeout=30)

# Manejo específico de errores de API
if response.status_code == 401:
    return "❌ Token de GitHub inválido"
elif response.status_code == 403:
    return "❌ Token sin permisos suficientes"

# Validación de entrada
if not message:
    return "❌ Debes proporcionar un mensaje"

# Fallback graceful
except Exception as e:
    return f"❌ Error: {str(e)}"
```

## 🚀 Extensibilidad

### Agregar Nuevos Modelos

```python
# En ollama_mcp_server.py
self.new_model = "nuevo-modelo:latest"

def new_function(self, query: str):
    return self._ollama_request(self.new_model, query, custom_prompt)
```

### Agregar Nuevas APIs

```python
# En mcp_direct.py
def new_api_integration(self, query: str) -> str:
    headers = {'Authorization': f'Bearer {self.new_token}'}
    response = requests.get(f'https://api.example.com/search?q={query}')
    return self._format_response(response.json())
```

### Agregar Comandos a .bashrc

```bash
# En .bashrc.example
new_command)
    shift
    echo "🔧 Nueva funcionalidad..."
    ~/mcp-servers/.venv/bin/python3 ~/mcp-servers/mcp_direct.py new_function "$@"
    ;;
```

## 📊 Métricas y Logging

### Logging Implementado
- ✅ Errores de conexión
- ✅ Timeouts de API
- ✅ Estados de configuración
- ✅ Verificaciones de modelos

### Posibles Mejoras
- [ ] Métricas de uso
- [ ] Log de comandos ejecutados
- [ ] Tiempo de respuesta por comando
- [ ] Estadísticas de tokens/requests

## 🔧 Configuración Avanzada

### Variables de Entorno Completas

```bash
# APIs
GITHUB_TOKEN=tu_token
OLLAMA_URL=http://localhost:11434

# Modelos
DEFAULT_MODEL=llama3.1:8b
CODING_MODEL=deepseek-coder:6.7b

# Timeouts
API_TIMEOUT=30
OLLAMA_TIMEOUT=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=/tmp/mcp.log
```

### Customización de Prompts

```python
# System prompts personalizables
CODING_PROMPT = """Eres un experto en programación.
Proporciona código limpio y documentado.
Incluye explicaciones claras."""

REVIEW_PROMPT = """Eres un revisor de código senior.
Enfócate en seguridad, rendimiento y mantenibilidad."""
```

## 🧪 Testing

### Comandos de Verificación

```bash
# Verificar estado completo
mcp status

# Test individual de componentes
mcp chat "test"
mcp github "python"
mcp models

# Verificar conexiones
curl http://localhost:11434/api/version  # Ollama
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user  # GitHub
```

### Tests Automáticos (Future)

```python
def test_ollama_connection():
    assert check_ollama_connection() == True

def test_github_search():
    result = github_search("test")
    assert "❌" not in result

def test_mcp_commands():
    # Test todos los comandos principales
    pass
```

---

Esta documentación técnica complementa el README principal con detalles de implementación y arquitectura.
