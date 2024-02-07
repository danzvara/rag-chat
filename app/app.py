from typing import Dict
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json
from dotenv import load_dotenv

from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from memory import ConversationSummaryBufferMemoryWithSummary
from agent import create_agent, stream_output_with_annotations


class ChatRequest(BaseModel):
    sessionId: str
    messages: list


# Load environment variables in local development
load_dotenv()

memories: Dict[str, ConversationSummaryBufferMemoryWithSummary] = {}

app = FastAPI()

origins = ["http://localhost:3000", "https://rag-chat.vercel.app"]

# Allow CORS for the chat client which is hosted on a different domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Experimental-Stream-Data"],
)


@app.get("/health")
def index():
    """
    Health check for Render.com
    """
    return "OK"


@app.post("/api/chat")
async def chat(data: ChatRequest):
    """
    Chat endpoint for the chatbot client. It takes a list of messages and a session ID and
    streams structured output from the agent to the client.

    We are using session IDs to keep track of the conversation history for each session.
    Conversation history is stored in memory for the demo purposes, and obviously this does not
    handle any authentication.
    """
    if len(data.messages) == 0:
        return Response(json.dumps({"error": "No messages provided"}), status_code=400)

    user_question = HumanMessage(content=data.messages[-1]["content"])

    # If we don't have a memory for the session yet, create one
    if data.sessionId not in memories:
        memories[data.sessionId] = ConversationSummaryBufferMemoryWithSummary(
            max_token_limit=1000,
            llm=ChatOpenAI(temperature=0),
            return_messages=True,
            output_key="output",
            input_key="input",
            memory_key="chat_history",
        )

    memory = memories[data.sessionId]

    # Refresh the summary to include the most recent question/answer from the previous exchange
    memory.refresh_summary()

    inputs = {
        "input": user_question,
        "chat_summary": memory.summary,
    }

    agent = create_agent(memory)

    output_stream = stream_output_with_annotations(agent, inputs)

    # Return the output stream to the client. Need to set the experimental header to let
    # the client know we are streaming structured output.
    return StreamingResponse(
        output_stream, headers={"X-Experimental-Stream-Data": "true"}
    )
