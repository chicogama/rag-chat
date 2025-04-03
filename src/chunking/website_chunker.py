import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import sent_tokenize

# Certifique-se de que os recursos do NLTK estão disponíveis
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class WebsiteChunker:
    def __init__(self, chunk_size=3, overlap=1):
        """
        Inicializa o chunker com o tamanho do chunk e sobreposição desejados.

        Parâmetros:
        chunk_size (int): Número de frases por chunk
        overlap (int): Número de frases sobrepostas entre chunks consecutivos
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def fetch_website(self, url):
        """Baixa o conteúdo de um website"""
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        return response.text

    def extract_text(self, html_content):
        """Extrai texto limpo do conteúdo HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove scripts, estilos e outros elementos não textuais
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()

        # Obtém o texto e remove espaços em branco extras
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def create_chunks_by_sentence(self, text):
        """Divide o texto em chunks com base em frases"""
        sentences = sent_tokenize(text)
        chunks = []
        chunk_metadata = []

        if len(sentences) <= self.chunk_size:
            chunks.append(" ".join(sentences))
            chunk_metadata.append(
                {"start_idx": 0, "end_idx": len(sentences)-1})
            return chunks, chunk_metadata

        i = 0
        while i < len(sentences):
            # Determina o final do chunk atual
            end_idx = min(i + self.chunk_size, len(sentences))
            # Cria o chunk unindo as frases
            chunk = " ".join(sentences[i:end_idx])
            chunks.append(chunk)
            chunk_metadata.append({"start_idx": i, "end_idx": end_idx-1})

            # Avança para o próximo chunk com sobreposição
            i = end_idx - self.overlap

        return chunks, chunk_metadata

    def process_website(self, url):
        """Processa um website - baixa, extrai texto e cria chunks"""
        html_content = self.fetch_website(url)
        text = self.extract_text(html_content)
        chunks, metadata = self.create_chunks_by_sentence(text)

        return {
            "url": url,
            "full_text": text,
            "chunks": chunks,
            "metadata": metadata
        }
