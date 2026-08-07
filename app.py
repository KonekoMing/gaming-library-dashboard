import streamlit as st
import json
import os
import requests
import base64

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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

    .block-container { max-width: 1250px !important; }
    .stMarkdown, .stMarkdown p { margin: 0 !important; padding: 0 !important; }
    
    .fancy-header {
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        color: #ffffff;
        margin-top: 1rem;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
    }
    
    /* Apple-Style Glass Game Cards */
    .custom-card {
        background: rgba(20, 30, 48, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        border-left: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 0; 
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 6px;
    }
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 45px rgba(56, 189, 248, 0.25);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    .img-container {
        position: relative;
        width: 100%;
        overflow: hidden;
        border-radius: 16px 16px 0 0; 
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    
    .card-img {
        width: 100%;
        display: block;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    .custom-card:hover .card-img { transform: scale(1.04); }
    
    .glare {
        position: absolute;
        top: 0;
        left: -150%;
        width: 50%;
        height: 100%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.25) 50%, rgba(255,255,255,0) 100%);
        transform: skewX(-25deg);
        pointer-events: none;
        z-index: 2;
    }
    .custom-card:hover .glare {
        left: 200%;
        transition: left 0.6s ease-in-out;
    }
    
    .card-body {
        padding: 12px 10px 14px 10px;
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
    
    .rank-info {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(0, 0, 0, 0.35);
        padding: 8px 10px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    .rank-icon { width: 32px; height: 32px; object-fit: contain; }
    .rank-text { font-size: 0.85rem; line-height: 1.4; }
    .peak-rank { color: #cbd5e1; }
    .peak-rank strong { color: #f8fafc; font-weight: 600; }
    .current-rank { font-weight: 500; color: #f1f5f9; }
    .highlight-blue { color: #38bdf8; font-weight: 700; text-shadow: 0 0 8px rgba(56, 189, 248, 0.4); }
    
    .stats-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        font-weight: 600;
        color: #e2e8f0;
        padding: 0 4px;
    }
    .progress-bar-bg {
        background-color: rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 6px;
        height: 8px;
        width: 100%;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    .progress-fill-green { background: linear-gradient(90deg, #10b981, #34d399); height: 100%; box-shadow: 0 0 10px rgba(16,185,129,0.5); }
    .progress-fill-yellow { background: linear-gradient(90deg, #f59e0b, #fbbf24); height: 100%; box-shadow: 0 0 10px rgba(245,158,11,0.5); }
    .progress-fill-red { background: linear-gradient(90deg, #ef4444, #f87171); height: 100%; box-shadow: 0 0 10px rgba(239,68,68,0.5); }
    
    .streak-text {
        font-size: 0.8rem;
        color: #cbd5e1;
        text-align: right;
        margin-top: -4px;
        padding-right: 4px;
    }
    
    /* Win / Loss Neon Glass Buttons */
    section[data-testid="stMain"] button[kind="primary"] {
        background: rgba(57, 255, 20, 0.08) !important;
        border: 2px solid rgba(57, 255, 20, 0.7) !important;
        color: #39FF14 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stMain"] button[kind="primary"]:hover {
        background: rgba(57, 255, 20, 0.25) !important;
        color: #ffffff !important;
        border: 2px solid #39FF14 !important;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.5) !important;
    }
    
    section[data-testid="stMain"] button[kind="secondary"] {
        background: rgba(255, 51, 51, 0.08) !important;
        border: 2px solid rgba(255, 51, 51, 0.7) !important;
        color: #FF3333 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stMain"] button[kind="secondary"]:hover {
        background: rgba(255, 51, 51, 0.25) !important;
        color: #ffffff !important;
        border: 2px solid #FF3333 !important;
        box-shadow: 0 0 15px rgba(255, 51, 51, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

if "games" not in st.session_state:
    st.session_state.games = load_games()

games = st.session_state.games

st.markdown('<div class="fancy-header">Rank Tracker</div>', unsafe_allow_html=True)

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

cols = st.columns(4)

for idx, game in enumerate(games):
    with cols[idx % 4]:
        total_m = game["wins"] + game["losses"]
        wr = (game["wins"] / total_m * 100) if total_m > 0 else 0.0
        
        bar_class = "progress-fill-green" if wr >= 55 else "progress-fill-yellow" if wr >= 50 else "progress-fill-red"
        stk = game.get("streak", 0)
        streak_str = f"🔥 {stk} W Streak" if stk > 0 else f"📉 {abs(stk)} L Streak" if stk < 0 else "Even"
        
        html_card = f'<div class="custom-card"><div class="img-container"><img src="{game["cover"]}" class="card-img" /><div class="glare"></div></div><div class="card-body"><div class="card-title">{game["title"]}</div><div class="rank-info"><img src="{game["rank_icon"]}" class="rank-icon" /><div class="rank-text"><span class="peak-rank">Peak: <strong>{game["peak_rank"]}</strong></span><br><span class="current-rank">Current: <span class="highlight-blue">{game["rank_name"]}</span></span></div></div><div class="stats-row"><span>W/L: {game["wins"]} - {game["losses"]}</span><span class="highlight-blue">{wr:.1f}% WR</span></div><div class="progress-bar-bg"><div class="{bar_class}" style="width: {min(wr, 100)}%;"></div></div><div class="streak-text">{streak_str}</div></div></div>'
        
        st.markdown(html_card, unsafe_allow_html=True)
        
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
            if st.button("Save Changes", key=f"btn_{game['id']}"):
                save_games()
                st.success("Updated & Saved!")
                st.rerun()
