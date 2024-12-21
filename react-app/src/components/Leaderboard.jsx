import React from "react";

const Leaderboard = ({ leaderboard }) => {
  if (leaderboard.length === 0) {
    return <p>No leaderboard data available yet.</p>;
  }

  return (
    <div style={{ marginTop: "20px", textAlign: "center" }}>
      <h2>Leaderboard</h2>
      {leaderboard.map((entry, index) => (
        <div key={index} style={{ padding: "5px" }}>
          {index + 1}. {entry.username} - {entry.score} points
        </div>
      ))}
    </div>
  );
};

export default Leaderboard;
