import React from "react"
import ReactDOM from "react-dom/client"
import NotesApp from "./NotesApp"

const rootEl = document.getElementById("notes-root")

console.log("rootEl:", rootEl)

const bookId = rootEl.dataset.bookId

console.log("bookId:", bookId)

ReactDOM.createRoot(rootEl).render(
  <React.StrictMode>
    <NotesApp bookId={bookId} />
  </React.StrictMode>
)
