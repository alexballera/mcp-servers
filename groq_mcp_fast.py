#!/usr/bin/env python3
"""
MCP Server ultra-rápido con Groq
Respuestas en 0.5-2 segundos
"""

import asyncio
import json
import sys
import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GroqMCPServer:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Modelo ultra-rápido
        self.model = "llama-3.1-8b-instant"  # El más rápido de Groq
        
        if not self.api_key:
            print("⚠️  GROQ_API_KEY no encontrada. Obtén una gratis en: https://console.groq.com/", file=sys.stderr)

    def _make_request(self, prompt: str, system: str = "", max_tokens: int = 500) -> str:
        """Request ultra-rápido a Groq"""
        if not self.api_key:
            return "❌ Configura GROQ_API_KEY en .env para usar esta herramienta"
        
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data,
                timeout=10  # Timeout corto porque Groq es súper rápido
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"❌ Error Groq: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "groq-mcp-fast",
                "version": "1.0.0"
            }
        }

    async def list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tools": [
                {
                    "name": "fast_chat",
                    "description": "Chat ultra-rápido con Llama-3.1 via Groq",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"message": {"type": "string"}},
                        "required": ["message"]
                    }
                },
                {
                    "name": "code_help",
                    "description": "Ayuda de código rápida y precisa",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"code_query": {"type": "string"}},
                        "required": ["code_query"]
                    }
                },
                {
                    "name": "quick_fix",
                    "description": "Solución rápida a problemas",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"problem": {"type": "string"}},
                        "required": ["problem"]
                    }
                }
            ]
        }

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "fast_chat":
                message = arguments.get("message", "")
                response = self._make_request(message)
                
            elif tool_name == "code_help":
                query = arguments.get("code_query", "")
                system = "Eres un experto programador. Da respuestas concisas con código funcional. Máximo 3 párrafos."
                response = self._make_request(query, system, max_tokens=800)
                
            elif tool_name == "quick_fix":
                problem = arguments.get("problem", "")
                system = "Da una solución directa y práctica. Máximo 2 párrafos."
                response = self._make_request(problem, system, max_tokens=400)
                
            else:
                response = f"Herramienta '{tool_name}' no encontrada"
                
            return {
                "content": [{"type": "text", "text": response}]
            }
            
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
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
    server = GroqMCPServer()
    asyncio.run(server.run())
