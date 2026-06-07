import { useState } from "react"

export default function EditNoteModal({ note, onClose, onUpdated }) {
  const [content, setContent] = useState(note.content)
  const [pageNumber, setPageNumber] = useState(note.page_number || "")
  const [chapter, setChapter] = useState(note.chapter || "")

  const handleSubmit = async (e) => {
    e.preventDefault()

    const response = await fetch(
      `/books/api/notes/${note.id}/edit/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          content,
          page_number: pageNumber,
          chapter,
        }),
      }
    )

    if (response.ok) {
      const updatedNote = await response.json()
      onUpdated(updatedNote)
    } else {
      alert("Error updating note")
    }
  }

  function getCSRFToken() {
    const name = "csrftoken="
    const decodedCookie = decodeURIComponent(document.cookie)
    const ca = decodedCookie.split(";")
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim()
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length)
      }
    }
    return ""
  }

  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <h2>Edit Note</h2>

        <form onSubmit={handleSubmit}>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />

          <br /><br />

          <input
            type="number"
            value={pageNumber}
            onChange={(e) => setPageNumber(e.target.value)}
            placeholder="Page"
          />

          <br /><br />

          <input
            type="text"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
            placeholder="Chapter"
          />

          <br /><br />

          <button type="submit">Save</button>
          <button type="button" onClick={onClose}>
            Cancel
          </button>
        </form>
      </div>
    </div>
  )
}

const overlayStyle = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  backgroundColor: "rgba(0,0,0,0.4)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
}

const modalStyle = {
  background: "white",
  padding: "20px",
  borderRadius: "8px",
  minWidth: "300px",
}
