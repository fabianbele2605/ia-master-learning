"""
Main entry point - Mes 4: Agentes Autónomos

Ejecutar ReAct agent con Ollama
"""

import sys
from pathlib import Path
import logging

# Setup path para imports
sys.path.insert(0, str(Path(__file__).parent))

from config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_ITERATIONS, DEBUG
from agents.react_agent import ReActAgent
from tools.calculator import calculator
from tools.web_search import web_search

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OllamaLLM:
    """Wrapper para Ollama local"""

    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        """
        Inicializar cliente Ollama

        Args:
            model: Modelo a usar (default: qwen:8b)
            base_url: URL de Ollama (default: http://localhost:11434)
        """
        import requests
        self.requests = requests
        self.model = model
        self.base_url = base_url.rstrip('/')
        logger.info(f"✅ Conectado a Ollama ({model})")

    def generate(self, prompt: str) -> str:
        """
        Generar respuesta del LLM

        Args:
            prompt: Prompt a enviar

        Returns:
            Respuesta del modelo
        """
        try:
            response = self.requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json().get('message', {}).get('content', '')
        except Exception as e:
            logger.error(f"❌ Error en generación: {str(e)}")
            return f"Error: {str(e)}"


def main():
    """Main execution"""
    
    logger.info("=" * 70)
    logger.info("MES 4: AGENTES AUTONOMOS - ReAct Framework")
    logger.info("=" * 70)
    logger.info(f"Model: {OLLAMA_MODEL}")
    logger.info(f"Base URL: {OLLAMA_BASE_URL}")
    logger.info(f"Max iterations: {MAX_ITERATIONS}")
    
    try:
        # 1. Conectar con Ollama
        logger.info("\n1. Conectando con Ollama...")
        llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        
        # 2. Definir tools
        logger.info("2. Cargando tools...")
        tools = {
            'calculator': calculator,
            'web_search': web_search
        }
        logger.info(f"   Tools disponibles: {list(tools.keys())}")
        
        # 3. Crear agent
        logger.info("3. Inicializando ReAct Agent...")
        agent = ReActAgent(
            llm=llm,
            tools=tools,
            max_iterations=MAX_ITERATIONS,
            verbose=True
        )
        
        # 4. Loop interactivo
        logger.info("\n4. Agent listo. Escribe 'salir' para terminar.\n")
        
        while True:
            try:
                # Input del usuario
                query = input("\n📝 Tu pregunta: ").strip()
                
                if query.lower() in ['salir', 'exit', 'quit']:
                    logger.info("👋 Hasta luego!")
                    break
                
                if not query:
                    continue
                
                # Ejecutar agent
                result = agent.run(query)
                
                # Mostrar resultado
                logger.info(f"\n✅ Respuesta: {result}")
            
            except KeyboardInterrupt:
                logger.info("\n👋 Interrumpido por usuario")
                break
            except Exception as e:
                logger.error(f"❌ Error: {str(e)}")
    
    except Exception as e:
        logger.error(f"❌ Error fatal: {str(e)}")
        logger.error("\nVerifica que Ollama está corriendo: ollama serve")
        sys.exit(1)


if __name__ == '__main__':
    main()
