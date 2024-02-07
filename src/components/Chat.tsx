import React, { useCallback, useRef } from "react";
import Message from "./Message";
import { v4 as uuidv4 } from "uuid";

import { useChat, Message as AiMessage } from "ai/react";
import { isDevelopment } from "../utils";

const INITIAL_MESSAGE: AiMessage = {
  role: "assistant",
  content: "Hi there! How can I help you?",
  id: "1",
};

const CHAT_ENDPOINT = isDevelopment()
  ? "http://localhost:3001/api/chat"
  : "https://rag-chat-backend.onrender.com/api/chat";

const Chat: React.FC = React.memo(() => {
  const sessionId = useRef(uuidv4());
  const {
    messages,
    input,
    isLoading,
    handleInputChange,
    handleSubmit,
    stop,
    setMessages,
  } = useChat({
    api: CHAT_ENDPOINT,
    initialMessages: [INITIAL_MESSAGE],
    body: {
      sessionId: sessionId.current,
    },
  });

  const clearChat = useCallback(() => {
    stop();
    setMessages([INITIAL_MESSAGE]);
    sessionId.current = uuidv4();
  }, [setMessages, stop]);

  return (
    <div
      style={{
        width: "700px",
        marginBottom: "8px",
        display: "flex",
        overflow: "hidden",
      }}
    >
      <form onSubmit={handleSubmit} style={{ display: "flex", width: "100%" }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            width: "100%",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column-reverse",
              overflow: "auto",
              marginBottom: "8px",
            }}
          >
            {messages
              .slice(0)
              .reverse()
              .map((message, index) => {
                return (
                  <Message
                    key={index}
                    text={message.content}
                    isUser={message.role === "user"}
                    annotations={message.annotations ?? []}
                  />
                );
              })}
          </div>
          <div>
            <div style={{ width: "100%" }}>
              <input value={input} onChange={handleInputChange} />
            </div>
            <div>
              <button
                style={{ width: "7rem", backgroundColor: "lightblue" }}
                type="submit"
                color="blue"
                disabled={!input || input === "" || isLoading}
              >
                Send
              </button>
              <button type="reset" onClick={stop} disabled={!isLoading}>
                Stop generation
              </button>
              <button type="reset" onClick={clearChat}>
                Clear chat
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
});

export default Chat;
