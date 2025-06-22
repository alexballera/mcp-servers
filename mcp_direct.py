#!/usr/bin/env python3
"""
MCP Direct - Comandos directos sin servidor interactivo
Para uso desde cualquier directorio como agente
"""

import sys
import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class MCPDirect:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.1:8b"
        self.coding_model = "deepseek-coder:6.7b"
    
    def _ollama_request(self, model: str, prompt: str, system: str = "") -> str:
        """Realizar solicitud a Ollama"""
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            if system:
                data["system"] = system
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=data, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', 'Sin respuesta')
            else:
                return f"❌ Error: Ollama no disponible ({response.status_code})"
        except requests.exceptions.Timeout:
            return "❌ Error: Timeout - Ollama tardó demasiado en responder"
        except Exception as e:
            return f"❌ Error conectando a Ollama: {str(e)}"
    
    def chat(self, message: str) -> str:
        """Chat directo con Llama"""
        if not message:
            return "❌ Debes proporcionar un mensaje"
        
        print("🤖 Procesando con Llama 3.1...")
        response = self._ollama_request(self.default_model, message)
        return response
    
    def code_assist(self, query: str) -> str:
        """Asistencia de código directa"""
        if not query:
            return "❌ Debes proporcionar una consulta de código"
        
        system_prompt = """Eres un asistente de programación experto. 
        Proporciona código limpio, bien documentado y siguiendo mejores prácticas.
        Incluye explicaciones claras y ejemplos cuando sea necesario."""
        
        print("💻 Procesando con DeepSeek Coder...")
        response = self._ollama_request(self.coding_model, query, system_prompt)
        return response
    
    def github_search(self, query: str) -> str:
        """Búsqueda directa en GitHub"""
        if not query:
            return "❌ Debes proporcionar un término de búsqueda"
        
        if not self.github_token:
            return "❌ GitHub token no configurado"
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            print("🔍 Buscando en GitHub...")
            url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5'
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                repos = []
                for repo in data.get('items', []):
                    repos.append(f"📦 {repo['full_name']} ({repo['stargazers_count']}⭐)")
                    repos.append(f"   {repo.get('description', 'Sin descripción')}")
                    repos.append(f"   🔗 {repo['html_url']}")
                    repos.append("")
                
                if repos:
                    return "\n".join(repos)
                else:
                    return "❌ No se encontraron repositorios"
            else:
                return f"❌ Error en GitHub API: {response.status_code}"
        
        except Exception as e:
            return f"❌ Error al buscar en GitHub: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: mcp_direct.py <comando> [argumentos]")
        print("Comandos: chat, code, github_search")
        sys.exit(1)
    
    command = sys.argv[1]
    args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    mcp = MCPDirect()
    
    if command == "chat":
        result = mcp.chat(args)
    elif command == "code":
        result = mcp.code_assist(args)
    elif command == "github_search":
        result = mcp.github_search(args)
    else:
        result = f"❌ Comando no reconocido: {command}"
    
    print(result)

if __name__ == "__main__":
    main()
