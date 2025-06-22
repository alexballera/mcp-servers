# Contribuir a Ollama MCP Server

¡Gracias por tu interés en contribuir! Este proyecto está diseñado para ser simple y fácil de extender.

## 🚀 Configuración para Desarrollo

```bash
# 1. Fork y clonar
git clone https://github.com/tu-usuario/mcp-servers.git
cd mcp-servers

# 2. Configurar entorno de desarrollo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu GitHub token

# 4. Probar instalación
python ollama_mcp_server.py
```

## 🛠️ Estructura del Código

- `ollama_mcp_server.py` - Servidor principal interactivo
- `mcp_direct.py` - Comandos directos para agente
- `install.py` - Instalador automático
- `requirements.txt` - Dependencias mínimas

## 📝 Cómo Contribuir

### Reportar Bugs
1. Verifica que el bug no esté ya reportado
2. Incluye detalles del sistema y pasos para reproducir
3. Agrega logs si es posible

### Sugerir Funcionalidades
1. Describe el caso de uso
2. Explica el beneficio para los usuarios
3. Propón una implementación si es posible

### Enviar Pull Requests
1. Fork del repositorio
2. Crear branch para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Hacer cambios con commits descriptivos
4. Probar que todo funciona
5. Enviar PR con descripción clara

## 🔧 Extensibilidad

### Agregar Nuevos Comandos

**Servidor Interactivo** (`ollama_mcp_server.py`):
```python
def nuevo_comando(self, parametros):
    """Descripción del nuevo comando"""
    # Tu lógica aquí
    return "Resultado"

# Agregar a self.tools en __init__
self.tools['nuevo'] = self.nuevo_comando
```

**Comandos Directos** (`mcp_direct.py`):
```python
def nuevo_comando(self, parametros):
    """Comando directo"""
    # Tu lógica aquí
    return resultado

# Agregar al main() del archivo
```

**Configuración Terminal** (`.bashrc.example`):
```bash
nuevo)
    shift
    echo "🆕 Nuevo comando..."
    $MCP_HOME/.venv/bin/python3 $MCP_HOME/mcp_direct.py nuevo_comando "$@"
    ;;
```

### Integrar Nuevas APIs

```python
def nueva_api_integration(self, query: str) -> str:
    """Integración con nueva API"""
    headers = {'Authorization': f'Bearer {self.api_token}'}
    response = requests.get(f'https://api.example.com/search?q={query}', headers=headers)
    return self._process_response(response.json())
```

## 🧪 Testing

```bash
# Probar servidor interactivo
python ollama_mcp_server.py

# Probar comandos directos
python mcp_direct.py chat "test"
python mcp_direct.py code "test"
python mcp_direct.py github_search "test"

# Verificar dependencias
python -c "import requests, dotenv, github; print('✅ OK')"
```

## 📋 Guidelines

### Código
- Mantener compatibilidad con Python 3.8+
- Documentar funciones con docstrings
- Usar nombres descriptivos para variables
- Manejar errores apropiadamente

### Documentación
- Actualizar README.md si es necesario
- Documentar nuevas funcionalidades
- Incluir ejemplos de uso

### Dependencias
- Minimizar nuevas dependencias
- Usar solo paquetes estables y mantenidos
- Actualizar requirements.txt si es necesario

## 🎯 Roadmap

Funcionalidades en desarrollo:
- [ ] Caché de respuestas frecuentes
- [ ] Integración con más APIs
- [ ] Análisis de proyectos completos
- [ ] Interfaz web opcional
- [ ] Métricas de uso

## 📞 Contacto

- Abre un Issue para preguntas
- Usa Discussions para ideas generales
- Revisa documentación técnica en `DOCUMENTATION.md`

¡Toda contribución es bienvenida! 🎉
