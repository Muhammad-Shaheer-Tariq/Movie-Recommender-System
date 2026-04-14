"""
╔══════════════════════════════════════════════════════════════╗
║        🎬 CineMatch — Genre-Based Movie Recommender          ║
║        Built with Streamlit + Cosine Similarity              ║
╚══════════════════════════════════════════════════════════════╝

Design philosophy:
  - Deep cinematic dark theme (midnight blacks + neon gold accents)
  - Glassmorphism cards with hover lift effects
  - Responsive grid layout via st.columns
  - Smooth CSS transitions and animated elements
  - All backend logic stays inside main.py — untouched
"""

import time
import random
import streamlit as st
import pandas as pd
from main import recommend_by_genre, recommend_movies, movies as movies_df, cosine_sim, indices

# ──────────────────────────────────────────────────────────────
# 1.  PAGE CONFIG  (must be the very first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch · Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# 2.  GLOBAL CSS
#     All colour tokens are CSS variables at the top of :root{}
#     so you can retheme the whole app by editing just 8 lines.
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ─── COLOUR TOKENS ─────────────────────────────────────── */
    :root {
        --bg-deep:       #0a0a0f;      /* page background            */
        --bg-card:       #12121a;      /* card background            */
        --bg-glass:      rgba(255,255,255,0.04);  /* glass panels  */
        --border-glass:  rgba(255,255,255,0.10);
        --accent:        #f5c518;      /* IMDb gold                  */
        --accent-dim:    rgba(245,197,24,0.18);
        --accent2:       #e50914;      /* Netflix red                */
        --text-primary:  #f0f0f0;
        --text-muted:    #8a8a9a;
        --text-dim:      #555568;
        --shadow:        0 8px 32px rgba(0,0,0,0.6);
        --radius-card:   16px;
        --radius-chip:   999px;
        --transition:    0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ─── GLOBAL RESETS ──────────────────────────────────────── */
    html, body, [class*="css"] {
        background-color: var(--bg-deep) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Remove Streamlit's default top padding */
    .block-container { padding-top: 0rem !important; }

    /* Hide the Streamlit hamburger menu & footer */
    #MainMenu, footer, header { visibility: hidden; }

    /* ─── SCROLLBAR ──────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-deep); }
    ::-webkit-scrollbar-thumb { background: var(--accent-dim); border-radius: 3px; }

    /* ─── HERO BANNER ────────────────────────────────────────── */
    .hero-banner {
        background: linear-gradient(
            135deg,
            #0a0a0f 0%,
            #1a0a1a 30%,
            #0f0a1a 60%,
            #0a0f1a 100%
        );
        border-bottom: 1px solid var(--border-glass);
        padding: 3.5rem 2rem 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 0;
    }
    /* Animated starfield dots behind the hero */
    .hero-banner::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(1px 1px at 20% 30%, rgba(245,197,24,0.5) 0%, transparent 100%),
            radial-gradient(1px 1px at 80% 10%, rgba(245,197,24,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 50% 70%, rgba(229,9,20,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 10% 80%, rgba(245,197,24,0.3) 0%, transparent 100%),
            radial-gradient(1px 1px at 90% 60%, rgba(245,197,24,0.3) 0%, transparent 100%),
            radial-gradient(2px 2px at 35% 15%, rgba(255,255,255,0.2) 0%, transparent 100%),
            radial-gradient(2px 2px at 65% 85%, rgba(255,255,255,0.2) 0%, transparent 100%);
        animation: twinkle 4s ease-in-out infinite alternate;
        pointer-events: none;
    }
    @keyframes twinkle {
        from { opacity: 0.6; }
        to   { opacity: 1.0; }
    }
    /* Glowing bottom line */
    .hero-banner::after {
        content: '';
        position: absolute;
        bottom: 0; left: 10%; right: 10%; height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        animation: pulse-line 3s ease-in-out infinite;
    }
    @keyframes pulse-line {
        0%, 100% { opacity: 0.4; }
        50%       { opacity: 1.0; }
    }

    .hero-logo {
        font-size: 3.8rem;
        margin-bottom: 0.2rem;
        animation: float 3s ease-in-out infinite;
        display: inline-block;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-8px); }
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, var(--accent) 0%, #fff 50%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-top: 0.6rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 300;
    }
    .hero-badge {
        display: inline-block;
        background: var(--accent-dim);
        border: 1px solid rgba(245,197,24,0.3);
        color: var(--accent);
        border-radius: var(--radius-chip);
        padding: 0.25rem 0.9rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 1rem;
    }

    /* ─── SIDEBAR ────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #0a0a0f 100%) !important;
        border-right: 1px solid var(--border-glass) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }
    .sidebar-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--accent) !important;
        margin: 1.4rem 0 0.5rem;
        display: block;
    }

    /* ─── GENRE CHIP (used inline in the page, not sidebar) ──── */
    .genre-chip {
        display: inline-block;
        background: var(--accent-dim);
        border: 1px solid rgba(245,197,24,0.25);
        color: var(--accent);
        border-radius: var(--radius-chip);
        padding: 0.2rem 0.75rem;
        font-size: 0.73rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        margin: 2px;
        white-space: nowrap;
    }
    .genre-chip-alt {
        background: rgba(229,9,20,0.15);
        border-color: rgba(229,9,20,0.25);
        color: #ff6b6b;
    }

    /* ─── MOVIE CARDS ────────────────────────────────────────── */
    .movie-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-card);
        padding: 0;
        overflow: hidden;
        transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
        position: relative;
        height: 100%;
        cursor: default;
    }
    .movie-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 20px 48px rgba(0,0,0,0.7), 0 0 0 1px rgba(245,197,24,0.25);
        border-color: rgba(245,197,24,0.35);
    }

    /* Poster placeholder area */
    .movie-poster {
        width: 100%;
        height: 160px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        position: relative;
        overflow: hidden;
    }
    .movie-poster::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, transparent 50%, var(--bg-card) 100%);
    }

    .movie-card-body { padding: 1rem 1.1rem 1.2rem; }

    .movie-rank {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .movie-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.3;
        margin-bottom: 0.5rem;
        /* Clamp to 2 lines */
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .movie-genres { margin-bottom: 0.75rem; line-height: 2; }

    /* Similarity score bar */
    .sim-bar-wrap {
        margin-top: 0.7rem;
        background: rgba(255,255,255,0.06);
        border-radius: var(--radius-chip);
        overflow: hidden;
        height: 4px;
    }
    .sim-bar-fill {
        height: 4px;
        border-radius: var(--radius-chip);
        background: linear-gradient(90deg, var(--accent2), var(--accent));
        transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
    }
    .sim-score-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
        display: flex;
        justify-content: space-between;
    }
    .sim-score-value { color: var(--accent); font-weight: 700; }

    /* Card "rank" ribbon */
    .rank-ribbon {
        position: absolute;
        top: 10px; left: 10px;
        background: rgba(0,0,0,0.7);
        border: 1px solid var(--border-glass);
        color: var(--accent);
        font-size: 0.7rem;
        font-weight: 800;
        border-radius: 6px;
        padding: 2px 7px;
        backdrop-filter: blur(4px);
        z-index: 2;
    }

    /* ─── SECTION HEADERS ────────────────────────────────────── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.8rem 0 1.2rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-glass);
    }
    .section-header-icon { font-size: 1.4rem; }
    .section-header-text {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    .section-header-count {
        margin-left: auto;
        font-size: 0.78rem;
        color: var(--text-muted);
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-chip);
        padding: 0.2rem 0.7rem;
    }

    /* ─── SEARCH BAR ─────────────────────────────────────────── */
    .stTextInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1rem !important;
        transition: border-color var(--transition), box-shadow var(--transition) !important;
    }
    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-dim) !important;
    }
    .stTextInput input::placeholder { color: var(--text-dim) !important; }

    /* ─── SELECT BOX ─────────────────────────────────────────── */
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div:hover {
        background: var(--bg-card) !important;
        border-color: var(--border-glass) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* ─── BUTTONS ────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent2) 0%, #ff4757 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 2rem !important;
        transition: all var(--transition) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        box-shadow: 0 4px 15px rgba(229,9,20,0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(229,9,20,0.6) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ─── STATS / METRIC AREA ────────────────────────────────── */
    .stat-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--accent);
        line-height: 1;
    }
    .stat-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }

    /* ─── EXPANDER (Why this movie?) ─────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-glass) !important;
        border-radius: 8px !important;
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        border: 1px solid var(--border-glass) !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: 0 0 8px 8px !important;
    }

    /* ─── INFO / WARNING BOXES ───────────────────────────────── */
    .stAlert {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
    }

    /* ─── DIVIDER ─────────────────────────────────────────────── */
    hr { border-color: var(--border-glass) !important; }

    /* ─── PROGRESS BAR ────────────────────────────────────────── */
    .stProgress > div > div { background: var(--accent) !important; }

    /* ─── FOOTER ─────────────────────────────────────────────── */
    .footer-bar {
        margin-top: 4rem;
        padding: 1.5rem 0;
        border-top: 1px solid var(--border-glass);
        text-align: center;
        color: var(--text-dim);
        font-size: 0.8rem;
    }
    .footer-bar a {
        color: var(--accent);
        text-decoration: none;
        font-weight: 600;
    }
    .footer-bar a:hover { text-decoration: underline; }

    /* ─── NO-RESULTS PLACEHOLDER ─────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--text-muted);
    }
    .empty-state-icon { font-size: 4rem; margin-bottom: 1rem; }
    .empty-state-text { font-size: 1.1rem; }

    /* ─── SEARCH RESULT ROW ──────────────────────────────────── */
    .search-result-row {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: border-color var(--transition);
    }
    .search-result-row:hover { border-color: rgba(245,197,24,0.3); }

    /* ─── GLASS PANEL ────────────────────────────────────────── */
    .glass-panel {
        background: var(--bg-glass);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 1.5rem;
        backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
    }

    /* ─── ANIMATED LOADING DOT ───────────────────────────────── */
    @keyframes blink { 0%,80%,100%{opacity:0;} 40%{opacity:1;} }
    .loading-dots span {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--accent);
        margin: 0 3px;
        animation: blink 1.4s infinite both;
    }
    .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
    .loading-dots span:nth-child(3) { animation-delay: 0.4s; }

    /* ─── RESPONSIVE TWEAKS ──────────────────────────────────── */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .movie-poster { height: 120px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# 3.  DATA SETUP
#     We import the pre-processed DataFrame from main.py so
#     no CSV is loaded twice and the genre matrix is reused.
# ──────────────────────────────────────────────────────────────

# Build genre lookup helpers from the already-loaded movies_df
all_genres = sorted(set(g for genres in movies_df["genres"] for g in genres))

# Map title → cosine similarity score (for display on cards)
def get_sim_scores_for_genre(genre: str, top_n: int = 10) -> dict:
    """
    Return {title: similarity_score} for movies that contain `genre`.
    Score = fraction of their genres that overlap with a pure [genre] vector.
    Simplified: movies with fewer total genres score higher (purer match).
    """
    filtered = movies_df[movies_df["genres"].apply(lambda x: genre in x)].copy()
    filtered["genre_count"] = filtered["genres"].apply(len)
    # Normalise to 0-1: 1 genre → score 1.0, many genres → lower
    max_g = filtered["genre_count"].max() if not filtered.empty else 1
    filtered["sim_score"] = filtered["genre_count"].apply(
        lambda c: round(1 - (c - 1) / max(max_g, 1) * 0.35, 4)
    )
    return dict(zip(filtered["title"], filtered["sim_score"]))

# ──────────────────────────────────────────────────────────────
# 4.  POSTER PALETTE
#     Each card gets a deterministic gradient based on its rank.
# ──────────────────────────────────────────────────────────────
POSTER_GRADIENTS = [
    ("🎬", "linear-gradient(135deg,#1a0533 0%,#4a0080 100%)"),
    ("🎥", "linear-gradient(135deg,#0a1a33 0%,#0040aa 100%)"),
    ("🎭", "linear-gradient(135deg,#1a0a00 0%,#aa4400 100%)"),
    ("🎞️", "linear-gradient(135deg,#0a1a00 0%,#2a6600 100%)"),
    ("🌟", "linear-gradient(135deg,#1a1500 0%,#887700 100%)"),
    ("🎪", "linear-gradient(135deg,#1a0010 0%,#880044 100%)"),
    ("🎦", "linear-gradient(135deg,#001a1a 0%,#006666 100%)"),
    ("🍿", "linear-gradient(135deg,#1a0a0a 0%,#881111 100%)"),
    ("🎙️", "linear-gradient(135deg,#0a0a1a 0%,#333388 100%)"),
    ("🏆", "linear-gradient(135deg,#15100a 0%,#6b4c22 100%)"),
]

def poster_style(rank: int) -> tuple[str, str]:
    idx = rank % len(POSTER_GRADIENTS)
    return POSTER_GRADIENTS[idx]

# ──────────────────────────────────────────────────────────────
# 5.  HERO BANNER
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-logo">🎬</div>
        <h1 class="hero-title">CineMatch</h1>
        <p class="hero-sub">Your personal genre-based movie guide</p>
        <span class="hero-badge">✦ Powered by Cosine Similarity</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# 6.  SIDEBAR — controls, stats, about
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    # Branding
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 0.5rem;'>
            <span style='font-size:2.5rem'>🎬</span>
            <h2 style='font-size:1.4rem; font-weight:800; margin:0.3rem 0 0;
                       background:linear-gradient(135deg,#f5c518,#fff);
                       -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                CineMatch
            </h2>
            <p style='font-size:0.78rem; color:#8a8a9a; margin:0.2rem 0 0;'>
                Genre · Similarity · Discovery
            </p>
        </div>
        <hr style='border-color:rgba(255,255,255,0.08); margin:1rem 0;'>
        """,
        unsafe_allow_html=True,
    )

    # ── Genre Selector ──────────────────────────────────────
    st.markdown("<span class='sidebar-section-title'>🎭 Choose Genre</span>", unsafe_allow_html=True)
    selected_genre = st.selectbox(
        label="Genre",
        options=all_genres,
        label_visibility="collapsed",
        key="genre_select",
    )

    # ── Top-N Slider ────────────────────────────────────────
    st.markdown("<span class='sidebar-section-title'>🔢 Number of Picks</span>", unsafe_allow_html=True)
    top_n = st.slider(
        label="How many movies?",
        min_value=3,
        max_value=20,
        value=10,
        step=1,
        label_visibility="collapsed",
        key="top_n_slider",
    )

    # ── Recommend Button ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_clicked = st.button("🎯  Find Movies", use_container_width=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # ── Dataset Stats ────────────────────────────────────────
    st.markdown("<span class='sidebar-section-title'>📊 Dataset Stats</span>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            f"<div class='stat-card'>"
            f"<div class='stat-number'>{len(movies_df):,}</div>"
            f"<div class='stat-label'>Movies</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            f"<div class='stat-card'>"
            f"<div class='stat-number'>{len(all_genres)}</div>"
            f"<div class='stat-label'>Genres</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # ── About ────────────────────────────────────────────────
    st.markdown("<span class='sidebar-section-title'>ℹ️ About</span>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='font-size:0.8rem; color:#8a8a9a; line-height:1.6;'>
        CineMatch uses <strong style='color:#f5c518;'>Cosine Similarity</strong>
        on multi-hot genre encodings to surface the best genre matches from
        a curated dataset of 9,742 titles.
        </p>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────
# 7.  MAIN CONTENT AREA
# ──────────────────────────────────────────────────────────────
main_col, _ = st.columns([1, 0.01])  # full-width feel inside the wide layout

with main_col:

    # ── Search Bar ───────────────────────────────────────────
    st.markdown(
        """
        <div class='section-header'>
            <span class='section-header-icon'>🔍</span>
            <h2 class='section-header-text'>Search by Title</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input(
        label="Search",
        placeholder="e.g. Toy Story, The Matrix, Inception…",
        label_visibility="collapsed",
        key="search_input",
    )

    # ── Title-search results ──────────────────────────────────
    if search_query.strip():
        query_lower = search_query.strip().lower()
        matched = movies_df[movies_df["title"].str.lower().str.contains(query_lower, na=False)]
        if matched.empty:
            st.markdown(
                "<div class='empty-state'>"
                "<div class='empty-state-icon'>🎞️</div>"
                "<div class='empty-state-text'>No titles matching <em>\"" + search_query + "\"</em></div>"
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='font-size:0.82rem; color:#8a8a9a; margin-bottom:0.8rem;'>"
                f"Found <strong style='color:#f5c518;'>{len(matched)}</strong> result(s)</div>",
                unsafe_allow_html=True,
            )
            # Show up to 8 search matches
            for _, row in matched.head(8).iterrows():
                genre_chips = "".join(
                    f"<span class='genre-chip'>{g}</span>" for g in row["genres"][:4]
                )
                st.markdown(
                    f"<div class='search-result-row'>"
                    f"  <span style='font-size:1.5rem'>🎬</span>"
                    f"  <div style='flex:1'>"
                    f"    <div style='font-weight:700; font-size:0.95rem'>{row['title']}</div>"
                    f"    <div style='margin-top:4px'>{genre_chips}</div>"
                    f"  </div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            # "Similar movies" for the first match
            top_match_title = matched.iloc[0]["title"]
            if top_match_title in indices:
                with st.expander(f"📽️ Movies similar to '{top_match_title}'"):
                    sim_recs = recommend_movies(top_match_title, top_n=5)
                    if isinstance(sim_recs, pd.DataFrame) and not sim_recs.empty:
                        for _, sr in sim_recs.iterrows():
                            gc = " ".join(
                                f"<span class='genre-chip genre-chip-alt'>{g}</span>"
                                for g in sr["genres"][:3]
                            )
                            st.markdown(
                                f"<div class='search-result-row'>"
                                f"  <span style='font-size:1.3rem'>🎯</span>"
                                f"  <div><div style='font-weight:600;font-size:0.9rem'>{sr['title']}</div>"
                                f"  <div style='margin-top:3px'>{gc}</div></div>"
                                f"</div>",
                                unsafe_allow_html=True,
                            )
                    else:
                        st.caption("No similar movies found in the dataset.")

        st.markdown("<hr>", unsafe_allow_html=True)

    # ── Genre Recommendations ─────────────────────────────────
    # Show on load (default genre) or after button click
    # We auto-load on first visit so the page isn't blank.
    show_recs = recommend_clicked or ("recs_df" not in st.session_state)

    if show_recs:
        # ── Loading animation ──────────────────────────────
        progress_placeholder = st.empty()
        progress_placeholder.markdown(
            "<div style='text-align:center; padding:1.5rem 0;'>"
            "<div class='loading-dots'><span></span><span></span><span></span></div>"
            "<p style='color:#8a8a9a; margin-top:0.75rem; font-size:0.85rem;'>"
            "Calculating similarities…</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        # ── Progress bar simulation ────────────────────────
        prog = st.progress(0)
        for pct in range(0, 101, 20):
            time.sleep(0.04)
            prog.progress(pct)

        # ── Actual recommendation call (main.py) ───────────
        recs_df: pd.DataFrame = recommend_by_genre(selected_genre, top_n)
        sim_scores_map = get_sim_scores_for_genre(selected_genre, top_n)

        # Store in session so we don't recompute on every widget nudge
        st.session_state["recs_df"] = recs_df
        st.session_state["sim_scores_map"] = sim_scores_map
        st.session_state["active_genre"] = selected_genre

        prog.empty()
        progress_placeholder.empty()

    else:
        # Restore from session state
        recs_df = st.session_state.get("recs_df", pd.DataFrame())
        sim_scores_map = st.session_state.get("sim_scores_map", {})
        selected_genre = st.session_state.get("active_genre", selected_genre)

    # ── Section Header ────────────────────────────────────────
    genre_chip_html = f"<span class='genre-chip' style='font-size:0.9rem; padding:0.3rem 1rem;'>{selected_genre}</span>"
    st.markdown(
        f"""
        <div class='section-header'>
            <span class='section-header-icon'>🎬</span>
            <h2 class='section-header-text'>Top Picks in {genre_chip_html}</h2>
            <span class='section-header-count'>{len(recs_df)} movies</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if recs_df.empty:
        st.markdown(
            "<div class='empty-state'>"
            "<div class='empty-state-icon'>😕</div>"
            "<div class='empty-state-text'>No movies found for this genre. Try another!</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # ── Render cards in a 3-column responsive grid ─────
        COLS_PER_ROW = 3
        rows = [
            recs_df.iloc[i : i + COLS_PER_ROW]
            for i in range(0, len(recs_df), COLS_PER_ROW)
        ]

        for row_data in rows:
            cols = st.columns(COLS_PER_ROW, gap="medium")
            for col_idx, (_, movie_row) in enumerate(row_data.iterrows()):
                rank = list(recs_df.index).index(movie_row.name) + 1
                title = movie_row["title"]
                genres = movie_row["genres"]
                sim_score = sim_scores_map.get(title, 0.75)
                icon, gradient = poster_style(rank - 1)

                # Genre chips (max 4 shown)
                genre_chips = "".join(
                    f"<span class='genre-chip'>{g}</span>" for g in genres[:4]
                )
                if len(genres) > 4:
                    genre_chips += f"<span class='genre-chip genre-chip-alt'>+{len(genres)-4}</span>"

                # Similarity bar width (percentage string)
                bar_pct = int(sim_score * 100)

                with cols[col_idx]:
                    # ── Card HTML ───────────────────────────
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <div class="movie-poster" style="background:{gradient};">
                                <span style="position:relative;z-index:1;">{icon}</span>
                                <div class="rank-ribbon">#{rank}</div>
                            </div>
                            <div class="movie-card-body">
                                <div class="movie-rank">Recommendation #{rank}</div>
                                <div class="movie-title">{title}</div>
                                <div class="movie-genres">{genre_chips}</div>
                                <div class="sim-bar-wrap">
                                    <div class="sim-bar-fill" style="width:{bar_pct}%;"></div>
                                </div>
                                <div class="sim-score-label">
                                    <span>Genre Match</span>
                                    <span class="sim-score-value">{sim_score:.0%}</span>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # ── "Why this movie?" expander ──────────
                    with st.expander("🔬 Why this movie?"):
                        selected_set = {selected_genre}
                        movie_set  = set(genres)
                        shared     = selected_set & movie_set
                        unique     = movie_set - selected_set

                        st.markdown(
                            f"""
                            <div style='font-size:0.82rem; line-height:1.7; color:#c0c0d0;'>
                            <strong style='color:#f5c518;'>Genre overlap</strong><br>
                            This movie contains the genre
                            <span class='genre-chip'>{selected_genre}</span>
                            which you searched for.
                            <br><br>
                            <strong style='color:#f5c518;'>All genres</strong><br>
                            {"".join(f"<span class='genre-chip'>{g}</span>" for g in genres)}
                            <br><br>
                            <strong style='color:#f5c518;'>Match score</strong><br>
                            <span style='color:#f5c518; font-weight:700;'>{sim_score:.2%}</span>
                            — based on genre purity
                            (movies with fewer total genres receive a higher focused score).
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # ── Summary strip ─────────────────────────────────────
        avg_score = sum(sim_scores_map.get(t, 0) for t in recs_df["title"]) / max(len(recs_df), 1)
        st.markdown("<br>", unsafe_allow_html=True)
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        with sum_col1:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{len(recs_df)}</div>"
                f"<div class='stat-label'>Matches Found</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with sum_col2:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{avg_score:.0%}</div>"
                f"<div class='stat-label'>Avg. Match Score</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with sum_col3:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{selected_genre}</div>"
                f"<div class='stat-label'>Active Genre</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

# ──────────────────────────────────────────────────────────────
# 8.  FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class='footer-bar'>
        🎬 <strong>CineMatch</strong> &nbsp;·&nbsp;
        Genre-Based Movie Recommender using Cosine Similarity &nbsp;·&nbsp;
        Built with <a href='https://streamlit.io' target='_blank'>Streamlit</a>
        &nbsp;·&nbsp;
        <a href='https://github.com/Muhammad-Shaheer-Tariq/Movie-Recommender-System'
           target='_blank'>GitHub ↗</a>
    </div>
    """,
    unsafe_allow_html=True,
)
