## Agent Strands Local MCP FileOps, Streamlit
It shows local mcp fileOps with AWS Strands.

Please run Python files on Linux, or WSL on Win.

Install AWS Strands Agents:
- pip install strands-agents
- pip install strands-agents-tools strands-agents-builder


### AWS Bedrock Model 
- First, to enable in your region or AWS-West for Model Access (AWS Bedrock > Bedrock Configuration > Model Access > Nova Pro, or Claude 3.7 Sonnet, or Llama 4)
- In these samples, we'll use AWS Nova Pro, because it's served in different regions by AWS. After model access, give permission to your IAM to access AWS Bedrock services. 
- 2 Options to reach AWS Bedrock Model using your AWS Account:

#### 1. AWS Config
- With 'aws configure', to create 'config' and 'credentials' files

#### 2. Getting variables using .env file
Add .env file:

``` 
AWS_ACCESS_KEY_ID= PASTE_YOUR_ACCESS_KEY_ID_HERE
AWS_SECRET_ACCESS_KEY=PASTE_YOUR_SECRET_ACCESS_KEY_HERE
``` 

### Run Agent

Please run non-root username. 

```
uvicorn agent:app --host 0.0.0.0 --port 8000
```


### GUI
After running container, then pls run streamlit, it asks to htttp://localhost:8000/ask

```
streamlit run app.py
or
python -m streamlit run app.py
```

### Prompts

```
- list the files in the '/home/omer/mcp-test'
- create test2.py in the '/home/omer/mcp-test' and write 'print("Added by MCP Tool: @modelcontextprotocol/server-filesystem")' in it.
- read test2.py in the '/home/omer/mcp-test'
- run the test2.py '/home/omer/mcp-test' with "python test2.py"
- delete the test2.py '/home/omer/mcp-test'
```

### Reference
https://strandsagents.com/