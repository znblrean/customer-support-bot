from langsmith import Client
from langchain.callbacks.manager import tracing_v2_enabled

def setup_tracing():
    return Client(
        api_key=os.getenv("LANGCHAIN_API_KEY"),
        project_name=os.getenv("LANGCHAIN_PROJECT")
    )

def trace_chain(func):
    def wrapper(*args, **kwargs):
        with tracing_v2_enabled(project_name=os.getenv("LANGCHAIN_PROJECT")):
            return func(*args, **kwargs)
    return wrapper