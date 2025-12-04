#from utils.api_client import GeminiClient
from utils import OpenAIClient,OllamaClient, PromptService, PromptType
from dotenv import load_dotenv

load_dotenv()

"""
llm_client = OpenAIClient()

prompt_service = PromptService(llm_Client=llm_client)

test_cases = [
    ("¿Qué es Python?", PromptType.EXPLANATION),
    ("Revisa este código", PromptType.CODE_REVIEW),
    ("Tengo un error en mi código", PromptType.DEBUGGING),
    ("Cuáles son las mejores prácticas?", PromptType.BEST_PRACTICES),
    ("Hola ¿como estás?", PromptType.GENERAL),
]

print("Probando la clasificación")
correct = 0

for input_text, expected in test_cases:
    detected = prompt_service.detect_prompt_type(input_text)
    status = "✅" if detected == expected else "❌"
    if detected == expected:
        correct += 1
    print(f"   {status} '{input_text}' -> {detected.value} (esperado: {expected.value})")

print(f"📶 Precisión: {correct} / {len(test_cases)} ({100*correct // len(test_cases)}%)")

"""
llm_client = OllamaClient()
response_generator = llm_client.generate_response("hola", {})
response = ""
for chunk in response_generator:
    if chunk:
        response += chunk

print(f"Respuesta del análisis : {response}")