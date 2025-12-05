"""
Calcular tokens en base a un prompt
"""

from datetime import datetime
from typing import Dict, Any

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api_client import OllamaClient

class TokenManager:
    """ Gestor simple de tokens y costos """

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model_name = model_name
        self.session_stats= {
            'total_input_tokens':0,
            'total_output_tokens':0,
            'total_requests':0,
            'total_cost':0,
            'session_start': datetime.now()
        }

        # Precios por 1.000 tokens (gemini-2.0-flash)
        self.pricing = {
            'input_cost_per_1k': 0.000075, # En $
            'output_cost_per_1k': 0.0003, # En $
        }
    
    def count_tokens(self, text:str) -> int:
        """
        Cuenta tokens de forma simple

        Args:
            texto: El texto a contar
        
        Returns:
            Número estimado de tokens
        """
        if not text:
            return 0
        
        words = len(text.split())
        return int(words * 1.3)
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calcula el coste de una consulta

        Args:
            input_tokens: Tokens de entrada
            output_tokens: Tokens de salida
        
        Returns:
            Coste en dólares
        """
        input_cost = (input_tokens / 1000) * self.pricing['input_cost_per_1k']
        output_cost = (output_tokens / 1000) * self.pricing['output_cost_per_1k']
        return input_cost + output_cost

    def track_usage(self, input_tokens:int, output_tokens:int):
        """
        Regsitra el uso de tokens de la sesión

        Args:
            input_tokens: Tokens de entrada usados
            output_tokens: Tokens de salida
        """
        cost = self.calculate_cost(input_tokens, output_tokens)

        self.session_stats['total_input_tokens'] += input_tokens
        self.session_stats['total_output_tokens'] += output_tokens
        self.session_stats['total_requests'] += 1
        self.session_stats['total_cost'] += cost

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Retorna un resumen de la sesión actual

        Returns:
            Diccionario con estadísticas de la sesión
        """

        total_tokens = self.session_stats['total_input_tokens'] + self.session_stats['total_output_tokens']

        return {
            'total_tokens': total_tokens,
            'input_tokens': self.session_stats['total_input_tokens'],
            'output_tokens': self.session_stats['total_output_tokens'],
            'total_requests': self.session_stats['total_requests'],
            'total_cost': self.session_stats['total_cost'],
            'average_tokens_per_request': total_tokens / max(1, self.session_stats['total_requests']),
            'session_duration': datetime.now() - self.session_stats['session_start'],
        }

if __name__ == "__main__":
    
    manager = TokenManager()

    llm = OllamaClient()

    test_text = "¿Qué es Python y cómo se usa?"
    generator = llm.generate_response(test_text, {})
    response = ""
    for chunk in generator:
        if chunk:
            response += chunk
            print(response, end="")
    print(response[:200])

    input_tokens = manager.count_tokens(test_text)
    output_tokens = manager.count_tokens(response)
    cost = manager.calculate_cost(input_tokens,output_tokens)
    tokens = input_tokens + output_tokens

    print("🧪 Test de TokenManager")
    print(f"🗒️ Texto: '{test_text}'")
    print(f"➕ Tokens estimados: {tokens}")
    print(f"💰 Coste estimado: ${cost:.6f}")

    manager.track_usage(tokens, tokens*2)
    test_text = "¿Como se usan las clases en Python?"
    tokens = manager.count_tokens(test_text)
    manager.track_usage(tokens, tokens*2)
    summary = manager.get_session_summary()

    print(f"📶 Resumen: {summary['total_tokens']} tokens, ${summary['total_cost']:.6f}")
