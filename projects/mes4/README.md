# Mes 4: Agentes Autónomos & Tool Use

**Duración:** 4 semanas
**Tema:** Autonomous agents con LangChain + ReAct framework
**Stack:** LangChain, Ollama (local LLM), LLMs, Tool Use

## 📚 Estructura

```
mes4/
├── week1_react_framework.ipynb         # Explicación ReAct
├── week2_langchain_agents.ipynb        # LangChain setup
├── week3_tool_use.ipynb                # Tool definitions
├── week4_multiagent_capstone.ipynb     # Capstone final
├── src/
│   ├── agents/
│   │   └── react_agent.py              # Implementación ReAct
│   ├── tools/
│   │   ├── web_search.py               # Buscar web
│   │   ├── calculator.py               # Cálculos
│   │   └── custom_tools.py             # Tools custom (TBD)
│   ├── config.py                       # Configuración
│   └── main.py                         # Entry point
├── tests/
│   ├── test_agents.py
│   └── test_tools.py
├── requirements_mes4.txt
├── .env.example
└── README.md (este archivo)
```

## 🚀 Setup Inicial

### 1. Crear entorno virtual
```bash
cd ~/Escritorio/IA_Local/ia-master/projects/mes4
python3.11 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements_mes4.txt
```

### 3. Setup Ollama (local LLM)
```bash
# Instalar Ollama: https://ollama.ai
ollama pull qwen:7b
ollama serve  # En otra terminal

# Verificar
curl http://localhost:11434/api/tags
```

### 4. Crear .env
```bash
cp .env.example .env
# Editar .env con tus valores
```

## 📖 Cómo estudiar

### Opción A: Jupyter + VS Code
1. Abre `week1_react_framework.ipynb` para entender conceptos
2. Implementa en `src/agents/react_agent.py`
3. Test con `pytest tests/`

### Opción B: Solo VS Code
1. Lee las explicaciones en el notebook
2. Desarrolla en carpeta `src/`
3. Ejecuta `python src/main.py`

## 🎯 Semanas

### Week 1: ReAct Framework
- Qué es ReAct (Reasoning + Acting)
- Thought → Action → Observation loop
- Implementar ReActAgent básico

### Week 2: LangChain Agents
- LangChain setup
- Agent types (ReAct, OpenAI Tools, etc)
- Integration con Ollama

### Week 3: Tool Use & Function Calling
- Definir tools (web_search, calculator, etc)
- Function calling
- Multi-tool routing

### Week 4: Multi-Agent Capstone
- Múltiples agentes colaborando
- Agent specialization
- Workflow coordination

## 🔧 Ejecutar código

```bash
# Activar venv
source venv/bin/activate

# Run main
python src/main.py

# Run tests
pytest tests/ -v

# Interactive REPL
python
>>> from src.agents import ReActAgent
>>> agent = ReActAgent(llm=..., tools=...)
>>> agent.run("¿Cuál es 2+2?")
```

## 📊 Progress

- [ ] Week 1: ReAct Framework
- [ ] Week 2: LangChain Agents
- [ ] Week 3: Tool Use
- [ ] Week 4: Multi-Agent Capstone

## 🚨 Troubleshooting

**Ollama not connecting:**
```bash
# Terminal 1
ollama serve

# Terminal 2
curl http://localhost:11434/api/tags
```

**Import errors:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main.py
```

## 📚 Recursos

- [LangChain Docs](https://docs.langchain.com/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Ollama](https://ollama.ai/)
- [Qwen LLM](https://huggingface.co/Qwen)

---

**Creado:** Junio 2026  
**Autor:** Fabián Beleño  
**Stack:** LangChain + Ollama + Python
