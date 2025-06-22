# Scripts de Sincronización .bashrc

Estos scripts permiten sincronizar automáticamente tu archivo `~/.bashrc` con el archivo `.bashrc.example` del repositorio, eliminando información sensible y manteniendo el repositorio actualizado.

## Características

✅ **Monitoreo automático** de cambios en `~/.bashrc`  
✅ **Limpieza automática** de tokens y información sensible  
✅ **Commit automático** de cambios al repositorio  
✅ **Push automático** al repositorio remoto  
✅ **Reemplazo de rutas** específicas por variables genéricas  

## Scripts Disponibles

### 1. `sync_bashrc.sh` (Recomendado)
Script en Bash sin dependencias externas.

```bash
# Monitoreo continuo (por defecto)
./sync_bashrc.sh

# Sincronización única
./sync_bashrc.sh --once

# Ver estado actual
./sync_bashrc.sh --status

# Ver ayuda
./sync_bashrc.sh --help
```

### 2. `sync_bashrc.py`
Script en Python con las mismas funcionalidades.

```bash
# Monitoreo continuo (por defecto)
./sync_bashrc.py

# Sincronización única
./sync_bashrc.py --once

# Ver estado actual
./sync_bashrc.py --status

# Ver ayuda
./sync_bashrc.py --help
```

## Funcionamiento

### 1. Detección de Cambios
- Monitorea `~/.bashrc` cada 5 segundos (configurable)
- Detecta cuando el archivo ha sido modificado

### 2. Limpieza Automática
El script limpia automáticamente:
- **Tokens y claves**: `GITHUB_TOKEN`, `API_KEY`, etc.
- **Rutas específicas**: `/home/usuario` → `$HOME`
- **Rutas del proyecto**: `/path/to/mcp-servers` → `$MCP_HOME`

### 3. Sincronización
- Actualiza `.bashrc.example` con el contenido limpio
- Hace commit si hay cambios
- Hace push al repositorio remoto

## Configuración Inicial

1. **Hacer ejecutables los scripts:**
   ```bash
   chmod +x sync_bashrc.sh sync_bashrc.py
   ```

2. **Ejecutar sincronización inicial:**
   ```bash
   ./sync_bashrc.sh --once
   ```

3. **Iniciar monitoreo continuo:**
   ```bash
   ./sync_bashrc.sh
   ```

## Ejemplo de Transformación

**Archivo original (`~/.bashrc`):**
```bash
# MCP Configuration
export MCP_HOME="/home/alexballera/tools/mcp-servers"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"

# Aliases
alias ll='ls -la'
```

**Archivo generado (`.bashrc.example`):**
```bash
# Archivo de ejemplo para configuración de entorno MCP
# Copia este archivo como .bashrc en tu directorio home y ajusta las variables
# según tu configuración específica.
#
# Variables que debes personalizar:
# - MCP_HOME: Ruta donde clonaste el repositorio
# - GITHUB_TOKEN: Tu token personal de GitHub (si usas integración)
# - Otras rutas específicas de tu sistema
#

# MCP Configuration
export MCP_HOME="$MCP_HOME"
GITHUB_TOKEN="YOUR_TOKEN_HERE"
OPENAI_API_KEY="YOUR_TOKEN_HERE"

# Aliases
alias ll='ls -la'
```

## Configuración Avanzada

### Cambiar Intervalo de Monitoreo (Bash)
Edita la variable `SYNC_INTERVAL` en `sync_bashrc.sh`:
```bash
SYNC_INTERVAL=10  # Segundos entre verificaciones
```

### Cambiar Intervalo de Monitoreo (Python)
Usa el parámetro en el método monitor:
```python
sync.monitor(interval=10)  # 10 segundos
```

## Seguridad

- ✅ **Nunca** se suben tokens al repositorio
- ✅ Las rutas específicas se reemplazan por variables
- ✅ Los archivos de configuración sensibles están en `.gitignore`
- ✅ Solo se sincronizan los cambios relevantes

## Troubleshooting

### Script no detecta cambios
```bash
# Verificar permisos del archivo
ls -la ~/.bashrc

# Verificar estado del repositorio
./sync_bashrc.sh --status
```

### Error de permisos de Git
```bash
# Verificar configuración de Git
git config --list

# Verificar autenticación
git remote -v
```

### Error de push
```bash
# Verificar conexión al remoto
git fetch origin

# Verificar branch actual
git status
```

## Comandos Útiles

```bash
# Ver logs de cambios
git log --oneline --grep="Auto-sync"

# Detener monitoreo
# Presionar Ctrl+C en la terminal donde corre el script

# Reiniciar monitoreo
./sync_bashrc.sh

# Forzar sincronización
./sync_bashrc.sh --once
```

## Integración con Servicios del Sistema

### Systemd (Linux)
Crear servicio para ejecutar automáticamente:

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/user/bashrc-sync.service
```

```ini
[Unit]
Description=Bashrc Auto Sync Service
After=network.target

[Service]
Type=simple
ExecStart=/home/alexballera/tools/mcp-servers/sync_bashrc.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
# Habilitar y iniciar servicio
systemctl --user enable bashrc-sync
systemctl --user start bashrc-sync
```

---

**Nota:** Los scripts están diseñados para ser seguros y no interferir con tu flujo de trabajo normal. Siempre puedes detener el monitoreo con `Ctrl+C`.
