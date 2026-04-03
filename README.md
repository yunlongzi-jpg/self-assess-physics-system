[README.md](https://github.com/user-attachments/files/26400359/README.md)
# Physics Quiz 🧪

An interactive web-based physics quiz application built with Flask. Questions are categorized into three difficulty levels — Easy, Medium, and Hard — and cover topics such as mechanics, waves, gravitation, and rotational dynamics.

## Features

- 📚 Multiple difficulty levels: Easy / Medium / Hard
- 🎲 Randomly selected questions each round
- 🖼️ Image-based questions and answer options
- 📊 Per-user score tracking with live leaderboard
- 🌐 Web interface accessible from any browser

## Project Structure

```
physics-quiz/
├── app.py                  # Main Flask application & question bank
├── requirements.txt        # Python dependencies
├── static/
│   ├── imgs/               # Question and answer images
│   ├── scripts.js          # Quiz logic
│   ├── index.js
│   ├── styles.css
│   └── index.css
└── templates/
    ├── web.html            # Home / leaderboard page
    ├── index.html          # Login page
    └── quiz.html           # Quiz page
```

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/physics-quiz.git
   cd physics-quiz
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Usage

1. Enter a username on the login page to start.
2. Choose a difficulty level (Easy / Medium / Hard).
3. Answer questions — each wrong answer deducts 5 points from your score.
4. View the leaderboard to compare scores with others.

## Topics Covered

- Conservation of energy & potential energy
- Gravitation & orbital mechanics
- Simple harmonic motion & wave mechanics
- Rotational dynamics & angular momentum
- Wave interference & phase relationships
- Newton's laws & friction

## Notes

- Scores are stored **in memory** and will reset when the server restarts. For persistent storage, a database (e.g., SQLite) would be needed.
- The app runs in debug mode by default — set `debug=False` for production use.
- The test username and password are both “1@example.com”

## License

This project is for educational purposes.
