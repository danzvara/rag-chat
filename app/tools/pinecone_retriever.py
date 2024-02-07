from functools import partial
from typing import Optional
from langchain_community.vectorstores.pinecone import Pinecone
from langchain.tools import Tool
from langchain_openai import OpenAIEmbeddings

from langchain_core.prompts import BasePromptTemplate, PromptTemplate, format_document
from langchain_core.retrievers import BaseRetriever
from langchain_core.pydantic_v1 import BaseModel, Field


class RetrieverInput(BaseModel):
    query: str = Field(description="query to look up in retriever")


def _get_relevant_documents(
    query: str,
    retriever: BaseRetriever,
    document_prompt: BasePromptTemplate,
    document_separator: str,
    callbacks: Optional[dict] = None,
) -> str:
    # HACK: Pass the callbacks to the retriever
    docs = retriever.get_relevant_documents(query, callbacks=callbacks)
    return document_separator.join(
        format_document(doc, document_prompt) for doc in docs
    )


async def _aget_relevant_documents(
    query: str,
    retriever: BaseRetriever,
    document_prompt: BasePromptTemplate,
    document_separator: str,
    callbacks: Optional[dict] = None,
) -> str:
    # HACK: Pass the callbacks to the retriever
    docs = await retriever.aget_relevant_documents(query, callbacks=callbacks)
    return document_separator.join(
        format_document(doc, document_prompt) for doc in docs
    )


def create_pinecone_retriever_tool(index_name):
    """
    Creates a pinecone retriever tool for the given index.
    This is a hacky reimplementation of the create_retriever_tool function from langchain.tools.retriever
    because the original function does not pass callbacks down to the retriever.

    Because of this, the retriever events are not propagated to the agent, and we cannot stream them to the client.
    """

    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(index_name, embeddings)

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            # I'm using a threshold of 0.85 for similarity score to filter out irrelevant results, selected
            # empirically. However because of langchain's normalization, score threshold has to be normalized
            # to [0, 1] range from pinecone's [-1,1]. So (0.8 + 1) / 2 = 0.9
            "score_threshold": 0.875,
            "k": 1,
            # Use filter to only return documents with version v2.1.1.
            # TODO: Agent should be able to specify the version of the document it wants to retrieve.
            "filter": {"version": "v2.1.1"},
        },
    )

    document_prompt = PromptTemplate.from_template("{page_content}")
    func = partial(
        _get_relevant_documents,
        retriever=retriever,
        document_prompt=document_prompt,
        document_separator="\n\n",
    )
    afunc = partial(
        _aget_relevant_documents,
        retriever=retriever,
        document_prompt=document_prompt,
        document_separator="\n\n",
    )
    return Tool(
        name="search_ibm_generative_ai_sdk",
        description="Searches and returns information about IBM Python Generative AI SDK",
        func=func,
        coroutine=afunc,
        args_schema=RetrieverInput,
    )
