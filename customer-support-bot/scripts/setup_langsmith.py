import os
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

def create_langsmith_project():
    # دریافت API Key از محیط
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        raise ValueError("LANGCHAIN_API_KEY not found in .env file")
    
    # ایجاد کلاینت LangSmith
    client = Client(api_key=api_key)
    
    # تنظیمات پروژه
    project_name = "customer-support-bot"
    project_description = "Project for tracking and improving customer support chatbot"
    
    # بررسی وجود پروژه
    existing_projects = list(client.list_projects(project_name=project_name))
    if existing_projects:
        print(f"Project '{project_name}' already exists. Skipping creation.")
        return existing_projects[0].id
    
    # ایجاد پروژه جدید
    project = client.create_project(
        project_name=project_name,
        description=project_description,
        metadata={
            "project_type": "customer-support",
            "framework": "FastAPI",
            "language": "persian"
        }
    )
    print(f"Created new project: {project.name} (ID: {project.id})")
    return project.id

if __name__ == "__main__":
    project_id = create_langsmith_project()
    print(f"LANGCHAIN_PROJECT_ID={project_id}")