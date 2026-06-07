import { useEffect, useState } from "react"
import AddNoteModal from "./AddNoteModal"
import EditNoteModal from "./EditNoteModal"

export default function NotesApp({ bookId }) {
  const [notes, setNotes] = useState([])
  const [editingNote, setEditingNote] = useState(null)

  const handleDelete = async (noteId) => {
    const response = await fetch(`/books/api/notes/${noteId}/delete/`, {
        method: "POST",
        headers: {
        "X-CSRFToken": getCSRFToken(),
        },
    })

    if (response.ok) {
        setNotes(notes.filter((note) => note.id !== noteId))
    } else {
        alert("Error deleting note")
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


  useEffect(() => {
    fetch(`/books/api/books/${bookId}/notes/`)
      .then(res => res.json())
      .then(data => setNotes(data))
  }, [bookId])

  const handleNoteAdded = (newNote) => {
    setNotes(prev => [newNote, ...prev])
  }

  return (
    <div>
      <AddNoteModal bookId={bookId} onNoteAdded={handleNoteAdded} />

      <h3>Notes</h3>

      {notes.map(note => (
        <div key={note.id} style={noteStyle}>
          {note.chapter && <p><strong>Chapter:</strong> {note.chapter}</p>}
          {note.page_number && <p><strong>Page:</strong> {note.page_number}</p>}
          <p>{note.content}</p>
          <button onClick={() => setEditingNote(note)}>
            Edit
          </button>
          <button onClick={() => handleDelete(note.id)}>
            Delete
          </button>
        </div>
      ))}

      {editingNote && (
  <EditNoteModal
    note={editingNote}
    onClose={() => setEditingNote(null)}
    onUpdated={(updatedNote) => {
    setNotes((prevNotes) =>
        prevNotes.map((n) =>
        n.id === updatedNote.id ? updatedNote : n
        )
    )
    setEditingNote(null)
    }}
  />
)}
    </div>
  )
}

const noteStyle = {
  background: "black",
  padding: "10px",
  borderRadius: "8px",
  marginBottom: "10px"
}
