from typing import List, Dict, Any
from abc import ABC, abstractmethod

class ContextStrategy(ABC):
    """ Clase abstracta para estrategias de optimización de contexto """

    @abstractmethod
    def optimize(self, messages: List[Dict[str,str]], new_query: str = "") -> List[Dict[str,str]]:
        """
        Optimiza el contexto de mensajes

        Args:
            messges: Lista de mensajes de la conversación
            new_query: Nueva pregunta del usuario

        Returns:
            Lista optimizada de mensajes
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """ Retorna el nombre de la estrategia """
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """ Retorna estadísticas de la estrategia"""
        pass

class SlidingWindowStrategy(ContextStrategy):
    """
    Estrategia 1 : Ventana Deslizante (la más simple y barata)

    Mantiene sólo los últimos N mensajes de la conversación
    """

    def __init__(self, max_messages:int = 10):
        """
        Inicializa la estrategia de ventana deslizante

        Args:
            max_messages: Número máximo de mensajes a mantener
        """
        self.max_messages = max_messages
        self.optimizations_count = 0
        self.total_messages_kept = 0

    def get_strategy_name(self) -> str:
        """ Retorna el nombre de la estrategia """
        return f"Ventana Deslizante ({self.max_messages} mensajes)"
    
    def optimize(self, messages: List[Dict[str,str]], new_query: str = "") -> List[Dict[str,str]]:
        """
        Mantiene los últimos N mensajes

        Args:
            messges: Lista de mensajes de la conversación
            new_query: Nueva pregunta del usuario

        Returns:
            Lista con los ultimos N mensajes
        """
        if len(messages) <= self.max_messages:
            return messages
        
        # Nos quedamos con los mensajes del sistema
        system_messages = [msg for msg in messages if msg.get('role') == "system"]
        other_messages = [msg for msg in messages if msg.get('role') != "system"]

        # Mantenemos los últimos N mensajes
        recent_messages = other_messages[-self.max_messages:]

        self.optimizations_count += 1
        self.total_messages_kept += len(recent_messages)

        return system_messages + recent_messages

    def get_stats(self) -> Dict[str, Any]:
        """ Retorna estadísticas de la estrategia"""
        avg_kept = self.total_messages_kept / max(1, self.optimizations_count)
        return {
            'strategy': self.get_strategy_name(),
            'max_messages': self.max_messages,
            'optimizations_count': self.optimizations_count,
            'average_messages_kept': avg_kept
        }
    
    
class SummaryStrategy(ContextStrategy):
    """
    Estrategia 2: Resumen automático

    Resume mensajes antigüos usando el LLM
    """

    def __init__(self, llm_client, keep_recent: int = 6, summarize_thresold: int = 15):
        """
        Inicializa la estrategia

        Args:
            llm_client: Cliente LLM para generar el resumen
            keep_recent: Últimos mensajes a mantener sin resumir
            summarize_thresold: Umbral de mensajes para activar el resumen
        """
        self.llm_client = llm_client
        self.keep_recent = keep_recent
        self.summarize_thresold = summarize_thresold
        self.optimizations_count = 0

    def get_strategy_name(self) -> str:
        """ Retorna el nombre de la estrategia """
        return f"Resúmen Automático (mantiene los últimos {self.keep_recent} mensajes sin resumir)"
    
    def optimize(self, messages: List[Dict[str,str]], new_query: str = "") -> List[Dict[str,str]]:
        """
        Resume mensajes antigüos y mantiene los últimos

        Args:
            messges: Lista de mensajes de la conversación
            new_query: Nueva pregunta del usuario

        Returns:
            Lista con el resúmen + mensajes recientes
        """
        if len(messages) <= self.summarize_thresold:
            return messages
        
        system_messages = [msg for msg in messages if msg.get('role') == "system"]
        other_messages = [msg for msg in messages if msg.get('role') != "system"]

        old_messages = other_messages[:-self.keep_recent]
        recent_messages = other_messages[-self.keep_recent:]

        summary = self._generate_summary(old_messages)

        summary_message = {
            'role':'system',
            'message':f"🗒️ Resumen de la conversación anterior:\n\n{summary}"
        }

        return system_messages + [summary_message] + recent_messages

if __name__ == "__main__":
    print("🧪 Test de la estrategia de ventana deslizante\n")
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
    stategy = SlidingWindowStrategy(max_messages=6)
    optimized = stategy.optimize(messages=messages)
    print("✅ Resultados del Test")
    print(f" Mensajes originales: {len(messages)}")
    print(f" Mensajes optimizados: {len(optimized)}")
    print(f" Estrategia: {stategy.get_strategy_name()}")
    print(f" Estadísticas: {stategy.get_stats()}")
    print("==== Mensajes Optimizados ===")
    for msg in optimized:
        print(msg)

