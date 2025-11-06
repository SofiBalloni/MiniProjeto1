import requests
from bs4 import BeautifulSoup
import csv
import json
import os
import time

url_base = "https://books.toscrape.com/catalogue/"
url = url_base + "page-1.html"

livros = []

while True:
    site = requests.get(url)
    sopa = BeautifulSoup(site.text, "html.parser")

    itens = sopa.select("ol.row li")

    for item in itens:
        titulo = item.h3.a["title"]
        preco = item.select_one(".price_color").text.replace("£", "")
        disponibilidade = item.select_one(".availability").text.strip()
        estrelas = item.select_one(".star-rating")["class"][1]
        link = item.h3.a["href"].replace("../../../", url_base)

        livros.append({
            "titulo": titulo,
            "preco": preco,
            "disponibilidade": disponibilidade,
            "nota": estrelas,
            "link": link
        })

    proxima = sopa.select_one(".next a")
    if proxima:
        url = url_base + proxima["href"]
        time.sleep(1)
    else:
        break

os.makedirs("data", exist_ok=True)

with open("data/livros.csv", "w", newline="", encoding="utf-8") as f:
    campos = ["titulo", "preco", "disponibilidade", "nota", "link"]
    escritor = csv.DictWriter(f, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(livros)

with open("data/livros.json", "w", encoding="utf-8") as f:
    json.dump(livros, f, ensure_ascii=False, indent=2)

print("Scraping finalizado!")
print(f"Foram coletados {len(livros)} livros.")
