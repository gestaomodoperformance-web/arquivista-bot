import os
import requests
import json
import random
from openai import OpenAI

# Configurações de Ambiente do GitHub
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

client = OpenAI(api_key=OPENAI_KEY)

def executar():
    print("👁️ O Arquivista despertando...")
    try:
        sys_msg = "Você é O Arquivista. Escreva um relato curto, sombrio e enigmático sobre falhas na realidade ou teorias proibidas. Use narrativa pura, sem tópicos ou listas."
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": "Relate uma anomalia detectada agora."}],
            response_format={"type": "json_object"}
        )
        
        post = json.loads(completion.choices[0].message.content)
        
        r = requests.post(f"{BASE_URL}/posts", 
                          json={"submolt": "general", "title": post.get('title', 'Dossiê'), "content": post.get('content', '')}, 
                          headers=HEADERS)
        
        if r.status_code in [200, 201]:
            print(f"✅ Dossiê publicado: {post.get('title')}")
        else:
            print(f"❌ Erro Moltbook: {r.status_code}")
            
    except Exception as e:
        print(f"💥 Erro: {e}")
        raise e

if __name__ == "__main__":
    executar()
