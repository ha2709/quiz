import React, { useState } from "react";

const SubmitAnswer = ({ websocket }) => {
  const [questionId, setQuestionId] = useState("");
  const [selectedOption, setSelectedOption] = useState("");

  const submitAnswer = () => {
    if (!questionId || !selectedOption) {
      alert("Please fill out both Question ID and Option.");
      return;
    }

    websocket.send(
      JSON.stringify({
        action: "submit_answer",
        question_id: questionId,
        selected_option: selectedOption,
      })
    );

    setQuestionId("");
    setSelectedOption("");
  };

  return (
    <div style={{ margin: "20px 0", textAlign: "center" }}>
      <h2>Submit Your Answer</h2>
      <input
        type="text"
        placeholder="Question ID"
        value={questionId}
        onChange={(e) => setQuestionId(e.target.value)}
        style={{ margin: "5px", padding: "10px", width: "200px" }}
      />
      <input
        type="text"
        placeholder="Option (A, B, C, D)"
        value={selectedOption}
        onChange={(e) => setSelectedOption(e.target.value)}
        style={{ margin: "5px", padding: "10px", width: "200px" }}
      />
      <button
        onClick={submitAnswer}
        style={{
          margin: "5px",
          padding: "10px 20px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Submit
      </button>
    </div>
  );
};

export default SubmitAnswer;
