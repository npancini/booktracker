# Book Tracker

A personal web app to track books you've read, organize notes, and visualize your reading habits over time. Built using Python and Flask, this CRUD application focuses on backend logic and user experience.

## Features

- User authentication (signup, login, logout)
- Add, edit, and delete books
- Track reading status (reading, finished)
- Timestamped notes for each book
- Reading statistics chart (books finished per month)
- Clean UI built with Jinja2 templates and HTML/CSS

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML/CSS
- Chart.js (for data visualization)

## Project Structure

```
booktracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── run.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/npancini/booktracker.git
   cd booktracker
   ```

2. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   python run.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/`

## Demo

 Vimeo walkthrough: https://vimeo.com/1095446913

## Future Improvements

- Password reset via email
- Tags or categories for books
- Export notes to PDF
- Mobile-friendly responsive design
