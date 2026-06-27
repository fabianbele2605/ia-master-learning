"""
Calculator Tool

Ejecutar operaciones matemáticas de forma segura
"""

import math
from typing import Union


def calculator(expression: str) -> Union[float, str]:
    """
    Evaluar expresión matemática de forma segura
    
    Solo permite:
    - Números
    - Operadores: +, -, *, /, //, %, **
    - Funciones math: sqrt, sin, cos, tan, log, exp
    
    Args:
        expression: Expresión a evaluar (ej: "2 + 2 * 3")
    
    Returns:
        Resultado como float, o mensaje de error
    
    Examples:
        >>> calculator("2 + 2")
        4.0
        >>> calculator("sqrt(16)")
        4.0
    """
    try:
        # Define funciones permitidas (whitelist)
        safe_dict = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pi': math.pi,
            'e': math.e,
            '__builtins__': {}  # Bloquea funciones peligrosas
        }
        
        # Evaluar de forma segura
        result = eval(expression, safe_dict)
        
        # Convertir a float
        return float(result)
    
    except ZeroDivisionError:
        return "Error: Division por cero"
    except ValueError as e:
        return f"Error: Valor invalido - {str(e)}"
    except NameError as e:
        return f"Error: Variable no definida - {str(e)}"
    except SyntaxError:
        return "Error: Sintaxis invalida"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


# Definicion de tool para LangChain
calculator_tool = {
    'name': 'calculator',
    'description': 'Realizar calculos matematicos. Soporta: +, -, *, /, sqrt, sin, cos, tan, log, exp',
    'schema': {
        'type': 'object',
        'properties': {
            'expression': {
                'type': 'string',
                'description': 'Expresion matematica (ej: "2 + 2 * 3" o "sqrt(16)")'
            }
        },
        'required': ['expression']
    }
}


if __name__ == '__main__':
    # Test basico
    print("Testing calculator tool:")
    print(f"  2 + 2 = {calculator('2 + 2')}")
    print(f"  10 / 2 = {calculator('10 / 2')}")
    print(f"  sqrt(16) = {calculator('sqrt(16)')}")
    print(f"  2 ** 3 = {calculator('2 ** 3')}")
    print(f"  1 / 0 = {calculator('1 / 0')}")  # Error handling
