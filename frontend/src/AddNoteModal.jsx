import { useState } from "react"

export default function AddNoteModal({ bookId, onNoteAdded }) {
  const [isOpen, setIsOpen] = useState(false)
  const [content, setContent] = useState("")
  const [pageNumber, setPageNumber] = useState("")
  const [chapter, setChapter] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()

    const response = await fetch(
      `/books/api/books/${bookId}/notes/add/`,
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
      const newNote = await response.json()
      onNoteAdded(newNote)

      setContent("")
      setPageNumber("")
      setChapter("")
      setIsOpen(false)
    } else {
      alert("Error adding note")
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
    <>
      <button onClick={() => setIsOpen(true)}>
        + Add Note
      </button>

      {isOpen && (
        <div style={overlayStyle}>
          <div style={modalStyle}>
            <h2>Add Note</h2>

            <form onSubmit={handleSubmit}>
              <textarea
                placeholder="Write your note..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
              />
              <br /><br />

              <input
                type="number"
                placeholder="Page (optional)"
                value={pageNumber}
                onChange={(e) => setPageNumber(e.target.value)}
              />
              <br /><br />

              <input
                type="text"
                placeholder="Chapter (optional)"
                value={chapter}
                onChange={(e) => setChapter(e.target.value)}
              />
              <br /><br />

              <button type="submit">Save</button>
              <button type="button" onClick={() => setIsOpen(false)}>
                Cancel
              </button>
            </form>
          </div>
        </div>
      )}
    </>
    
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
