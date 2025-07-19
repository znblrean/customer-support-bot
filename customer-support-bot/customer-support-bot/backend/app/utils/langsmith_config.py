import os
from langsmith import Client
from langchain.callbacks.tracers import LangChainTracer

def setup_langsmith():
    client = Client(
        api_key=os.getenv("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"),
        project_name=os.getenv(" customer-support-bot")
    )
    
    tracer = LangChainTracer(
        project_name=os.getenv("LANGCHAIN_PROJECT"),
        client=client
    )
    
    return client, tracer