import ReactDOM from "react-dom/client";
import App from "./App";
import React from "react";

const mountPoint = document.getElementById("react-root");

if (mountPoint) {
  const root = ReactDOM.createRoot(mountPoint);
  root.render(<App />);
}

const rootElement = document.getElementById("status-modal-root");
