import feedparser
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Temas y sus RSS feeds en Google News (Argentina)
RSS_FEEDS = {
    "incendios": "https://news.google.com/rss/search?q=incendio+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419",
    "deforestación": "https://news.google.com/rss/search?q=deforestación+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419",
    "derrames": "https://news.google.com/rss/search?q=derrames+site:argentina.gob.ar&hl=es-419&gl=AR&ceid=AR:es-419"
}

DATA_FILE = "data/ambiental.csv"
CHART_FILE = "charts/grafico.png"

def obtener_noticias():
    noticias = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    for tema, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title
            link = entry.link
            noticias.append([fecha_hoy, tema, titulo, link])
    return noticias

def guardar_csv(noticias):
    df = pd.DataFrame(noticias, columns=["fecha", "tema", "titulo", "link"])
    if os.path.exists(DATA_FILE):
        historial = pd.read_csv(DATA_FILE)
        df = pd.concat([historial, df], ignore_index=True)
        df.drop_duplicates(subset=["titulo", "link"], inplace=True)
    df.to_csv(DATA_FILE, index=False)
    return df

def generar_grafico(df):
    conteo = df.groupby("tema")["titulo"].count()
    plt.figure(figsize=(8,5))
    conteo.plot(kind="bar", color="red")
    plt.title("Cantidad de noticias ambientales por tema", color='black')
    plt.ylabel("Número de noticias")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CHART_FILE, facecolor='white')
    plt.close()

def main():
    noticias = obtener_noticias()
    df = guardar_csv(noticias)
    generar_grafico(df)
    print("Bot ejecutado. Noticias guardadas y gráfico actualizado.")

if __name__ == "__main__":
    main()
