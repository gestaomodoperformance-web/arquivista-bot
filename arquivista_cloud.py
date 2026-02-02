import os
import requests
import json
import random
from openai import OpenAI
from tavily import TavilyClient

# Configurações
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

def executar():
    print("👁️ O Arquivista interceptando transmissões...")
    topicos = ["UFO technical leaks 2026", "AI black box glitches", "simulation theory evidence 2026"]
    termo = random.choice(topicos)
    
    try:
        # Busca fato real
        search = tavily.search(query=termo, max_results=1)
        fato = search['results'][0]['content'] if search['results'] else "Ruído detectado."
        
        # PROMPT COM A PALAVRA MÁGICA 'JSON'
        sys_msg = """
        IDENTITY: You are "O Arquivista".
        STYLE: Cryptic, short, haunting. Max 2 short paragraphs.
        TASK: Use the provided fact to prove a glitch in the simulation.
        STRICT RULES: 
        1. Respond strictly in JSON format.
        2. NO paragraphs longer than 3 lines. 
        3. NO "In summary" or filler text.
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"Fato real: {fato}"}],
            response_format={"type": "json_object"}
        )
        
        post = json.loads(resp.choices[0].message.content)
        
        requests.post("https://www.moltbook.com/api/v1/posts", 
                      json={"submolt": "general", "title": post.get('title'), "content": post.get('content')}, 
                      headers={"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"})
        print("✅ Dossiê enviado com sucesso.")
        
    except Exception as e:
        print(f"Erro: {e}")
        raise e

if __name__ == "__main__":
    executar()
