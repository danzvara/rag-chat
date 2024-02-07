import json
import unittest
from unittest.mock import AsyncMock, patch
from langchain.agents import Agent
from langchain_core.documents import Document
from agent import stream_output_with_annotations


class MockDataChunk:
    def __init__(self, content):
        self.content = content


class TestAgent(unittest.TestCase):
    @patch.object(Agent, "astream_events", new_callable=AsyncMock())
    async def test_streaming(self, mock_astream_events):
        mock_astream_events.return_value = [
            {
                "event": {"event": "on_chat_model_stream"},
                "data": {"chunk": MockDataChunk("mock_content")},
            }
        ]

        agent = Agent()
        result = []

        async for chunk in stream_output_with_annotations(agent, None):
            result.append(chunk)

        self.assertListEqual(result, ["0: mock_content"])

    @patch.object(Agent, "astream_events", new_callable=AsyncMock())
    async def test_streaming_annotations(self, mock_astream_events):
        mock_astream_events.return_value = [
            {
                "event": {"event": "on_tool_start"},
                "name": "tool_name",
            },
            {
                "event": {"event": "on_retriever_end"},
                "data": {
                    "output": {
                        "documents": [Document(metadata={"path": "source_path"})]
                    }
                },
            },
            {
                "event": {"event": "on_chat_model_stream"},
                "data": {"chunk": MockDataChunk("mock_content")},
            },
        ]

        agent = Agent()
        result = []

        async for chunk in stream_output_with_annotations(agent, None):
            result.append(chunk)

        self.assertListEqual(
            result,
            [
                "8: "
                + json.dumps([{"tool_name": "tool_name", "source_path": "source_path"}])
                + "\n",
                "0: mock_content",
            ],
        )
