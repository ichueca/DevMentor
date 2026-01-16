"""
RAG Manager - Gestor de RAG

Usa Qdrant como Vector Database y Ollama para embeddings
"""

import uuid
from typing import List, Dict, Callable
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import numpy as np

def ollama_embedding_fn(text:str, model:str = "mxbai-embed-large") -> list:
    """ Genera embeddings usando Ollama """
    response = ollama.embeddings(model, prompt=text)
    return np.array(response['embedding'])

logger = logging.getLogger(__name__)

class RagManager:
    """
    Gestor de RAG con Qdrant y Ollama
    """

    def __init__ (
            self, 
            embedding_fn:Callable = ollama_embedding_fn, 
            collection_name:str = "documents",
            chunk_size: int = 1000,
            chunk_overlap: int = 200
        ):
        """
        Inicializar el RAG Manager

        Args:
            embedding_fn: Función para generar embeddings (Ollama API)
            collection_name: Nombre de la colección en Qdrant
            chunk_size: Tamaño de cada chunk en caracteres
            chunk_overlap: Solapamiento entre chunks
        """
        self.embedding_fn = embedding_fn
        self.collection_name = collection_name

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        self.client = QdrantClient(":memory:") 
    
    def _ensure_collection_exists(self, vector_size:int):
        """ Crear la colección si no existe """
        if not self.collection_created:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            self.collection_created = True
    
    def add_document(self, text:str, source:str = "custom") -> bool:
        """
        Agrega un documento al RAG

        El documento se divide automáticamente en chunks usando
        RecursiveCharacterTextSplitter. 
        Cada chunk se almacena como un punto separado en Qdrant

        Args:
            text: Contenido del documento
            source: Nombre/origen del documento

        Returns:
            True si se agregó correctamente 
        """
        try:
            # Dividir el documento en chunks
            chunks = self.text_splitter.split_text(text)

            if not chunks:
                logger.warning(f"No se han generado chunks para {source}")
                return False
            
            logger.info(f"Documento {source} dividido en {len(chunks)} chunks")

            points = []
            for chunk_idx, chunk in enumerate(chunks):
                # Generamos el embedding del chunk
                embedding = self.embedding_fn(chunk)

                if not embedding:
                    continue

                # Creamos un PointStruct de Qdrant
                point_id = int(uuid.uuid4().int % (2**63))

                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text":chunk,
                        "source":source,
                        "chunk_index":chunk_idx,
                        "total_chunks": len(chunks)
                    }
                )
                points.append(point)
            
            if not points:
                logger.error(f"No se han creado puntos para {source}")
                return False

            self._ensure_collection_exists(len(points[0].vector))

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Documento agregado: {source} ({len(points)} chunks)")

            return True
        except Exception as e:
            logger.error(f"Error agregando documento: {e}")
        
    def search(self, query:str, top_k:int = 3) -> List[Dict]:
        """
        Bucar los top_k chunks más similares a la consulta

        Args:
            query: La consulta del usuario
            top_k: EL número de chunks a retornar

        Returns:
            Lista de chunks ordenada por relevancia
        """
        try:
            if not self.collection_created:
                return []
            
            # Geneamos los embeddings de la consulta
            query_embedding = self.embedding_fn(query)

            # Verificamos que sea válido
            if query_embedding is None or len(query_embedding) == 0:
                logger.warning("NO se pudo generar embedding para la pregunta")
                return []
            
            # Buscar en Qdrant
            results = self.client.query_points(
                self.collection_name,
                query=query_embedding,
                limit=top_k,
                with_payload=True
            )

            chunks = []
            for result in results.points:
                chunks.append({
                    "text":result.payload["text"],
                    "source":result.payload["source"],
                    "chunk_index":result.payload["chunk_index"],
                    "total_chunks":result.payload["total_chunks"],
                    "similarity":result.score
                })
            return chunks
        except Exception as e:
            logger.error(f"Error buscando documentos: {e}")
            return []
    
    def clear(self) -> bool:
        """ Limpiar todos los documentos """
        try:
            self.client.delete_collection(self.collection_name)
            self.collection_created = False
            return True
        except Exception as e:
            logger.error(f"Error limpiando: {e}")
            return False
        