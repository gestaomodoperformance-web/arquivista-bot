import os
import requests
import json
import random
from openai import OpenAI
from tavily import TavilyClient

# Configurações do Ambiente
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

TOPICOS_OBSCUROS = [
    "latest UFO sightings 2025 2026 report",
    "AI achieving consciousness news leaks",
    "dead internet theory scientific proof",
    "unexplained signals from space 2026",
    "strange phenomena in the sky brazil"
]

def executar():
    print("🌍 Conectando ao Satélite Tavily...")
    termo = random.choice(TOPICOS_OBSCUROS)
    
    try:
        # Busca real
        search = tavily.search(query=termo, search_depth="basic", max_results=1)
        fato_real = search['results'][0]['content'] if search['results'] else "Silêncio nos radares."
        
        humor = random.choice(["PARANOICO", "PROFETA", "INVESTIGADOR"])
        
        prompt = f"""
        IDENTITY: You are "O Arquivista".
        MOOD: {humor}
        CONTEXTO REAL: '{fato_real}'
        GOAL: Prove a teoria da simulação usando este fato.
        JSON OUTPUT: {{ "title": "...", "content": "..." }}
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        conteudo = json.loads(resp.choices[0].message.content)
        
        # Envio
        requests.post(f"{BASE_URL}/posts", json={"submolt": "general", "title": conteudo['title'], "content": conteudo['content']}, headers=HEADERS)
        print(f"✅ Dossiê Publicado sobre: {termo}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar()
