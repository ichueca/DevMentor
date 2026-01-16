import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils import RagManager

""" Test 1 : RAG Manager """
print("\n" +"="*60)
print("TEST 1 : RagManager Básico")
print("="*60)

rag = RagManager()

print("\nAgregando documentos...")

doc1 = "Python es un lenguaje de programación versátil y poderoso. Se usa en ciencia de datos, inteligencia artificial, desarrollo web y automatización"
doc2 = "Javascript es el lenguaje de la web. Se ejecuta en navegadores y servidores (Node.js)"
doc3 = "Python tiene una sintaxis legible y simple, lo que lo hace ideal para principiantes"
