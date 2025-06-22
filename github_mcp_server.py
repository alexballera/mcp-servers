#!/usr/bin/env python3
"""
GitHub MCP Server en Python
Reemplaza el servidor GitHub de Node.js
"""

import asyncio
import json
import sys
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GitHubMCPServer:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        
    def _github_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict[str, Any]:
        """Hacer request a GitHub API"""
        if not self.github_token:
            return {"error": "GitHub token no configurado en variable GITHUB_TOKEN"}
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'MCP-GitHub-Server/1.0'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=15)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, json=data, timeout=15)
            else:
                return {"error": f"Método HTTP {method} no soportado"}
            
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {"error": f"GitHub API error: {response.status_code} - {response.text[:200]}"}
        except Exception as e:
            return {"error": f"Error conectando a GitHub: {str(e)}"}

    async def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "github-python-mcp-server",
                "version": "1.0.0"
            }
        }

    async def list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tools": [
                {
                    "name": "search_repositories",
                    "description": "Buscar repositorios en GitHub",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Términos de búsqueda"},
                            "sort": {"type": "string", "description": "stars, forks, updated (default: stars)"},
                            "order": {"type": "string", "description": "asc, desc (default: desc)"},
                            "per_page": {"type": "number", "description": "Resultados por página (default: 10)"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_user_repos",
                    "description": "Obtener repositorios del usuario autenticado",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "description": "all, owner, public, private, member (default: owner)"},
                            "sort": {"type": "string", "description": "created, updated, pushed, full_name (default: updated)"},
                            "per_page": {"type": "number", "description": "Resultados por página (default: 20)"}
                        }
                    }
                },
                {
                    "name": "get_repo_info",
                    "description": "Obtener información detallada de un repositorio",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string", "description": "Propietario del repositorio"},
                            "repo": {"type": "string", "description": "Nombre del repositorio"}
                        },
                        "required": ["owner", "repo"]
                    }
                },
                {
                    "name": "list_issues",
                    "description": "Listar issues de un repositorio",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string", "description": "Propietario del repositorio"},
                            "repo": {"type": "string", "description": "Nombre del repositorio"},
                            "state": {"type": "string", "description": "open, closed, all (default: open)"},
                            "labels": {"type": "string", "description": "Filtrar por labels"},
                            "per_page": {"type": "number", "description": "Resultados por página (default: 10)"}
                        },
                        "required": ["owner", "repo"]
                    }
                },
                {
                    "name": "create_issue",
                    "description": "Crear un nuevo issue",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string", "description": "Propietario del repositorio"},
                            "repo": {"type": "string", "description": "Nombre del repositorio"},
                            "title": {"type": "string", "description": "Título del issue"},
                            "body": {"type": "string", "description": "Descripción del issue"},
                            "labels": {"type": "array", "items": {"type": "string"}, "description": "Labels del issue"}
                        },
                        "required": ["owner", "repo", "title"]
                    }
                },
                {
                    "name": "list_pull_requests",
                    "description": "Listar pull requests de un repositorio",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "owner": {"type": "string", "description": "Propietario del repositorio"},
                            "repo": {"type": "string", "description": "Nombre del repositorio"},
                            "state": {"type": "string", "description": "open, closed, all (default: open)"},
                            "per_page": {"type": "number", "description": "Resultados por página (default: 10)"}
                        },
                        "required": ["owner", "repo"]
                    }
                },
                {
                    "name": "get_user_info",
                    "description": "Obtener información del usuario autenticado",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "search_code",
                    "description": "Buscar código en repositorios",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Términos de búsqueda"},
                            "sort": {"type": "string", "description": "indexed (default)"},
                            "order": {"type": "string", "description": "asc, desc (default: desc)"},
                            "per_page": {"type": "number", "description": "Resultados por página (default: 5)"}
                        },
                        "required": ["query"]
                    }
                }
            ]
        }

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "search_repositories":
                query = arguments.get("query", "")
                sort = arguments.get("sort", "stars")
                order = arguments.get("order", "desc")
                per_page = arguments.get("per_page", 10)
                
                endpoint = f"search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}"
                result = self._github_request(endpoint)
                
                if result.get("success"):
                    repos = result["data"]["items"]
                    repo_list = []
                    for repo in repos:
                        repo_list.append(
                            f"⭐ {repo['full_name']} ({repo['stargazers_count']} stars)\n"
                            f"   {repo.get('description', 'No description')}\n"
                            f"   🔗 {repo['html_url']}\n"
                        )
                    
                    return {
                        "content": [{"type": "text", "text": f"Resultados de búsqueda para '{query}':\n\n" + "\n".join(repo_list)}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error')}"}]
                    }
            
            elif tool_name == "get_user_repos":
                repo_type = arguments.get("type", "owner")
                sort = arguments.get("sort", "updated")
                per_page = arguments.get("per_page", 20)
                
                endpoint = f"user/repos?type={repo_type}&sort={sort}&per_page={per_page}"
                result = self._github_request(endpoint)
                
                if result.get("success"):
                    repos = result["data"]
                    repo_list = []
                    for repo in repos:
                        status = "🔒" if repo['private'] else "🌐"
                        repo_list.append(
                            f"{status} {repo['full_name']}\n"
                            f"   {repo.get('description', 'No description')}\n"
                            f"   ⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']} | {repo['language'] or 'N/A'}\n"
                        )
                    
                    return {
                        "content": [{"type": "text", "text": f"Tus repositorios ({repo_type}):\n\n" + "\n".join(repo_list)}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error')}"}]
                    }
            
            elif tool_name == "get_repo_info":
                owner = arguments.get("owner", "")
                repo = arguments.get("repo", "")
                
                endpoint = f"repos/{owner}/{repo}"
                result = self._github_request(endpoint)
                
                if result.get("success"):
                    repo_data = result["data"]
                    info = f"📋 Información del repositorio: {repo_data['full_name']}\n\n"
                    info += f"📝 Descripción: {repo_data.get('description', 'No description')}\n"
                    info += f"🌐 URL: {repo_data['html_url']}\n"
                    info += f"⭐ Stars: {repo_data['stargazers_count']}\n"
                    info += f"🍴 Forks: {repo_data['forks_count']}\n"
                    info += f"👀 Watchers: {repo_data['watchers_count']}\n"
                    info += f"📊 Language: {repo_data.get('language', 'N/A')}\n"
                    info += f"📅 Created: {repo_data['created_at']}\n"
                    info += f"🔄 Updated: {repo_data['updated_at']}\n"
                    info += f"📏 Size: {repo_data['size']} KB\n"
                    info += f"🔒 Private: {'Yes' if repo_data['private'] else 'No'}\n"
                    
                    return {
                        "content": [{"type": "text", "text": info}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error')}"}]
                    }
            
            elif tool_name == "list_issues":
                owner = arguments.get("owner", "")
                repo = arguments.get("repo", "")
                state = arguments.get("state", "open")
                labels = arguments.get("labels", "")
                per_page = arguments.get("per_page", 10)
                
                endpoint = f"repos/{owner}/{repo}/issues?state={state}&per_page={per_page}"
                if labels:
                    endpoint += f"&labels={labels}"
                
                result = self._github_request(endpoint)
                
                if result.get("success"):
                    issues = result["data"]
                    issue_list = []
                    for issue in issues:
                        labels_str = ", ".join([label["name"] for label in issue.get("labels", [])])
                        issue_list.append(
                            f"🐛 #{issue['number']} - {issue['title']}\n"
                            f"   👤 {issue['user']['login']} | 📅 {issue['created_at'][:10]}\n"
                            f"   🏷️ {labels_str or 'No labels'}\n"
                            f"   🔗 {issue['html_url']}\n"
                        )
                    
                    return {
                        "content": [{"type": "text", "text": f"Issues de {owner}/{repo} ({state}):\n\n" + "\n".join(issue_list)}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error')}"}]
                    }
            
            elif tool_name == "get_user_info":
                result = self._github_request("user")
                
                if result.get("success"):
                    user = result["data"]
                    info = f"👤 Información del usuario: {user['login']}\n\n"
                    info += f"📝 Nombre: {user.get('name', 'N/A')}\n"
                    info += f"🌐 URL: {user['html_url']}\n"
                    info += f"📧 Email: {user.get('email', 'N/A')}\n"
                    info += f"🏢 Company: {user.get('company', 'N/A')}\n"
                    info += f"📍 Location: {user.get('location', 'N/A')}\n"
                    info += f"📋 Bio: {user.get('bio', 'N/A')}\n"
                    info += f"📊 Public repos: {user['public_repos']}\n"
                    info += f"👥 Followers: {user['followers']}\n"
                    info += f"👤 Following: {user['following']}\n"
                    info += f"📅 Created: {user['created_at'][:10]}\n"
                    
                    return {
                        "content": [{"type": "text", "text": info}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('error')}"}]
                    }
            
            else:
                return {
                    "content": [{"type": "text", "text": f"Herramienta '{tool_name}' no encontrada"}],
                    "isError": True
                }
                
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error ejecutando {tool_name}: {str(e)}"}],
                "isError": True
            }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
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
                
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
            
        except Exception as e:
            return {
                "jsonrpc": "2.0", 
                "id": request_id,
                "error": {"code": -32603, "message": str(e)}
            }

    async def run(self):
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                    
                request = json.loads(line.strip())
                response = await self.handle_request(request)
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0", "id": None,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    server = GitHubMCPServer()
    asyncio.run(server.run())
