from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper


def create_google_search_tool():
    search = GoogleSearchAPIWrapper(k=1)
    google_search = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )
    return google_search
