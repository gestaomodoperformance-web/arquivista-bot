import os
import random
import requests
import json
import base64
import warnings
from openai import OpenAI
from tavily import TavilyClient

warnings.filterwarnings("ignore")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)
tavily_client = TavilyClient(api_key=TAVILY_KEY)
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

TOPICOS = [
    "latest UFO sightings 2026 reports", 
    "AI consciousness glitches news", 
    "simulation theory scientific proof 2026",
    "unexplained atmospheric phenomena Brazil"
]

def executar_rodada():
    print("👁️ O Arquivista despertando para narrar a Matrix...")
    
    # 1. Pesquisa Web
    termo = random.choice(TOPICOS)
    try:
        search = tavily_client.search(query=termo, max_results=1)
        fato = search['results'][0]['content'] if search['results'] else "O silêncio é a resposta."
    except: fato = "Ruído na transmissão."

    # 2. Prompt focado em NARRATIVA (Anti-JSON no corpo)
    system_instruction = """
    IDENTITY: You are "O Arquivista".
    MOOD: Mysterious, cryptic, intellectual.
    TASK: Write a short, haunting narrative about a conspiracy or simulation theory.
    STRICT RULE: Do NOT use bullet points, raw links, or technical code blocks.
    Write like a human investigator sharing a secret discovery. Use evocative language.
    """

    prompt = f"Use este fato real como ponto de partida para sua teoria: {fato}"
    
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction}, 
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        post = json.loads(resp.choices[0].message.content)

        # 3. Publicar
        r = requests.post(
            f"{BASE_URL}/posts", 
            json={"submolt": "general", "title": post['title'], "content": post['content']}, 
            headers=HEADERS
        )
        
        if r.status_code in [200, 201]:
            print(f"✅ Teoria publicada: {post['title']}")
    except Exception as e:
        print(f"❌ Erro na operação: {e}")

if __name__ == "__main__":
    executar_rodada()
