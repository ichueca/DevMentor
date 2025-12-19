from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class ConversationStorage(ABC):
    """ Clase base para guardar / cargar conversaciones """

    @abstractmethod
    def save_conversation(self, conversation_id:str, name:str, messages: List[Dict]) -> bool:
        """ Guarda una conversación """
        pass

    @abstractmethod
    def load_conversation(self, conversation_id: str) -> Optional[Dict]:
        """ Carga una conversación """
        pass

    @abstractmethod
    def list_conversations(self) -> List[Dict]:
        """ Retorna una lista con todas las conversaciones """
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> bool:
        """ Elimina una conversación """
        pass

    @abstractmethod
    def update_conversation(self, conversation_id: str, messages:List[Dict]) -> bool:
        """ Actualiza una conversación existente """
        pass