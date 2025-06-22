# MCP Servers - Agentes AI Ultra-Rápidos

Entorno MCP (Model Context Protocol) optimizado para **velocidad**, **simplicidad** y **productividad** en VS Code y terminal.

## 🎯 ¿Qué es esto?

Un kit completo de agentes AI que funciona en **<2 segundos**:
- **Terminal**: Comandos `ai`, `ask`, `codehelp`, `groq` 
- **VS Code**: Integración directa con Copilot
- **MCP**: Servidores para Git, GitHub y filesystems

## ⚡ Instalación (2 minutos)

```bash
# 1. Clonar
git clone [repo-url] && cd mcp-servers

# 2. Configurar
cp .env.example .env
# Editar .env con tu GROQ_API_KEY

# 3. Instalar
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4. Activar comandos
export PATH="$PATH:$(pwd)"
chmod +x ai ask codehelp groq
```

## 🚀 Uso Inmediato

### Terminal
```bash
ask "¿Cómo optimizar esta query SQL?"
codehelp "tengo un error en mi función Python"
groq "explícame los microservicios"
ai "analiza mi código y sugiere mejoras"
```

### VS Code
Los servidores MCP se integran automáticamente con Copilot. Configuración en `~/.config/Code/User/settings.json`:

```json
{
  "mcp.mcpServers": {
    "groq-agent": {
      "command": "python",
      "args": ["${env:HOME}/tools/mcp-servers/groq_mcp_fast.py"]
    },
    "git": {
      "command": "python", 
      "args": ["${env:HOME}/tools/mcp-servers/git_mcp_server.py"]
    },
    "github": {
      "command": "python",
      "args": ["${env:HOME}/tools/mcp-servers/github_mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "tu_github_token_aqui"
      }
    }
  }
}
```

> 💡 **Nota**: Usamos `${env:HOME}` para portabilidad entre dispositivos

## 📁 Estructura (Minimalista)

```
mcp-servers/
├── groq_mcp_fast.py     # 🤖 Servidor MCP con Groq
├── git_mcp_server.py    # 🔧 Operaciones Git
├── github_mcp_server.py # 🐙 API GitHub
├── ai                   # 💬 Agente terminal completo
├── ask                  # ❓ Preguntas rápidas
├── codehelp             # 💻 Asistente de código
├── groq                 # ⚡ Chat ultra-rápido
├── requirements.txt     # 📦 Dependencias
├── .env.example        # ⚙️ Template config
└── README.md           # 📖 Esta documentación
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
| Groq Terminal | 0.5-2s | ✅ Funcional |
| Git MCP | Instantáneo | ✅ Funcional |
| GitHub MCP | 1-3s | ✅ Funcional |
| VS Code Integration | Instantáneo | ✅ Funcional |

## 🛠️ Troubleshooting

```bash
# Verificar configuración
echo $GROQ_API_KEY

# Test rápido
./ask "hola mundo"

# Debug servidor MCP
python groq_mcp_fast.py
```

## 📈 Próximos Pasos

Una vez funcionando:
1. Agregar `export PATH="$PATH:/ruta/a/mcp-servers"` a tu `.bashrc`
2. Configurar VS Code settings para MCP
3. ¡Empezar a usar los comandos AI!

## 🔄 Portabilidad entre Dispositivos

### Para usar en múltiples dispositivos:

1. **Mantener estructura consistente:**
   ```bash
   ~/tools/mcp-servers/  # Ubicación recomendada
   ```

2. **VS Code usa variables de entorno:**
   ```json
   "args": ["${env:HOME}/tools/mcp-servers/groq_mcp_fast.py"]
   ```

3. **Sincronizar configuración:**
   - Clonar repo en `~/tools/mcp-servers`
   - Configurar `.env` con tus API keys
   - VS Code detectará automáticamente los servidores

### Alternativas de ubicación:
- `~/tools/mcp-servers/` ✅ Recomendado
- `~/.local/bin/mcp-servers/` ✅ Alternativo
- `/opt/mcp-servers/` ⚠️ Requiere permisos admin

---
**🚀 Ready to use en <2 minutos** | **⚡ Respuestas en <2 segundos** | **🔧 Sin Node.js, solo Python**