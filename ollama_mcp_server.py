#!/usr/bin/env python3
"""
Ollama MCP Server - Integración optimizada GitHub + Ollama
Servidor MCP especializado para desarrollo con modelos locales
"""

import asyncio
import json
import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar conexión con Ollama al inicio
def check_ollama_connection():
    """Verificar que Ollama esté funcionando"""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

class OllamaMCPServer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.1:8b"
        self.coding_model = "deepseek-coder:6.7b"
        
        # Herramientas disponibles
        self.tools = {
            'chat': self.chat,
            'code': self.code_assist,
            'github_search': self.github_search,
            'github_repo': self.github_repo_info,
            'github_file': self.github_get_file,
            'analyze_code': self.analyze_code,
            'review_code': self.review_code,
            'explain_repo': self.explain_repo,
            'help': self.show_help
        }
    
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
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=data)
            if response.status_code == 200:
                return response.json().get('response', 'Sin respuesta')
            else:
                return f"Error: Ollama no disponible ({response.status_code})"
        except Exception as e:
            return f"Error conectando a Ollama: {str(e)}"
    
    def chat(self, message: str) -> Dict[str, Any]:
        """Chat general con Llama"""
        response = self._ollama_request(self.default_model, message)
        return {"type": "chat", "response": response}
    
    def code_assist(self, query: str) -> Dict[str, Any]:
        """Asistencia de código con modelo especializado"""
        system_prompt = """Eres un asistente de programación experto. 
        Proporciona código limpio, bien documentado y siguiendo mejores prácticas.
        Incluye explicaciones claras y ejemplos cuando sea necesario."""
        
        response = self._ollama_request(self.coding_model, query, system_prompt)
        return {"type": "code", "response": response}
    
    def github_search(self, query: str) -> Dict[str, Any]:
        """Buscar repositorios en GitHub"""
        if not self.github_token:
            return {"error": "GitHub token no configurado"}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                repos = []
                for repo in data.get('items', []):
                    repos.append({
                        'name': repo['full_name'],
                        'description': repo.get('description', 'Sin descripción'),
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language', 'No especificado'),
                        'url': repo['html_url']
                    })
                return {"type": "github", "repositories": repos}
            else:
                return {"error": f"Error en GitHub API: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"Error al buscar en GitHub: {str(e)}"}
    
    def github_repo_info(self, repo: str) -> Dict[str, Any]:
        """Información detallada de un repositorio"""
        if not self.github_token:
            return {"error": "GitHub token no configurado"}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            url = f'https://api.github.com/repos/{repo}'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "type": "github",
                    "repo_info": {
                        'name': data['full_name'],
                        'description': data.get('description', 'Sin descripción'),
                        'language': data.get('language', 'No especificado'),
                        'stars': data['stargazers_count'],
                        'forks': data['forks_count'],
                        'issues': data['open_issues_count'],
                        'url': data['html_url'],
                        'clone_url': data['clone_url']
                    }
                }
            else:
                return {"error": f"Repositorio no encontrado: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"Error al obtener info del repositorio: {str(e)}"}
    
    def github_get_file(self, repo: str, file_path: str) -> Dict[str, Any]:
        """Obtener contenido de un archivo de GitHub"""
        if not self.github_token:
            return {"error": "GitHub token no configurado"}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            url = f'https://api.github.com/repos/{repo}/contents/{file_path}'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
                return {
                    "type": "github",
                    "file": {
                        'path': file_path,
                        'size': data['size'],
                        'content': content[:2000] + '...' if len(content) > 2000 else content
                    }
                }
            else:
                return {"error": f"Archivo no encontrado: {response.status_code}"}
        
        except Exception as e:
            return {"error": f"Error al obtener archivo: {str(e)}"}
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analizar código con IA"""
        system_prompt = """Eres un experto en análisis de código. 
        Analiza el código proporcionado y ofrece:
        1. Resumen de funcionalidad
        2. Posibles mejoras
        3. Problemas de seguridad
        4. Optimizaciones de rendimiento"""
        
        prompt = f"Analiza este código:\n\n```\n{code}\n```"
        response = self._ollama_request(self.coding_model, prompt, system_prompt)
        return {"type": "analysis", "response": response}
    
    def review_code(self, code: str) -> Dict[str, Any]:
        """Revisión de código con IA"""
        system_prompt = """Eres un revisor de código senior. 
        Proporciona una revisión detallada incluyendo:
        - Calidad del código
        - Mejores prácticas
        - Sugerencias específicas
        - Refactoring recomendado"""
        
        prompt = f"Revisa este código:\n\n```\n{code}\n```"
        response = self._ollama_request(self.coding_model, prompt, system_prompt)
        return {"type": "review", "response": response}
    
    def explain_repo(self, repo: str) -> Dict[str, Any]:
        """Explicar un repositorio usando GitHub + IA"""
        # Primero obtener info del repo
        repo_info = self.github_repo_info(repo)
        if "error" in repo_info:
            return repo_info
        
        # Luego pedir explicación a la IA
        repo_data = repo_info['repo_info']
        prompt = f"""Explica este repositorio de GitHub:
        
        Nombre: {repo_data['name']}
        Descripción: {repo_data['description']}
        Lenguaje: {repo_data['language']}
        Estrellas: {repo_data['stars']}
        
        Proporciona:
        1. Resumen del proyecto
        2. Tecnologías utilizadas
        3. Posibles casos de uso
        4. Nivel de madurez del proyecto"""
        
        response = self._ollama_request(self.default_model, prompt)
        return {
            "type": "explanation",
            "repo_info": repo_data,
            "explanation": response
        }
    
    def show_help(self) -> Dict[str, Any]:
        """Mostrar ayuda del servidor"""
        return {
            "tools": [
                {"name": "chat", "description": "Chat general con Llama", "usage": "chat <mensaje>"},
                {"name": "code", "description": "Asistencia de código", "usage": "code <consulta>"},
                {"name": "github_search", "description": "Buscar repos en GitHub", "usage": "github_search <query>"},
                {"name": "github_repo", "description": "Info de repositorio", "usage": "github_repo <owner/repo>"},
                {"name": "github_file", "description": "Obtener archivo", "usage": "github_file <owner/repo> <path>"},
                {"name": "analyze_code", "description": "Analizar código", "usage": "analyze_code <código>"},
                {"name": "review_code", "description": "Revisar código", "usage": "review_code <código>"},
                {"name": "explain_repo", "description": "Explicar repositorio", "usage": "explain_repo <owner/repo>"},
                {"name": "help", "description": "Mostrar ayuda", "usage": "help"}
            ],
            "models": {
                "chat": self.default_model,
                "coding": self.coding_model
            }
        }
    
    def parse_command(self, user_input: str) -> Dict[str, Any]:
        """Parsear comando del usuario"""
        parts = user_input.strip().split(' ', 2)
        tool_name = parts[0].lower()
        
        if tool_name not in self.tools:
            return {"error": f"Herramienta '{tool_name}' no encontrada. Usa 'help' para ver opciones."}
        
        if tool_name == 'help':
            return {"tool": "help", "params": {}}
        elif tool_name in ['chat', 'code', 'github_search', 'analyze_code', 'review_code']:
            if len(parts) < 2:
                return {"error": f"Uso: {tool_name} <mensaje/query/código>"}
            message = ' '.join(parts[1:])
            return {"tool": tool_name, "params": {"message": message}}
        elif tool_name in ['github_repo', 'explain_repo']:
            if len(parts) < 2:
                return {"error": f"Uso: {tool_name} <owner/repo>"}
            return {"tool": tool_name, "params": {"repo": parts[1]}}
        elif tool_name == 'github_file':
            if len(parts) < 3:
                return {"error": "Uso: github_file <owner/repo> <file_path>"}
            return {"tool": tool_name, "params": {"repo": parts[1], "file_path": parts[2]}}
        
        return {"error": "Comando no reconocido"}
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Manejar solicitudes del cliente"""
        tool_name = request.get('tool')
        params = request.get('params', {})
        
        if tool_name not in self.tools:
            return {"error": f"Herramienta no encontrada: {tool_name}"}
        
        try:
            if tool_name == 'help':
                return self.tools[tool_name]()
            elif tool_name in ['chat', 'code', 'github_search', 'analyze_code', 'review_code']:
                return self.tools[tool_name](params.get('message', ''))
            elif tool_name in ['github_repo', 'explain_repo']:
                return self.tools[tool_name](params.get('repo', ''))
            elif tool_name == 'github_file':
                return self.tools[tool_name](params.get('repo', ''), params.get('file_path', ''))
            else:
                return {"error": "Parámetros incorrectos"}
        except Exception as e:
            return {"error": f"Error ejecutando {tool_name}: {str(e)}"}
    
    async def run(self):
        """Ejecutar servidor en modo interactivo"""
        # Verificar conexión inicial
        if not check_ollama_connection():
            print("❌ Error: No se puede conectar a Ollama")
            print("� Asegúrate de que Ollama esté ejecutándose: ollama serve")
            return
        
        print("�🚀 Ollama MCP Server iniciado")
        print(f"📊 Modelo chat: {self.default_model}")
        print(f"💻 Modelo coding: {self.coding_model}")
        print(f"🔗 GitHub token: {'✅ Configurado' if self.github_token else '❌ No configurado'}")
        print("📚 Escribe 'help' para ver comandos disponibles")
        print("🚪 Escribe 'quit' para salir\n")
        
        while True:
            try:
                user_input = input("🤖 MCP> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Servidor MCP terminado")
                    break
                
                if not user_input:
                    continue
                
                # Parsear y ejecutar comando
                parsed = self.parse_command(user_input)
                if "error" in parsed:
                    print(f"❌ {parsed['error']}")
                    continue
                
                result = await self.handle_request(parsed)
                
                # Mostrar resultado formateado
                if 'error' in result:
                    print(f"❌ Error: {result['error']}")
                elif result.get('type') == 'chat':
                    print(f"💬 {result['response']}")
                elif result.get('type') == 'code':
                    print(f"💻 {result['response']}")
                elif result.get('type') == 'github':
                    print("📁 GitHub:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                elif result.get('type') == 'analysis':
                    print(f"🔍 Análisis:\n{result['response']}")
                elif result.get('type') == 'review':
                    print(f"📝 Revisión:\n{result['response']}")
                elif result.get('type') == 'explanation':
                    print(f"📖 Explicación del repo {result['repo_info']['name']}:")
                    print(f"{result['explanation']}")
                else:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                
                print()  # Línea en blanco
                
            except KeyboardInterrupt:
                print("\n👋 Servidor MCP terminado")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    server = OllamaMCPServer()
    asyncio.run(server.run())
