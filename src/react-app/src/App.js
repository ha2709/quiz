import React from 'react';
import './App.css';
import QuizApp from './components/QuizApp'; // Import QuizApp from the components folder

function App() {
  return (
    <div className="App">
      <header className="">
        <h1>Welcome to the Quiz App</h1>
      </header>
      <main>
        <QuizApp /> {/* Add the QuizApp component */}
      </main>
    </div>
  );
}

export default App;
