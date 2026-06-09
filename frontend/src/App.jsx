import { useEffect, useState } from "react"
import AddBookModal from "./AddBookModal"
import NotesApp from "./NotesApp";

export default function App() {
  const [books, setBooks] = useState([])

  // Fetch books when component mounts
  useEffect(() => {
    fetch("/books/api/books/")
      .then(res => res.json())
      .then(data => setBooks(data))
      .catch(err => console.error("Error fetching books:", err))
  }, [])

  // Function to add new book to state
  const handleBookAdded = (newBook) => {
    setBooks(prevBooks => [...prevBooks, newBook])
  }

  return (
      <div style={{ marginBottom: "20px" }}>
        <AddBookModal onBookAdded={handleBookAdded} />
      </div>
  )
}

export default function App() {
  const notesRoot = document.getElementById("notes-root");

  const bookId = notesRoot?.dataset?.bookId;

  return (
    <>
      {notesRoot && <NotesApp bookId={bookId} />}
    </>
  );
}