#!/bin/bash
# Script para sincronizar automáticamente .bashrc con .bashrc.example
# y hacer push al repositorio cuando hay cambios.

set -e

# Configuración
BASHRC_FILE="$HOME/.bashrc"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLE_FILE="$REPO_DIR/.bashrc.example"
SYNC_INTERVAL=5  # Segundos entre verificaciones

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

error() {
    echo -e "${RED}❌${NC} $1"
}

# Función para limpiar contenido del bashrc
clean_bashrc_content() {
    local input_file="$1"
    local temp_file=$(mktemp)
    
    # Header explicativo
    cat > "$temp_file" << 'EOF'
# Archivo de ejemplo para configuración de entorno MCP
# Copia este archivo como .bashrc en tu directorio home y ajusta las variables
# según tu configuración específica.
#
# Variables que debes personalizar:
# - MCP_HOME: Ruta donde clonaste el repositorio
# - GITHUB_TOKEN: Tu token personal de GitHub (si usas integración)
# - Otras rutas específicas de tu sistema
#

EOF
    
    # Procesar línea por línea
    while IFS= read -r line; do
        # Eliminar líneas con tokens o claves sensibles
        if echo "$line" | grep -iE "(token|key|secret|password|github_pat|ghp_)" > /dev/null; then
            if echo "$line" | grep "=" > /dev/null && ! echo "$line" | grep "^#" > /dev/null; then
                var_name=$(echo "$line" | cut -d'=' -f1 | xargs)
                echo "${var_name}=\"YOUR_TOKEN_HERE\"" >> "$temp_file"
            fi
            continue
        fi
        
        # Reemplazar rutas específicas del usuario
        line=$(echo "$line" | sed "s|$HOME|\$HOME|g")
        line=$(echo "$line" | sed "s|/home/alexballera|\$HOME|g")
        line=$(echo "$line" | sed "s|/tools/mcp-servers|\$MCP_HOME|g")
        line=$(echo "$line" | sed "s|$REPO_DIR|\$MCP_HOME|g")
        
        echo "$line" >> "$temp_file"
    done < "$input_file"
    
    echo "$temp_file"
}

# Función para sincronizar y hacer push
sync_and_push() {
    log "Verificando cambios en $BASHRC_FILE..."
    
    # Verificar que existe el .bashrc
    if [[ ! -f "$BASHRC_FILE" ]]; then
        warning "No existe $BASHRC_FILE"
        return 1
    fi
    
    # Limpiar contenido
    local cleaned_file=$(clean_bashrc_content "$BASHRC_FILE")
    
    # Verificar si hay cambios
    if [[ -f "$EXAMPLE_FILE" ]] && cmp -s "$cleaned_file" "$EXAMPLE_FILE"; then
        rm "$cleaned_file"
        return 0  # No hay cambios
    fi
    
    # Copiar archivo limpio
    cp "$cleaned_file" "$EXAMPLE_FILE"
    rm "$cleaned_file"
    
    success "Actualizado $EXAMPLE_FILE"
    
    # Cambiar al directorio del repositorio
    cd "$REPO_DIR"
    
    # Verificar si hay cambios en git
    if git diff --quiet .bashrc.example; then
        log "No hay cambios en git para .bashrc.example"
        return 0
    fi
    
    # Hacer commit y push
    log "Haciendo commit de los cambios..."
    git add .bashrc.example
    git commit -m "🔄 Auto-sync: Update .bashrc.example from .bashrc changes"
    
    log "Enviando cambios al repositorio remoto..."
    git push origin main
    
    success "Cambios sincronizados y enviados al repositorio remoto"
}

# Función para monitoreo continuo
monitor_mode() {
    log "🔍 Iniciando monitoreo de $BASHRC_FILE"
    log "📝 Sincronizando con $EXAMPLE_FILE"
    log "📁 Repositorio: $REPO_DIR"
    log "⏰ Intervalo de verificación: ${SYNC_INTERVAL}s"
    echo
    log "Presiona Ctrl+C para detener el monitoreo"
    echo
    
    # Sincronización inicial
    log "Realizando sincronización inicial..."
    sync_and_push
    echo
    
    # Obtener timestamp inicial del archivo
    local last_modified=""
    if [[ -f "$BASHRC_FILE" ]]; then
        last_modified=$(stat -c %Y "$BASHRC_FILE" 2>/dev/null || stat -f %m "$BASHRC_FILE" 2>/dev/null)
    fi
    
    # Loop de monitoreo
    while true; do
        if [[ -f "$BASHRC_FILE" ]]; then
            current_modified=$(stat -c %Y "$BASHRC_FILE" 2>/dev/null || stat -f %m "$BASHRC_FILE" 2>/dev/null)
            
            if [[ "$current_modified" != "$last_modified" ]]; then
                log "📝 Detectado cambio en $BASHRC_FILE"
                sync_and_push
                last_modified="$current_modified"
                echo
            fi
        fi
        
        sleep $SYNC_INTERVAL
    done
}

# Función de ayuda
show_help() {
    echo "Script de sincronización automática .bashrc -> .bashrc.example"
    echo
    echo "Uso: $0 [OPCION]"
    echo
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -m, --monitor  Monitoreo continuo (por defecto)"
    echo "  -o, --once     Sincronizar una sola vez y salir"
    echo "  -s, --status   Mostrar estado actual"
    echo
    echo "El script monitore cambios en ~/.bashrc y automáticamente:"
    echo "  1. Actualiza .bashrc.example eliminando tokens y rutas específicas"
    echo "  2. Hace commit de los cambios"
    echo "  3. Hace push al repositorio remoto"
}

# Función para mostrar estado
show_status() {
    echo "Estado de sincronización .bashrc:"
    echo
    echo "📁 Archivo fuente: $BASHRC_FILE"
    if [[ -f "$BASHRC_FILE" ]]; then
        echo "   ✅ Existe ($(stat -c %s "$BASHRC_FILE" 2>/dev/null || stat -f %z "$BASHRC_FILE" 2>/dev/null) bytes)"
        echo "   📅 Modificado: $(stat -c %y "$BASHRC_FILE" 2>/dev/null || stat -f %Sm "$BASHRC_FILE" 2>/dev/null)"
    else
        echo "   ❌ No existe"
    fi
    echo
    echo "📁 Archivo destino: $EXAMPLE_FILE"
    if [[ -f "$EXAMPLE_FILE" ]]; then
        echo "   ✅ Existe ($(stat -c %s "$EXAMPLE_FILE" 2>/dev/null || stat -f %z "$EXAMPLE_FILE" 2>/dev/null) bytes)"
        echo "   📅 Modificado: $(stat -c %y "$EXAMPLE_FILE" 2>/dev/null || stat -f %Sm "$EXAMPLE_FILE" 2>/dev/null)"
    else
        echo "   ❌ No existe"
    fi
    echo
    echo "📁 Repositorio: $REPO_DIR"
    cd "$REPO_DIR"
    echo "   📝 Branch: $(git branch --show-current)"
    echo "   🔄 Estado: $(git status --porcelain .bashrc.example | wc -l | xargs) archivo(s) con cambios"
}

# Manejo de señales para salida limpia
cleanup() {
    echo
    log "🛑 Deteniendo monitoreo..."
    success "Monitoreo detenido"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Procesamiento de argumentos
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -o|--once)
        log "Ejecutando sincronización única..."
        sync_and_push
        success "Sincronización completada"
        exit 0
        ;;
    -s|--status)
        show_status
        exit 0
        ;;
    -m|--monitor|"")
        monitor_mode
        ;;
    *)
        error "Opción desconocida: $1"
        echo "Usa -h para ver la ayuda"
        exit 1
        ;;
esac
