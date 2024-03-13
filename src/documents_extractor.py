import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# URL base
base_url = "https://www.neurotech.com.br/categoria/neurotech/page/{}/"

# Número total de páginas
total_pages = 35  # Atualize para o número correto de páginas

# Pasta de saída
output_folder = "/data/output"

# Certificar-se de que a pasta de saída exista ou criá-la
os.makedirs(output_folder, exist_ok=True)

# Loop através das páginas
for page_num in range(1, total_pages + 1):
    url = base_url.format(page_num)
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar os links para os artigos usando XPath
    article_links = [a['href'] for a in soup.select('h3.entry-title a')]

    # Loop através dos links dos artigos
    for article_link in article_links:
        article_response = requests.get(article_link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        # Extrair o texto do artigo
        article_text = ""
        for paragraph in article_soup.select('.entry-summary p'):
            article_text += paragraph.get_text() + "\n"

        final_text = article_text.encode('latin-1', 'replace').decode('latin-1')

        # Criar um arquivo PDF na pasta de saída
        pdf_filename = f"artigo_{page_num}_{article_links.index(article_link) + 1}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)

        # Usar a biblioteca fpdf para criar o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, final_text)
        pdf.output(pdf_path)

        print(f"Artigo salvo como {pdf_path}")

print("Concluído.")
