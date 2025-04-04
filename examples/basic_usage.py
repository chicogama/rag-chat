import sys
import os

# Adiciona o diretório raiz ao sys.path para importação dos módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.search.semantic_search import SemanticSearchEngine
from src.embedding.text_embedder import TextEmbedder
from src.chunking.website_chunker import WebsiteChunker
import nltk

nltk.download('punkt_tab')

def run_example():
    # URL de exemplo
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    # 1. Chunking do website
    print("Realizando chunking do website...")
    chunker = WebsiteChunker(chunk_size=3, overlap=1)
    website_data = chunker.process_website(url)
    chunks = website_data["chunks"]

    print(f"Texto extraído e dividido em {len(chunks)} chunks")

    # 2. Gerando embeddings
    print("\nGerando embeddings para os chunks...")
    embedder = TextEmbedder()

    # 3. Criando o motor de busca semântica
    search_engine = SemanticSearchEngine(embedder)
    search_engine.add_documents(chunks)

    print("Motor de busca semântica criado com sucesso!")

    # 4. Realizando uma busca
    query = "Quais são os desafios éticos da inteligência artificial?"
    print(f"\nBuscando: '{query}'")

    results = search_engine.search(query, top_k=5)

    print("\nResultados iniciais:")
    for i, result in enumerate(results):
        print(f"{i+1}. Similaridade: {result['similarity']:.4f}")
        print(f"   Chunk: {result['chunk'][:100]}...\n")

    # 5. Aplicando reranking
    print("\nAplicando reranking...")
    reranked_results = search_engine.rerank_results(
        query, results, method="hybrid")

    print("\nResultados após reranking:")
    for i, result in enumerate(reranked_results):
        print(f"{i+1}. Score híbrido: {result['hybrid_score']:.4f}")
        print(f"   Chunk: {result['chunk'][:100]}...\n")


if __name__ == "__main__":
    run_example()
