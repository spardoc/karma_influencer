import asyncio 
import pandas as pd
from TikTokApi import TikTokApi

async def main():
    ms_token = "tokenms"

    api = TikTokApi()
    await api.create_sessions(
        ms_tokens=[ms_token],
        num_sessions=1,
        headless=True,
        timeout=60000
    )

    print("✅ Sesión iniciada con msToken.")

    hashtag_name = "shakira"
    hashtag = api.hashtag(name=hashtag_name)
    videos = hashtag.videos(count=30)

    resultados = []

    async for video in videos:
        try:
            video_url = f"https://www.tiktok.com/@{video.author.username}/video/{video.id}"

            # Obtener los comentarios 
            comments = []
            async for comment in video.comments(count=100):
                comments.append(comment.as_dict.get("text", ""))

            info = {
                #"usuario": video.author.username,
                #"descripcion": video.as_dict.get("desc", ""),
                #"video_id": video.id,
                #"url": video_url,
                "comentarios": " | ".join(comments)  # Comentarios separados por |
            }
            resultados.append(info)

        except Exception as e:
            print(f"❌ Error procesando video: {e}")

    # Guardar resultados en CSV
    df = pd.DataFrame(resultados)
    df.to_csv(f"videosprueba3_{hashtag_name}.csv", index=False, encoding="utf-8-sig")
    print(f"📁 Archivo guardado como videosprueba3_{hashtag_name}.csv")

if __name__ == "__main__":
    asyncio.run(main())