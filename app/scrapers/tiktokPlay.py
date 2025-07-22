from playwright.sync_api import sync_playwright
import pandas as pd
import time

def get_user_input():
    """Obtiene todos los parámetros necesarios antes de abrir el navegador"""
    print("═══════════════════════════════════════")
    print("   SCRAPER DE COMENTARIOS DE TIKTOK   ")
    print("═══════════════════════════════════════\n")
    
    query = input("🔍 ¿Qué hashtag  quieres buscar? (ej: shakira ): ").strip()
    num_videos = int(input("📽️ ¿Cuántos videos quieres procesar?: "))
    
    print("\n⚠️ IMPORTANTE: Una vez se abra el navegador:")
    print("- Inicia sesión manualmente si es necesario")
    print("- Espera a que cargue completamente la página")
    print("- NO interactúes con el navegador durante el scraping\n")
    input("Presiona ENTER para comenzar el scraping...")
    
    return query, num_videos

def scrape_comments():
    # Obtener parámetros antes de abrir el navegador
    query, num_videos = get_user_input()
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=False,
            viewport={"width": 1200, "height": 800}
        )

        page = browser.new_page()
        
        # Determinar si es un hashtag o perfil
        if query.startswith("@"):
            url = f"https://www.tiktok.com/{query}"
        else:
            url = f"https://www.tiktok.com/tag/{query}"

        print(f"\n🚀 Abriendo {url}...")
        page.goto(url, timeout=60000)
        time.sleep(3)

        # Esperar a que aparezcan los videos
        page.wait_for_selector('div[data-e2e="challenge-item-list"]', timeout=20000)
        
        # Localizar todos los videos visibles
        videos = page.locator('div[id="column-item-video-container"]')
        total_videos = min(videos.count(), num_videos)
        
        all_comments = []
        
        for video_idx in range(total_videos):
            print(f"\n📽️ Procesando video {video_idx + 1} de {total_videos}...")
            
            # Hacer clic en el video actual
            videos.nth(video_idx).click()
            time.sleep(4)

            try:
                # Obtener el título del video
                try:
                    title = page.locator('span[data-e2e="new-desc-span"]').nth(0).inner_text()

                except:
                    title = "Sin título o no encontrado"

                # Esperar comentarios
                page.wait_for_selector('div[data-e2e="search-comment-container"]', timeout=10000)
                
                # Hacer scroll para más comentarios
                for _ in range(6):
                    page.mouse.wheel(0, 1200)
                    time.sleep(1.5)
                
                # Extraer comentarios
                comments = page.locator('div[data-e2e="search-comment-container"] p[data-e2e="comment-level-1"] span[dir]')
                count = comments.count()
                print(f"📝 Comentarios encontrados: {count}")
                
                for i in range(count):
                    text = comments.nth(i).inner_text()
                    all_comments.append({
                        "video_num": video_idx + 1,
                        "titulo_video": title,
                        "comentario": text
                    })
                
            except Exception as e:
                print(f"⚠️ Error en video {video_idx + 1}: {str(e)}")
                continue
            
            # Volver para el siguiente video
            if video_idx < total_videos - 1:
                page.go_back()
                time.sleep(3)
                page.wait_for_selector('div[data-e2e="challenge-item-list"]', timeout=10000)
                videos = page.locator('div[id="column-item-video-container"]')

        # Guardar resultados
        if all_comments:
            clean_query = query.replace("@", "").replace("#", "")
            filename = f"comentarios_{clean_query}_{total_videos}videos.csv"
            
            df = pd.DataFrame(all_comments)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"\n✅ Resultados guardados en: {filename}")
            print(f"📊 Total de comentarios: {len(all_comments)}")
        else:
            print("\n❌ No se encontraron comentarios")

        browser.close()

if __name__ == "__main__":
    scrape_comments()
