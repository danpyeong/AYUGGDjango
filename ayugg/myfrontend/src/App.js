import React, { useState, useEffect } from 'react';
function App() {
  const [items, setItems] = useState([]);
  const [gameName, setGameName] = useState('');

  useEffect(() => {
    if (gameName) {
      fetch(`http://localhost:8000/search/${gameName}/`)
        .then(response => response.json())
        .then(data => setItems(data));
    } else {
      fetch('http://localhost:8000/search/Hide%20on%20bush')
        .then(response => response.json())
        .then(data => setItems(data));
    }
  }, [gameName]);

  return (
    <div className="App">
      <h1>Items</h1>
      <ul>
        {items.map(item => (
          <li key={item['id']}>{item['gameName']} #{item['tagLine']}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

