import unittest

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from memory import ConversationSummaryBufferMemoryWithSummary

load_dotenv()


class TestMemory(unittest.TestCase):

    def test_summary_refresh(self):
        memory = ConversationSummaryBufferMemoryWithSummary(
            max_token_limit=1000,
            llm=ChatOpenAI(temperature=0),
            return_messages=True,
            output_key="output",
            input_key="input",
            memory_key="chat_history",
        )

        old_summary = memory.summary
        memory.save_context(
            {"input": "Question about the weather"}, {"output": "It's sunny today"}
        )

        memory.refresh_summary()
        self.assertNotEqual(old_summary, memory.summary)
        self.assertIn("sunny", memory.summary)
