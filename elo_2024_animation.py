import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.cm import get_cmap
from pathlib import Path
import requests

##############################################################################
# 1.  Load & pre-process the data
##############################################################################
# Download the CSV if not present

CSV_PATH = Path("atp_matches_2024.csv")
if not CSV_PATH.exists():
    url = "https://github.com/JeffSackmann/tennis_atp/raw/master/atp_matches_2024.csv"
    response = requests.get(url)
    response.raise_for_status()
    CSV_PATH.write_bytes(response.content)
CSV_PATH = Path("atp_matches_2024.csv")
K             = 32          # Elo sensitivity
DEFAULT_ELO   = 1500
MIN_ELO_SHOWN = 1400        # y-axis lower bound in the animation

df = pd.read_csv(CSV_PATH)

# Pick a date column and convert to datetime -------------------------------
if "tourney_date" in df.columns:                         # --> 20240529
    df["match_date"] = pd.to_datetime(df["tourney_date"].astype(str))
elif "date" in df.columns:                               # --> 2024-05-29
    df["match_date"] = pd.to_datetime(df["date"])
else:
    raise ValueError(
        "CSV must contain either a 'tourney_date' (yyyymmdd) "
        "or a 'date' (yyyy-mm-dd) column."
    )

# Keep only 2024 matches and sort chronologically --------------------------
df = df[df["match_date"].dt.year == 2024].sort_values("match_date").reset_index(drop=True)

##############################################################################
# 2.  Compute Elo ratings after every match
##############################################################################
def expected_score(r_a, r_b):
    """Probability that player-A beats player-B under Elo."""
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))

elo = {}             # current ratings {player: rating}
snapshots = []       # list of (date, ratings-dict)

current_day = None
for _, row in df.iterrows():
    winner, loser = row["winner_name"], row["loser_name"]
    day          = row["match_date"].date()

    r_w = elo.get(winner, DEFAULT_ELO)
    r_l = elo.get(loser,  DEFAULT_ELO)

    exp_w = expected_score(r_w, r_l)

    # Update ratings --------------------------------------------------------
    r_w += K * (1 - exp_w)
    r_l += K * (0 - (1 - exp_w))
    elo[winner] = r_w
    elo[loser]  = r_l

    # Store a snapshot *once per calendar day* -----------------------------
    if current_day is None or day != current_day:
        snapshots.append((day, elo.copy()))
        current_day = day

##############################################################################
# 3.  Prepare the animation data
##############################################################################
frames = []
for day, rating_dict in snapshots:
    top10 = sorted(rating_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    players, scores = zip(*top10)
    frames.append((day, list(players), list(scores)))

parula = get_cmap("parula") if "parula" in plt.colormaps() else get_cmap("viridis")

##############################################################################
# 4.  Build the bar-chart race with Matplotlib
##############################################################################
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

def init():
    ax.set_xlim(MIN_ELO_SHOWN, 2400)
    ax.set_xlabel("Elo rating")
    return []

def update(frame_idx):
    day, players, scores = frames[frame_idx]
    ax.clear()

    # Reverse order so highest Elo is at the top
    players = players[::-1]
    scores = scores[::-1]

    bars = ax.barh(
        players,
        scores,
        color=parula(np.linspace(0, 1, len(players))),
        edgecolor="k",
    )

    # Labels & styling
    ax.set_xlim(MIN_ELO_SHOWN, 2400)
    ax.set_xlabel("Elo rating")
    ax.set_title(f"Top-10 Elo ratings · {day.strftime('%d %b %Y')}")
    ax.set_yticklabels(players, rotation=0)
    ax.set_ylabel("Players (ranked)")
    ax.grid(axis="x", linestyle=":", alpha=0.4)

    # Add value labels at the end of bars
    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_width() + 5,
            bar.get_y() + bar.get_height() / 2,
            f"{score:.0f}",
            ha="left",
            va="center",
            fontsize=8,
        )
    return bars

anim = FuncAnimation(
    fig,
    update,
    frames=len(frames),
    init_func=init,
    interval=500,       # ms between frames
    blit=False,
)

##############################################################################
# 5.  Save as GIF
##############################################################################
OUTPUT_GIF = Path("elo_2024_animation.gif")
anim.save(OUTPUT_GIF, writer=PillowWriter(fps=2))
plt.close(fig)

print(f"✔ Animation saved to {OUTPUT_GIF.resolve()}")