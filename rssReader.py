import logging
from pathlib import Path
import json

from utils import carregar_feeds, extrair_noticias

# ---------- Configurações ----------
LOG_FILE = "rss_reader.log"
OUTPUT_FILE = Path("raw_noticias.json")
FEEDS_FILE = Path("feeds.json")
MAX_ITENS = None  # ou defina um número para limitar por feed

# ---------- Logger ----------
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)

# ---------- Execução ----------
def main():
    todas_noticias = []
    feeds = carregar_feeds(FEEDS_FILE)

    for fonte, url in feeds.items():
        logging.info(f"Coletando notícias de: {fonte}")
        noticias = extrair_noticias(fonte, url, MAX_ITENS)
        logging.info(f"Encontradas {len(noticias)} notícias de {fonte}")
        todas_noticias.extend(noticias)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(todas_noticias, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(todas_noticias)} notícias salvas em {OUTPUT_FILE}")
        logging.info(f"Arquivo salvo: {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Erro ao salvar JSON: {e}")

if __name__ == "__main__":
    main()
