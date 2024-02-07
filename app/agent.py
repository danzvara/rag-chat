from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models.openai import ChatOpenAI
from langchain.memory.chat_memory import BaseChatMemory
import json
import os

from tools import (
    create_pinecone_retriever_tool,
    create_google_search_tool,
    create_python_repl_tool,
)
from prompt import agent_prompt


def create_agent(memory: BaseChatMemory):
    """
    Create an agent with the provided memory and with tools.

    Agent is capped at 3 iterations to prevent long loops / runaway executions.
    """
    tools = [
        create_pinecone_retriever_tool(os.environ["PINECONE_INDEX_NAME"]),
        create_google_search_tool(),
        create_python_repl_tool(),
    ]

    llm = ChatOpenAI(temperature=0, streaming=True, callbacks=[])

    agent = create_openai_tools_agent(llm, tools, agent_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        max_iterations=3,
        verbose=True,
        return_intermediate_steps=False,
    )

    return agent_executor


async def stream_output_with_annotations(agent: AgentExecutor, inputs):
    """
    Helper for streaming structured output with message annotations from the agent.

    We're using Vercel's AI SDK on the client, which implements structured streaming
    by sending chunks prefixed with a message type. However they don't provide Python SDK
    for the server side, so I'm implementing the streaming protocol manually here.
    """
    tool_name, source_path = None, None
    streaming_content = False

    async for event in agent.astream_events(inputs, version="v1"):
        kind = event["event"]

        if kind == "on_retriever_end":
            output = event["data"]["output"]
            documents = output["documents"]
            if len(documents):
                source_path = documents[0].metadata["path"]

        if kind == "on_tool_start":
            tool_name = event["name"]

        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                if not streaming_content:
                    annotations = {}
                    if tool_name:
                        annotations["tool_name"] = tool_name
                    if source_path:
                        annotations["source_path"] = source_path
                    yield "8:" + json.dumps([annotations]) + "\n"
                    streaming_content = True

                yield "0:" + json.dumps(content) + "\n"
