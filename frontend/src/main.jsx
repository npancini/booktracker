import ReactDOM from "react-dom/client";
import App from "./App";
import React from "react";
import NotesApp from "./NotesApp"

const mountPoint = document.getElementById("react-root");

if (mountPoint) {
  const root = ReactDOM.createRoot(mountPoint);
  root.render(<App />);
}

const rootElement = document.getElementById("status-modal-root");

const rootEl = document.getElementById("notes-root");

if (rootEl) {
  const bookId = rootEl.dataset.bookId;

  ReactDOM.createRoot(rootEl).render(
    <React.StrictMode>
      <NotesApp bookId={bookId} />
    </React.StrictMode>
  );
}