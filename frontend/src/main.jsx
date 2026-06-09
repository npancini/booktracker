import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import NotesApp from "./NotesApp";

const reactRoot = document.getElementById("react-root");

if (reactRoot) {
  ReactDOM.createRoot(reactRoot).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

const notesRoot = document.getElementById("notes-root");

if (notesRoot) {
  const bookId = notesRoot.dataset.bookId;

  ReactDOM.createRoot(notesRoot).render(
    <React.StrictMode>
      <NotesApp bookId={bookId} />
    </React.StrictMode>
  );
}