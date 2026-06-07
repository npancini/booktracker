import { useState } from "react";

export default function AddBookModal({ onBookAdded }) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("/books/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ title, author }),
    });

    if (response.ok) {
      const newBook = await response.json();

      // 👇 tell parent (App) about new book
      onBookAdded(newBook);

      // reset form + close modal
      setTitle("");
      setAuthor("");
      setIsOpen(false);

    } else {
      alert("Error adding book");
    }
  };

  function getCSRFToken() {
    return document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
  }

  return (
    <>
      <button onClick={() => setIsOpen(true)}>
        + Add Book
      </button>

      {isOpen && (
        <div style={overlayStyle}>
          <div style={modalStyle}>
            <h2>Add Book</h2>

            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
              <br /><br />
              <input
                type="text"
                placeholder="Author"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                required
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
  );
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
  zIndex: 9999,
};

const modalStyle = {
  background: "white",
  padding: "20px",
  borderRadius: "8px",
  minWidth: "300px",
};
