import typing
import langchain_core
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)

"""
This is a prompt template for the agent. It is based on hwchase17/openai-functions-agent
prompt, but with modifications to include chat summary and hints to prefer retrieval from
the pinecone retriever tool.
"""

agent_prompt = ChatPromptTemplate(
    input_variables=["agent_scratchpad", "input"],
    input_types={
        "chat_history": typing.List[
            typing.Union[
                langchain_core.messages.ai.AIMessage,
                langchain_core.messages.human.HumanMessage,
                langchain_core.messages.chat.ChatMessage,
                langchain_core.messages.system.SystemMessage,
                langchain_core.messages.function.FunctionMessage,
                langchain_core.messages.tool.ToolMessage,
            ]
        ],
        "agent_scratchpad": typing.List[
            typing.Union[
                langchain_core.messages.ai.AIMessage,
                langchain_core.messages.human.HumanMessage,
                langchain_core.messages.chat.ChatMessage,
                langchain_core.messages.system.SystemMessage,
                langchain_core.messages.function.FunctionMessage,
                langchain_core.messages.tool.ToolMessage,
            ]
        ],
    },
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],
                template="""You are a helpful assistant, with access to IBM Python Generative AI SDK.
If the question is about the SDK, always use search_ibm_generative_ai_sdk retriever tool to search for the answer.""",
            )
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["chat_summary"], template="{input}"),
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["input"], template="{input}")
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)
