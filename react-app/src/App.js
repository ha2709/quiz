import React, { useState } from "react";
import Leaderboard from "./components/Leaderboard";
import Login from "./components/Login";
import QuizConnection from "./components/QuizConnection";
import SubmitAnswer from "./components/SubmitAnswer";

function App() {
  const [token, setToken] = useState("");
  const [websocket, setWebSocket] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  const handleWebSocketMessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "leaderboard_update") {
      setLeaderboard(message.data.entries);
    }
  };

  const onConnected = (ws) => {
    ws.onmessage = handleWebSocketMessage;
    setWebSocket(ws);
  };

  return (
    <div className="App">
      {!token && <Login onLoginSuccess={setToken} />}
      {token && !websocket && <QuizConnection token={token} onConnected={onConnected} />}
      {websocket && (
        <>
          <SubmitAnswer websocket={websocket} />
          <Leaderboard leaderboard={leaderboard} />
        </>
      )}
    </div>
  );
}

export default App;
