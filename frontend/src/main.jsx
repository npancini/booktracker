import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import NotesApp from "./NotesApp";

ReactDOM.createRoot(document.getElementById("react-root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

const notesRoot = document.getElementById("notes-root");

if (notesRoot) {
  const bookId = notesRoot.dataset.bookId;

  ReactDOM.createRoot(notesRoot).render(
    <React.StrictMode>
      <NotesApp bookId={bookId} />
    </React.StrictMode>
  );
}