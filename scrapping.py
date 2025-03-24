import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile


# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
pasta_download = "anexos"


os.makedirs(pasta_download, exist_ok=True)


# Função baixar o PDF
def baixar_pdf(link_pdf, nome_arquivo):
    try:
        resposta = requests.get(link_pdf, timeout=10)  # Adicionando timeout para evitar travamentos
        if resposta.status_code == 200:
            with open(os.path.join(pasta_download, nome_arquivo), 'wb') as f:
                f.write(resposta.content)
            print(f'{nome_arquivo} baixado com sucesso!')
        else:
            print(f'Erro ao baixar {nome_arquivo}. Status: {resposta.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Erro de conexão ao tentar baixar {nome_arquivo}: {e}')


# Função compactar os arquivos PDF
def compactar_em_zip():
    try:
        with ZipFile("anexos.zip", 'w') as zipf:
            for arquivo in os.listdir(pasta_download):
                zipf.write(os.path.join(pasta_download, arquivo), arquivo)
        print('Todos os arquivos foram compactados em anexos.zip.')
    except Exception as e:
        print(f'Ocorreu um erro ao tentar compactar os arquivos: {e}')


# Função Main
def main():
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            print('Site acessado com sucesso! Buscando os PDFs...')
            sopa = BeautifulSoup(resposta.text, 'html.parser')
            links_pdfs = [link['href'] for link in sopa.find_all('a', href=True) if link['href'].endswith('.pdf')]

            # Links para os Anexos
            anexo1_link = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
            anexo2_link = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"

            # Baixar os PDFs (Anexo I e II)
            print('Encontrados links para os PDFs. Iniciando o download...')
            baixar_pdf(anexo1_link, "Anexo_I.pdf")
            baixar_pdf(anexo2_link, "Anexo_II.pdf")

            # Compactar em zip
            compactar_em_zip()
        else:
            print(f"Não consegui acessar o site. Status: {resposta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f'Erro de conexão ao tentar acessar o site: {e}')


if __name__ == "__main__":
    main()
