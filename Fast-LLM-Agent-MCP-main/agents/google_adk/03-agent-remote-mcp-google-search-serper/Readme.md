## Agent Remote MCP Tool, Web Search with Serper, Streamlit UI

It shows how to run remote MCP tool with Gemini.

Link: https://github.com/omerbsezer/Fast-LLM-Agent-MCP/tree/main/agents/google_adk/03-agent-remote-mcp-google-search-serper

![sample-03](https://github.com/omerbsezer/Fast-LLM-Agent-MCP/blob/main/agents/google_adk/03-agent-remote-mcp-google-search-serper/gif/agent-remote-mcp-google-search-serper.gif)


Please add .env with Gemini and Serper API Keys 

``` 
# agent/.env
SERPER_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
``` 

Please install nodejs, npm, npx in your system to run npx-based MCP tool.

## Run Agent

Please run non-root username. 
```
uvicorn agent:app --host 0.0.0.0 --port 8000
```


## GUI
After running container, then pls run streamlit, it asks to htttp://localhost:8000/ask

```
streamlit run app.py
or
python -m streamlit run app.py
```

## Prompts

```
- I want to search "what is llm agent" on Google using Serper?
- what is the latest match of Real Madrid and when?
- what is the latest match of Barcelona and when?
```
