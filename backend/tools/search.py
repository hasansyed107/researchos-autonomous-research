import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(

    api_key=os.getenv("TAVILY_API_KEY")

)
def search_tavily(query):
    result=client.search(query=query,
    max_results=5)
    return result
