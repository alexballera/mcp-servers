#!/usr/bin/env python3
"""
Script de instalación y configuración automática
Ollama MCP Server - Sistema completo de IA para desarrollo
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header():
    print("🚀" + "="*60 + "🚀")
    print("   OLLAMA MCP SERVER - INSTALACIÓN AUTOMÁTICA")
    print("   Sistema integrado de IA para desarrollo")
    print("🚀" + "="*60 + "🚀\n")

def check_ollama():
    """Verificar si Ollama está instalado y funcionando"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama está instalado y funcionando")
            return True
        else:
            print("❌ Ollama no está funcionando correctamente")
            return False
    except FileNotFoundError:
        print("❌ Ollama no está instalado")
        print("   Instala desde: https://ollama.ai/")
        return False

def setup_venv():
    """Configurar entorno virtual"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("📦 Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        print("✅ Entorno virtual creado")
    else:
        print("✅ Entorno virtual ya existe")
    
    return venv_path

def install_dependencies(venv_path):
    """Instalar dependencias"""
    pip_path = venv_path / "bin" / "pip"
    
    if not pip_path.exists():
        pip_path = venv_path / "Scripts" / "pip.exe"  # Windows
    
    if pip_path.exists():
        print("📚 Instalando dependencias...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas")
    else:
        print("❌ No se encontró pip en el entorno virtual")

def setup_env_file():
    """Configurar archivo .env"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚙️ Configurando archivo .env...")
        env_content = """# Ollama MCP Server Configuration

# GitHub Personal Access Token
# Get from: https://github.com/settings/tokens
# Required scopes: repo, public_repo, read:org
GITHUB_TOKEN=your_github_token_here

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
DEFAULT_MODEL=llama3.1:8b
CODING_MODEL=deepseek-coder:6.7b

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=8000
"""
        env_path.write_text(env_content)
        print("✅ Archivo .env creado")
        print("📝 IMPORTANTE: Edita .env con tu GitHub token")
    else:
        print("✅ Archivo .env ya existe")

def install_models():
    """Instalar modelos recomendados de Ollama"""
    models = [
        ("llama3.1:8b", "Chat general"),
        ("deepseek-coder:6.7b", "Asistencia de código"),
        ("qwen2.5-coder:7b", "Código alternativo")
    ]
    
    print("🤖 Verificando modelos de Ollama...")
    
    for model, description in models:
        print(f"📥 Instalando {model} ({description})...")
        result = subprocess.run(['ollama', 'pull', model], capture_output=True)
        if result.returncode == 0:
            print(f"✅ {model} instalado")
        else:
            print(f"⚠️ Error instalando {model} (opcional)")

def create_aliases():
    """Crear aliases para ~/.bashrc"""
    mcp_path = os.path.abspath(".")
    python_path = os.path.join(mcp_path, ".venv/bin/python")
    server_path = os.path.join(mcp_path, "ollama_mcp_server.py")
    
    aliases = f"""
# ======================================
# OLLAMA MCP SERVER - ALIASES OPTIMIZADOS
# ======================================

# Función principal MCP
mcp() {{
    case "$1" in
        start|server)
            cd {mcp_path} && {python_path} {server_path}
            ;;
        install|setup)
            cd {mcp_path} && {python_path} install.py
            ;;
        models)
            ollama list
            ;;
        pull)
            if [ -z "$2" ]; then
                echo "Uso: mcp pull <modelo>"
                echo "Ejemplos: mcp pull deepseek-coder:6.7b"
            else
                ollama pull "$2"
            fi
            ;;
        help|*)
            echo "🤖 Ollama MCP Server"
            echo "Comandos disponibles:"
            echo "  mcp start    - Iniciar servidor MCP"
            echo "  mcp models   - Ver modelos instalados"
            echo "  mcp pull     - Instalar modelo"
            echo "  mcp install  - Reinstalar sistema"
            echo "  mcp help     - Mostrar ayuda"
            ;;
    esac
}}

# Aliases de compatibilidad
alias mcp-server='mcp start'
alias mcp-models='mcp models'
"""
    
    return aliases

def update_bashrc():
    """Actualizar ~/.bashrc con aliases"""
    bashrc_path = Path.home() / ".bashrc"
    
    if bashrc_path.exists():
        content = bashrc_path.read_text()
        if "OLLAMA MCP SERVER" not in content:
            aliases = create_aliases()
            with open(bashrc_path, "a") as f:
                f.write(aliases)
            print("✅ Aliases agregados a ~/.bashrc")
            print("🔄 Ejecuta: source ~/.bashrc")
        else:
            print("✅ Aliases ya configurados en ~/.bashrc")
    else:
        print("⚠️ ~/.bashrc no encontrado")

def main():
    """Función principal de instalación"""
    print_header()
    
    # Verificar que estamos en el directorio correcto
    if not Path("ollama_mcp_server.py").exists():
        print("❌ Error: Ejecuta este script desde el directorio del MCP Server")
        sys.exit(1)
    
    # Paso 1: Verificar Ollama
    if not check_ollama():
        print("❌ Instala Ollama primero: https://ollama.ai/")
        sys.exit(1)
    
    # Paso 2: Configurar entorno virtual
    venv_path = setup_venv()
    
    # Paso 3: Instalar dependencias
    install_dependencies(venv_path)
    
    # Paso 4: Configurar .env
    setup_env_file()
    
    # Paso 5: Instalar modelos (opcional)
    install_choice = input("¿Instalar modelos recomendados? (y/N): ").strip().lower()
    if install_choice in ['y', 'yes', 'sí', 's']:
        install_models()
    
    # Paso 6: Configurar aliases
    update_bashrc()
    
    # Resumen final
    print("\n🎉" + "="*60 + "🎉")
    print("   ¡INSTALACIÓN COMPLETADA!")
    print("🎉" + "="*60 + "🎉")
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. source ~/.bashrc")
    print("2. Edita .env con tu GitHub token")
    print("3. mcp start")
    print("\n🚀 ¡Disfruta tu sistema de IA local!")

if __name__ == "__main__":
    main()
