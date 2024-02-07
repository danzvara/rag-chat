from langchain_community.vectorstores.pinecone import Pinecone
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings


def create_retriever_tool(index_name):
    """Creates a retriever tool for the given index."""

    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(index_name, embeddings)

    # Had to select (0.8 + 1) / 2 = 0.9 threshold, because pinecone's value is being normalized
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "score_threshold": 0.9,
            "k": 1,
        },
    )

    retriever_tool = create_retriever_tool(
        retriever,
        "search_ibm_generative_ai_sdk",
        "Searches and returns information about IBM Python Generative AI SDK",
    )

    return retriever_tool
