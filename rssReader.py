import json
from pathlib import Path
#from email.utils import parsedate_to_datetime
import datetime
import feedparser

# ---------- Configuração ----------
FEEDS = {
    "G1": "https://g1.globo.com/rss/g1//",
    "BBC News Brasil": "https://feeds.bbci.co.uk/portuguese/rss.xml",
}

OUTPUT_FILE = Path("noticias.json")
MAX_ITENS  = None        # defina um inteiro p/ limitar por feed, ou deixe None

# ---------- Funções utilitárias ----------
def normaliza_data(pub_date: str) -> str:
    """
    Converte 'Tue, 02 Jul 2025 14:30:00 GMT' ➜ '2025-07-02T14:30:00+00:00'.
    Se falhar, devolve a string original.
    """
    try:
        return parsedate_to_datetime(pub_date).isoformat()
    except Exception:
        return pub_date or ""

def limpa(texto: str | None) -> str:
    return (texto or "").strip()

# ---------- Coleta ----------
noticias = []

for fonte, url in FEEDS.items():
    feed = feedparser.parse(url)

    if feed.bozo:  # feed mal‑formado ou erro de rede
        print(f"[WARN] Problema ao ler {fonte}: {feed.bozo_exception}")
        continue

    for idx, entry in enumerate(feed.entries):
        if MAX_ITENS and idx >= MAX_ITENS:
            break

        noticias.append(
            {
                "titulo": limpa(entry.get("title")),
                "link": limpa(entry.get("link")),
                "resumo": limpa(
                    entry.get("summary")
                    or entry.get("description")
                    or entry.get("subtitle")
                ),
                "data": normaliza_data(
                    entry.get("published")
                    or entry.get("updated")
                    or ""
                ),
                "fonte": fonte,
            }
        )

# ---------- Persistência ----------
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(noticias, f, ensure_ascii=False, indent=2)

print(f"✅ {len(noticias)} notícias gravadas em {OUTPUT_FILE.resolve()}")
