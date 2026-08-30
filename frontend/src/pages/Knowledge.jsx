import { useState } from "react";

import {
  MessageCircle,
  Send,
  Loader2,
  User,
  Bot,
  Sparkles,
  Trash2,
  Leaf,
  CloudSun,
  Droplets,
  Bug,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function Knowledge() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  /* =====================================================
     ASK AI
  ===================================================== */

  const askQuestion = async (text = question) => {

    const userQuestion = text.trim();

    if (!userQuestion) {
      return;
    }

    setError("");

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: userQuestion,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setQuestion("");

    setLoading(true);

    try {

      const response = await fetch(
        `${API_BASE_URL}/knowledge/ask`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: userQuestion,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to get an answer from the AI Knowledge Agent."
        );

      }

      /*
       * Support several possible backend response formats.
       */

      const answer =
        data.answer ||
        data.response ||
        data.result ||
        data.message ||
        "I could not generate an answer.";

      const botMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: answer,
      };

      setMessages((previous) => [
        ...previous,
        botMessage,
      ]);

    } catch (err) {

      console.error(
        "Knowledge Agent error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to the AI Knowledge Agent."
      );

    } finally {

      setLoading(false);

    }
  };


  /* =====================================================
     FORM
  ===================================================== */

  const handleSubmit = (event) => {

    event.preventDefault();

    askQuestion();

  };


  /* =====================================================
     CLEAR CHAT
  ===================================================== */

  const clearChat = () => {

    setMessages([]);

    setError("");

  };


  /* =====================================================
     QUICK QUESTIONS
  ===================================================== */

  const quickQuestions = [

    {
      icon: <CloudSun size={16} />,
      title: "Weather",
      question:
        "What weather conditions should farmers watch before irrigating their crops?",
    },

    {
      icon: <Droplets size={16} />,
      title: "Irrigation",
      question:
        "How can I decide when my crop needs irrigation?",
    },

    {
      icon: <Bug size={16} />,
      title: "Crop disease",
      question:
        "What are common signs of crop disease and how should I respond?",
    },

    {
      icon: <Leaf size={16} />,
      title: "Crop care",
      question:
        "What are some important practices for maintaining healthy crops?",
    },

  ];


  return (

    <div className="knowledge-page agent-page">


      {/* =================================================
          HEADER
      ================================================= */}

      <section className="agent-page-header">

        <div>

          <div className="agent-eyebrow">

            <MessageCircle size={14} />

            AI KNOWLEDGE ASSISTANT

          </div>

          <h1>
            Ask your farming questions
          </h1>

          <p>
            Get practical agricultural guidance
            using AgriSphere's AI knowledge system.
          </p>

        </div>

        <div className="agent-header-icon">

          <Sparkles size={31} />

        </div>

      </section>


      {/* =================================================
          CHAT CARD
      ================================================= */}

      <section className="knowledge-chat-card">


        {/* CHAT HEADER */}

        <div className="knowledge-chat-header">

          <div className="knowledge-bot-avatar">

            <Bot size={20} />

          </div>

          <div>

            <h2>
              AgriSphere AI Assistant
            </h2>

            <p>
              Ask questions about farming,
              crops, soil, weather and crop care.
            </p>

          </div>


          {messages.length > 0 && (

            <button
              type="button"
              className="knowledge-clear-button"
              onClick={clearChat}
              title="Clear conversation"
            >

              <Trash2 size={15} />

              Clear

            </button>

          )}

        </div>


        {/* =================================================
            QUICK QUESTIONS
        ================================================= */}

        {messages.length === 0 && (

          <div className="knowledge-welcome">

            <div className="knowledge-welcome-icon">

              <Sparkles size={22} />

            </div>

            <h2>
              How can I help you today?
            </h2>

            <p>
              Ask a question or choose one of
              the common farming topics below.
            </p>


            <div className="knowledge-quick-grid">

              {quickQuestions.map(
                (item, index) => (

                  <button
                    type="button"
                    key={index}
                    className="knowledge-quick-card"
                    onClick={() =>
                      askQuestion(
                        item.question
                      )
                    }
                  >

                    <span className="knowledge-quick-icon">

                      {item.icon}

                    </span>

                    <span>

                      <strong>
                        {item.title}
                      </strong>

                      <small>
                        {item.question}
                      </small>

                    </span>

                  </button>

                )
              )}

            </div>

          </div>

        )}


        {/* =================================================
            MESSAGES
        ================================================= */}

        {messages.length > 0 && (

          <div className="knowledge-messages">

            {messages.map((message) => (

              <div
                key={message.id}
                className={`knowledge-message ${
                  message.role === "user"
                    ? "knowledge-user-message"
                    : "knowledge-ai-message"
                }`}
              >

                <div className="knowledge-message-avatar">

                  {message.role === "user" ? (

                    <User size={15} />

                  ) : (

                    <Bot size={15} />

                  )}

                </div>


                <div className="knowledge-message-content">

                  <span className="knowledge-message-label">

                    {message.role === "user"
                      ? "You"
                      : "AgriSphere AI"}

                  </span>

                  <p>
                    {message.content}
                  </p>

                </div>

              </div>

            ))}


            {loading && (

              <div className="knowledge-message knowledge-ai-message">

                <div className="knowledge-message-avatar">

                  <Bot size={15} />

                </div>

                <div className="knowledge-message-content">

                  <span className="knowledge-message-label">
                    AgriSphere AI
                  </span>

                  <div className="knowledge-thinking">

                    <Loader2
                      size={14}
                      className="spin"
                    />

                    Thinking...

                  </div>

                </div>

              </div>

            )}

          </div>

        )}


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (

          <div className="agent-error knowledge-error">

            <span>
              {error}
            </span>

          </div>

        )}


        {/* =================================================
            INPUT
        ================================================= */}

        <form
          className="knowledge-input-area"
          onSubmit={handleSubmit}
        >

          <div className="knowledge-input-wrapper">

            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(
                  event.target.value
                )
              }
              placeholder="Ask something about your farm..."
              rows={1}
              disabled={loading}
              onKeyDown={(event) => {

                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {

                  event.preventDefault();

                  handleSubmit(event);

                }

              }}
            />

            <button
              type="submit"
              disabled={
                loading ||
                !question.trim()
              }
              className="knowledge-send-button"
            >

              {loading ? (

                <Loader2
                  size={17}
                  className="spin"
                />

              ) : (

                <Send size={17} />

              )}

            </button>

          </div>

          <span className="knowledge-input-hint">

            Press Enter to send • Shift + Enter for a new line

          </span>

        </form>

      </section>

    </div>

  );
}

export default Knowledge;