import React, { useState } from "react";

const QuizApp = () => {
  const [quizId, setQuizId] = useState("");
  const [username, setUsername] = useState("");
  const [websocket, setWebSocket] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [questionId, setQuestionId] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [isConnected, setIsConnected] = useState(false);

  // Handle WebSocket Connection
  const connectWebSocket = () => {
    if (!quizId || !username) {
      alert("Please enter a quiz ID and username.");
      return;
    }

    const ws = new WebSocket(`ws://localhost:8000/quiz/${quizId}`);
    ws.onopen = () => {
      console.log("Connected to WebSocket");
      setIsConnected(true);

      // Send join action
      ws.send(
        JSON.stringify({
          action: "join",
          user_id: username,
        })
      );
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Message from server:", message);

      if (message.type === "leaderboard_update") {
        setLeaderboard(message.data.entries);
      }
    };

    ws.onclose = () => {
      console.log("Disconnected from WebSocket");
      setIsConnected(false);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("WebSocket connection failed. Please try again.");
    };

    setWebSocket(ws);
  };

  // Handle answer submission
  const submitAnswer = () => {
    if (!questionId || !selectedOption) {
      alert("Please select a question and an option.");
      return;
    }

    websocket.send(
      JSON.stringify({
        action: "submit_answer",
        user_id: username,
        question_id: questionId,
        selected_option: selectedOption,
      })
    );

    setQuestionId("");
    setSelectedOption("");
  };

  // Render the leaderboard
  const renderLeaderboard = () => {
    if (leaderboard.length === 0) {
      return <p>No leaderboard data available yet.</p>;
    }

    return leaderboard.map((entry, index) => (
      <div key={index} className="leaderboard-entry">
        {index + 1}. {entry.username} - {entry.score} points
      </div>
    ));
  };

  return (
    <div className="quiz-app" style={{ padding: "20px", textAlign: "center" }}>
      <h1>Real-Time Quiz</h1>

      {!isConnected && (
        <div className="connection-form" style={{ margin: "20px 0" }}>
          <input
            type="text"
            placeholder="Enter Quiz ID"
            value={quizId}
            onChange={(e) => setQuizId(e.target.value)}
            style={{ margin: "5px", padding: "10px", width: "200px" }}
          />
          <input
            type="text"
            placeholder="Enter Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ margin: "5px", padding: "10px", width: "200px" }}
          />
          <button
            onClick={connectWebSocket}
            disabled={isConnected}
            style={{
              margin: "5px",
              padding: "10px 20px",
              backgroundColor: "#4CAF50",
              color: "white",
              border: "none",
              cursor: "pointer",
            }}
          >
            Join Quiz
          </button>
        </div>
      )}

      {isConnected && (
        <>
          <div className="question-form" style={{ margin: "20px 0" }}>
            <h2>Submit Your Answer</h2>
            <input
              type="text"
              placeholder="Enter Question ID"
              value={questionId}
              onChange={(e) => setQuestionId(e.target.value)}
              style={{ margin: "5px", padding: "10px", width: "200px" }}
            />
            <input
              type="text"
              placeholder="Enter Your Option (A, B, C, D)"
              value={selectedOption}
              onChange={(e) => setSelectedOption(e.target.value)}
              style={{ margin: "5px", padding: "10px", width: "200px" }}
            />
            <button
              onClick={submitAnswer}
              style={{
                margin: "5px",
                padding: "10px 20px",
                backgroundColor: "#2196F3",
                color: "white",
                border: "none",
                cursor: "pointer",
              }}
            >
              Submit Answer
            </button>
          </div>

          <div className="leaderboard" style={{ marginTop: "20px" }}>
            <h2>Leaderboard</h2>
            {renderLeaderboard()}
          </div>
        </>
      )}
    </div>
  );
};

export default QuizApp;
