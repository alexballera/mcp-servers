#!/usr/bin/env python3
"""
Test simple del servidor MCP sin dependencias externas
"""

import os
import sys

print("🤖 Ollama MCP Server - Test Mode")
print("=" * 50)

# Test 1: Verificar conexión Ollama
try:
    import subprocess
    result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✅ Ollama: Conectado")
    else:
        print("❌ Ollama: No disponible")
        print("🔧 Solución: ollama serve")
except Exception as e:
    print(f"❌ Error verificando Ollama: {e}")

# Test 2: Verificar modelos
try:
    result = subprocess.run(['ollama', 'list'], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        models = [line.split()[0] for line in lines if line.strip()]
        print(f"✅ Modelos disponibles: {len(models)}")
        for model in models[:3]:  # Show first 3
            print(f"   📦 {model}")
        if len(models) > 3:
            print(f"   ... y {len(models) - 3} más")
    else:
        print("❌ No se pudieron listar modelos")
except Exception as e:
    print(f"❌ Error listando modelos: {e}")

# Test 3: Verificar token GitHub
github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    print("✅ GitHub Token: Configurado")
else:
    print("⚠️  GitHub Token: No configurado")
    print("🔧 Solución: Configurar GITHUB_TOKEN en .env")

print("\n🎯 Comandos de diagnóstico:")
print("   status  - Ver estado completo del sistema")
print("   models  - Listar todos los modelos disponibles")
print("   help    - Ver ayuda completa")

# Modo interactivo básico
print("\n🤖 MCP>", end=" ", flush=True)

try:
    while True:
        user_input = input().strip().lower()
        
        if user_input in ['quit', 'exit', 'q']:
            print("👋 ¡Hasta luego!")
            break
        elif user_input == 'status':
            print("📊 Estado del sistema:")
            print("   🔄 Reinicia con ollama_mcp_server.py para estado completo")
        elif user_input == 'models':
            try:
                result = subprocess.run(['ollama', 'list'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("📦 Modelos disponibles:")
                    print(result.stdout)
                else:
                    print("❌ Error listando modelos")
            except Exception as e:
                print(f"❌ Error: {e}")
        elif user_input == 'help':
            print("🆘 Ayuda básica:")
            print("   quit    - Salir")
            print("   status  - Ver estado")
            print("   models  - Listar modelos")
        else:
            print("❓ Comando no reconocido. Escribe 'help' para ayuda.")
        
        print("🤖 MCP>", end=" ", flush=True)

except KeyboardInterrupt:
    print("\n👋 ¡Hasta luego!")
except Exception as e:
    print(f"\n❌ Error: {e}")
