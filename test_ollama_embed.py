"""
Script para validar el funcionamiento de los embeddings de Ollama
"""

import ollama
import numpy as np
from numpy.linalg import norm

MODELO =  "mxbai-embed-large" #"all-minilm" 

def get_embedding(texto):
    response = ollama.embeddings(model=MODELO, prompt=texto)
    return np.array(response['embedding'])

def similitud_coseno(v1, v2):
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

print("--- 1. Identidad semántica (buscar frases que signifiquen lo mismo o parecios) ---")
frases = [
    "El sistema de salud, los hospitales, está colapsado por la pandemia",
    "Los hospitales no dan abasto debido a la crisis sanitaria",
    "El sistema operativo se colgó al instalar la actualización"
]
emb_pandemia = get_embedding(frases[0])
emb_hospital = get_embedding(frases[1])
emb_so = get_embedding(frases[2])

print(f"Similitud Pandemia-Hospital (Mismo dominio): {similitud_coseno(emb_pandemia, emb_hospital):.4f}")
print(f"Similitud Pandemia-SO (Distinto dominio alguna palabra igual): {similitud_coseno(emb_pandemia, emb_so):.4f}")

print("\n-- 2. Desambiguación por contexto ---")
frases = [
    "Fui al banco a pedir un préstamo personal",
    "Me senté en el banco del parque a leer un libro",
    "La entidad financiera aprobó mi crédito en la oficina"
]

emb_banco = get_embedding(frases[0])
emb_parque = get_embedding(frases[1])
emb_credito = get_embedding(frases[2])

print(f"Similitud Banco-Parque (Misma palabra contexto distinto): {similitud_coseno(emb_banco, emb_parque):.4f}")
print(f"Similitud Banco-Credito (Sin palabras en común mismo dominio): {similitud_coseno(emb_banco, emb_credito):.4f}")

print("\n-- 3. Aritmética de Frases ---")
frases = [
    "El servicio de hoy fué excelente y la comida deliciosa",
    "Excelente Delicioso",
    "Horrible Terrible"
]

resultado = get_embedding(frases[0]) - get_embedding(frases[1]) + get_embedding(frases[2])

print(f"La comida fue horrible: {similitud_coseno(resultado, get_embedding("La comida fue horrible")):.4f}")
print(f"La comida fue excelente: {similitud_coseno(resultado, get_embedding("La comida fue excelente")):.4f}")
