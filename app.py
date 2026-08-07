import streamlit as st
import json
import os
import requests
import base64

# Page Configuration
st.set_page_config(page_title="Rank Tracker", layout="wide")

DATA_FILE = "games.json"

DEFAULT_GAMES = [
    {
        "id": 1,
        "title": "Overwatch",
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 2,
        "title": "Rainbow Six Siege",
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 3,
        "title": "Fortnite",
        "cover": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 4,
        "title": "Modern Warfare 4",
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 5,
        "title": "Tekken 8",
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 6,
        "title": "Arena Breakout Infinite",
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 7,
        "title": "Delta Force",
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    },
    {
        "id": 8,
        "title": "FragPunk",
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0,
        "losses": 0,
        "streak": 0,
        "notes": ""
    }
]

def load_games():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved_data = json.load(f)
                if saved_data and len(saved_data) > 0:
                    for g in saved_data:
                        g.setdefault("streak", 0)
                        g.setdefault("notes", "")
                    return saved_data
        except Exception as e:
            st.error(f"Error loading saved data: {e}")
    return DEFAULT_GAMES

def save_games():
    if "GITHUB_TOKEN" in st.secrets and "REPO_NAME" in st.secrets:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["REPO_NAME"]
        url = f"https://api.github.com/repos/{repo}/contents/{DATA_FILE}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        sha = None
        get_res = requests.get(url, headers=headers)
        if get_res.status_code == 200:
            sha = get_res.json().get("sha")
            
        json_data = json.dumps(st.session_state.games, indent=4)
        encoded_content = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
        
        payload = {
            "message": "Auto-save stats from Rank Tracker app",
            "content": encoded_content
        }
        if sha:
            payload["sha"] = sha
            
        put_res = requests.put(url, headers=headers, json=payload)
        if put_res.status_code in [200, 201]:
            st.toast("Saved permanently to GitHub!", icon="✅")
        else:
            st.error(f"GitHub API Save Error: {put_res.status_code} - {put_res.text}")
    else:
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(st.session_state.games, f, indent=4)
            st.toast("Saved locally", icon="⚠️")
        except Exception as e:
            st.error(f"Error saving data: {e}")

# CSS Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e141d;
        color: #f3f3f3;
    }
    
    /* Steam Card */
    .steam-card {
        background: linear-gradient(145deg, #18222d 0%, #111822 100%);
        border: 1px solid #283d52;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 6px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }
    .steam-card:hover {
        border-color: #66c0f4;
    }
    
    /* 2:3 Aspect Ratio */
    .cover-art {
        width: 100%;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    
    .game-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .rank-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
        background: rgba(0,0,0,0.35);
        padding: 6px 10px;
        border-radius: 6px;
    }
    
    .rank-icon {
        width: 26px;
        height: 26px;
        object-fit: contain;
    }
    
    /* Stat Badges */
    .stat-badge {
        background-color: #1e2c3c;
        color: #66c0f4;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.82rem;
    }
    
    /* Progress Bar */
    .progress-container {
        background-color: #16202c;
        border-radius: 4px;
        height: 6px;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 8px;
        overflow: hidden;
    }
    .progress-fill-green { background-color: #2ecc71; height: 100%; }
    .progress-fill-yellow { background-color: #f1c40f; height: 100%; }
    .progress-fill-red { background-color: #e74c3c; height: 100%; }
    
    /* Compact Buttons */
    div[data-testid="stHorizontalBlock"] button {
        padding: 2px 6px !important;
        font-size: 0.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

if "games" not in st.session_state:
    st.session_state.games = load_games()

games = st.session_state.games

# Calculate Global Summary Stats
total_wins = sum(g["wins"] for g in games)
total_losses = sum(g["losses"] for g in games)
total_all_matches = total_wins + total_losses
global_wr = (total_wins / total_all_matches * 100) if total_all_matches > 0 else 0.0
most_played = max(games, key=lambda x: (x["wins"] + x["losses"])) if games else None
most_played_title = most_played["title"] if (most_played and (most_played["wins"] + most_played["losses"]) > 0) else "N/A"

# Dashboard Header
st.title("Rank Tracker")

# Summary Cards Header
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Matches", total_all_matches)
with m2:
    st.metric("Overall Win Rate", f"{global_wr:.1f}%")
with m3:
    st.metric("Record (W - L)", f"{total_wins} - {total_losses}")
with m4:
    st.metric("Most Played", most_played_title)

st.divider()

# Sidebar Controls
st.sidebar.header("Management")

with st.sidebar.expander("➕ Add New Game", expanded=False):
    new_title = st.text_input("Game Title")
    new_cover = st.text_input("Cover Image URL (2:3 Poster)", "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600")
    new_rank = st.text_input("Current Rank Name", "Unranked")
    new_peak = st.text_input("Peak Rank Name", "Unranked")
    new_rank_icon = st.text_input("Rank Icon Image URL", "https://cdn-icons-png.flaticon.com/512/616/616490.png")
    
    if st.button("Save Game"):
        if new_title:
            new_id = max([g["id"] for g in games] + [0]) + 1
            games.append({
                "id": new_id,
                "title": new_title,
                "cover": new_cover,
                "rank_name": new_rank,
                "peak_rank": new_peak,
                "rank_icon": new_rank_icon,
                "wins": 0,
                "losses": 0,
                "streak": 0,
                "notes": ""
            })
            save_games()
            st.success(f"Added {new_title}!")
            st.rerun()

with st.sidebar.expander("🗑️ Remove Game"):
    if games:
        game_to_remove = st.selectbox("Select Game to Delete", [g["title"] for g in games])
        if st.button("Confirm Delete"):
            st.session_state.games = [g for g in games if g["title"] != game_to_remove]
            save_games()
            st.warning(f"Deleted {game_to_remove}")
            st.rerun()

# 4-Column Card Grid
cols_per_row = 4

for i in range(0, len(games), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(games):
            game = games[i + j]
            total_m = game["wins"] + game["losses"]
            wr = (game["wins"] / total_m * 100) if total_m > 0 else 0.0
            
            # Progress bar color logic
            if wr >= 55.0:
                bar_class = "progress-fill-green"
            elif wr >= 50.0:
                bar_class = "progress-fill-yellow"
            else:
                bar_class = "progress-fill-red"
            
            # Streak formatting
            stk = game.get("streak", 0)
            if stk > 0:
                streak_str = f"🔥 {stk} W Streak"
            elif stk < 0:
                streak_str = f"📉 {abs(stk)} L Streak"
            else:
                streak_str = "Even"

            with cols[j]:
                # Poster & Stats Container
                st.markdown(f"""
                <div class="steam-card">
                    <img src="{game['cover']}" class="cover-art" />
                    <div class="game-title">{game['title']}</div>
                    
                    <div class="rank-row">
                        <img src="{game['rank_icon']}" class="rank-icon" />
                        <div style="font-size:0.83rem; color:#8f98a0;">Peak: <strong style="color:#ffffff;">{game['peak_rank']}</strong></div>
                    </div>
                    
                    <div style="font-size:0.88rem; font-weight:600; margin-bottom:6px; padding-left:2px;">
                        Current: <span style="color:#66c0f4;">{game['rank_name']}</span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="stat-badge">W/L: {game['wins']}-{game['losses']}</span>
                        <span class="stat-badge">{wr:.1f}% WR</span>
                    </div>
                    
                    <div class="progress-container">
                        <div class="{bar_class}" style="width: {min(wr, 100)}%;"></div>
                    </div>
                    
                    <div style="font-size:0.75rem; color:#8f98a0; text-align:right;">
                        {streak_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick Match Logger Buttons
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if st.button("➕ Win", key=f"qw_{game['id']}", use_container_width=True):
                        game["wins"] += 1
                        game["streak"] = (game.get("streak", 0) + 1) if game.get("streak", 0) >= 0 else 1
                        save_games()
                        st.rerun()
                with btn_c2:
                    if st.button("➕ Loss", key=f"ql_{game['id']}", use_container_width=True):
                        game["losses"] += 1
                        game["streak"] = (game.get("streak", 0) - 1) if game.get("streak", 0) <= 0 else -1
                        save_games()
                        st.rerun()
                
                # Extended Edit & Notes Drawer
                with st.expander("⚙️ Edit Game & Notes"):
                    st.caption("📊 Match Stats & Streak")
                    col_w, col_l = st.columns(2)
                    with col_w:
                        game['wins'] = st.number_input("Wins", min_value=0, value=game['wins'], key=f"w_{game['id']}")
                    with col_l:
                        game['losses'] = st.number_input("Losses", min_value=0, value=game['losses'], key=f"l_{game['id']}")
                    
                    game['streak'] = st.number_input("Streak (+ Win / - Loss)", value=game.get('streak', 0), key=f"stk_{game['id']}")
                    
                    st.divider()
                    st.caption("🏆 Rank Details")
                    game['rank_name'] = st.text_input("Current Rank", value=game['rank_name'], key=f"rn_{game['id']}")
                    game['peak_rank'] = st.text_input("Peak Rank", value=game['peak_rank'], key=f"pr_{game['id']}")
                    game['rank_icon'] = st.text_input("Rank Icon URL", value=game['rank_icon'], key=f"ri_{game['id']}")
                    
                    st.divider()
                    st.caption("🖼️ Artwork & Notes")
                    game['cover'] = st.text_input("2:3 Poster URL", value=game['cover'], key=f"c_{game['id']}")
                    game['notes'] = st.text_area("Session Notes", value=game.get('notes', ""), key=f"nt_{game['id']}", placeholder="e.g., Aim was locked in on hitscan today...")
                    
                    st.divider()
                    if st.button("Save Changes", key=f"btn_{game['id']}"):
                        save_games()
                        st.success("Updated & Saved!")
                        st.rerun()
