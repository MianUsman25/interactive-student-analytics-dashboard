from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("data.csv")

# =========================
# LIGHT WARM COLOR PALETTE
# =========================

COLORS = {
    "bg_main":      "#fffbf0",        # warm cream background
    "bg_card":      "#ffffff",        # white cards
    "bg_header":    "#fef9ec",        # soft yellow header strip
    "accent_yellow":"#f59e0b",        # golden yellow — primary accent
    "accent_orange":"#f97316",        # warm orange
    "accent_teal":  "#0d9488",        # teal green
    "accent_rose":  "#e11d48",        # rose red
    "accent_purple":"#7c3aed",        # purple
    "accent_blue":  "#2563eb",        # blue
    "text_primary": "#1c1917",        # near-black text
    "text_muted":   "#78716c",        # warm grey
    "border":       "#fde68a",        # light yellow border
    "border_card":  "#e7e5e4",        # card border
    "shadow":       "rgba(245, 158, 11, 0.12)",
}

PLOTLY_LIGHT = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(255,251,240,0.5)",
        "font": {"color": "#1c1917", "family": "Nunito, sans-serif"},
        "xaxis": {
            "gridcolor":     "#fde68a",
            "zerolinecolor": "#fcd34d",
            "tickfont":      {"color": "#78716c"},
            "linecolor":     "#fde68a",
        },
        "yaxis": {
            "gridcolor":     "#fde68a",
            "zerolinecolor": "#fcd34d",
            "tickfont":      {"color": "#78716c"},
            "linecolor":     "#fde68a",
        },
        "legend": {
            "bgcolor":     "rgba(255,255,255,0.9)",
            "bordercolor": "#fde68a",
            "borderwidth": 1,
        },
        "margin": {"l": 50, "r": 20, "t": 50, "b": 50},
    }
}

# =========================
# CREATE DASH APP
# =========================

app = Dash(__name__)

app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Student Productivity Analytics</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: #fffbf0;
            font-family: 'Nunito', sans-serif;
        }

        ::-webkit-scrollbar { width: 7px; }
        ::-webkit-scrollbar-track { background: #fef3c7; }
        ::-webkit-scrollbar-thumb { background: #fcd34d; border-radius: 4px; }

        .kpi-card {
            transition: transform 0.22s ease, box-shadow 0.22s ease;
            cursor: default;
        }
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 16px 40px rgba(245,158,11,0.18) !important;
        }

        .chart-card {
            transition: box-shadow 0.2s ease;
        }
        .chart-card:hover {
            box-shadow: 0 8px 30px rgba(245,158,11,0.15) !important;
        }

        .dropdown-filter .Select-control {
            background-color: #fffbf0 !important;
            border: 1.5px solid #fcd34d !important;
            border-radius: 10px !important;
        }
        .dropdown-filter .Select-value-label { color: #1c1917 !important; }
        .dropdown-filter .Select-placeholder   { color: #a8a29e !important; }
        .dropdown-filter .Select-menu-outer {
            background-color: #fffdf5 !important;
            border: 1.5px solid #fcd34d !important;
            border-radius: 10px !important;
        }
        .dropdown-filter .VirtualizedSelectOption    { color: #1c1917 !important; }
        .dropdown-filter .VirtualizedSelectFocusedOption { background-color: #fef3c7 !important; }
        .dropdown-filter .Select-arrow { border-top-color: #f59e0b !important; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""

# =========================
# APP LAYOUT
# =========================

app.layout = html.Div(
    style={
        "backgroundColor": COLORS["bg_main"],
        "minHeight": "100vh",
        "padding": "28px 36px",
        "fontFamily": "Nunito, sans-serif",
    },
    children=[

        # ── HEADER ────────────────────────────────────────────────────
        html.Div(
            style={
                "background": "linear-gradient(135deg, #fef3c7 0%, #fffbf0 60%, #fef9ec 100%)",
                "border": f"1.5px solid {COLORS['border']}",
                "borderRadius": "20px",
                "padding": "24px 30px",
                "marginBottom": "28px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "boxShadow": f"0 4px 20px {COLORS['shadow']}",
            },
            children=[
                html.Div([
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "14px", "marginBottom": "6px"},
                        children=[
                            html.Div("🎓", style={"fontSize": "36px", "lineHeight": "1"}),
                            html.H1(
                                "Student Productivity Analytics",
                                style={
                                    "color": COLORS["text_primary"],
                                    "fontSize": "26px",
                                    "fontFamily": "Playfair Display, serif",
                                    "fontWeight": "700",
                                    "letterSpacing": "-0.3px",
                                }
                            )
                        ]
                    ),
                    html.P(
                        "Track academic performance, burnout levels, and productivity insights.",
                        style={"color": COLORS["text_muted"], "fontSize": "13.5px", "paddingLeft": "50px"}
                    )
                ]),

                html.Div(
                    style={
                        "background": "#fef3c7",
                        "border": f"1.5px solid {COLORS['border']}",
                        "borderRadius": "12px",
                        "padding": "10px 22px",
                        "textAlign": "center",
                    },
                    children=[
                        html.Div("📊", style={"fontSize": "20px", "marginBottom": "2px"}),
                        html.Div(f"{len(df):,}", style={"color": COLORS["accent_yellow"], "fontWeight": "800", "fontSize": "22px"}),
                        html.Div("students", style={"color": COLORS["text_muted"], "fontSize": "11px", "fontWeight": "600"})
                    ]
                )
            ]
        ),

        # ── FILTER SECTION ────────────────────────────────────────────
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px", "marginBottom": "24px"},
            children=[

                html.Div(
                    style={
                        "background": COLORS["bg_card"],
                        "border": f"1.5px solid {COLORS['border_card']}",
                        "borderLeft": f"4px solid {COLORS['accent_yellow']}",
                        "borderRadius": "14px",
                        "padding": "16px 20px",
                        "boxShadow": f"0 2px 10px {COLORS['shadow']}",
                    },
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "gap": "8px", "marginBottom": "10px"},
                            children=[
                                html.Span("👤", style={"fontSize": "16px"}),
                                html.Label("Filter by Gender", style={"color": COLORS["text_muted"], "fontSize": "11.5px", "fontWeight": "700", "letterSpacing": "0.6px", "textTransform": "uppercase"})
                            ]
                        ),
                        dcc.Dropdown(
                            id="gender_filter",
                            className="dropdown-filter",
                            options=[{"label": g, "value": g} for g in df["gender"].unique()],
                            value=df["gender"].unique()[0],
                        )
                    ]
                ),

                html.Div(
                    style={
                        "background": COLORS["bg_card"],
                        "border": f"1.5px solid {COLORS['border_card']}",
                        "borderLeft": f"4px solid {COLORS['accent_orange']}",
                        "borderRadius": "14px",
                        "padding": "16px 20px",
                        "boxShadow": f"0 2px 10px {COLORS['shadow']}",
                    },
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "gap": "8px", "marginBottom": "10px"},
                            children=[
                                html.Span("🎓", style={"fontSize": "16px"}),
                                html.Label("Filter by Academic Level", style={"color": COLORS["text_muted"], "fontSize": "11.5px", "fontWeight": "700", "letterSpacing": "0.6px", "textTransform": "uppercase"})
                            ]
                        ),
                        dcc.Dropdown(
                            id="academic_filter",
                            className="dropdown-filter",
                            options=[{"label": a, "value": a} for a in df["academic_level"].unique()],
                            value=df["academic_level"].unique()[0],
                        )
                    ]
                ),

            ]
        ),

        # ── KPI CARDS ─────────────────────────────────────────────────
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "16px", "marginBottom": "24px"},
            children=[

                html.Div(
                    className="kpi-card",
                    style={
                        "background": "linear-gradient(135deg, #fffbeb, #fef3c7)",
                        "border": f"1.5px solid {COLORS['border']}",
                        "borderRadius": "16px",
                        "padding": "22px",
                        "boxShadow": f"0 4px 16px {COLORS['shadow']}",
                    },
                    children=[
                        html.Div("📝", style={"fontSize": "28px", "marginBottom": "10px"}),
                        html.P("Avg Exam Score", style={"color": COLORS["text_muted"], "fontSize": "11px", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.6px", "marginBottom": "6px"}),
                        html.H2(f"{round(df['exam_score'].mean(), 1)}", style={"color": COLORS["accent_yellow"], "fontSize": "36px", "fontFamily": "Playfair Display, serif", "fontWeight": "700"}),
                        html.P("out of 100", style={"color": COLORS["text_muted"], "fontSize": "12px", "marginTop": "4px"}),
                    ]
                ),

                html.Div(
                    className="kpi-card",
                    style={
                        "background": "linear-gradient(135deg, #f0fdfa, #ccfbf1)",
                        "border": "1.5px solid #99f6e4",
                        "borderRadius": "16px",
                        "padding": "22px",
                        "boxShadow": "0 4px 16px rgba(13,148,136,0.10)",
                    },
                    children=[
                        html.Div("⚡", style={"fontSize": "28px", "marginBottom": "10px"}),
                        html.P("Avg Productivity", style={"color": COLORS["text_muted"], "fontSize": "11px", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.6px", "marginBottom": "6px"}),
                        html.H2(f"{round(df['productivity_score'].mean(), 1)}", style={"color": COLORS["accent_teal"], "fontSize": "36px", "fontFamily": "Playfair Display, serif", "fontWeight": "700"}),
                        html.P("productivity index", style={"color": COLORS["text_muted"], "fontSize": "12px", "marginTop": "4px"}),
                    ]
                ),

                html.Div(
                    className="kpi-card",
                    style={
                        "background": "linear-gradient(135deg, #fff1f2, #ffe4e6)",
                        "border": "1.5px solid #fecdd3",
                        "borderRadius": "16px",
                        "padding": "22px",
                        "boxShadow": "0 4px 16px rgba(225,29,72,0.08)",
                    },
                    children=[
                        html.Div("🔥", style={"fontSize": "28px", "marginBottom": "10px"}),
                        html.P("Avg Burnout", style={"color": COLORS["text_muted"], "fontSize": "11px", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.6px", "marginBottom": "6px"}),
                        html.H2(f"{round(df['burnout_level'].mean(), 1)}", style={"color": COLORS["accent_rose"], "fontSize": "36px", "fontFamily": "Playfair Display, serif", "fontWeight": "700"}),
                        html.P("burnout index", style={"color": COLORS["text_muted"], "fontSize": "12px", "marginTop": "4px"}),
                    ]
                ),

                html.Div(
                    className="kpi-card",
                    style={
                        "background": "linear-gradient(135deg, #f5f3ff, #ede9fe)",
                        "border": "1.5px solid #ddd6fe",
                        "borderRadius": "16px",
                        "padding": "22px",
                        "boxShadow": "0 4px 16px rgba(124,58,237,0.08)",
                    },
                    children=[
                        html.Div("😴", style={"fontSize": "28px", "marginBottom": "10px"}),
                        html.P("Avg Sleep Hours", style={"color": COLORS["text_muted"], "fontSize": "11px", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.6px", "marginBottom": "6px"}),
                        html.H2(f"{round(df['sleep_hours'].mean(), 1)}h", style={"color": COLORS["accent_purple"], "fontSize": "36px", "fontFamily": "Playfair Display, serif", "fontWeight": "700"}),
                        html.P("per night avg", style={"color": COLORS["text_muted"], "fontSize": "12px", "marginTop": "4px"}),
                    ]
                ),

            ]
        ),

        # ── CHARTS ROW 1 ──────────────────────────────────────────────
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "3fr 2fr", "gap": "16px", "marginBottom": "16px"},
            children=[

                html.Div(
                    className="chart-card",
                    style={"background": COLORS["bg_card"], "border": f"1.5px solid {COLORS['border_card']}", "borderRadius": "16px", "padding": "8px", "boxShadow": f"0 2px 12px {COLORS['shadow']}"},
                    children=[dcc.Graph(id="scatter_chart", style={"height": "380px"})]
                ),

                html.Div(
                    className="chart-card",
                    style={"background": COLORS["bg_card"], "border": f"1.5px solid {COLORS['border_card']}", "borderRadius": "16px", "padding": "8px", "boxShadow": f"0 2px 12px {COLORS['shadow']}"},
                    children=[dcc.Graph(id="bar_chart", style={"height": "380px"})]
                )

            ]
        ),

        # ── CHARTS ROW 2 ──────────────────────────────────────────────
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
            children=[

                html.Div(
                    className="chart-card",
                    style={"background": COLORS["bg_card"], "border": f"1.5px solid {COLORS['border_card']}", "borderRadius": "16px", "padding": "8px", "boxShadow": f"0 2px 12px {COLORS['shadow']}"},
                    children=[dcc.Graph(id="box_chart", style={"height": "340px"})]
                ),

                html.Div(
                    className="chart-card",
                    style={"background": COLORS["bg_card"], "border": f"1.5px solid {COLORS['border_card']}", "borderRadius": "16px", "padding": "8px", "boxShadow": f"0 2px 12px {COLORS['shadow']}"},
                    children=[dcc.Graph(id="heatmap_chart", style={"height": "340px"})]
                )

            ]
        ),

        # ── FOOTER ────────────────────────────────────────────────────
        html.Div(
            style={"marginTop": "28px", "textAlign": "center"},
            children=[
                html.P(
                    "✨ Student Productivity Analytics Dashboard  ·  Built with Plotly Dash",
                    style={"color": COLORS["text_muted"], "fontSize": "12px"}
                )
            ]
        )

    ]
)

# =========================
# CALLBACK
# =========================

@app.callback(
    [
        Output("scatter_chart", "figure"),
        Output("bar_chart",     "figure"),
        Output("box_chart",     "figure"),
        Output("heatmap_chart", "figure"),
    ],
    [
        Input("gender_filter",   "value"),
        Input("academic_filter", "value"),
    ]
)
def update_dashboard(selected_gender, selected_academic):

    filtered_df = df[
        (df["gender"] == selected_gender) &
        (df["academic_level"] == selected_academic)
    ]

    title_style = {"font": {"size": 14, "color": "#1c1917", "family": "Playfair Display, serif"}, "x": 0.03}

    # ── SCATTER ──────────────────────────────
    scatter_fig = px.scatter(
        filtered_df,
        x="study_hours",
        y="exam_score",
        color="burnout_level",
        size="productivity_score",
        color_continuous_scale=["#34d399", "#fbbf24", "#f43f5e"],
        hover_data=["sleep_hours", "focus_index", "mental_health_score"],
        title="<b>Study Hours vs Exam Score</b>",
        labels={"study_hours": "Study Hours / Day", "exam_score": "Exam Score"},
    )
    scatter_fig.update_layout(
        **PLOTLY_LIGHT["layout"],
        title=title_style,
        coloraxis_colorbar={"title": "Burnout", "tickfont": {"color": "#78716c"}, "title_font": {"color": "#78716c"}},
    )
    scatter_fig.update_traces(marker=dict(opacity=0.82, line=dict(width=0.6, color="white")))

    # ── BAR ──────────────────────────────────
    avg_productivity = (
        filtered_df.groupby("internet_quality")["productivity_score"]
        .mean().reset_index()
        .sort_values("productivity_score", ascending=True)
    )
    bar_fig = px.bar(
        avg_productivity,
        x="productivity_score",
        y="internet_quality",
        orientation="h",
        color="productivity_score",
        color_continuous_scale=["#fde68a", "#f59e0b", "#d97706"],
        title="<b>Productivity by Internet Quality</b>",
        labels={"productivity_score": "Avg Productivity", "internet_quality": ""},
        text=avg_productivity["productivity_score"].round(1),
    )
    bar_fig.update_layout(
        **PLOTLY_LIGHT["layout"],
        title=title_style,
        showlegend=False,
        coloraxis_showscale=False,
    )
    bar_fig.update_traces(textposition="outside", textfont={"color": "#78716c", "size": 11}, marker_line_width=0)

    # ── BOX PLOT ─────────────────────────────
    box_fig = px.box(
        filtered_df,
        x="internet_quality",
        y="exam_score",
        color="internet_quality",
        color_discrete_sequence=["#f59e0b", "#0d9488", "#e11d48", "#7c3aed"],
        title="<b>Exam Score Distribution by Internet Quality</b>",
        labels={"exam_score": "Exam Score", "internet_quality": "Internet Quality"},
    )
    box_fig.update_layout(**PLOTLY_LIGHT["layout"], title=title_style, showlegend=False)

    # ── HEATMAP ──────────────────────────────
    numeric_cols = ["study_hours", "exam_score", "sleep_hours", "productivity_score", "burnout_level", "focus_index"]
    corr = filtered_df[numeric_cols].corr().round(2)

    heatmap_fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=[c.replace("_", " ").title() for c in corr.columns],
        y=[c.replace("_", " ").title() for c in corr.index],
        colorscale=[[0.0, "#e11d48"], [0.5, "#fef9ec"], [1.0, "#0d9488"]],
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text}",
        textfont={"size": 10, "color": "#1c1917"},
        hoverongaps=False,
    ))
    heatmap_fig.update_layout(
        **PLOTLY_LIGHT["layout"],
        title={"text": "<b>Correlation Heatmap</b>", **title_style},
    )

    return scatter_fig, bar_fig, box_fig, heatmap_fig


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)