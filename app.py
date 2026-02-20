import streamlit as st
from utils.recommender import load_data, recommend
from utils.tmdb_api import fetch_movie_details

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Netflix Recommender", layout="wide")

# -----------------------------
# Session State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"  # home, login, recommender
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.main-title { font-size: 45px; font-weight: bold; color: #E50914; text-align:center; margin-bottom:30px; }
.login-box { background-color:#1c1f26; padding:40px; border-radius:20px; max-width:450px; margin:auto; box-shadow:0 0 30px rgba(255,0,0,0.6);}
.stTextInput>div>input { background-color:#2a2d37; color:white; border-radius:10px; height:35px; }
.stTextInput>div>label { color:#bbbbbb; font-weight:bold; }
.movie-card { background-color:#1c1f26; padding:10px; border-radius:15px; text-align:center; transition:0.3s; display:inline-block; }
.movie-card:hover { transform:scale(1.05); }
.movie-title { font-size:16px; font-weight:bold; color:black; margin-top:10px; }
.overview { font-size:12px; color:#bbbbbb; margin-top:8px; }
.trailer-btn { display:inline-block; margin-top:10px; padding:8px 14px; background-color:black; color:white; text-decoration:none; border-radius:8px; font-size:13px; border:1px solid white; transition:0.3s; }
.trailer-btn:hover { background-color:white; color:black; }
.logout-btn { position:absolute; top:20px; right:20px; padding:8px 15px; background-color:#E50914; color:white; border:none; border-radius:8px; cursor:pointer; transition:0.3s; }
.logout-btn:hover { background-color:#ff1a1a; }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Helper Function
# -----------------------------
def rating_color(rating):
    try:
        rating = float(rating)
        if rating >= 7:
            return "#00ff99"
        elif rating >= 5:
            return "#ffa500"
        else:
            return "#ff4d4d"
    except:
        return "white"


# -----------------------------
# Home Page – Attractive
# -----------------------------
def home_page():
    st.markdown("""
        <div style="text-align:center; margin-top:50px;">
            <h1 style="font-size:60px; color:#E50914; font-weight:bold;">🏠 Netflix Movie Recommender</h1>
            <p style="color:#bbbbbb; font-size:18px; margin-top:10px;">
                Discover similar movies instantly using Machine Learning
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Login button – attractive gradient
    if st.button("🚀 Login", key="home_login"):
        st.session_state.page = "login"


# -----------------------------
# Login Page – Attractivegit --version
# -----------------------------
def login_page():
    st.markdown('<div class="main-title">🔐 Login</div>', unsafe_allow_html=True)

    # Login box
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    # Welcome heading inside box
    st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <h2 style="color:black; margin:0; font-size:32px;">Welcome!</h2>
            <p style="color:#bbbbbb; margin-top:8px; font-size:16px;">
                Start your movie journey with Netflix Style Recommender 🎬
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Input fields
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Login button with hover effect
    if st.button("Login", key="login_btn"):
        if username.strip() != "" and password.strip() != "":
            st.session_state.page = "recommender"
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Username or Password cannot be empty")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Recommender Page
# -----------------------------
def recommender_page():
    st.markdown('<div class="main-title">🎬 Netflix Style Movie Recommender</div>', unsafe_allow_html=True)

    # Logout button top right
    if st.button("🔒 Logout", key="logout"):
        st.session_state.page = "home"
        st.session_state.logged_in = False
        return

    # Load Data
    with st.spinner("Loading data..."):
        new_df, similarity = load_data()

    # Movie Selection
    movie_list = sorted(new_df['title'].values)
    selected_movie = st.selectbox("🔍 Search Movie", movie_list)

    # Recommendation Section
    if st.button("🔥 Recommend"):
        recommendations = recommend(selected_movie, new_df, similarity)

        if recommendations:
            st.subheader("⭐ Top Recommendations")
            cols = st.columns(5)
            for idx, movie in enumerate(recommendations):
                poster, rating, overview, trailer = fetch_movie_details(movie)
                with cols[idx]:
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    if poster: st.image(poster, width=200)
                    st.markdown(f'<div class="movie-title">{movie}</div>', unsafe_allow_html=True)
                    color = rating_color(rating)
                    st.markdown(f'<div style="color:{color}; font-weight:bold;">⭐ {rating}/10</div>',
                                unsafe_allow_html=True)
                    if overview: st.markdown(f'<div class="overview">{overview[:100]}...</div>', unsafe_allow_html=True)
                    if trailer: st.markdown(
                        f'<a href="{trailer}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>',
                        unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No recommendations found.")


# -----------------------------
# Page Navigation
# -----------------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "recommender":
    recommender_page()
