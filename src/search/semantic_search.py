import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..embedding.text_embedder import TextEmbedder
from .reranking import ReRanker


class SemanticSearchEngine:
    def __init__(self, embedder=None, chunks=None, embeddings=None):
        """
        Inicializa o motor de busca semântica.

        Parâmetros:
        embedder (TextEmbedder): Instância do embedder para processar consultas
        chunks (list): Lista de chunks de texto
        embeddings (numpy.ndarray): Array de embeddings correspondentes
        """
        self.embedder = embedder or TextEmbedder()
        self.chunks = chunks or []
        self.embeddings = embeddings
        self.reranker = ReRanker()

    def add_documents(self, chunks):
        """Adiciona novos documentos (chunks) ao motor de busca"""
        if not chunks:
            return

        # Gera embeddings para os novos chunks
        new_embeddings = self.embedder.generate_embeddings(chunks)

        # Adiciona os chunks e seus embeddings
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack((self.embeddings, new_embeddings))

        self.chunks.extend(chunks)

    def search(self, query, top_k=5):
        """
        Realiza uma busca semântica.

        Parâmetros:
        query (str): Consulta de busca
        top_k (int): Número de resultados a retornar

        Retorna:
        list: Lista dos top_k resultados mais relevantes
        """
        # Gera embedding para a consulta
        query_embedding = self.embedder.generate_embeddings([query])[0]

        # Calcula similaridade com todos os chunks
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]

        # Obtém os índices dos top_k resultados
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "chunk": self.chunks[idx],
                "similarity": similarities[idx]
            })

        return results

    def rerank_results(self, query, initial_results, method="hybrid"):
        """
        Reordena os resultados iniciais usando um método de reranking.

        Parâmetros:
        query (str): Consulta original
        initial_results (list): Resultados iniciais
        method (str): Método de reranking a ser utilizado

        Retorna:
        list: Lista de resultados reordenados
        """
        if method == "cross_encoder":
            return self.reranker.rerank_cross_encoder(query, initial_results, self.embedder)
        elif method == "hybrid":
            return self.reranker.rerank_hybrid(query, initial_results)
        else:
            return initial_results
