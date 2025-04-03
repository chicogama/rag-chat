import numpy as np
from sentence_transformers import SentenceTransformer


class TextEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Inicializa o embedder com o modelo especificado.

        Parâmetros:
        model_name (str): Nome do modelo sentence-transformers a ser usado
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, chunks):
        """Gera embeddings para uma lista de chunks de texto"""
        return self.model.encode(chunks)

    def save_embeddings(self, embeddings, file_path):
        """Salva embeddings em um arquivo numpy"""
        np.save(file_path, embeddings)

    def load_embeddings(self, file_path):
        """Carrega embeddings de um arquivo numpy"""
        return np.load(file_path)
