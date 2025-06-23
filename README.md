# MCP Servers - Agentes AI Ultra-Rápidos

Entorno MCP (Model Context Protocol) optimizado para **velocidad**, **simplicidad** y **productividad** en VS Code y terminal.

## 📦 Configuración Respaldada

Para una implementación rápida de tu entorno optimizado:

```bash
# .bashrc optimizado con prompt Git y configuración MCP
https://gist.github.com/alexballera
```

## 🎯 ¿Qué es esto?

Un kit completo de agentes AI que funciona en **<2 segundos**:
- **Terminal**: Comandos `mcpai`, `mcpask`, `mcpcode`, `mcpgroq` 
- **VS Code**: Integración directa con Copilot
- **MCP**: Servidores para Git, GitHub y filesystems

## ⚡ Instalación (2 minutos)

```bash
# 1. Clonar
git clone [repo-url] ~/mcp-servers && cd ~/mcp-servers

# 2. Setup automático
chmod +x setup_portable.sh
./setup_portable.sh

# 3. Configurar API keys
nano .env  # Agregar GROQ_API_KEY
```

## 🚀 Uso Inmediato

### Terminal
```bash
mcpask "¿Cómo optimizar esta query SQL?"
mcpcode "tengo un error en mi función Python"  
mcpgroq "explícame los microservicios"
mcpai chat "analiza mi código y sugiere mejoras"
```

### VS Code
Los servidores MCP se integran automáticamente con Copilot. Configuración en `settings.json`:

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

> 💡 **Nota**: Usamos `${env:HOME}` para portabilidad entre dispositivos
## 📁 Estructura (Optimizada)

```
mcp-servers/
├── groq_mcp_fast.py     # 🤖 Servidor MCP con Groq
├── git_mcp_server.py    # 🔧 Operaciones Git
├── github_mcp_server.py # 🐙 API GitHub
├── mcpai                # 💬 Agente terminal completo
├── mcpask               # ❓ Preguntas rápidas
├── mcpcode              # 💻 Asistente de código
├── mcpgroq              # ⚡ Chat ultra-rápido
├── requirements.txt     # 📦 Dependencias
├── setup_portable.sh    # 🚀 Setup automático
├── .env.example         # ⚙️ Template config
├── PORTABILITY.md       # 🌍 Guía multi-dispositivo
└── README.md            # 📖 Esta documentación
```

## 🔑 Configuración

### Variables Requeridas (.env)
```bash
GROQ_API_KEY=gsk_...           # Requerido - groq.com
GITHUB_TOKEN=ghp_...           # Opcional - para GitHub MCP
```

### Obtener API Keys
- **Groq**: [console.groq.com](https://console.groq.com) (gratis, ultra-rápido)
- **GitHub**: [github.com/settings/tokens](https://github.com/settings/tokens) (opcional)

## 🎯 Performance

| Componente | Velocidad | Estado |
|------------|-----------|--------|
| mcpask | 0.4-0.8s | ✅ Funcional |
| mcpcode | 1.0-1.5s | ✅ Funcional |
| mcpai | 0.8-1.2s | ✅ Funcional |
| mcpgroq | 0.5-1.0s | ✅ Funcional |
| Git MCP | Instantáneo | ✅ Funcional |
| GitHub MCP | 1-3s | ✅ Funcional |
| VS Code Integration | Instantáneo | ✅ Funcional |

## 🛠️ Troubleshooting

```bash
# Verificar configuración
echo $GROQ_API_KEY

# Test rápido
./mcpask "hola mundo"

# Debug servidor MCP
python3 groq_mcp_fast.py
```

## 📈 Próximos Pasos

Una vez funcionando:
1. Agregar `export PATH="$PATH:$HOME/mcp-servers"` a tu `.bashrc`
2. Configurar VS Code settings para MCP
3. ¡Empezar a usar los comandos AI!

## 🔄 Portabilidad entre Dispositivos

### Para usar en múltiples dispositivos:

1. **Clonar en ubicación estándar:**
   ```bash
   git clone [repo] ~/mcp-servers
   cd ~/mcp-servers
   ./setup_portable.sh
   ```

2. **VS Code detecta automáticamente** con `${env:HOME}`

3. **Comandos funcionan inmediatamente** después del setup

### Beneficios del enfoque actual:
- ✅ **Setup automático** con un solo script
- ✅ **Rutas portátiles** usando variables de entorno
- ✅ **Sin conflictos** con otros comandos
- ✅ **Entorno virtual aislado**

---
**🚀 Ready to use en <2 minutos** | **⚡ Respuestas en <2 segundos** | **🔧 Sin Node.js, solo Python**