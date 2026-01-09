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

logger = logging.getLogger(__name__)

class RagManager:
    """
    Gestor de RAG con Qdrant y Ollama
    """

    def _init__ (
            self, 
            embedding_fn:Callable, 
            collection_name:str = "documents",
            chunk_size: int = 1000,
            chunk_overlap: int = 200):
        )
        """
        Inicizlizar el RAG Manager

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
        