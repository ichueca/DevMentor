import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))
from datetime import datetime
from typing import List, Dict, Optional
from utils.conversation_storage import ConversationStorage


class JSONStorage(ConversationStorage):
    """ Almacenamiento basado en archivos JSON """


    def __init__(self, storage_dir: str = "conversations"):
        """ Inicializa el almacenamiento JSON """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def save_conversation(self, conversation_id, name, messages):
        """
        Guarda una conversación en un archivo JSON

        Args:
            conversation_id: El id de la conversación
            name: Un nombre significativo
            messages: La lista de mensajes
        
        Returns:
            True si la conversación se ha guardado correctamente
        """

        try:
            data = {
                "id": conversation_id,
                "name": name,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "messages": messages
            }

            filepath = self.storage_dir / f"{conversation_id}.json"
            with open(filepath, 'w', encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"❌ Error al guardar la conversación : {e}")
            return False

    def load_conversation(self, conversation_id):
        """
        Carga una conversación desde un archivo JSON

        Args:
            conversation_id: El identificador de la conversación

        Returns:
            Un Optional con los datos de la conversación
        """
        try:
            filepath = self.storage_dir / f"{conversation_id}.json"
            with open(filepath, 'r', encoding="UTF-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error al cargar la conversación : {e}")
            return None  

    def list_conversations(self):
        """
        Retorna todas las conversaciones guardadas

        Returns:
            La lista de conversaciones

            [
              {"id":"...", "name":"...","created_at":fecha, "updated_at":fecha, "message_count":nn}
            ]
        """

        conversations = []
        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath,"r", encoding="UTF-8") as f:
                    data = json.load(f)
                    conversations.append({
                        "id": data["id"],
                        "name": data["name"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "message_count": len(data["messages"])
                    })
            except Exception as e:
                print(f"⚠️ Error leyendo {filepath} : {e}")
        
        return sorted(conversations, key=lambda x: x["updated_at"], reverse=True)

    def delete_conversation(self, conversation_id):
        """
        Elimina una conversación en base al id

        Args:
            conversation_id: El id de la conversación a eliminar

        Returns:
            True si la eliminación ha tenido éxito
        """
        try:
            filepath = self.storage_dir / f"{conversation_id}.json"
            if filepath.exists():
                filepath.unlink()
                return True 
            else:
                return False
        except Exception as e:
            print(f"❌ Error eliminando {filepath} : {e}")
            return False

    def update_conversation(self, conversation_id, messages):
        """
        Actualiza la conversación

        Args:
            conversation_id: El id de la conversación a actualizar
            messages: Los mensajes
        
        Returns:
            True si la actualización ha tenido éxito
        """

        try:
            filepath = self.storage_dir / f"{conversation_id}.json"
            if not filepath.exists():
                return False

            with open(filepath, 'r', encoding="UTF-8") as f:
                data = json.load(f)
            
            data["updated_at"] = datetime.now().isoformat()
            data["messages"] = messages

            with open(filepath, 'w', encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True    
        except Exception as e:
            print(f"❌ Error actualizando conversación con id {conversation_id}: {e}")
            return False

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))
    print("🧪 Test de almacenamiento JSON\n")
    print("=" * 80)
    messages = [
        {"role":"system","message":"Eres DevMentor, un asistente de código"},
        {"role":"user","message":"Qué es Python?"},
        {"role":"assistant","message":"Python es un lenguaje de programación..."},
        {"role":"user","message":"Cómo instali Python?"},
        {"role":"assistant","message":"Descarga Python desde python.org..."},
    ]

    print("1️⃣. Inicializando almacenamiento JSON")
    storage = JSONStorage(storage_dir="test_conversations")

    print("2️⃣Guardar la conversación")
    success = storage.save_conversation(
        conversation_id="conv_001",
        name="Primera Conversación",
        messages=messages
    )
    print(f"✅ Éxito" if success else "❌ error")

    messages= [
        {"role":"user","message":"Qué son las variables en Python?"},
        {"role":"assistant","message":"Las variables son contenedores para almacenar información..."},
        {"role":"user","message":"Explícame las funciones"},
        {"role":"assistant","message":"Las funciones son bloques de código que..."},
        {"role":"user","message":"Qué son las clases"},
        {"role":"assistant","message":"Las clases son plantillas para crear objetos..."},
    ]
    
    print("3️⃣ Guardar Otra Conversación")
    success = storage.save_conversation(
        conversation_id="conv_002",
        name="Segunda Conversación",
        messages=messages
    )
    print(f"✅ Éxito" if success else "❌ error")

    print("4️⃣. Listar Conversaciones")
    conversations = storage.list_conversations()
    print(f"    Total: {len(conversations)} conversaciones")
    for conv in conversations:
        print(f"    - {conv["name"]} ({conv["message_count"]} mensajes)")
    
    print("5️. Actualizar Conversación")
    loaded = storage.load_conversation("conv_002")
    if loaded:
        loaded["messages"].append({
            "role":"user",
            "message":"¿Cómo creo una función?"}
        )
        loaded["messages"].append({
            "role":"assistant",
            "message":"Usa la palabra clave 'def' ..."}
        )

        success = storage.update_conversation("conv_002", loaded["messages"])
        print(f"✅ Éxito" if success else "❌ error")

        if success:
            updated = storage.load_conversation("conv_002")
            print(f"  Tras actualizar : {len(updated["messages"])} mensajes.")
    
    print("6️⃣. Eliminar Conversación")
    success = storage.delete_conversation("conv_001")
    print(f"✅ Éxito" if success else "❌ error")

    print("\nEn la carpeta 'test_conversations debería estar 'conv_002.json'")