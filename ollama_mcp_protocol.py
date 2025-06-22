#!/usr/bin/env python3
"""
Ollama MCP Server - Protocolo MCP estándar
Servidor compatible con Model Context Protocol para VS Code
"""

import asyncio
import json
import sys
from typing import Dict, Any
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class OllamaMCPServer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_url = "http://localhost:11434"
        self.default_model = "llama3.1:8b"
        self.coding_model = "deepseek-coder:6.7b"
        
    def _ollama_request(self, model: str, prompt: str, system: str = "") -> str:
        """Realizar solicitud a Ollama con timeout optimizado"""
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            if system:
                data["system"] = system
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=data, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', 'Sin respuesta')
            else:
                return f"Error: Ollama no disponible ({response.status_code})"
        except requests.exceptions.Timeout:
            return "Error: Timeout - Ollama tardó demasiado en responder."
        except Exception as e:
            return f"Error conectando a Ollama: {str(e)}"

    async def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Inicializar servidor MCP"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            },
            "serverInfo": {
                "name": "ollama-mcp-server",
                "version": "1.0.0"
            }
        }

    async def list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Listar herramientas disponibles"""
        return {
            "tools": [
                {
                    "name": "chat",
                    "description": "Chat general con Llama",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Mensaje para el chat"}
                        },
                        "required": ["message"]
                    }
                },
                {
                    "name": "code_assist", 
                    "description": "Asistencia de código especializada",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Consulta de programación"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "github_search",
                    "description": "Buscar repositorios en GitHub",
                    "inputSchema": {
                        "type": "object", 
                        "properties": {
                            "query": {"type": "string", "description": "Términos de búsqueda"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "analyze_code",
                    "description": "Analizar código con IA",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "Código a analizar"}
                        },
                        "required": ["code"]
                    }
                }
            ]
        }

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar herramienta"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "chat":
                message = arguments.get("message", "")
                response = self._ollama_request(self.default_model, message)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": response
                        }
                    ]
                }
                
            elif tool_name == "code_assist":
                query = arguments.get("query", "")
                system_prompt = """Eres un asistente de programación experto. 
                Proporciona código limpio, bien documentado y siguiendo mejores prácticas."""
                response = self._ollama_request(self.coding_model, query, system_prompt)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": response
                        }
                    ]
                }
                
            elif tool_name == "github_search":
                query = arguments.get("query", "")
                result = await self._github_search(query)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }
                
            elif tool_name == "analyze_code":
                code = arguments.get("code", "")
                system_prompt = """Eres un experto en análisis de código. 
                Analiza el código y ofrece mejoras, problemas de seguridad y optimizaciones."""
                prompt = f"Analiza este código:\n\n```\n{code}\n```"
                response = self._ollama_request(self.coding_model, prompt, system_prompt)
                return {
                    "content": [
                        {
                            "type": "text", 
                            "text": response
                        }
                    ]
                }
                
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Herramienta '{tool_name}' no encontrada"
                        }
                    ],
                    "isError": True
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error ejecutando {tool_name}: {str(e)}"
                    }
                ],
                "isError": True
            }

    async def _github_search(self, query: str) -> Dict[str, Any]:
        """Buscar repositorios en GitHub"""
        if not self.github_token:
            return {"error": "GitHub token no configurado"}
        
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5'
            response = requests.get(url, headers=headers, timeout=15)
            
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
                return {"repositories": repos}
            else:
                return {"error": f"Error en GitHub API: {response.status_code}"}
        except Exception as e:
            return {"error": f"Error al buscar en GitHub: {str(e)}"}

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Manejar solicitudes JSON-RPC"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = await self.initialize(params)
            elif method == "tools/list":
                result = await self.list_tools(params)
            elif method == "tools/call":
                result = await self.call_tool(params)
            else:
                result = {"error": f"Método no soportado: {method}"}
                
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0", 
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    async def run(self):
        """Ejecutar servidor MCP"""
        while True:
            try:
                # Leer línea de stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                    
                # Parsear JSON-RPC
                request = json.loads(line.strip())
                
                # Procesar solicitud
                response = await self.handle_request(request)
                
                # Enviar respuesta
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0", 
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    server = OllamaMCPServer()
    asyncio.run(server.run())
