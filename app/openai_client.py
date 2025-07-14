import os
import openai

from flask import current_app

class OpenAIClient:
    def __init__(self):
        openai.api_key = current_app.config['OPENAI_API_KEY']

    def analyze_sentiment(self, text):
        prompt = f"Clasifica el sentimiento de este texto: '{text}' como positivo, negativo o neutral, y devuelve un JSON con 'sentiment' y 'score' (entre -1 y 1)."
        resp = openai.ChatCompletion.create(
            model='gpt-4', messages=[{'role':'user','content':prompt}],
            temperature=0
        )
        # Asumimos que la respuesta está en contenido JSON
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
            return data['sentiment'], data['score']
        except Exception:
            # fallback neutral
            return 'neutral', 0.0