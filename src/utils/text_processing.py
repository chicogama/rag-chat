import re


def clean_text(text):
    """
    Limpa e normaliza texto.

    Parâmetros:
    text (str): Texto para limpar

    Retorna:
    str: Texto limpo
    """
    # Remove múltiplos espaços em branco
    text = re.sub(r'\s+', ' ', text)

    # Remove caracteres especiais desnecessários
    text = re.sub(r'[^\w\s.,?!;:()\[\]{}-]', '', text)

    return text.strip()


def truncate_text(text, max_length=500):
    """
    Trunca texto para um comprimento máximo.

    Parâmetros:
    text (str): Texto para truncar
    max_length (int): Comprimento máximo

    Retorna:
    str: Texto truncado
    """
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]
    # Tenta truncar no último espaço para não cortar palavras
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]

    return truncated + "..."
