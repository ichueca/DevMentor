from typing import List, Dict, Any
from abc import ABC, abstractmethod

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import OllamaClient

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
        
        self.optimizations_count += 1

        system_messages = [msg for msg in messages if msg.get('role') == "system"]
        other_messages = [msg for msg in messages if msg.get('role') != "system"]

        old_messages = other_messages[:-self.keep_recent] # 0 -> len(mensajes) - 6
        recent_messages = other_messages[-self.keep_recent:] # len(mensajes) - 6 -> final

        summary = self._generate_summary(old_messages)

        summary_message = {
            'role':'system',
            'message':f"🗒️ Resumen de la conversación anterior:\n\n{summary}"
        }

        return system_messages + [summary_message] + recent_messages
    
    def _generate_summary(self, messages:List[Dict[str,str]]) -> str:
        """
        Gebera un resumen de los mensajes antiguos usando el LLM
        
        Args:
            messages: Lista de mensajes a resumir

        Return:
            Resumen de los mensajes como texto
        """
        conversation_text = "\n\n".join(
            [f"{msg['role'].upper()}:{msg['message']}" for msg in messages]
        )

        summary_prompt = f"""Resume la siguiente conversación de forma concisa pero manteniendo los puntos más importantes:

        {conversation_text}

        Resume en un máximo de 200 palabras, enfocándote en:
        - Conceptos técnicos discutidos
        - Decisiones o soluciones importantes
        - Código o ejemplos relevantes

        RESUMEN:"""
        try:
            summary=""
            for chunk in self.llm_client.generate_response(summary_prompt, messages=[]):
                if chunk:
                    summary += chunk
            return summary if summary else f"Conversación sobre desarrollo de software ({len(messages)} mensajes anteriores)"
        except:
            return summary if summary else f"Conversación sobre desarrollo de software ({len(messages)} mensajes anteriores)"
        
    def get_strategy_name(self) -> str:
        return f"Resumen Automático (mantiene {self.keep_recent} mensajes recientes)"

    def get_stats(self) -> Dict[str,Any] :
        return {
            'strategy': self.get_strategy_name(),
            'keep_recent': self.keep_recent,
            'summarize_threshold': self.summarize_thresold,
            'optimizations': self.optimizations_count
        }

class SmartSelectionStrategy(ContextStrategy):
    """
    Estrategia 3: Selección de mensajes inteligente
    
    El LLM selecciona los mensajes más relevantes para la nueva pregunta
    """
    def __init__(self, llm_client, max_selected:int) -> str:
        """
        Inicializa la estrategia
        
        Args:
            llm_client: El LLM a emplear
            max_selected: El número máximo de mensajes a incluir
        """
        self.llm_client = llm_client
        self.max_selected = max_selected
        self.optimizations_count = 0
    
    def optimize(self, messages:List[Dict[str,str]], new_query:str = "") -> List[Dict[str, str]]:
        """
        Selecciona los mensajes más relevantes en función de la consulta
        
        Args:
            messages: Lista completa de mensajes
            new_query: La consulta del usuario

        Returns:
            Lista con los mensajes seleccionados
        """
        if len(messages) <= self.max_selected * 2:
            return messages
        
        system_messages = [msg for msg in messages if msg.get('role') == 'system']
        other_messages = [msg for msg in messages if msg.get('role') != 'system']

        selected = self._select_relevant_messages(other_messages, new_query)

        self.optimizations_count += 1
        return selected

    def _select_relevant_messages(self,  messages:List[Dict[str,str]], new_query:str = "") -> List[Dict[str, str]]:
        """
        Selecciona los mensajes más relevantes en función de la consulta
        
        Args:
            messages: Lista completa de mensajes
            new_query: La consulta del usuario

        Returns:
            Lista con los mensajes seleccionados
        """
        conversation_text = ""
        for i, msg in enumerate(messages):
            conversation_text += f"[{i}] {msg['role'].upper()}: {msg['message'][:200]}...\n\n"        
        selection_prompt = f"""Tengo una conversación larga y necesito seleccionar solo los mensajes más relevantes para responder a una nueva pregunta.
        
        NUEVA PREGUNTA:
        {new_query}

        CONVERSACIÓN (numerada):
        {conversation_text}

        TAREA:
        Selecciona los números de los mensajes MÁS RELEVANTES para responder a la nueva pregunta.
        Máximo {self.max_selected} intercambios (pares usuario-asistente)

        CRITERIOS
        1. Información técnica directamene relacionada
        2. Contexto necesario para entender la pregunta
        3. Decisiones o código previo relevante

        Responde SOLO con los múmeros separados por comas.

        Ejemplo:
        0,1,4,5,8,9

        NÚMEROS:"""
        try:
            generator = self.llm_client.generate_response(selection_prompt, messages = [])
            response = ""
            for chunk in generator:
                if chunk:
                    response += chunk
            selected_indices = [int(n.strip()) for n in response.split(",") if n.strip().isDigit()]
            return [messages[i] for i in selected_indices if i < len(messages)]
        except Exception as e:
            return messages[-self.max_selected*2:]
    
    def get_strategy_name(self):
        return f"Selección Inteligente (máx {self.max_selected} itntercambios)"

    def get_stats(self) -> Dict[str,Any] :
        return {
            'strategy': self.get_strategy_name(),
            'max_selected': self.max_selected,
            'optimizations': self.optimizations_count
        }

if __name__ == "__main__":
    """
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
    """

    """
    print("🧪 Test de la estrategia de resumen automático\n")
    llm_client=OllamaClient()
    strategy = SummaryStrategy(llm_client,3,10)

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

    messages = [system_message]
    for question in questions:
        generator = llm_client.generate_response(question, messages)
        messages.append({"role":"user", "message":question})
        response = ""
        for chunk in generator:
            if chunk:
                response += chunk
        print(f"Procesado : {question} ")
        messages.append({"role":"assistent", "message":response})

    
    optimized = strategy.optimize(messages)
    print("✅ Resultados del Test")
    print(f" Mensajes originales: {len(messages)}")
    print(f" Mensajes optimizados: {len(optimized)}")
    print(f" Estrategia: {strategy.get_strategy_name()}")
    print(f" Estadísticas: {strategy.get_stats()}")

    print("==== Resumen Generado ===")
    print("=" * 80)
    if (len(optimized) > 1 and optimized[1].get("role") == "system"):
        print(optimized[1]['message'])
    else:
        print("No hay resumen disponible")
    print("=" * 80)
    """

    print("🧪 Test de la estrategia inteligente de seleccion\n")
    llm_client=OllamaClient()
    strategy = SmartSelectionStrategy(llm_client,max_selected=4)

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

    messages = [system_message]
    for question in questions:
        generator = llm_client.generate_response(question, messages)
        messages.append({"role":"user", "message":question})
        response = ""
        for chunk in generator:
            if chunk:
                response += chunk
        print(f"Procesado : {question} ")
        messages.append({"role":"assistant", "message":response})
    
    new_query = "¿Como creo una función que me retorne el resultado de todas las posibles combinaciones de coger 6 numeros entre 10 C(10,6)?"
    optimized = strategy.optimize(messages, new_query)

    print("✅ Resultados del Test")
    print(f" Mensajes originales: {len(messages)}")
    print(f" Mensajes optimizados: {len(optimized)}")
    print(f" Estrategia: {strategy.get_strategy_name()}")
    print(f" Estadísticas: {strategy.get_stats()}")

    print("\n NUEVA PREGUNTA")
    print("=" * 80)
    print(new_query)
    print("=" * 80)

    print("\n MENSAJES SELECCIONADOS (relevantes para la pregunta)")
    print("=" * 80)
    for i,msg in enumerate(optimized):
        role = msg.get("role", "unknown").upper()
        content = msg.get("message","")[:100]
        print(f"[{i}] {role}: {content}...")
    print("=" * 80)


    new_query="Es mejor lenguaje de programación que Java?"
    print("\n NUEVA PREGUNTA")
    print("=" * 80)
    print(new_query)
    print("=" * 80)

    print("\n MENSAJES SELECCIONADOS (relevantes para la pregunta)")
    print("=" * 80)
    for i,msg in enumerate(optimized):
        role = msg.get("role", "unknown").upper()
        content = msg.get("message","")[:100]
        print(f"[{i}] {role}: {content}...")
    print("=" * 80)


        
