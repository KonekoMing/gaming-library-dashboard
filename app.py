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
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 2,
        "title": "Rainbow Six Siege",
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 3,
        "title": "Fortnite",
        "cover": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 4,
        "title": "Modern Warfare 4",
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 5,
        "title": "Tekken 8",
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 6,
        "title": "Arena Breakout Infinite",
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 7,
        "title": "Delta Force",
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/616/616490.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
    },
    {
        "id": 8,
        "title": "FragPunk",
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600",
        "rank_name": "Unranked",
        "peak_rank": "Unranked",
        "rank_icon": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        "wins": 0, "losses": 0, "streak": 0, "notes": ""
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

# High-End Global CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

    /* Dark Theme Background */
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    
    /* Lock max width to prevent stretching on Macs */
    .block-container { max-width: 1250px !important; }
    .stMarkdown, .stMarkdown p { margin: 0 !important; padding: 0 !important; }
    
    /* Fancy Centered Header */
    .fancy-header {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        color: #f8fafc;
        margin-top: 1rem;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.6), 0 0 30px rgba(56, 189, 248, 0.4);
    }
    
    /* Modern Custom Game Card - FULL BLEED EDGE-TO-EDGE */
    .custom-card {
        background: linear-gradient(145deg, #151f2b 0%, #0d131a 100%);
        border: 1px solid #233547;
        border-radius: 12px;
        padding: 0; 
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 6px;
    }
    .custom-card:hover {
        border-color: #38bdf8;
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.2);
    }
    
    /* Image Container for Glare Effect */
    .img-container {
        position: relative;
        width: 100%;
        overflow: hidden;
        border-radius: 12px 12px 0 0; 
        border-bottom: 1px solid #233547;
    }
    
    /* 2:3 Vertical Poster Settings */
    .card-img {
        width: 100%;
        display: block;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    .custom-card:hover .card-img {
        transform: scale(1.04);
    }
    
    /* Steam Style Glare */
    .glare {
        position: absolute;
        top: 0;
        left: -150%;
        width: 50%;
        height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
        transform: skewX(-25deg);
        pointer-events: none;
        z-index: 2;
    }
    .custom-card:hover .glare {
        left: 200%;
        transition: left 0.6s ease-in-out;
    }
    
    /* Stats and Text Container */
    .card-body {
        padding: 10px 10px 14px 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc;
        text-align: center;
        letter-spacing: 0.5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Rank Pill Box */
    .rank-info {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(0,0,0,0.3);
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid #1e293b;
    }
    .rank-icon { width: 32px; height: 32px; object-fit: contain; }
    .rank-text { font-size: 0.85rem; line-height: 1.4; }
    .peak-rank { color: #94a3b8; }
    .peak-rank strong { color: #f1f5f9; font-weight: 600; }
    .current-rank { font-weight: 500; color: #e2e8f0; }
    .highlight-blue { color: #38bdf8; font-weight: 700; }
    
    /* Stats & Progress */
    .stats-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        font-weight: 600;
        color: #cbd5e1;
        padding: 0 4px;
    }
    .progress-bar-bg {
        background-color: #1e293b;
        border-radius: 6px;
        height: 6px;
        width: 100%;
        overflow: hidden;
    }
    .progress-fill-green { background-color: #10b981; height: 100%; }
    .progress-fill-yellow { background-color: #f59e0b; height: 100%; }
    .progress-fill-red { background-color: #ef4444; height: 100%; }
    
    .streak-text {
        font-size: 0.8rem;
        color: #94a3b8;
        text-align: right;
        margin-top: -4px;
        padding-right: 4px;
    }
    
    /* ==========================================
       VIBRANT NEON OUTLINE BUTTONS
       Targeting nested grid columns safely
       ========================================== */
       
    /* 1. WIN BUTTONS (Neon Lime Green Outline) */
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: rgba(57, 255, 20, 0.05) !important;
        border: 2px solid #39FF14 !important;
        color: #39FF14 !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    /* Inner & Outer Glow on Hover */
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="primary"]:hover {
        background-color: rgba(57, 255, 20, 0.15) !important;
        color: #ffffff !important;
        text-shadow: 0 0 5px rgba(255,255,255,0.8) !important;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.4), inset 0 0 15px rgba(57, 255, 20, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="primary"]:active {
        transform: translateY(1px) !important;
        box-shadow: 0 0 8px rgba(57, 255, 20, 0.3), inset 0 0 8px rgba(57, 255, 20, 0.4) !important;
    }
    
    /* 2. LOSS BUTTONS (Neon Ruby Red Outline) */
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: rgba(255, 51, 51, 0.05) !important;
        border: 2px solid #FF3333 !important;
        color: #FF3333 !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    /* Inner & Outer Glow on Hover */
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
        background-color: rgba(255, 51, 51, 0.15) !important;
        color: #ffffff !important;
        text-shadow: 0 0 5px rgba(255,255,255,0.8) !important;
        box-shadow: 0 0 15px rgba(255, 51, 51, 0.4), inset 0 0 15px rgba(255, 51, 51, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    section[data-testid="stMain"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] button[kind="secondary"]:active {
        transform: translateY(1px) !important;
        box-shadow: 0 0 8px rgba(255, 51, 51, 0.3), inset 0 0 8px rgba(255, 51, 51, 0.4) !important;
    }

    /* STEALTHY EDIT EXPANDER */
    div[data-testid="stExpander"] {
        border: 1px solid #233547 !important;
        border-radius: 8px !important;
        background-color: #0f1722 !important;
        margin-top: -5px;
    }
    div[data-testid="stExpander"] summary {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #38bdf8 !important;
    }
    
    /* Ensure the "Save Changes" button inside the expander stays subtle */
    div[data-testid="stExpander"] button[kind="secondary"] {
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
    }
    div[data-testid="stExpander"] button[kind="secondary"]:hover {
        background: #38bdf8 !important;
        color: #0b0f19 !important;
    }
</style>
""", unsafe_allow_html=True)

if "games" not in st.session_state:
    st.session_state.games = load_games()

games = st.session_state.games

# Display Centered Fancy Header
st.markdown('<div class="fancy-header">Rank Tracker</div>', unsafe_allow_html=True)

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
                "id": new_id, "title": new_title, "cover": new_cover,
                "rank_name": new_rank, "peak_rank": new_peak, "rank_icon": new_rank_icon,
                "wins": 0, "losses": 0, "streak": 0, "notes": ""
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

# Dynamic Card Grid
cols = st.columns(4)

for idx, game in enumerate(games):
    with cols[idx % 4]:
        total_m = game["wins"] + game["losses"]
        wr = (game["wins"] / total_m * 100) if total_m > 0 else 0.0
        
        bar_class = "progress-fill-green" if wr >= 55 else "progress-fill-yellow" if wr >= 50 else "progress-fill-red"
        stk = game.get("streak", 0)
        streak_str = f"🔥 {stk} W Streak" if stk > 0 else f"📉 {abs(stk)} L Streak" if stk < 0 else "Even"
        
        # 100% flat HTML string
        html_card = f'<div class="custom-card"><div class="img-container"><img src="{game["cover"]}" class="card-img" /><div class="glare"></div></div><div class="card-body"><div class="card-title">{game["title"]}</div><div class="rank-info"><img src="{game["rank_icon"]}" class="rank-icon" /><div class="rank-text"><span class="peak-rank">Peak: <strong>{game["peak_rank"]}</strong></span><br><span class="current-rank">Current: <span class="highlight-blue">{game["rank_name"]}</span></span></div></div><div class="stats-row"><span>W/L: {game["wins"]} - {game["losses"]}</span><span class="highlight-blue">{wr:.1f}% WR</span></div><div class="progress-bar-bg"><div class="{bar_class}" style="width: {min(wr, 100)}%;"></div></div><div class="streak-text">{streak_str}</div></div></div>'
        
        st.markdown(html_card, unsafe_allow_html=True)
        
        # === FOOLPROOF BUTTON ROUTING ===
        # Win is hardcoded to "primary", Loss is hardcoded to "secondary"
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("➕ Win", key=f"qw_{game['id']}", use_container_width=True, type="primary"):
                game["wins"] += 1
                game["streak"] = (game.get("streak", 0) + 1) if game.get("streak", 0) >= 0 else 1
                save_games()
                st.rerun()
        with btn_c2:
            if st.button("➕ Loss", key=f"ql_{game['id']}", use_container_width=True, type="secondary"):
                game["losses"] += 1
                game["streak"] = (game.get("streak", 0) - 1) if game.get("streak", 0) <= 0 else -1
                save_games()
                st.rerun()
        
        with st.expander("⚙️ Edit Options"):
            st.caption("📊 Match Stats & Streak")
            col_w, col_l = st.columns(2)
            with col_w: game['wins'] = st.number_input("Wins", min_value=0, value=game['wins'], key=f"w_{game['id']}")
            with col_l: game['losses'] = st.number_input("Losses", min_value=0, value=game['losses'], key=f"l_{game['id']}")
            
            game['streak'] = st.number_input("Streak", value=game.get('streak', 0), key=f"stk_{game['id']}")
            
            st.divider()
            st.caption("🏆 Rank Details")
            game['rank_name'] = st.text_input("Current Rank", value=game['rank_name'], key=f"rn_{game['id']}")
            game['peak_rank'] = st.text_input("Peak Rank", value=game['peak_rank'], key=f"pr_{game['id']}")
            game['rank_icon'] = st.text_input("Rank Icon URL", value=game['rank_icon'], key=f"ri_{game['id']}")
            
            st.divider()
            st.caption("🖼️ Artwork & Notes")
            game['cover'] = st.text_input("2:3 Poster URL", value=game['cover'], key=f"c_{game['id']}")
            game['notes'] = st.text_area("Session Notes", value=game.get('notes', ""), key=f"nt_{game['id']}")
            
            st.divider()
            # This is "secondary" by default, so it gets the grey override in CSS
            if st.button("Save Changes", key=f"btn_{game['id']}"):
                save_games()
                st.success("Updated & Saved!")
                st.rerun()
