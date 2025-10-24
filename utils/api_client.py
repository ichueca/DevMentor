import os
import google.genai as genai
from openai import OpenAI
from config import DEFAULT_SETTINGS
from typing import Generator, Optional, Dict, Any


class GeminiClient:
    """Cliente para Google Gemini API."""

    def __init__(self, api_key:Optional[str] = None):
        """
        Inicializa el cliente de Gemini

        Args:
            api_key: Clave de API de Google. 
                  Si no se proporciona, se busca en la variable de entorno GEMINI_API_KEY
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere GEMINI_API_KEY en las variables de entorno")
        self.client = genai.Client(api_key=self.api_key)
        self.modelo = DEFAULT_SETTINGS["model"]

    def generate_response(self, prompt:str, **kwargs:Dict) -> Generator:
        """
        Genera una respuesta en streaming usando Gemini

        Args:
            prompt: El prompt para enviar al modelo
            **kwargs: Parámetros adicionales

        Returns:
            La respuesta generada por el modelo como un objeto Generator
        """

        temperature = kwargs.get("temperature")
        max_tokens = kwargs.get("max_tokens")
        gen_config ={
            "temperature":temperature,
            "maxOutputTokens":max_tokens
        }

        try:
            response = self.client.models.generate_content_stream(
                model= self.modelo,
                contents=prompt,
                config = gen_config,
            )

            for chunks in response:
                yield chunks.text
        except Exception as ex:
            yield f"Error al generar respuesta: {str(ex)}"


class OpenAIClient:
    """ Cliente para OpenAI """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de OpenAI

        Args:
            api_key: Clave de API de Google. 
                  Si no se proporciona, se busca en la variable de entorno OPENAI_API_KEY
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere OPENAI_API_KEY en las variables de entorno")
        
        self.model = DEFAULT_SETTINGS["model_openai"] # self.model = "gpt-4.0"

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai" # SÖLO SI USAMOS GEMINI para simular OpenAI
        )

    def generate_response(self, prompt:str, **kwargs:Dict) -> Generator:
        """
        Genera una respuesta en streaming usando OpenAI

        Args:
            prompt: El prompt para enviar al modelo
            **kwargs: Parametros adicionales

        Returns:
            La respuesta generada por el modelo como un objeto Generator
        """
        try:
            response =  self.client.chat.completions.create(
                model=self.model,
                messages=[{"role":"user", "content":prompt}],
                stream=True,
                **kwargs,
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
        except Exception as e:
            yield f"Error al generar respuesta: {str(e)}"

def create_llm_provider(provider:str = "gemini") -> Any:
    """
    Crea un cliente LLM basado en el proveedor especificado

    Args:
        provider: El proveedor ('gemnini' u 'openai')

    Returns;
        Una instancia del cliente seleccionado
    """
    if provider.lower() == 'genini':
        return GeminiClient()
    elif provider.lower() == 'openai':
        return OpenAIClient()
    else:
        raise ValueError(f"Proveedor no soprtado : {provider}")