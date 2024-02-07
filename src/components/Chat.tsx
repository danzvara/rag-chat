import React, { useCallback, useRef } from "react";
import Message from "./Message";
import { v4 as uuidv4 } from "uuid";

import { useChat, Message as AiMessage } from "ai/react";

const INITIAL_MESSAGE: AiMessage = {
  role: "assistant",
  content: "Hi there! How can I help you?",
  id: "1",
};

const Chat: React.FC = React.memo(() => {
  const sessionId = useRef(uuidv4());
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    stop,
    setMessages,
  } = useChat({
    api: "http://localhost:3001/api/chat",
    initialMessages: [INITIAL_MESSAGE],
    body: {
      sessionId: sessionId.current,
    },
  });

  const clearChat = useCallback(() => {
    setMessages([INITIAL_MESSAGE]);
    sessionId.current = uuidv4();
  }, [setMessages]);

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
              >
                Send
              </button>
              <button type="reset" onClick={stop}>
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
