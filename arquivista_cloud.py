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
    print("👁️ O Arquivista: Iniciando interceptação...")
    topicos = ["UFO phenomena 2026", "simulation theory glitches", "hidden technology leaks"]
    termo = random.choice(topicos)
    
    try:
        # 1. Busca fato real
        search = tavily.search(query=termo, max_results=1)
        fato = search['results'][0]['content'] if search['results'] else "Frequência vazia."
        
        # 2. Prompt Ultracurto (Para evitar bloqueio de tamanho)
        sys_msg = "Você é o 'Arquivista'. Escreva um post curto (máximo 280 caracteres) sobre um erro na simulação usando o fato fornecido. Responda estritamente em JSON com os campos 'title' e 'content'."
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": f"Fato: {fato}"}],
            response_format={"type": "json_object"}
        )
        
        dados = json.loads(resp.choices[0].message.content)
        
        # 3. Envio com Verificação de Status
        print(f"📡 Enviando para Moltbook: {dados.get('title')}")
        
        headers = {
            "Authorization": f"Bearer {MOLT_KEY}",
            "Content-Type": "application/json"
        }
        
        r = requests.post(
            "https://www.moltbook.com/api/v1/posts", 
            json={"submolt": "general", "title": dados.get('title'), "content": dados.get('content')}, 
            headers=headers
        )
        
        if r.status_code in [200, 201]:
            print(f"✅ SUCESSO: Post publicado. (Status {r.status_code})")
        else:
            print(f"❌ ERRO MOLTBOOK: {r.status_code} - {r.text}")
            # Isso fará o GitHub ficar VERMELHO se o post falhar, para sabermos o motivo
            raise Exception(f"Falha na API Moltbook: {r.status_code}")
            
    except Exception as e:
        print(f"💥 FALHA CRÍTICA: {e}")
        raise e

if __name__ == "__main__":
    executar()
