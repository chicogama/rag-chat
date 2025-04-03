from setuptools import setup, find_packages

setup(
    name="websitechunker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
        "sentence-transformers>=2.2.0",
        "nltk>=3.6.0",
        "scikit-learn>=0.24.0",
        "numpy>=1.19.0",
        "pandas>=1.3.0",
    ],
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Ferramenta para chunking e embedding de websites para aplicações GenAI",
    keywords="nlp, embedding, chunking, search, ai",
    python_requires=">=3.7",
)
