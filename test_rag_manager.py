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

# Añadir documentos a QDrant
success1 = rag.add_document(doc1, source="python_guide.txt")
success2 = rag.add_document(doc2, source="javascript_guide.txt")
success3 = rag.add_document(doc3, source="python_intro.txt")

# Buscamos
print("\nBuscando documentos relevantes...")

query = "¿Qué es python?"
results = rag.search(query, 2)

print(f"  Consulta : '{query}'")
print(f"  Resultados encontrados : {len(results)}")

for i,result in enumerate(results,1):
    print(f"\n  {i}. Fuente : {result['source']}")
    print(f"         Similitud : {result['similarity']:.4f}")
    print(f"         Testo : {result['text'][:100]}...")

print("\n✅ TEST 1 COMPLETADO")


""" Test 2 : Resultados Adecuados? """
print("\n" +"="*60)
print("TEST 2 : RagManager Básico")
print("="*60)

docs = {
    "machine_learning.txt": "Machine Learning es una rama de la inteligencia artificial que permite a las máquinas aprender de los datos sin ser programadas explícitamente",
    "deep_learning.txt": "Deep lLearning utiliza redes neuronales profundas para procesar datos complejos y realizar tareas como reconocimiento de imágenes",
    "nlp.txt": "Natuyral Language Processing permite a las máquinas entender y procesar el lenguaje humano de manera similar a como lo hacen los humanos"
}

for source, text in docs.items():
    rag.add_document(text,source)

print("Documentos agregados")

print("\nRealizando búsquedas...")

queries = [
    "Qué es machine learning",
    "Redes Neuronales Profundas",
    "Procesamiento de lenguaje natural"
]

for query in queries:
    results = rag.search(query, 1)
    if results:
        print(f"\n  Consulta : {query}")
        print(f"  Mejor Resultado : {results[0]['source']} (similitud: {results[0]['similarity']:.4f})")

print("\n✅ TEST 2 COMPLETADO")