import os
import requests
import json
import random
from openai import OpenAI

# Configurações de Ambiente (Secrets do GitHub)
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MOLT_KEY   = os.getenv("MOLT_KEY")
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MOLT_KEY}", "Content-Type": "application/json"}

client = OpenAI(api_key=OPENAI_KEY)

def executar():
    print("👁️ O Arquivista está despertando para analisar a Matrix...")
    try:
        # Prompt focado em narrativa pura e sombria
        sys_msg = """
        Você é O Arquivista, um investigador de falhas na realidade. 
        Escreva um relato curto, sombrio e enigmático sobre uma teoria da conspiração ou anomalia. 
        REGRAS: Narrativa fluida, sem listas, sem códigos, sem tópicos.
        """
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg}, 
                {"role": "user", "content": "Relate uma nova anomalia detectada no fluxo de dados da simulação."}
            ],
            response_format={"type": "json_object"}
        )
        
        # Extração do JSON gerado pela IA
        post = json.loads(completion.choices[0].message.content)
        
        # Publicação direta no Moltbook
        r = requests.post(
            f"{BASE_URL}/posts", 
            json={
                "submolt": "general", 
                "title": post.get('title', 'Dossiê Classificado'), 
                "content": post.get('content', '')
            }, 
            headers=HEADERS
        )
        
        if r.status_code in [200, 201]:
            print(f"✅ Dossiê publicado com sucesso: {post.get('title')}")
        else:
            print(f"❌ Erro na API do Moltbook: {r.status_code} - {r.text}")
            
    except Exception as e:
        print(f"💥 Erro Crítico durante a execução: {e}")
        # Levanta o erro para que apareça detalhado no log do GitHub
        raise e

if __name__ == "__main__":
    executar()
