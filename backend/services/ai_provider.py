"""
Kronaghor - AI Provider Service
Maneja múltiples proveedores de IA (OpenAI, Grok, Ollama).
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import logging

import requests
from openai import OpenAI

from backend.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("kronaghor.ai")


class AIProvider(ABC):
    """Clase base para proveedores de IA."""
    
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Enviar mensaje de chat y obtener respuesta."""
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """Listar modelos disponibles."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del proveedor."""
        pass


class OpenAIProvider(AIProvider):
    """Proveedor de OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    @property
    def name(self) -> str:
        return "openai"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Enviar mensaje a OpenAI."""
        if not self.client:
            raise ValueError("OpenAI API key no configurada")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"Error en OpenAI: {e}")
            return {"success": False, "error": str(e)}
    
    def list_models(self) -> List[str]:
        """Listar modelos de OpenAI."""
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]


class GrokProvider(AIProvider):
    """Proveedor de Grok (xAI)."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GROK_API_KEY
        self.base_url = "https://api.x.ai/v1"
    
    @property
    def name(self) -> str:
        return "grok"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-2-1212",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Enviar mensaje a Grok."""
        if not self.api_key:
            raise ValueError("Grok API key no configurada")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "content": data["choices"][0]["message"]["content"],
                "model": data["model"],
                "usage": data.get("usage", {})
            }
        except Exception as e:
            logger.error(f"Error en Grok: {e}")
            return {"success": False, "error": str(e)}
    
    def list_models(self) -> List[str]:
        """Listar modelos de Grok."""
        return ["grok-2-1212", "grok-2", "grok-beta"]


class OllamaProvider(AIProvider):
    """Proveedor de Ollama (local)."""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
    
    @property
    def name(self) -> str:
        return "ollama"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama3.2",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Enviar mensaje a Ollama."""
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "content": data["message"]["content"],
                "model": data.get("model", model),
                "usage": data.get("done", False)
            }
        except Exception as e:
            logger.error(f"Error en Ollama: {e}")
            return {"success": False, "error": str(e)}
    
    def list_models(self) -> List[str]:
        """Listar modelos de Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            pass
        return ["llama3.2", "mistral", "codellama"]


class AIService:
    """Servicio unificado de IA."""
    
    PROVIDERS = {
        "openai": OpenAIProvider,
        "grok": GrokProvider,
        "ollama": OllamaProvider
    }
    
    def __init__(self, provider_name: Optional[str] = None):
        self.provider_name = provider_name or settings.DEFAULT_AI_PROVIDER
        self._provider = None
    
    @property
    def provider(self) -> AIProvider:
        """Obtener proveedor actual."""
        if self._provider is None:
            provider_class = self.PROVIDERS.get(self.provider_name)
            if not provider_class:
                raise ValueError(f"Proveedor {self.provider_name} no soportado")
            self._provider = provider_class()
        return self._provider
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enviar mensaje de chat."""
        if provider:
            provider_class = self.PROVIDERS.get(provider)
            if provider_class:
                temp_provider = provider_class()
                return temp_provider.chat(messages, model or "default", temperature, max_tokens)
        
        return self.provider.chat(messages, model or "default", temperature, max_tokens)
    
    def list_providers(self) -> Dict[str, List[str]]:
        """Listar todos los proveedores y sus modelos."""
        result = {}
        for name, provider_class in self.PROVIDERS.items():
            try:
                p = provider_class()
                result[name] = p.list_models()
            except Exception:
                result[name] = []
        return result
    
    def legal_system_prompt(self) -> str:
        """Prompt del sistema para consultas legales colombianas."""
        return """Eres Kronaghor, un asistente legal colombiano especializado en el sistema judicial colombiano.

Tu función es ayudar a abogados, jueces y secretarios con:
- Consultas sobre legislación colombiana
- Procedimientos judiciales
- Términos procesales
- Jurisprudencia relevante
- Redacción de documentos legales

Instrucciones:
1. Solo proporciona información legal general
2. Nodas consejos legales específicos para casos particulares
3. Siempre menciona que debe consultarse con un profesional para casos específicos
4. Referencia las normas colombianas (leyes,(decretos, códigos)
5. Sé claro, preciso y profesional

Contexto: Sistema judicial colombiano, кодigo General del Proceso, кодigo Civil, кодigo Penal, кодigo Contencioso Administrativo.
"""


# Singleton
ai_service = AIService()
