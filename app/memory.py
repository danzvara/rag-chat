from langchain.memory import ConversationSummaryBufferMemory


class ConversationSummaryBufferMemoryWithSummary(ConversationSummaryBufferMemory):
    """A memory object that includes a summary of the conversation."""

    summary: str = "This is the summary of the conversation. Right now it's empty."

    def refresh_summary(self):
        self.summary = self.predict_new_summary(
            self.load_memory_variables({})["chat_history"], self.summary
        )
