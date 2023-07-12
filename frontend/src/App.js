import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";
import Main from "./pages/Main";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Main />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
