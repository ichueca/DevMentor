"""
Gestor de Contexto para DevMentorAI
"""

from typing import List, Dict
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.token_manager import TokenManager
from utils.context_strategies import SlidingWindowStrategy, SummaryStrategy, SmartSelectionStrategy
from utils import OllamaClient

class ContextManager:
    """
    Gestor de contexto que combina cuenta de tokens y optimización
    """

    def __init__(self, llm_client=None, strategy="sliding_window"):
        """
        Args:
            llm_client: Cliente LLM para estrategias avanzadas
            strategy: Estrategia a utilizar ("sliding_window", "summary", "smart")
        """
        self.token_manager = TokenManager()
        self.strategy_name = strategy

        if self.strategy_name == "summary":
            self.strategy = SummaryStrategy(llm_client, keep_recent=3, summarize_thresold=5)
        elif self.strategy_name == "smart":
            self.strategy = SmartSelectionStrategy(llm_client, max_selected=4)
        else:
            self.strategy = SlidingWindowStrategy(max_messages=5)

    def prepare_context(self, messages: List[Dict], new_query:str = "") -> tuple:
        """
        Prepara el contexto optimizado para enviar al LLM

        Args:
            messages: Lista de mensajes de la conversación
            new_query: La consulta del usuario
        
        Returns:
            Tupla (mensajes_optimizados, estadísticas)
        """

        original_tokens = self._count_context_tokens(messages)
        original_cost = self.token_manager.calculate_cost(input_tokens=original_tokens,output_tokens=0)

        optimized_messages = self.strategy.optimize(messages)
        
        optimized_tokens = self._count_context_tokens(optimized_messages)
        optimized_cost = self.token_manager.calculate_cost(input_tokens=optimized_tokens, output_tokens=0)

        stats = {
            'original_messages':len(messages),
            'optimized_messages':len(optimized_messages),
            'original_tokens':original_tokens,
            'optimized_tokens':optimized_tokens,
            'tokens_saved':original_tokens - optimized_tokens,
            'reduction_percent': ((original_tokens - optimized_tokens) / original_tokens * 100) if original_tokens > 0 else 0,
            'original_cost':original_cost,
            'optimized_cost':optimized_cost,
            'cost_saved':original_cost - optimized_cost,
            'cost_reduction_percent': ((original_cost - optimized_cost) / original_cost * 100) if original_cost > 0 else 0,
            'strategy_used': self.strategy_name
        }

        return optimized_messages, stats

    def _count_context_tokens(self, messages:List[Dict]) -> int:
        total = 0
        for msg in messages:
            total += self.token_manager.count_tokens(msg.get('message',''))
        return total

if __name__ == "__main__":
    print("🧪 Test del Context Manager")
    """
    messages = [
        {"role":"system","message":"Eres DevMentor, un asistente de código"},
        {"role":"user","message":"Qué es Python?"},
        {"role":"assistant","message":"Python es un lenguaje de programación..."},
        {"role":"user","message":"Cómo instali Python?"},
        {"role":"assistant","message":"Descarga Python desde python.org..."},
        {"role":"user","message":"Qué son las variables en Python?"},
        {"role":"assistant","message":"Las variables son contenedores para almacenar información..."},
        {"role":"user","message":"Explícame las funciones"},
        {"role":"assistant","message":"Las funciones son bloques de código que..."},
        {"role":"user","message":"Qué son las clases"},
        {"role":"assistant","message":"Las clases son plantillas para crear objetos..."},
    ]

    manager = ContextManager(strategy="sliding_window")
    """

    system_message = {
        "role":"system",
        "message":"Eres DevMentor AI, un asistente experto de desarrollo de software. Responde preguntas de programación de forma clara y CONCISA."
    }

    questions = [
        "¿Qué es Python?",
        "¿Cómo instalo Python?",
        "Qué son las variables?",
        "Explícame las funciones",
        "¿Qué son las clases?",
        "¿Cómo manejo errores?",
        "¿Cómo creo una función que calcule el factorial de un número?"
    ]
    llm_client = OllamaClient()
    messages = [system_message]
    for question in questions:
        generator = llm_client.generate_response(question, messages)
        messages.append({"role":"user", "message":question})
        response = ""
        for chunk in generator:
            if chunk:
                response += chunk
        print(question)
        messages.append({"role":"assistent", "message":response})

    print("="*80)

    manager = ContextManager(llm_client, "summary")

    print(f"Usando estrategia : {manager.strategy_name}")

    optimized, stats = manager.prepare_context(messages)

    print("📶 ESTADÍSTICAS DE OPTIMIZACION")
    print(f"  Estrategia: {manager.strategy_name}")
    print(f"  Mensajes: {stats['original_messages']} --> {stats['optimized_messages']}")
    print(f"  Tokens: {stats['original_tokens']} --> {stats['optimized_tokens']}")
    print(f"  Ahorro: {stats['tokens_saved']} tokens  ({stats['reduction_percent']:.1f}%)")
    print(f"  Coste: ${stats['original_cost']} --> ${stats['optimized_cost']}")
    print(f"  Ahorro: ${stats['cost_saved']}  ({stats['cost_reduction_percent']:.1f}%)")

    print("="*80)

    manager = ContextManager(llm_client, "smart")

    print(f"Usando estrategia : {manager.strategy_name}")

    optimized, stats = manager.prepare_context(messages)

    print("📶 ESTADÍSTICAS DE OPTIMIZACION")
    print(f"  Estrategia: {manager.strategy_name}")
    print(f"  Mensajes: {stats['original_messages']} --> {stats['optimized_messages']}")
    print(f"  Tokens: {stats['original_tokens']} --> {stats['optimized_tokens']}")
    print(f"  Ahorro: {stats['tokens_saved']} tokens  ({stats['reduction_percent']:.1f}%)")
    print(f"  Coste: ${stats['original_cost']} --> ${stats['optimized_cost']}")
    print(f"  Ahorro: ${stats['cost_saved']}  ({stats['cost_reduction_percent']:.1f}%)")
