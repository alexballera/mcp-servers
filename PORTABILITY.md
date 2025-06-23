# 🌍 Guía de Portabilidad - MCP Servers

Cómo usar este proyecto en **cualquier dispositivo** sin problemas de rutas.

## � Respaldo de Configuración

Para implementar rápidamente tu entorno optimizado en cualquier dispositivo, utiliza el backup de tu configuración:

```bash
# .bashrc optimizado con prompt Git y configuración MCP
https://gist.github.com/alexballera
```

## �🚀 Setup Rápido en Nuevo Dispositivo

### 1. Clonar el proyecto
```bash
git clone [tu-repo-url] ~/mcp-servers
cd ~/mcp-servers
```

### 2. Ejecutar setup automático
```bash
chmod +x setup_portable.sh
./setup_portable.sh
```

### 3. Configurar API keys
```bash
# Editar .env con tus keys
nano .env
```

## 🔧 Configuración Manual de VS Code

Si prefieres configurar VS Code manualmente, usa **variables de entorno** en lugar de rutas absolutas:

### ✅ Correcto (Portátil):
```json
{
  "mcp.mcpServers": {
    "groq-agent": {
      "command": "${env:HOME}/mcp-servers/.venv/bin/python",
      "args": ["${env:HOME}/mcp-servers/groq_mcp_fast.py"]
    }
  }
}
```

### ❌ Incorrecto (No portátil):
```json
{
  "mcp.mcpServers": {
    "groq-agent": {
      "command": "/home/alexballera/mcp-servers/.venv/bin/python",
      "args": ["/home/alexballera/mcp-servers/groq_mcp_fast.py"]
    }
  }
}
```

## 📁 Ubicaciones Recomendadas

### Opción 1: En el home (Recomendado)

```bash
~/mcp-servers/
```

Configuración VS Code:

```json
"command": "${env:HOME}/mcp-servers/.venv/bin/python"
```

### Opción 2: Ubicación personalizada

```bash
# En cualquier lugar, pero definir variable
export MCP_PATH="/mi/ubicacion/custom/mcp-servers"
```

Configuración VS Code:

```json
"command": "${env:MCP_PATH}/.venv/bin/python"
```

## 🔑 Variables de Entorno Importantes

### Para uso general:
```bash
# En .bashrc o .zshrc
export PATH="$PATH:$HOME/mcp-servers"
export MCP_PATH="$HOME/mcp-servers"
```

### Para VS Code:
```bash
# En .env del proyecto
GROQ_API_KEY=gsk_...
GITHUB_TOKEN=ghp_...
```

## 📋 Checklist para Nuevo Dispositivo

- [ ] Clonar repositorio en ubicación consistente
- [ ] Ejecutar `./setup_portable.sh`
- [ ] Configurar `.env` con API keys
- [ ] Actualizar VS Code settings.json con `${env:HOME}`
- [ ] Probar comandos: `./mcpask "test"`
- [ ] Reiniciar VS Code para detectar MCP servers

## 🐛 Troubleshooting

### Problema: "No module named 'requests'"
**Solución:**
```bash
cd ~/mcp-servers
source .venv/bin/activate
pip install -r requirements.txt
```

### Problema: "Permission denied"

**Solución:**
```bash
chmod +x ~/mcp-servers/{mcpai,mcpask,mcpcode,mcpgroq}
```

### Problema: VS Code no detecta servidores MCP
**Solución:**
1. Verificar rutas en settings.json usan `${env:HOME}`
2. Reiniciar VS Code completamente
3. Verificar que `.venv/bin/python` existe

## 🎯 Beneficios de este Enfoque

✅ **Portátil**: Funciona en cualquier usuario/dispositivo  
✅ **Automático**: Setup en 2 comandos  
✅ **Consistente**: Misma configuración everywhere  
✅ **Mantenible**: Un solo lugar para cambios  
✅ **Escalable**: Fácil agregar nuevos servidores  

---
**🚀 Ready to use en cualquier dispositivo en <5 minutos**
