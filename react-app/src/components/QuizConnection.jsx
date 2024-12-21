import React, { useState } from "react";

const QuizConnection = ({ token, onConnected }) => {
  const [quizId, setQuizId] = useState("");

  const connectToQuiz = () => {
    if (!quizId) {
      alert("Please enter a Quiz ID.");
      return;
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/${quizId}`);
    ws.onopen = () => {
      console.log("Connected to WebSocket");
      ws.send(
        JSON.stringify({
          action: "join",
          token,
        })
      );
      onConnected(ws); // Pass the WebSocket instance back to the parent
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("WebSocket connection failed.");
    };
  };

  return (
    <div style={{ margin: "20px 0", textAlign: "center" }}>
      <h2>Join a Quiz</h2>
      <input
        type="text"
        placeholder="Enter Quiz ID"
        value={quizId}
        onChange={(e) => setQuizId(e.target.value)}
        style={{ margin: "5px", padding: "10px", width: "200px" }}
      />
      <button
        onClick={connectToQuiz}
        style={{
          margin: "5px",
          padding: "10px 20px",
          backgroundColor: "#2196F3",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Join Quiz
      </button>
    </div>
  );
};

export default QuizConnection;
