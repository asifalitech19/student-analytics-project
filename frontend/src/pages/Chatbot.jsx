


import { useEffect, useRef, useState } from "react";

import {
  Bot,
  X,
  Send,
  Sparkles,
  ShieldCheck,
  BarChart3,
  Database,
  Trash2,
  Loader2,
  MessageCircle,
  GraduationCap,
  BookOpen,
  Users,
} from "lucide-react";


const API_URL =
  "http://127.0.0.1:8000/api/chatbot/";


// ============================================================
// QUICK ACTIONS
// ============================================================

const QUICK_ACTIONS = [
  {
    id: "dataset",
    title: "About the Dataset",
    icon: Database,
    query:
      "Give me a concise structured overview of the finalized student dataset, including the number of students, number of columns, CGPA information, demographic information, academic information, and study-behavior information.",
  },

  {
    id: "cgpa",
    title: "Average CGPA",
    icon: GraduationCap,
    query:
      "What is the average CGPA in the dataset? Also tell me the minimum and maximum CGPA.",
  },

  {
    id: "study",
    title: "Study & CGPA",
    icon: BookOpen,
    query:
      "Explain the study-related information available in the dataset and describe the observed CGPA pattern across study-hour groups. Do not claim causation.",
  },

  {
    id: "analytics",
    title: "Student Analytics",
    icon: BarChart3,
    query:
      "Give me the most useful descriptive student analytics available in the dataset, including student count, gender distribution, scholarship distribution, English proficiency, study behavior, and CGPA.",
  },
];


// ============================================================
// CLEAN AI RESPONSE
// ============================================================

function cleanResponse(text) {

  if (!text) {
    return "";
  }

  let cleaned = String(text);

  // ----------------------------------------------------------
  // Remove markdown headings
  // ----------------------------------------------------------

  cleaned = cleaned.replace(
    /^#{1,6}\s*/gm,
    ""
  );

  // ----------------------------------------------------------
  // Normalize markdown bullets
  // ----------------------------------------------------------

  cleaned = cleaned.replace(
    /^\s*[-*+]\s+/gm,
    "• "
  );

  // ----------------------------------------------------------
  // Remove bold / italic markers
  // ----------------------------------------------------------

  cleaned = cleaned.replace(
    /\*\*(.*?)\*\*/g,
    "$1"
  );

  cleaned = cleaned.replace(
    /__(.*?)__/g,
    "$1"
  );

  cleaned = cleaned.replace(
    /\*(.*?)\*/g,
    "$1"
  );

  cleaned = cleaned.replace(
    /_(.*?)_/g,
    "$1"
  );

  // ----------------------------------------------------------
  // Remove inline code markers
  // ----------------------------------------------------------

  cleaned = cleaned.replace(
    /```/g,
    ""
  );

  cleaned = cleaned.replace(
    /`([^`]+)`/g,
    "$1"
  );

  // ----------------------------------------------------------
  // Normalize whitespace
  // ----------------------------------------------------------

  cleaned = cleaned.replace(
    /\n{3,}/g,
    "\n\n"
  );

  return cleaned.trim();
}


// ============================================================
// MESSAGE CONTENT
// ============================================================

function MessageContent({
  content,
}) {

  const cleaned =
    cleanResponse(content);

  if (!cleaned) {
    return null;
  }

  const lines =
    cleaned.split("\n");

  return (
    <div className="space-y-1.5">

      {lines.map(
        (line, index) => {

          const trimmed =
            line.trim();

          if (!trimmed) {
            return (
              <div
                key={index}
                className="h-1"
              />
            );
          }

          // ----------------------------------------------------
          // Bullet
          // ----------------------------------------------------

          if (
            trimmed.startsWith("•")
          ) {

            return (
              <div
                key={index}
                className="
                  flex
                  gap-2
                  items-start
                "
              >

                <span
                  className="
                    mt-1.5
                    text-blue-500
                  "
                >
                  •
                </span>

                <span>
                  {trimmed
                    .substring(1)
                    .trim()}
                </span>

              </div>
            );
          }

          // ----------------------------------------------------
          // Simple heading
          // ----------------------------------------------------

          const isHeading =
            trimmed.length < 90 &&
            !trimmed.endsWith(".") &&
            (
              trimmed.endsWith(":") ||
              index === 0
            );

          if (isHeading) {

            return (
              <div
                key={index}
                className="
                  font-semibold
                  text-slate-800
                  pt-1
                "
              >
                {trimmed.replace(
                  /:$/,
                  ""
                )}
              </div>
            );
          }

          return (
            <div key={index}>
              {trimmed}
            </div>
          );
        }
      )}

    </div>
  );
}


// ============================================================
// CHATBOT
// ============================================================

function Chatbot() {

  const [
    isOpen,
    setIsOpen,
  ] = useState(false);

  const [
    messages,
    setMessages,
  ] = useState([]);

  const [
    question,
    setQuestion,
  ] = useState("");

  const [
    loading,
    setLoading,
  ] = useState(false);

  const messagesEndRef =
    useRef(null);


  // ==========================================================
  // AUTO SCROLL
  // ==========================================================

  useEffect(() => {

    if (!isOpen) {
      return;
    }

    messagesEndRef.current?.scrollIntoView(
      {
        behavior: "smooth",
      }
    );

  }, [
    messages,
    loading,
    isOpen,
  ]);


  // ==========================================================
  // WELCOME
  // ==========================================================

  const createWelcomeMessage =
    () => ({
      id: Date.now(),
      role: "assistant",
      type: "welcome",
      content:
        "Hello! 👋 I am the AI Assistant for the Student Analytics Dashboard. I can help you explore the student dataset, CGPA, study behavior, and descriptive analytics.",
    });


  // ==========================================================
  // OPEN
  // ==========================================================

  const openChat = () => {

    setIsOpen(true);

    if (
      messages.length === 0
    ) {

      setMessages([
        createWelcomeMessage(),
      ]);
    }
  };


  // ==========================================================
  // CLOSE
  // ==========================================================

  const closeChat = () => {

    setIsOpen(false);
  };


  // ==========================================================
  // SEND MESSAGE
  // ==========================================================

  const sendMessage = async ({
    displayText,
    query,
  }) => {

    const userText =
      displayText?.trim();

    const backendQuery =
      query?.trim();

    if (
      !userText ||
      !backendQuery ||
      loading
    ) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: userText,
    };

    const currentConversation = [
      ...messages,
      userMessage,
    ];

    setMessages(
      currentConversation
    );

    setQuestion("");

    setLoading(true);

    try {

      // ------------------------------------------------------
      // Conversation history
      // ------------------------------------------------------

      const conversation =
        currentConversation
          .filter(
            (message) =>
              message.role ===
                "user" ||
              message.role ===
                "assistant"
          )
          .slice(-8)
          .map(
            (message) => ({
              role:
                message.role,
              content:
                message.content,
            })
          );

      // ------------------------------------------------------
      // API
      // ------------------------------------------------------

      const response =
        await fetch(
          API_URL,
          {
            method: "POST",

            headers: {
              Accept:
                "application/json",

              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify({
                question:
                  backendQuery,

                conversation,
              }),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data?.detail ||
            "Unable to process the request."
        );
      }

      // ------------------------------------------------------
      // Backend response
      // ------------------------------------------------------

      const assistantResponse =
        data?.response ||
        data?.answer ||
        "I could not generate a response.";

      const assistantMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content:
          assistantResponse,
      };

      setMessages(
        (previous) => [
          ...previous,
          assistantMessage,
        ]
      );

    } catch (error) {

      console.error(
        "Chatbot request failed:",
        error
      );

      setMessages(
        (previous) => [
          ...previous,
          {
            id:
              Date.now() + 1,

            role:
              "assistant",

            error:
              true,

            content:
              "I could not connect to the local AI assistant. Please make sure FastAPI and Ollama are running.",
          },
        ]
      );

    } finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // QUICK ACTION
  // ==========================================================

  const handleQuickAction =
    (action) => {

      sendMessage({
        displayText:
          action.title,

        query:
          action.query,
      });
    };


  // ==========================================================
  // CUSTOM QUESTION
  // ==========================================================

  const handleCustomQuestion =
    () => {

      const text =
        question.trim();

      if (!text) {
        return;
      }

      sendMessage({
        displayText:
          text,

        query:
          text,
      });
    };


  // ==========================================================
  // ENTER KEY
  // ==========================================================

  const handleKeyDown =
    (event) => {

      if (
        event.key ===
          "Enter" &&
        !event.shiftKey
      ) {

        event.preventDefault();

        handleCustomQuestion();
      }
    };


  // ==========================================================
  // CLEAR CHAT
  // ==========================================================

  const clearChat = () => {

    setMessages([
      createWelcomeMessage(),
    ]);

    setQuestion("");
  };


  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <>
      {/* =====================================================
          FLOATING BUTTON
      ====================================================== */}

      {!isOpen && (

        <button
          onClick={openChat}
          aria-label="Open AI Assistant"
          className="
            fixed
            bottom-6
            right-6
            z-50
            w-16
            h-16
            rounded-full
            bg-blue-600
            text-white
            shadow-xl
            shadow-blue-200
            flex
            items-center
            justify-center
            hover:bg-blue-700
            hover:scale-105
            transition-all
            duration-200
            group
          "
        >

          <MessageCircle
            size={28}
            strokeWidth={2}
          />

          <span
            className="
              absolute
              top-1
              right-1
              w-4
              h-4
              rounded-full
              bg-emerald-500
              border-2
              border-white
            "
          />

          <span
            className="
              absolute
              right-20
              whitespace-nowrap
              bg-slate-800
              text-white
              text-xs
              px-3
              py-2
              rounded-lg
              opacity-0
              group-hover:opacity-100
              transition
              pointer-events-none
            "
          >
            AI Assistant
          </span>

        </button>
      )}


      {/* =====================================================
          CHAT WINDOW
      ====================================================== */}

      {isOpen && (

        <div
          className="
            fixed
            bottom-6
            right-6
            z-50
            w-[420px]
            max-w-[calc(100vw-32px)]
            h-[680px]
            max-h-[calc(100vh-48px)]
            bg-white
            border
            border-slate-200
            rounded-2xl
            shadow-2xl
            overflow-hidden
            flex
            flex-col
          "
        >

          {/* =================================================
              HEADER
          ================================================== */}

          <div
            className="
              px-5
              py-4
              bg-white
              border-b
              border-slate-100
              flex
              items-center
              justify-between
            "
          >

            <div className="
              flex
              items-center
              gap-3
            ">

              <div
                className="
                  w-10
                  h-10
                  rounded-xl
                  bg-blue-600
                  flex
                  items-center
                  justify-center
                "
              >

                <Bot
                  size={21}
                  className="text-white"
                />

              </div>

              <div>

                <h2 className="
                  font-bold
                  text-slate-800
                  text-sm
                ">
                  AI Student Analytics
                </h2>

                <div className="
                  flex
                  items-center
                  gap-1.5
                  mt-0.5
                ">

                  <span
                    className="
                      w-2
                      h-2
                      rounded-full
                      bg-emerald-500
                    "
                  />

                  <span className="
                    text-[11px]
                    text-slate-500
                  ">
                    Local AI Assistant
                  </span>

                </div>

              </div>

            </div>


            <div className="
              flex
              items-center
              gap-1
            ">

              <button
                onClick={clearChat}
                title="Clear chat"
                className="
                  w-8
                  h-8
                  rounded-lg
                  flex
                  items-center
                  justify-center
                  text-slate-400
                  hover:text-slate-700
                  hover:bg-slate-100
                  transition
                "
              >
                <Trash2
                  size={16}
                />
              </button>

              <button
                onClick={closeChat}
                title="Close"
                className="
                  w-8
                  h-8
                  rounded-lg
                  flex
                  items-center
                  justify-center
                  text-slate-400
                  hover:text-slate-700
                  hover:bg-slate-100
                  transition
                "
              >
                <X
                  size={18}
                />
              </button>

            </div>

          </div>


          {/* =================================================
              CHAT CONTENT
          ================================================== */}

          <div
            className="
              flex-1
              overflow-y-auto
              bg-slate-50/60
              p-4
            "
          >

            {/* ------------------------------------------------
                WELCOME
            ------------------------------------------------- */}

            {messages.length === 1 &&
              messages[0]?.type ===
                "welcome" && (

              <div className="mb-5">

                <div className="
                  flex
                  gap-3
                ">

                  <div
                    className="
                      w-8
                      h-8
                      flex-shrink-0
                      rounded-lg
                      bg-blue-600
                      flex
                      items-center
                      justify-center
                    "
                  >

                    <Bot
                      size={17}
                      className="text-white"
                    />

                  </div>

                  <div
                    className="
                      bg-white
                      border
                      border-slate-200
                      rounded-2xl
                      rounded-tl-sm
                      px-4
                      py-3
                      shadow-sm
                    "
                  >

                    <p className="
                      text-sm
                      text-slate-700
                      leading-6
                    ">
                      Hello! 👋
                    </p>

                    <p className="
                      text-sm
                      text-slate-700
                      leading-6
                      mt-1
                    ">
                      I am your AI Assistant for
                      the Student Analytics Dashboard.
                    </p>

                    <p className="
                      text-xs
                      text-slate-500
                      leading-5
                      mt-2
                    ">
                      Ask me about the dataset,
                      CGPA, study behavior,
                      scholarship, or student
                      analytics.
                    </p>

                  </div>

                </div>

              </div>
            )}


            {/* =================================================
                QUICK ACTIONS
            ================================================== */}

            {messages.length <= 1 && (

              <div className="mb-5">

                <div className="
                  flex
                  items-center
                  gap-2
                  mb-3
                ">

                  <Sparkles
                    size={15}
                    className="text-blue-600"
                  />

                  <span className="
                    text-xs
                    font-semibold
                    text-slate-600
                  ">
                    Explore the dashboard
                  </span>

                </div>


                <div className="space-y-2">

                  {QUICK_ACTIONS.map(
                    (action) => {

                      const Icon =
                        action.icon;

                      return (

                        <button
                          key={action.id}
                          onClick={() =>
                            handleQuickAction(
                              action
                            )
                          }
                          disabled={loading}
                          className="
                            w-full
                            text-left
                            bg-white
                            border
                            border-slate-200
                            rounded-xl
                            px-3
                            py-3
                            flex
                            items-center
                            gap-3
                            hover:border-blue-300
                            hover:bg-blue-50/50
                            transition
                            disabled:opacity-50
                          "
                        >

                          <div
                            className="
                              w-9
                              h-9
                              rounded-lg
                              bg-blue-100
                              flex
                              items-center
                              justify-center
                              flex-shrink-0
                            "
                          >

                            <Icon
                              size={18}
                              className="
                                text-blue-600
                              "
                            />

                          </div>

                          <div>

                            <p className="
                              text-sm
                              font-semibold
                              text-slate-700
                            ">
                              {action.title}
                            </p>

                            <p className="
                              text-[11px]
                              text-slate-400
                              mt-0.5
                            ">
                              Explore this topic
                            </p>

                          </div>

                        </button>
                      );
                    }
                  )}

                </div>

              </div>
            )}


            {/* =================================================
                MESSAGES
            ================================================== */}

            {messages
              .filter(
                (_, index) =>
                  !(
                    index === 0 &&
                    messages[0]?.type ===
                      "welcome"
                  )
              )
              .map(
                (message) => {

                  const isUser =
                    message.role ===
                    "user";

                  return (

                    <div
                      key={message.id}
                      className={`
                        flex
                        gap-2.5
                        mb-4
                        ${
                          isUser
                            ? "justify-end"
                            : "justify-start"
                        }
                      `}
                    >

                      {!isUser && (

                        <div
                          className="
                            w-8
                            h-8
                            flex-shrink-0
                            rounded-lg
                            bg-blue-600
                            flex
                            items-center
                            justify-center
                          "
                        >

                          <Bot
                            size={16}
                            className="text-white"
                          />

                        </div>
                      )}


                      <div
                        className={`
                          max-w-[82%]
                          px-3.5
                          py-2.5
                          rounded-2xl
                          text-sm
                          leading-6
                          ${
                            isUser
                              ? `
                                bg-blue-600
                                text-white
                                rounded-tr-sm
                              `
                              : message.error
                              ? `
                                bg-red-50
                                border
                                border-red-100
                                text-red-700
                                rounded-tl-sm
                              `
                              : `
                                bg-white
                                border
                                border-slate-200
                                text-slate-700
                                rounded-tl-sm
                                shadow-sm
                              `
                          }
                        `}
                      >

                        {isUser
                          ? message.content
                          : (
                            <MessageContent
                              content={
                                message.content
                              }
                            />
                          )}

                      </div>

                    </div>
                  );
                }
              )}


            {/* =================================================
                LOADING
            ================================================== */}

            {loading && (

              <div className="
                flex
                gap-2.5
                mb-4
              ">

                <div
                  className="
                    w-8
                    h-8
                    rounded-lg
                    bg-blue-600
                    flex
                    items-center
                    justify-center
                    flex-shrink-0
                  "
                >

                  <Bot
                    size={16}
                    className="text-white"
                  />

                </div>


                <div
                  className="
                    bg-white
                    border
                    border-slate-200
                    rounded-2xl
                    rounded-tl-sm
                    px-3.5
                    py-3
                    shadow-sm
                  "
                >

                  <div className="
                    flex
                    items-center
                    gap-2
                    text-xs
                    text-slate-500
                  ">

                    <Loader2
                      size={15}
                      className="
                        animate-spin
                        text-blue-600
                      "
                    />

                    Analyzing student data...

                  </div>

                </div>

              </div>
            )}


            <div
              ref={messagesEndRef}
            />

          </div>


          {/* =================================================
              INPUT
          ================================================== */}

          <div
            className="
              p-3
              bg-white
              border-t
              border-slate-100
            "
          >

            <div
              className="
                flex
                items-end
                gap-2
                border
                border-slate-200
                rounded-xl
                p-1.5
                focus-within:border-blue-400
                focus-within:ring-2
                focus-within:ring-blue-50
                transition
              "
            >

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(
                    event.target.value
                  )
                }
                onKeyDown={
                  handleKeyDown
                }
                disabled={loading}
                rows={1}
                placeholder="Ask about student data..."
                className="
                  flex-1
                  resize-none
                  border-0
                  outline-none
                  px-2
                  py-2
                  text-sm
                  text-slate-700
                  placeholder:text-slate-400
                  bg-transparent
                  max-h-24
                "
              />


              <button
                onClick={
                  handleCustomQuestion
                }
                disabled={
                  loading ||
                  !question.trim()
                }
                className="
                  w-9
                  h-9
                  rounded-lg
                  bg-blue-600
                  text-white
                  flex
                  items-center
                  justify-center
                  hover:bg-blue-700
                  transition
                  disabled:opacity-40
                  disabled:cursor-not-allowed
                "
              >

                {loading ? (

                  <Loader2
                    size={17}
                    className="animate-spin"
                  />

                ) : (

                  <Send
                    size={17}
                  />

                )}

              </button>

            </div>


            {/* ------------------------------------------------
                PRIVACY FOOTER
            ------------------------------------------------- */}

            <div className="
              flex
              items-center
              justify-center
              gap-1.5
              mt-2
            ">

              <ShieldCheck
                size={12}
                className="text-emerald-500"
              />

              <span className="
                text-[10px]
                text-slate-400
              ">
                Local AI • Privacy-first analytics
              </span>

            </div>

          </div>

        </div>
      )}
    </>
  );
}

export default Chatbot;