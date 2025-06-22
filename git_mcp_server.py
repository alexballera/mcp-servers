#!/usr/bin/env python3
"""
Git MCP Server en Python
Reemplaza el servidor Git de Node.js
"""

import asyncio
import json
import sys
import os
import subprocess
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class GitMCPServer:
    def __init__(self):
        self.base_path = os.getcwd()
        
    def _run_git_command(self, command: List[str], cwd: str = None) -> Dict[str, Any]:
        """Ejecutar comando git y retornar resultado"""
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=cwd or self.base_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "code": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "git-python-mcp-server",
                "version": "1.0.0"
            }
        }

    async def list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tools": [
                {
                    "name": "git_status",
                    "description": "Obtener estado del repositorio git",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "git_log",
                    "description": "Ver historial de commits",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "limit": {"type": "number", "description": "Número de commits (default: 10)"},
                            "oneline": {"type": "boolean", "description": "Formato compacto"}
                        }
                    }
                },
                {
                    "name": "git_diff",
                    "description": "Ver diferencias en archivos",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file": {"type": "string", "description": "Archivo específico"},
                            "staged": {"type": "boolean", "description": "Ver cambios en staging"}
                        }
                    }
                },
                {
                    "name": "git_branch",
                    "description": "Gestionar ramas",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "description": "list, create, switch, delete"},
                            "name": {"type": "string", "description": "Nombre de rama"}
                        }
                    }
                },
                {
                    "name": "git_add",
                    "description": "Agregar archivos al staging",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "files": {"type": "array", "items": {"type": "string"}, "description": "Archivos a agregar"}
                        }
                    }
                },
                {
                    "name": "git_commit",
                    "description": "Crear commit",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Mensaje del commit"}
                        },
                        "required": ["message"]
                    }
                },
                {
                    "name": "git_push",
                    "description": "Enviar cambios al repositorio remoto",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "remote": {"type": "string", "description": "Remoto (default: origin)"},
                            "branch": {"type": "string", "description": "Rama (default: current)"}
                        }
                    }
                },
                {
                    "name": "git_pull",
                    "description": "Traer cambios del repositorio remoto",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "remote": {"type": "string", "description": "Remoto (default: origin)"},
                            "branch": {"type": "string", "description": "Rama (default: current)"}
                        }
                    }
                }
            ]
        }

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "git_status":
                result = self._run_git_command(["status", "--porcelain"])
                if result["success"]:
                    detailed = self._run_git_command(["status"])
                    return {
                        "content": [{"type": "text", "text": f"Git Status:\n{detailed['stdout']}"}]
                    }
                else:
                    return {
                        "content": [{"type": "text", "text": f"Error: {result.get('stderr', 'Error ejecutando git status')}"}]
                    }
            
            elif tool_name == "git_log":
                limit = arguments.get("limit", 10)
                oneline = arguments.get("oneline", True)
                
                cmd = ["log", f"-{limit}"]
                if oneline:
                    cmd.append("--oneline")
                else:
                    cmd.extend(["--graph", "--pretty=format:%h - %an, %ar : %s"])
                
                result = self._run_git_command(cmd)
                return {
                    "content": [{"type": "text", "text": f"Git Log:\n{result['stdout']}"}]
                }
            
            elif tool_name == "git_diff":
                file_path = arguments.get("file", "")
                staged = arguments.get("staged", False)
                
                cmd = ["diff"]
                if staged:
                    cmd.append("--staged")
                if file_path:
                    cmd.append(file_path)
                
                result = self._run_git_command(cmd)
                return {
                    "content": [{"type": "text", "text": f"Git Diff:\n{result['stdout'] or 'No changes'}"}]
                }
            
            elif tool_name == "git_branch":
                action = arguments.get("action", "list")
                name = arguments.get("name", "")
                
                if action == "list":
                    result = self._run_git_command(["branch", "-a"])
                elif action == "create" and name:
                    result = self._run_git_command(["checkout", "-b", name])
                elif action == "switch" and name:
                    result = self._run_git_command(["checkout", name])
                elif action == "delete" and name:
                    result = self._run_git_command(["branch", "-d", name])
                else:
                    return {
                        "content": [{"type": "text", "text": "Acción no válida o falta nombre de rama"}]
                    }
                
                return {
                    "content": [{"type": "text", "text": f"Git Branch ({action}):\n{result['stdout']}\n{result.get('stderr', '')}"}]
                }
            
            elif tool_name == "git_add":
                files = arguments.get("files", [])
                if not files:
                    files = ["."]
                
                result = self._run_git_command(["add"] + files)
                return {
                    "content": [{"type": "text", "text": f"Git Add:\n{result['stdout'] or 'Files added successfully'}\n{result.get('stderr', '')}"}]
                }
            
            elif tool_name == "git_commit":
                message = arguments.get("message", "")
                if not message:
                    return {
                        "content": [{"type": "text", "text": "Error: Mensaje de commit requerido"}]
                    }
                
                result = self._run_git_command(["commit", "-m", message])
                return {
                    "content": [{"type": "text", "text": f"Git Commit:\n{result['stdout']}\n{result.get('stderr', '')}"}]
                }
            
            elif tool_name == "git_push":
                remote = arguments.get("remote", "origin")
                branch = arguments.get("branch", "")
                
                cmd = ["push", remote]
                if branch:
                    cmd.append(branch)
                
                result = self._run_git_command(cmd)
                return {
                    "content": [{"type": "text", "text": f"Git Push:\n{result['stdout']}\n{result.get('stderr', '')}"}]
                }
            
            elif tool_name == "git_pull":
                remote = arguments.get("remote", "origin")
                branch = arguments.get("branch", "")
                
                cmd = ["pull", remote]
                if branch:
                    cmd.append(branch)
                
                result = self._run_git_command(cmd)
                return {
                    "content": [{"type": "text", "text": f"Git Pull:\n{result['stdout']}\n{result.get('stderr', '')}"}]
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
    server = GitMCPServer()
    asyncio.run(server.run())
