# 📋 Comandos MCP - Guía de Uso

Todos los comandos del proyecto MCP Servers optimizados y listos para usar.

## � Configuración y Respaldo

Para implementar rápidamente este entorno en un nuevo dispositivo:

```bash
# Respaldo de .bashrc optimizado con prompt Git y configuración MCP
https://gist.github.com/alexballera
```

## �🚀 Comandos de Terminal

### `mcpask` - Preguntas Rápidas
**Uso más simple para consultas directas**
```bash
./mcpask "¿Cómo funciona Docker?"
./mcpask "¿Qué es GraphQL?"
./mcpask "Diferencia entre REST y gRPC"
```
- ⚡ **Velocidad**: 0.4-0.8 segundos
- 🎯 **Propósito**: Respuestas concisas
- 📝 **Límite**: 500 tokens

### `mcpcode` - Asistente de Código
**Especializado en problemas de programación**
```bash
./mcpcode "¿cómo hacer un loop en Python?"
./mcpcode --fix "ModuleNotFoundError: No module named 'requests'"
./mcpcode "optimizar esta función SQL"
```
- ⚡ **Velocidad**: 1.0-1.5 segundos
- 🎯 **Propósito**: Código funcional + explicaciones
- 📝 **Límite**: 800 tokens
- 🔧 **Flag `--fix`**: Modo solución de errores

### `mcpai` - Agente Completo
**Conversaciones extensas y análisis profundo**
```bash
./mcpai chat "analiza mi arquitectura de microservicios"
./mcpai analyze "revisa este código y sugiere mejoras"
./mcpai explain "¿cómo implementar autenticación JWT?"
```
- ⚡ **Velocidad**: 0.8-1.2 segundos
- 🎯 **Propósito**: Conversaciones complejas
- 📝 **Límite**: 1000 tokens
- 🤖 **Modos**: chat, analyze, explain

### `mcpgroq` - Chat Directo
**Interfaz directa con Groq**
```bash
./mcpgroq "explícame los patrones de diseño"
./mcpgroq "¿cuál es la diferencia entre Docker y Kubernetes?"
```
- ⚡ **Velocidad**: 0.5-1.0 segundos
- 🎯 **Propósito**: Chat sin restricciones
- 📝 **Límite**: 1000 tokens

## 🎯 ¿Cuál comando usar?

| Situación | Comando Recomendado | Por qué |
|-----------|-------------------|---------|
| Pregunta rápida | `mcpask` | Más rápido, respuesta concisa |
| Error de código | `mcpcode --fix` | Especializado en debugging |
| Explicar código | `mcpcode` | Mejor para ejemplos de código |
| Conversación larga | `mcpai chat` | Más contexto y detalle |
| Chat libre | `mcpgroq` | Sin restricciones específicas |

## 🔧 Servidores MCP (VS Code)

### `groq-agent`
- **Función**: Chat ultra-rápido integrado en Copilot
- **Velocidad**: Instantáneo
- **Uso**: Automático en VS Code

### `git-python`
- **Función**: Operaciones Git avanzadas
- **Capacidades**: status, diff, commit, branch, etc.
- **Uso**: Automático en VS Code

### `github-python`
- **Función**: API GitHub completa
- **Capacidades**: issues, repos, búsqueda de código
- **Requisito**: GITHUB_TOKEN en configuración

## 🛠️ Troubleshooting

### Error: "No module named 'requests'"
```bash
cd ~/mcp-servers
source .venv/bin/activate
pip install -r requirements.txt
```

### Error: "Permission denied"
```bash
chmod +x ~/mcp-servers/{mcpai,mcpask,mcpcode,mcpgroq}
```

### Error: "GROQ_API_KEY not found"
```bash
nano ~/mcp-servers/.env
# Agregar: GROQ_API_KEY=gsk_tu_key_aqui
```

### Comando no responde
```bash
# Verificar el shebang
head -1 ~/mcp-servers/mcpask
# Debe ser: #!${HOME}/mcp-servers/.venv/bin/python3
```

## 📊 Performance Comparison

```bash
# Test de velocidad (con comandos en el PATH)
time mcpask "test"      # ~0.5s
time mcpcode "test"     # ~1.2s  
time mcpai chat "test"  # ~0.9s
time mcpgroq "test"     # ~0.7s
```

## 🎨 Ejemplos Prácticos

### Desarrollo Web
```bash
# Si estás en el directorio del proyecto
./mcpcode "crear API REST con FastAPI"

# Si los comandos están en el PATH (recomendado)
mcpcode "crear API REST con FastAPI"
mcpask "diferencia entre session y cookies"
mcpai chat "diseñar base de datos para e-commerce"
```

### DevOps
```bash
mcpcode "dockerfile para aplicación Python"
mcpask "¿qué es Kubernetes?"
mcpai analyze "mi pipeline de CI/CD"
```

### Data Science
```bash
mcpcode "análisis de datos con pandas"
mcpask "¿qué es machine learning?"
mcpai chat "diseñar modelo de recomendación"
```

---
**💡 Tip**: Usa `mcpask` para preguntas rápidas y `mcpai` para análisis profundos
