"""
Web Search Tool

Buscar información en internet usando DuckDuckGo
"""

from typing import List, Dict
from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    """
    Buscar en internet usando DuckDuckGo

    Args:
        query: Término a buscar (ej: "capital de España")
        max_results: Número máximo de resultados (default: 3)

    Returns:
        String con resultados formateados

    Examples:
        >>> web_search("capital de España")
        "Madrid is the capital..."
    """
    try:
        # Inicializar cliente DuckDuckGo
        ddgs = DDGS()

        # Buscar
        results = ddgs.text(query, max_results=max_results)

        if not results:
            return f"No se encontraron resultados para: {query}"
        
        # Formatear resultados
        formatted = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Sin título')
            body = result.get('body', 'Sin descripción')
            link = result.get('link', 'Sin enlace')

            formatted.append(
                f"{i}. {title}\n"
                f"   {body[:150]}...\n"
                f"   Fuente: {link}"
            )

        return "\n\n".join(formatted)
    
    except ImportError:
        return "Error: duckduckgo-search no está instalado. Ejecuta: pip install duckduckgo-search"
    except Exception as e:
        return f"Error en búsqueda: {type(e).__name__} - {str(e)}"
    


# Definicion de tool para LangChain
web_search_tool = {
    'name': 'web_search',
    'description': 'Buscar información en internet usando DuckDuckGo',
    'schema': {
        'type': 'object',
        'properties': {
            'query': {
                'type': 'string',
                'description': 'Término a buscar (ej: "última noticias sobre IA")'
            }
        },
        'required': ['query']
    } 
}

if __name__ == "__main__":
    # Test basico
    print("Testing web search tool:")
    print("=" * 70)

    queries = [
        "capital de España",
        "Python programming language",
        "últimas noticias sobre inteligencia artificial",
    ]

    for query in queries:
        print(f"\nBúsqueda: {query}")
        print("-" * 70)
        result = web_search(query, max_results=2)
        print(result)
        print()