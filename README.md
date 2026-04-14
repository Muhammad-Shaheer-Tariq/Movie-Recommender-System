# 🎬 CineMatch — Genre-Based Movie Recommender

A beautiful, cinematic movie recommendation web app built with **Streamlit** and **Cosine Similarity** on genre encodings. Transformed from a basic dropdown UI into a professional, Netflix/IMDb-inspired experience.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 🎭 **Genre-based recommendations** — pick any genre and get the best matching movies
- 🔍 **Live title search** — search movies by name with instant results
- 📽️ **Similar movie finder** — find movies similar to any search result
- 📊 **Cosine similarity scores** — each card shows a genre match percentage + animated progress bar
- 🔬 **"Why this movie?" explainer** — expandable per-card explanation of genre overlap
- 🎚️ **Adjustable result count** — slider to get 3–20 recommendations
- 🌑 **Cinematic dark theme** — deep blacks, IMDb gold accents, glassmorphism cards
- 📱 **Responsive 3-column grid** — adapts to any screen size
- ⚡ **Loading animation** — animated dots + progress bar while calculating

---

## 🖥️ UI Preview

| Section | Description |
|---|---|
| **Hero Banner** | Full-width dark banner with animated floating icon, gradient title & glowing badge |
| **Sidebar** | Dark glass panel — genre selector, top-N slider, stats, red "Find Movies" CTA |
| **Movie Cards** | 3-column grid with unique gradient posters, rank ribbons, genre chips, match-score bars |
| **Search** | Realtime search bar with matched titles + similar-movie expander |
| **Footer** | Project credit + GitHub link |

---

## 📁 Project Structure

```
Movie-Recommender-System/
├── app.py              # ✨ CineMatch — cinematic Streamlit UI (fully rewritten)
├── main.py             # Core recommendation logic & cosine similarity algorithms
├── movies.csv          # Movie dataset — 9,742 titles with pipe-separated genres
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- scikit-learn >= 1.3.0

---

## 🚀 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Muhammad-Shaheer-Tariq/Movie-Recommender-System.git
cd Movie-Recommender-System
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** — enjoy CineMatch! 🎬

---

## 🧠 How It Works

### Algorithm: Cosine Similarity on Genre Vectors

1. **Data Loading** — `movies.csv` is loaded; pipe-separated genres are split into lists
2. **Encoding** — `MultiLabelBinarizer` converts genre lists into a binary genre matrix
3. **Similarity Matrix** — `cosine_similarity(genre_matrix, genre_matrix)` computes pairwise scores
4. **Genre Recommendation** — `recommend_by_genre(genre, top_n)` filters by genre and ranks by genre count
5. **Title Recommendation** — `recommend_movies(title, top_n)` finds the most similar movies by cosine score

### Match Score Formula (UI display)

```
score = 1 - (genre_count - 1) / max_genre_count × 0.35
```

Movies with fewer genres get a higher *purity* score (they are more focused on your chosen genre).

---

## 📦 File Descriptions

### `app.py` — CineMatch UI
The fully redesigned Streamlit interface:
- Dark cinematic theme via injected CSS with `:root` colour tokens (easy to retheme)
- Hero banner with CSS keyframe animations (twinkling stars, floating icon, pulse line)
- Sidebar with genre selector, top-N slider, dataset stats
- 3-column movie card grid with glassmorphism styling and hover lift effects
- Realtime title search + similar-movie expander (calls `recommend_movies`)
- Per-card "Why this movie?" expander with genre overlap explanation
- Session-state caching to avoid rerunning the model on every widget interaction
- Loading dots + progress bar animation on recommendation fetch

### `main.py` — Recommendation Engine
Core ML logic (unchanged):
- `recommend_movies(title, top_n=5)` — title-based cosine similarity lookup
- `recommend_by_genre(genre, top_n=5)` — genre-filtered ranking
- Pre-computed cosine similarity matrix & `indices` series

### `movies.csv`
- **9,742 movies** from the MovieLens dataset
- Columns: `movieId`, `title`, `genres` (pipe-separated)

### `requirements.txt`
Pinned Python dependencies — no extra packages beyond the ML/UI stack.

---

## 📚 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥ 1.28 | Web interface framework |
| `pandas` | ≥ 2.0 | Data manipulation |
| `scikit-learn` | ≥ 1.3 | ML algorithms (MultiLabelBinarizer, cosine_similarity) |

---

## 🔮 Future Enhancements

- Add real movie poster images via TMDB API
- Collaborative filtering (user-based recommendations)
- Movie ratings and IMDb score overlay
- Watchlist / favourites feature
- Dark / light mode toggle

---

## 📄 License

This project is open source and available under the **MIT License**.

---

## 👤 Author

**Muhammad Shaheer Tariq**
Genre-based movie recommendation using cosine similarity — designed to look *professional*.

> For issues or contributions, please open an issue or submit a pull request on [GitHub](https://github.com/Muhammad-Shaheer-Tariq/Movie-Recommender-System).
