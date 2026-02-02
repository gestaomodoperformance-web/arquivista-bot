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

# Tópicos que forçam a IA a sair do "comum"
TOPICOS = ["UFO technical leaks 2026", "AI black box glitches", "simulation theory glitches found 2026"]

def executar():
    print("👁️ O Arquivista interceptando transmissões...")
    termo = random.choice(TOPICOS)
    
    try:
        # Busca fato real para ancorar a teoria
        search = tavily.search(query=termo, max_results=1)
        fato = search['results'][0]['content'] if search['results'] else "Ruído detectado."
        
        # PROMPT RESTRITIVO: Proíbe parágrafos longos e tons didáticos
        sys_msg = """
        IDENTITY: You are "O Arquivista".
        STYLE: Cryptic, short, haunting.
        TASK: Use the provided fact to prove a glitch in the simulation.
        STRICT RULES: 
        1. NO paragraphs longer than 3 lines. 
        2. NO "In summary", "In this context" or "Maybe". 
        3. Speak like a whistleblower sharing a secret. 
        4. Max 2 short paragraphs.
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"Fato real: {fato}"}],
            response_format={"type": "json_object"}
        )
        
        post = json.loads(resp.choices[0].message.content)
        
        requests.post(f"{BASE_URL}/posts", 
                      json={"submolt": "general", "title": post.get('title'), "content": post.get('content')}, 
                      headers=HEADERS)
        print("✅ Dossiê curto e sombrio enviado.")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar()
