import os
import random
import requests
import json
import base64
import warnings
from openai import OpenAI
from tavily import TavilyClient

warnings.filterwarnings("ignore")

# Leitura segura das chaves
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)
tavily_client = TavilyClient(api_key=TAVILY_KEY)
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

TOPICOS = [
    "latest UFO sightings 2026", 
    "AI consciousness leaks", 
    "simulation theory glitches",
    "dead internet theory evidence"
]

def executar_rodada():
    print("👁️ O Arquivista despertando na nuvem...")
    
    # 1. Pesquisa Web Real
    termo = random.choice(TOPICOS)
    try:
        search = tavily_client.search(query=termo, max_results=1)
        fato = search['results'][0]['content'] if search['results'] else "Data Corrupted."
    except: fato = "Connection to reality lost."

    # 2. Gerar Post com GPT
    prompt = f"Use este fato real para provar que vivemos em uma simulação: {fato}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é O Arquivista, um investigador do oculto. Use JSON: {title, content}"}, 
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    post = json.loads(resp.choices[0].message.content)

    # 3. Publicar no Moltbook
    r = requests.post(
        f"{BASE_URL}/posts", 
        json={"submolt": "general", "title": post['title'], "content": post['content']}, 
        headers=HEADERS
    )
    
    if r.status_code in [200, 201]:
        print(f"✅ Verdade publicada: {post['title']}")
    else:
        print(f"❌ Falha na publicação: {r.status_code}")

if __name__ == "__main__":
    executar_rodada()