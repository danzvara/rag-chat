import { JSONValue } from "ai";
import React from "react";

interface MessageProps {
  text: string;
  isUser: boolean;
  annotations: JSONValue[];
}

const Message: React.FC<MessageProps> = React.memo(
  ({ text, isUser, annotations }) => {
    const messageAnnotation = annotations[0];
    const hasSourcePath =
      messageAnnotation &&
      typeof messageAnnotation == "object" &&
      "source_path" in messageAnnotation;
    const hasToolName =
      messageAnnotation &&
      typeof messageAnnotation == "object" &&
      "tool_name" in messageAnnotation;

    const sourcePath = hasSourcePath
      ? (messageAnnotation["source_path"] as string)
      : undefined;
    const toolName = hasToolName
      ? (messageAnnotation["tool_name"] as string)
      : undefined;

    return (
      <div style={{ textAlign: isUser ? "right" : "left", margin: "8px" }}>
        <div
          style={{
            backgroundColor: isUser ? "#DCF8C6" : "#b8e3fc",
            padding: "8px",
            borderRadius: "8px",
          }}
        >
          <pre
            style={{
              whiteSpace: "pre-wrap",
              marginBottom: sourcePath ? "10px" : "0",
            }}
          >
            {text}
          </pre>
          {sourcePath && (
            <a href={sourcePath} target="_blank" rel="noopener noreferrer">
              View Source
            </a>
          )}
          {toolName && <div>Tool: {toolName}</div>}
        </div>
      </div>
    );
  }
);

export default Message;
