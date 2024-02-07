import React from "react";

const InfoCard = React.memo(() => {
  return (
    <div
      style={{
        backgroundColor: "beige",
        marginBottom: "40px",
        padding: "16px",
      }}
    >
      <h1>Chat with documentation 🦜</h1>
      <ul style={{ lineHeight: 2 }}>
        <li>
          Ask questions about{" "}
          <a
            href="https://ibm.github.io/ibm-generative-ai/main/index.html"
            target="_blank"
          >
            IBM Generative AI Python SDK documentation
          </a>
        </li>
        <li>
          The agent remembers the conversation context and includes link to the
          sources where relevant.
        </li>
        <li>
          It can also execute Python code and answer questions using Google
          search.
        </li>
        <li>
          The agent will let you know which tool it used to answer your
          question, if any.
        </li>
        <li>
          Check out the implementation in my{" "}
          <a href="https://github.com/danzvara/rag-chat" target="_blank">
            Github repo!
          </a>
        </li>
      </ul>
    </div>
  );
});

export default InfoCard;
