#!/usr/bin/env python3
"""
Test simple para diagnosticar el problema de timeout de Ollama
"""

import requests
import time

def test_ollama_direct():
    """Test directo de la API de Ollama"""
    print("🔍 Diagnosticando problema de timeout...")
    
    # 1. Test básico
    print("\n1. Verificando conexión básica...")
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        print(f"✅ Ollama responde: {response.json()}")
    except Exception as e:
        print(f"❌ Error básico: {e}")
        return
    
    # 2. Test de modelos disponibles
    print("\n2. Verificando modelos...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get("models", [])
        print(f"📦 Modelos disponibles: {len(models)}")
        for model in models[:2]:
            print(f"   • {model['name']}")
    except Exception as e:
        print(f"❌ Error listando modelos: {e}")
        return
    
    # 3. Test de generación simple
    print("\n3. Probando generación simple...")
    start_time = time.time()
    
    try:
        data = {
            "model": "llama3.1:8b",
            "prompt": "Di solo 'hola'",
            "stream": False
        }
        
        print("   🔄 Enviando request...")
        response = requests.post("http://localhost:11434/api/generate", 
                               json=data, timeout=30)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            text = result.get('response', 'Sin respuesta')
            print(f"✅ Respuesta recibida en {duration:.1f}s: '{text.strip()}'")
        else:
            print(f"❌ Error HTTP {response.status_code}")
            
    except requests.exceptions.Timeout:
        duration = time.time() - start_time
        print(f"❌ Timeout después de {duration:.1f}s")
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Error después de {duration:.1f}s: {e}")

if __name__ == "__main__":
    test_ollama_direct()
