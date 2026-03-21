# Genre-Based Movie Recommendation System

A machine learning web application that recommends movies based on genre similarity using **Cosine Similarity** algorithms.

## Features

- 🎬 Browse movies by genre
- 🎯 Get personalized movie recommendations
- 📊 Uses cosine similarity for genre-based matching
- 🚀 Built with Streamlit for easy interaction

## Project Structure

```
Cosine-Similarity/
├── app.py              # Main Streamlit web application
├── main.py             # Movie recommendation logic & algorithms
├── movies.csv          # Movie dataset (title, genres)
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── __pycache__/       # Python cache files
```

## Requirements

- Python 3.8+
- pandas
- scikit-learn
- streamlit

## Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/Muhammad-Shaheer-Tariq/Movie-Recommender-System.git>
cd Cosine-Similarity
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### How to Use:

1. Select a genre from the dropdown menu
2. Click the "Recommend" button
3. View the top 10 movie recommendations for that genre

## How It Works

### Algorithm: Cosine Similarity

1. **Data Processing**:
   - Loads movie dataset with genres
   - Splits genres for each movie
   
2. **Feature Encoding**:
   - Uses `MultiLabelBinarizer` to convert genres into binary matrix
   
3. **Similarity Calculation**:
   - Computes cosine similarity between genre vectors
   - Identifies movies with similar genre profiles
   
4. **Recommendation**:
   - Filters movies by selected genre
   - Ranks by genre overlap and similarity score
   - Returns top N recommendations

## File Descriptions

### `app.py`
Streamlit web interface for the recommendation system:
- Genre selection dropdown
- Movie recommendation display
- UI configuration and styling

### `main.py`
Core recommendation logic:
- `recommend_movies(title, top_n)` - Get similar movies by title
- `recommend_by_genre(genre, top_n)` - Get movies by genre preference
- Cosine similarity matrix computation

### `movies.csv`
Dataset containing:
- Movie titles
- Genres (pipe-separated)

### `requirements.txt`
Python package dependencies with versions

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web interface framework |
| `pandas` | Data manipulation & analysis |
| `scikit-learn` | Machine learning algorithms |

## Future Enhancements

- Add movie ratings and popularity scores
- Implement collaborative filtering
- Add user rating history
- Support for multiple recommendation algorithms
- Movie details and IMDb links

## License

This project is open source and available under the MIT License.

## Author

Created for genre-based movie recommendations using cosine similarity.

---

**For issues or contributions, please submit a pull request or open an issue on GitHub.**
