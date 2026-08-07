import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Gaming Vault", page_icon="🎮", layout="wide")

# Custom Steam-style CSS
st.markdown("""
<style>
    /* Dark Steam Background */
    .stApp {
        background-color: #101822;
        color: #f3f3f3;
    }
    
    /* Steam Card Styling */
    .steam-card {
        background: linear-gradient(135deg, #1b2838 0%, #171a21 100%);
        border: 1px solid #2a475e;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .steam-card:hover {
        border-color: #66c0f4;
        transform: translateY(-2px);
    }
    
    /* Cover Art (66% Aspect Ratio like Steam vertical posters) */
    .cover-art {
        width: 100%;
        height: 240px;
        object-fit: cover;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    
    /* Title & Rank Badges */
    .game-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .rank-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        background: rgba(0,0,0,0.3);
        padding: 4px 8px;
        border-radius: 4px;
    }
    
    .rank-icon {
        width: 28px;
        height: 28px;
        object-fit: contain;
    }
    
    .stat-badge {
        background-color: #213245;
        color: #66c0f4;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session Data with Defaults if Empty
if "games" not in st.session_state:
    st.session_state.games = [
        {
            "id": 1,
            "title": "Overwatch 2",
            "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
            "rank_name": "Diamond 2",
            "peak_rank": "Master 5",
            "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
            "wins": 42,
            "losses": 28
        },
        {
            "id": 2,
            "title": "Rainbow Six Siege",
            "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400",
            "rank_name": "Emerald III",
            "peak_rank": "Diamond I",
            "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
            "wins": 65,
            "losses": 40
        }
    ]

# Header
st.title("🎮 Steam Vault Stats")

# Sidebar Controls
st.sidebar.header("🕹️ Vault Management")

# Section: Add New Game
with st.sidebar.expander("➕ Add New Game", expanded=False):
    new_title = st.text_input("Game Title")
    new_cover = st.text_input("Cover Image URL (Vertical)", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400")
    new_rank = st.text_input("Current Rank Name", "Unranked")
    new_peak = st.text_input("Peak Rank Name", "Unranked")
    new_rank_icon = st.text_input("Rank Icon Image URL", "https://cdn-icons-png.flaticon.com/512/616/616490.png")
    new_wins = st.number_input("Initial Wins", min_value=0, value=0)
    new_losses = st.number_input("Initial Losses", min_value=0, value=0)
    
    if st.button("Save Game to Vault"):
        if new_title:
            new_id = max([g["id"] for g in st.session_state.games] + [0]) + 1
            st.session_state.games.append({
                "id": new_id,
                "title": new_title,
                "cover": new_cover,
                "rank_name": new_rank,
                "peak_rank": new_peak,
                "rank_icon": new_rank_icon,
                "wins": new_wins,
                "losses": new_losses
            })
            st.success(f"Added {new_title}!")
            st.rerun()

# Section: Remove Game
with st.sidebar.expander("🗑️ Remove Game"):
    if st.session_state.games:
        game_to_remove = st.selectbox("Select Game to Delete", [g["title"] for g in st.session_state.games])
        if st.button("Confirm Delete"):
            st.session_state.games = [g for g in st.session_state.games if g["title"] != game_to_remove]
            st.warning(f"Deleted {game_to_remove}")
            st.rerun()

# Render Grid (4 Columns wide like Steam)
cols_per_row = 4
games = st.session_state.games

for i in range(0, len(games), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(games):
            game = games[i + j]
            total_matches = game["wins"] + game["losses"]
            win_rate = (game["wins"] / total_matches * 100) if total_matches > 0 else 0.0
            
            with cols[j]:
                # Custom Card Container
                st.markdown(f"""
                <div class="steam-card">
                    <img src="{game['cover']}" class="cover-art" />
                    <div class="game-title">{game['title']}</div>
                    <div class="rank-container">
                        <img src="{game['rank_icon']}" class="rank-icon" />
                        <div>
                            <div style="font-size:0.85rem; font-weight:600;">{game['rank_name']}</div>
                            <div style="font-size:0.75rem; color:#8f98a0;">Peak: {game['peak_rank']}</div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span class="stat-badge">W/L: {game['wins']}-{game['losses']}</span>
                        <span class="stat-badge">{win_rate:.1f}% WR</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Update Controls (Stats, Rank, & Images)
                with st.popover("⚙️ Edit Game & Rank"):
                    st.subheader(f"Edit {game['title']}")
                    game['wins'] = st.number_input("Wins", min_value=0, value=game['wins'], key=f"w_{game['id']}")
                    game['losses'] = st.number_input("Losses", min_value=0, value=game['losses'], key=f"l_{game['id']}")
                    
                    st.divider()
                    st.caption("🏆 Rank Details")
                    game['rank_name'] = st.text_input("Current Rank Name", value=game['rank_name'], key=f"rn_{game['id']}")
                    game['peak_rank'] = st.text_input("Peak Rank Name", value=game['peak_rank'], key=f"pr_{game['id']}")
                    game['rank_icon'] = st.text_input("Rank Icon Image URL", value=game['rank_icon'], key=f"ri_{game['id']}")
                    
                    st.divider()
                    st.caption("🖼️ Artwork")
                    game['cover'] = st.text_input("Cover Image URL", value=game['cover'], key=f"c_{game['id']}")
                    
                    if st.button("Save Changes", key=f"btn_{game['id']}"):
                        st.success("Updated successfully!")
                        st.rerun()
