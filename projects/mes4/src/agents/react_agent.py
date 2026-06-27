"""
ReActAgent - Reasoning + Acting Framework

Implementación de ReAct con LangChain y Ollama
"""

import re
from typing import Any, List, Dict, Callable
import logging


logger = logging.getLogger(__name__)


class ReActAgent:
    """
    Agent que alterna entre Reasoning (pensar) y Acting (actuar)
    
    ReAct loop:
    1. Thought: ¿Qué debo hacer?
    2. Action: ¿Qué tool uso?
    3. Observation: ¿Qué pasó?
    4. Repeat hasta encontrar respuesta
    """

    def __init__(
        self,
        llm: Any,
        tools: Dict[str, Callable],
        max_iterations: int = 10,
        verbose: bool = True
    ):
        """
        Inicializar ReAct Agent
        
        Args:
            llm: Language model (Ollama/GPT)
            tools: Dict de {nombre: función} disponibles
            max_iterations: Máximo de pasos
            verbose: Mostrar logs detallados
        """
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.history = []

    def _format_prompt(self, query: str, history: List[str]) -> str:
        """Construir prompt para el LLM"""
        
        # Lista de tools disponibles
        tools_str = "\n".join(
            f"- {name}: {func.__doc__.split(chr(10))[0] if func.__doc__ else name}"
            for name, func in self.tools.items()
        )
        
        # Historial de pasos previos
        history_str = "\n".join(history) if history else "No hay pasos previos"
        
        prompt = f"""Eres un agente inteligente que resuelve problemas paso a paso.

HERRAMIENTAS DISPONIBLES:
{tools_str}

HISTORIAL:
{history_str}

QUERY: {query}

Responde con el siguiente formato:
Thought: <tu razonamiento>
Action: <nombre de la tool o 'Final Answer'>
Input: <input para la tool>

Si tienes la respuesta final, usa:
Thought: <razonamiento>
Final Answer: <respuesta>
"""
        return prompt

    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parsear respuesta del LLM"""
        
        result = {
            'thought': '',
            'action': '',
            'action_input': '',
            'is_final': False
        }
        
        # Extraer Thought
        thought_match = re.search(r'Thought:\s*(.+?)(?=Action:|Final Answer:|$)', response, re.DOTALL)
        if thought_match:
            result['thought'] = thought_match.group(1).strip()
        
        # Extraer Final Answer
        final_match = re.search(r'Final Answer:\s*(.+?)$', response, re.DOTALL)
        if final_match:
            result['is_final'] = True
            result['action'] = 'Final Answer'
            result['action_input'] = final_match.group(1).strip()
            return result
        
        # Extraer Action
        action_match = re.search(r'Action:\s*(.+?)(?=Input:|$)', response, re.DOTALL)
        if action_match:
            result['action'] = action_match.group(1).strip()
        
        # Extraer Input
        input_match = re.search(r'Input:\s*(.+?)$', response, re.DOTALL)
        if input_match:
            result['action_input'] = input_match.group(1).strip()
        
        return result

    def _execute_tool(self, action: str, action_input: str) -> str:
        """Ejecutar una tool"""
        
        if action not in self.tools:
            return f"Error: Tool '{action}' no existe"
        
        try:
            tool = self.tools[action]
            result = tool(action_input)
            return str(result)
        except Exception as e:
            return f"Error ejecutando {action}: {str(e)}"

    def run(self, query: str) -> str:
        """
        Ejecutar agent con query
        
        Args:
            query: Pregunta/tarea a resolver
        
        Returns:
            Respuesta final
        """
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"QUERY: {query}")
            print(f"{'='*70}\n")
        
        self.history = []
        
        for iteration in range(self.max_iterations):
            # 1. REASONING: Ask LLM
            prompt = self._format_prompt(query, self.history)
            llm_response = self.llm.generate(prompt)
            
            # 2. PARSE: Extract thought, action, answer
            parsed = self._parse_response(llm_response)
            
            # Agregar a historial
            step = f"Thought: {parsed['thought']}\nAction: {parsed['action']}\nInput: {parsed['action_input']}"
            self.history.append(step)
            
            if self.verbose:
                print(f"Step {iteration + 1}:")
                print(f"  Thought: {parsed['thought']}")
                print(f"  Action: {parsed['action']}")
                print(f"  Input: {parsed['action_input']}")
            
            # 3. CHECK: Is it final answer?
            if parsed['is_final']:
                if self.verbose:
                    print(f"\n{'='*70}")
                    print(f"FINAL ANSWER: {parsed['action_input']}")
                    print(f"{'='*70}\n")
                return parsed['action_input']
            
            # 4. ACTING: Execute the tool
            observation = self._execute_tool(parsed['action'], parsed['action_input'])
            self.history.append(f"Observation: {observation}")
            
            if self.verbose:
                print(f"  Observation: {observation}\n")
        
        return "Max iterations reached. Unable to solve the query."

    def get_history(self) -> List[str]:
        """Retornar historial de pasos"""
        return self.history


# Test basico
if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from tools.calculator import calculator
    from tools.web_search import web_search
    
    print("Testing ReActAgent (mock LLM):")
    print("=" * 70)
    
    # Mock LLM para testing
    class MockLLM:
        def generate(self, prompt: str) -> str:
            if "2" in prompt and "2" in prompt:
                return "Thought: Necesito calcular 2+2\nAction: calculator\nInput: 2+2"
            else:
                return "Thought: Tengo la respuesta\nFinal Answer: Test exitoso"
    
    tools = {
        'calculator': calculator,
        'web_search': web_search
    }
    
    agent = ReActAgent(MockLLM(), tools, verbose=True)
    result = agent.run("Cual es 2+2?")
    print(f"Resultado final: {result}")
