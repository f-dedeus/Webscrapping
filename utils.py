import feedparser
import logging
import json
from datetime import datetime
from pathlib import Path

def carregar_feeds(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar feeds.json: {e}")
        return {}

def normaliza_data(pub_date: str) -> str:
    try:
        dt = datetime(*feedparser._parse_date(pub_date)[:6])
        return dt.isoformat()
    except Exception:
        return pub_date or ""

def limpa(texto: str | None) -> str:
    return (texto or "").strip()

def extrair_noticias(fonte: str, url: str, limite=None) -> list:
    noticias = []
    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            raise feed.bozo_exception

        for idx, entry in enumerate(feed.entries):
            if limite and idx >= limite:
                break

            noticias.append(
                {
                    "titulo": limpa(entry.get("title")),
                    "link": limpa(entry.get("link")),
                    "resumo": limpa(
                        entry.get("summary") or entry.get("description") or entry.get("subtitle")
                    ),
                    "data": normaliza_data(
                        entry.get("published") or entry.get("updated") or ""
                    ),
                    "fonte": fonte,
                }
            )

    except Exception as e:
        logging.warning(f"Erro ao processar feed '{fonte}': {e}")

    return noticias
