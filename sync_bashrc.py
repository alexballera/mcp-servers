#!/usr/bin/env python3
"""
Script para sincronizar automáticamente .bashrc con .bashrc.example
y hacer push al repositorio cuando hay cambios.
Version simplificada sin dependencias externas.
"""

import os
import time
import subprocess
from pathlib import Path

class BashrcSync:
    def __init__(self):
        self.home_dir = Path.home()
        self.bashrc_path = self.home_dir / '.bashrc'
        self.repo_path = Path(__file__).parent.absolute()
        self.example_path = self.repo_path / '.bashrc.example'
        self.last_modified = 0
        
    def clean_bashrc_content(self, content):
        """
        Limpia el contenido del .bashrc para crear el .example
        Elimina tokens, rutas específicas del usuario, etc.
        """
        lines = content.split('\n')
        cleaned_lines = []
        
        # Header explicativo
        header = [
            "# Archivo de ejemplo para configuración de entorno MCP",
            "# Copia este archivo como .bashrc en tu directorio home y ajusta las variables",
            "# según tu configuración específica.",
            "#",
            "# Variables que debes personalizar:",
            "# - MCP_HOME: Ruta donde clonaste el repositorio",
            "# - GITHUB_TOKEN: Tu token personal de GitHub (si usas integración)",
            "# - Otras rutas específicas de tu sistema",
            "#",
            ""
        ]
        
        cleaned_lines.extend(header)
        
        for line in lines:
            # Eliminar líneas con tokens o claves
            if any(sensitive in line.lower() for sensitive in [
                'token', 'key', 'secret', 'password', 'github_pat', 'ghp_'
            ]):
                # Reemplazar con placeholder
                if '=' in line and not line.strip().startswith('#'):
                    var_name = line.split('=')[0].strip()
                    cleaned_lines.append(f'{var_name}="YOUR_TOKEN_HERE"')
                continue
            
            # Reemplazar rutas específicas del usuario con variables genéricas
            line = line.replace(str(self.home_dir), '$HOME')
            line = line.replace('/home/alexballera', '$HOME')
            
            # Reemplazar ruta específica del proyecto con variable
            if '/tools/mcp-servers' in line:
                line = line.replace('/tools/mcp-servers', '$MCP_HOME')
            elif 'mcp-servers' in line and str(self.home_dir) in line:
                line = line.replace(str(self.repo_path), '$MCP_HOME')
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def get_file_modified_time(self, file_path):
        """Obtiene el tiempo de modificación de un archivo"""
        try:
            return os.path.getmtime(file_path)
        except OSError:
            return 0
    
    def sync_and_push(self):
        """Sincroniza .bashrc con .bashrc.example y hace push"""
        try:
            # Verificar que existe el archivo .bashrc
            if not self.bashrc_path.exists():
                print(f"❌ No existe {self.bashrc_path}")
                return False
            
            # Leer contenido del .bashrc
            with open(self.bashrc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limpiar contenido para el example
            cleaned_content = self.clean_bashrc_content(content)
            
            # Verificar si hay cambios
            try:
                with open(self.example_path, 'r', encoding='utf-8') as f:
                    current_content = f.read()
                if current_content == cleaned_content:
                    return False  # No hay cambios
            except FileNotFoundError:
                pass  # El archivo no existe, se creará
            
            # Escribir al archivo example
            with open(self.example_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Actualizado {self.example_path}")
            
            # Cambiar al directorio del repositorio
            os.chdir(self.repo_path)
            
            # Verificar si hay cambios en git
            result = subprocess.run(['git', 'diff', '--quiet', '.bashrc.example'], 
                                 capture_output=True)
            
            if result.returncode != 0:  # Hay cambios
                # Agregar archivo al stage
                subprocess.run(['git', 'add', '.bashrc.example'], check=True)
                
                # Hacer commit
                commit_msg = "🔄 Auto-sync: Update .bashrc.example from .bashrc changes"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                
                # Push al remoto
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                
                print("🚀 Cambios sincronizados y enviados al repositorio remoto")
                return True
            else:
                print("ℹ️  No hay cambios en git para .bashrc.example")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en git: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sincronizando: {e}")
            return False
    
    def monitor(self, interval=5):
        """Monitorea cambios en .bashrc y sincroniza automáticamente"""
        print(f"🔍 Monitoreando: {self.bashrc_path}")
        print(f"📝 Sincronizando con: {self.example_path}")
        print(f"📁 Repositorio: {self.repo_path}")
        print(f"⏰ Intervalo de verificación: {interval}s")
        print("⏰ Presiona Ctrl+C para detener el monitoreo")
        print()
        
        # Sincronización inicial
        print("🔄 Realizando sincronización inicial...")
        self.sync_and_push()
        print()
        
        # Obtener timestamp inicial
        self.last_modified = self.get_file_modified_time(self.bashrc_path)
        
        try:
            while True:
                current_modified = self.get_file_modified_time(self.bashrc_path)
                
                if current_modified > self.last_modified:
                    print(f"📝 Detectado cambio en {self.bashrc_path}")
                    if self.sync_and_push():
                        print()
                    self.last_modified = current_modified
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo monitoreo...")
            print("✅ Monitoreo detenido")
    
    def sync_once(self):
        """Ejecuta una sincronización única"""
        print("🔄 Ejecutando sincronización única...")
        if self.sync_and_push():
            print("✅ Sincronización completada con cambios")
        else:
            print("ℹ️  Sincronización completada sin cambios")
    
    def show_status(self):
        """Muestra el estado actual de los archivos"""
        print("Estado de sincronización .bashrc:")
        print()
        print(f"📁 Archivo fuente: {self.bashrc_path}")
        if self.bashrc_path.exists():
            size = self.bashrc_path.stat().st_size
            mtime = time.ctime(self.bashrc_path.stat().st_mtime)
            print(f"   ✅ Existe ({size} bytes)")
            print(f"   📅 Modificado: {mtime}")
        else:
            print("   ❌ No existe")
        
        print()
        print(f"📁 Archivo destino: {self.example_path}")
        if self.example_path.exists():
            size = self.example_path.stat().st_size
            mtime = time.ctime(self.example_path.stat().st_mtime)
            print(f"   ✅ Existe ({size} bytes)")
            print(f"   📅 Modificado: {mtime}")
        else:
            print("   ❌ No existe")
        
        print()
        print(f"📁 Repositorio: {self.repo_path}")
        try:
            os.chdir(self.repo_path)
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            branch = result.stdout.strip() if result.returncode == 0 else "unknown"
            print(f"   📝 Branch: {branch}")
            
            result = subprocess.run(['git', 'status', '--porcelain', '.bashrc.example'], 
                                  capture_output=True, text=True)
            changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"   🔄 Estado: {changes} archivo(s) con cambios")
        except Exception as e:
            print(f"   ❌ Error obteniendo estado git: {e}")

def main():
    import sys
    
    sync = BashrcSync()
    
    # Procesamiento de argumentos
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ['-h', '--help']:
            print("Script de sincronización automática .bashrc -> .bashrc.example")
            print()
            print(f"Uso: {sys.argv[0]} [OPCION]")
            print()
            print("Opciones:")
            print("  -h, --help     Mostrar esta ayuda")
            print("  -m, --monitor  Monitoreo continuo (por defecto)")
            print("  -o, --once     Sincronizar una sola vez y salir")
            print("  -s, --status   Mostrar estado actual")
            print()
            print("El script monitorea cambios en ~/.bashrc y automáticamente:")
            print("  1. Actualiza .bashrc.example eliminando tokens y rutas específicas")
            print("  2. Hace commit de los cambios")
            print("  3. Hace push al repositorio remoto")
            return
        elif arg in ['-o', '--once']:
            sync.sync_once()
            return
        elif arg in ['-s', '--status']:
            sync.show_status()
            return
        elif arg in ['-m', '--monitor']:
            pass  # Continuar con monitoreo
        else:
            print(f"❌ Opción desconocida: {arg}")
            print("Usa -h para ver la ayuda")
            sys.exit(1)
    
    # Monitoreo por defecto
    sync.monitor()

if __name__ == "__main__":
    main()
