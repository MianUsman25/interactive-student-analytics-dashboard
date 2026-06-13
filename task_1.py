import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import http.server
import socketserver

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("data.csv")

# ============================================================
# DATA CLEANING
# ============================================================

# Remove infinite values
df = df.replace([float("inf"), -float("inf")], 0)

# Fill missing numeric values
numeric_cols = [
    "study_hours",
    "exam_score",
    "productivity_score",
    "sleep_hours",
    "burnout_level"
]

df[numeric_cols] = df[numeric_cols].fillna(0)

print("\n✅ Missing Values Check")
print(df[numeric_cols].isna().sum())

# ============================================================
# LIGHT CREAM THEME COLORS
# ============================================================

BG_COLOR = "#FFFDF7"          # Main cream background
CARD_COLOR = "#FFF8E7"        # Soft card cream
GRID_COLOR = "#E9DFC3"        # Warm grid
TEXT_COLOR = "#3B3024"        # Dark brown text
ACCENT_YELLOW = "#F4C542"     # Main yellow
ACCENT_GOLD = "#E8B923"       # Gold
ACCENT_ORANGE = "#F59E0B"     # Orange yellow
ACCENT_SOFT = "#FFE082"       # Soft yellow

# ============================================================
# CHART 1 — INTERACTIVE SCATTER PLOT
# ============================================================

fig1 = px.scatter(
    df,
    x="study_hours",
    y="exam_score",
    color="gender",
    size="productivity_score",
    hover_data={
        "academic_level": True,
        "sleep_hours": True,
        "burnout_level": True,
        "productivity_score": ":.1f",
    },
    color_discrete_sequence=[
        ACCENT_YELLOW,
        ACCENT_ORANGE,
        "#FFD54F"
    ],
    title="Study Hours vs Exam Score",
    template="plotly_white",
    opacity=0.80,
)

fig1.update_traces(
    marker=dict(
        line=dict(width=1.2, color="white")
    )
)

fig1.update_layout(
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=CARD_COLOR,
    font=dict(
        family="Segoe UI",
        size=14,
        color=TEXT_COLOR
    ),
    title=dict(
        text="📚 Study Hours vs Exam Score",
        x=0.03,
        font=dict(size=24)
    ),
    xaxis=dict(
        title="Daily Study Hours",
        gridcolor=GRID_COLOR,
        showspikes=True,
        spikecolor=ACCENT_GOLD,
        spikesnap="cursor",
    ),
    yaxis=dict(
        title="Exam Score",
        gridcolor=GRID_COLOR,
        showspikes=True,
        spikecolor=ACCENT_GOLD,
    ),
    legend=dict(
        bgcolor="#FFF9EC",
        bordercolor=ACCENT_SOFT,
        borderwidth=1
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Segoe UI"
    ),
    height=600,
)

fig1.add_annotation(
    text="✨ Bubble size represents productivity score",
    xref="paper",
    yref="paper",
    x=0.99,
    y=1.08,
    showarrow=False,
    font=dict(size=12, color="#7C5E10")
)

# ============================================================
# CHART 2 — INTERACTIVE BAR CHART
# ============================================================

avg_scores = (
    df.groupby("academic_level")["exam_score"]
    .agg(["mean", "std", "count"])
    .reset_index()
    .rename(columns={
        "mean": "avg_score",
        "std": "std_score",
        "count": "n"
    })
)

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=avg_scores["academic_level"],
    y=avg_scores["avg_score"],
    text=avg_scores["avg_score"].round(1),
    textposition="outside",
    customdata=avg_scores[["n"]].values,
    marker=dict(
        color=avg_scores["avg_score"],
        colorscale=[
            [0, "#FFE082"],
            [0.5, "#F4C542"],
            [1, "#E8B923"]
        ],
        line=dict(color="white", width=1.5)
    ),
    hovertemplate=(
        "<b>%{x}</b><br><br>"
        "Average Score: %{y:.1f}<br>"
        "Students: %{customdata[0]}<extra></extra>"
    )
))

fig2.update_layout(
    title=dict(
        text="🏆 Average Exam Score by Academic Level",
        x=0.03,
        font=dict(size=24)
    ),
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=CARD_COLOR,
    font=dict(
        family="Segoe UI",
        size=14,
        color=TEXT_COLOR
    ),
    xaxis=dict(
        title="Academic Level",
        gridcolor=GRID_COLOR
    ),
    yaxis=dict(
        title="Average Exam Score",
        gridcolor=GRID_COLOR
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13
    ),
    showlegend=False,
    height=550,
)

# ============================================================
# CHART 3 — MULTI PANEL DASHBOARD
# ============================================================

fig3 = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "Study Hours vs Exam Score",
        "Average Score by Academic Level",
        "Sleep Hours vs Productivity",
        "Burnout by Internet Quality"
    ],
    horizontal_spacing=0.10,
    vertical_spacing=0.12
)

# ------------------------------------------------------------
# PANEL 1
# ------------------------------------------------------------

for gender, grp in df.groupby("gender"):
    fig3.add_trace(
        go.Scatter(
            x=grp["study_hours"],
            y=grp["exam_score"],
            mode="markers",
            name=gender,
            marker=dict(
                size=7,
                opacity=0.7
            )
        ),
        row=1,
        col=1
    )

# ------------------------------------------------------------
# PANEL 2
# ------------------------------------------------------------

avg_lvl = (
    df.groupby("academic_level")["exam_score"]
    .mean()
    .reset_index()
)

fig3.add_trace(
    go.Bar(
        x=avg_lvl["academic_level"],
        y=avg_lvl["exam_score"],
        marker_color=ACCENT_YELLOW,
        showlegend=False
    ),
    row=1,
    col=2
)

# ------------------------------------------------------------
# PANEL 3
# ------------------------------------------------------------

fig3.add_trace(
    go.Scatter(
        x=df["sleep_hours"],
        y=df["productivity_score"],
        mode="markers",
        marker=dict(
            color=df["burnout_level"],
            colorscale="YlOrBr",
            size=6,
            opacity=0.7,
            showscale=True,
            colorbar=dict(
                title="Burnout"
            )
        ),
        showlegend=False
    ),
    row=2,
    col=1
)

# ------------------------------------------------------------
# PANEL 4
# ------------------------------------------------------------

for quality, grp in df.groupby("internet_quality"):
    fig3.add_trace(
        go.Box(
            y=grp["burnout_level"],
            name=quality,
            boxmean=True,
            fillcolor=ACCENT_SOFT,
            marker_color=ACCENT_ORANGE
        ),
        row=2,
        col=2
    )

# ============================================================
# DASHBOARD STYLING
# ============================================================

fig3.update_layout(
    title=dict(
        text="📊 Student Productivity Analytics Dashboard",
        x=0.03,
        font=dict(size=26)
    ),
    paper_bgcolor=BG_COLOR,
    plot_bgcolor=CARD_COLOR,
    font=dict(
        family="Segoe UI",
        size=13,
        color=TEXT_COLOR
    ),
    height=750,
    hoverlabel=dict(
        bgcolor="white"
    ),
    legend=dict(
        bgcolor="#FFF9EC",
        bordercolor=ACCENT_SOFT,
        borderwidth=1
    )
)

# Grid styling
for ax in [
    fig3.layout.xaxis,
    fig3.layout.xaxis2,
    fig3.layout.xaxis3,
    fig3.layout.xaxis4,
    fig3.layout.yaxis,
    fig3.layout.yaxis2,
    fig3.layout.yaxis3,
    fig3.layout.yaxis4,
]:
    ax.update(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR
    )

# ============================================================
# SAVE HTML FILES
# ============================================================

fig1.write_html(
    "scatter_plot.html",
    include_plotlyjs="inline"
)

fig2.write_html(
    "bar_chart.html",
    include_plotlyjs="inline"
)

fig3.write_html(
    "multi_panel.html",
    include_plotlyjs="inline"
)

print("\n📁 HTML Files Saved Successfully")
print("   ✔ scatter_plot.html")
print("   ✔ bar_chart.html")
print("   ✔ multi_panel.html")

# ============================================================
# LOCALHOST SERVER
# ============================================================

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("\n🚀 LOCAL SERVER STARTED")
    print("\nOpen these links in your browser:\n")

    print(f"📊 Scatter Plot : http://localhost:{PORT}/scatter_plot.html")
    print(f"📊 Bar Chart    : http://localhost:{PORT}/bar_chart.html")
    print(f"📊 Dashboard    : http://localhost:{PORT}/multi_panel.html")

    print("\n🛑 Press CTRL + C to stop server")

    httpd.serve_forever()