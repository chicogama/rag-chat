from sklearn.metrics.pairwise import cosine_similarity


class ReRanker:
    @staticmethod
    def rerank_cross_encoder(query, results, embedder):
        """
        Reordena resultados usando uma abordagem tipo cross-encoder.

        Parâmetros:
        query (str): Consulta original
        results (list): Lista de resultados (dicionários)
        embedder: Instância do TextEmbedder para gerar embeddings

        Retorna:
        list: Resultados reordenados
        """
        chunks = [result["chunk"] for result in results]

        # Na implementação real, usaríamos um Cross-Encoder
        # Como exemplo, estamos simulando com similaridade de cosseno
        query_embedding = embedder.generate_embeddings([query])[0]
        chunk_embeddings = embedder.generate_embeddings(chunks)
        scores = cosine_similarity([query_embedding], chunk_embeddings)[0]

        # Atualiza resultados com novos scores
        for i, result in enumerate(results):
            result["rerank_score"] = scores[i]

        # Reordena com base nos novos scores
        reranked_results = sorted(
            results, key=lambda x: x["rerank_score"], reverse=True)
        return reranked_results

    @staticmethod
    def rerank_hybrid(query, results):
        """
        Reordena resultados usando uma abordagem híbrida (semântica + lexical).

        Parâmetros:
        query (str): Consulta original
        results (list): Lista de resultados (dicionários)

        Retorna:
        list: Resultados reordenados
        """
        query_terms = set(query.lower().split())

        for result in results:
            # Calcula um score lexical simples baseado na sobreposição de termos
            chunk_terms = set(result["chunk"].lower().split())
            term_overlap = len(query_terms.intersection(
                chunk_terms)) / len(query_terms) if query_terms else 0

            # Combina scores semântico e lexical
            result["hybrid_score"] = 0.7 * \
                result["similarity"] + 0.3 * term_overlap

        # Reordena com base no score híbrido
        reranked_results = sorted(
            results, key=lambda x: x["hybrid_score"], reverse=True)
        return reranked_results
