from langchain_community.vectorstores.pinecone import Pinecone
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings


def create_pinecone_retriever_tool(index_name):
    """Creates a pinecone retriever tool for the given index."""

    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(index_name, embeddings)

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            # I'm using a threshold of 0.8 for similarity score to filter out irrelevant results, selected
            # empirically. However because of langchain's normalization, score threshold has to be normalized
            # to [0, 1] range from pinecone's [-1,1]. So (0.8 + 1) / 2 = 0.9
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
