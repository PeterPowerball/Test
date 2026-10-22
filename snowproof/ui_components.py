"""Reusable UI pieces: header, map, gauge and charts.

Pages call these functions and pass in data they got from data_access.py.
Nothing in here fetches data on its own.
"""

import folium
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium

from snowproof import config


# ----------------------------------------------------------------- small helpers
def format_minutes(minutes: int) -> str:
    """135 -> '2 h 15 min'."""
    hours, mins = divmod(int(minutes), 60)
    return f"{hours} h {mins:02d} min" if hours else f"{mins} min"


def _style(fig: go.Figure, height: int = 320) -> go.Figure:
    """Same look for every chart."""
    fig.update_layout(
        template="plotly_white", height=height, margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color=config.TEXT_DARK), legend=dict(orientation="h", y=-0.2),
    )
    return fig


def show_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch")


# ------------------------------------------------------------------------ header
def app_header() -> None:
    """Title, tagline and the prototype banner."""
    st.markdown(
        f"<h1 style='color:{config.BRAND_BLUE};margin-bottom:0'>🏔️ Snow-Proof</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("##### Where will the snow be good for your ski holiday?")
    st.caption("Prototype: all numbers are mock data.")


# --------------------------------------------------------------------------- map
def build_map(resorts: pd.DataFrame, chances: dict[str, float] | None, selected_id: str | None) -> folium.Map:
    """Map with one circle per resort.

    Size = total piste km. Color = neutral blue, grey without station, or traffic light
    if `chances` (resort_id -> chance) is given.
    """
    fmap = folium.Map(location=config.MAP_CENTER, zoom_start=config.MAP_ZOOM, tiles=None,
                      control_scale=True, zoom_control=True)
    folium.TileLayer(tiles=config.SWISSTOPO_TILES, attr=config.SWISSTOPO_ATTRIBUTION,
                     name="swisstopo map", max_zoom=18).add_to(fmap)
    # Fallback base map, can be switched on in the layer control
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="© OpenStreetMap contributors © CARTO", name="CartoDB positron (fallback)", show=False,
    ).add_to(fmap)
    folium.LayerControl(collapsed=True).add_to(fmap)

    for _, r in resorts.iterrows():
        if not r["has_station"]:
            color = config.GREY
        elif chances is not None and r["resort_id"] in chances:
            color = config.chance_color(chances[r["resort_id"]])
        else:
            color = config.ACCENT_BLUE
        is_selected = r["resort_id"] == selected_id
        folium.CircleMarker(
            location=[r["lat"], r["lon"]],
            radius=5 + r["total_piste_km"] ** 0.5 * 0.7,
            color=config.TEXT_DARK if is_selected else "white",
            weight=4 if is_selected else 1.5,
            fill=True, fill_color=color, fill_opacity=0.85,
            tooltip=r["name"],
        ).add_to(fmap)
    return fmap


def show_map(fmap: folium.Map, key: str) -> str | None:
    """Render the map and return the name of the clicked resort (or None).

    We only ask for the last clicked tooltip, so panning and zooming do not rerun the app.
    """
    out = st_folium(fmap, height=520, use_container_width=True, key=key,
                    returned_objects=["last_object_clicked_tooltip"])
    clicked = (out or {}).get("last_object_clicked_tooltip")
    return clicked.strip() if clicked else None


def map_legend(with_chances: bool) -> None:
    """Small legend below the map."""
    def dot(color: str, text: str) -> str:
        return (f"<span style='display:inline-block;width:12px;height:12px;border-radius:50%;"
                f"background:{color};margin-right:6px;vertical-align:middle'></span>{text}"
                f"<span style='margin-right:16px'></span>")

    if with_chances:
        html = (dot(config.GREEN, "Good odds") + dot(config.AMBER, "Mixed odds")
                + dot(config.RED, "Poor odds") + dot(config.GREY, "No station nearby"))
    else:
        html = dot(config.ACCENT_BLUE, "Resort with snow data") + dot(config.GREY, "No station nearby")
    st.markdown(html + "<br><small>Circle size = total piste km</small>", unsafe_allow_html=True)


# ------------------------------------------------------------------ resort panel
def piste_bar(pistes: pd.DataFrame) -> go.Figure:
    """Horizontal stacked bar of piste km by difficulty."""
    fig = go.Figure()
    for _, row in pistes.iterrows():
        fig.add_bar(y=["Pistes"], x=[row["km"]], name=row["difficulty"], orientation="h",
                    marker_color=config.PISTE_COLORS[row["difficulty"]],
                    text=[f"{row['km']:.0f} km"], textposition="inside",
                    textfont=dict(color="white"))
    fig.update_layout(barmode="stack", yaxis=dict(visible=False), xaxis_title="km")
    return _style(fig, height=170)


def station_box(station: dict | None) -> None:
    """Which station the snow data comes from, or a warning if there is none."""
    if station:
        st.info(f"Snow data from station **{station['name']}** "
                f"({station['altitude_m']:,} m, {station['distance_km']:g} km away)")
    else:
        st.warning("No reliable measurement station nearby. A snow forecast is not available for this resort.")


# --------------------------------------------------------------------- snow check
def chance_bar(chance: float, baseline: float, verdict: str) -> None:
    """One card with the chance as a 0 to 100% bar and the historical average as a marker.

    Plain HTML instead of a chart: it is just one bar, and this way it scales nicely on phones.
    """
    color = config.chance_color(chance)
    pct, base_pct = round(chance * 100), round(baseline * 100)
    st.markdown(
        f"""
        <div style="border:1px solid {config.ICE_BLUE};border-radius:12px;padding:20px 24px;margin:8px 0 16px">
          <div style="font-size:2rem;font-weight:700;color:{color}">{pct}%
            <span style="font-size:1.2rem;font-weight:600;color:{config.TEXT_DARK}">chance of a good ski week</span>
          </div>
          <div style="position:relative;height:28px;background:#EEF2F6;border-radius:14px;margin:18px 0 6px">
            <div style="width:{pct}%;height:100%;background:{color};border-radius:14px"></div>
            <div title="Historical average" style="position:absolute;left:{base_pct}%;top:-6px;bottom:-6px;
                 width:3px;background:{config.BRAND_BLUE};transform:translateX(-50%)"></div>
          </div>
          <div style="position:relative;height:20px;font-size:0.8rem;color:#5B6675">
            <span style="position:absolute;left:0">0%</span>
            <span style="position:absolute;left:50%;transform:translateX(-50%)">50%</span>
            <span style="position:absolute;right:0">100%</span>
          </div>
          <div style="margin-top:10px">
            <span style="display:inline-block;width:3px;height:14px;background:{config.BRAND_BLUE};
                  vertical-align:middle;margin-right:6px"></span>
            Historical average for this week: <b>{base_pct}%</b>
          </div>
          <div style="margin-top:6px">{verdict}</div>
          <div style="margin-top:10px;font-size:0.85rem;color:#5B6675">
            A good ski week means at least {config.GOOD_SNOW_CM} cm of snow depth on all
            {config.GOOD_WEEK_DAYS} days at the linked station.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def weekly_chart(weekly: pd.DataFrame) -> go.Figure:
    """Chance per week of the stay, with the historical average as markers."""
    fig = go.Figure()
    fig.add_bar(x=weekly["label"], y=weekly["chance"] * 100, name="Model",
                marker_color=[config.chance_color(c) for c in weekly["chance"]],
                text=[f"{c:.0%}" for c in weekly["chance"]], textposition="outside")
    fig.add_scatter(x=weekly["label"], y=weekly["baseline"] * 100, name="Historical average",
                    mode="markers", marker=dict(symbol="diamond", size=11, color=config.BRAND_BLUE))
    fig.update_layout(title="Chance of a good week", yaxis=dict(title="%", range=[0, 110]))
    return _style(fig)


def daily_snow_chart(daily: pd.DataFrame) -> go.Figure:
    """Expected snow depth per day with an uncertainty band and the 50 cm line."""
    fig = go.Figure()
    fig.add_scatter(x=daily["date"], y=daily["high_cm"], mode="lines", line=dict(width=0),
                    showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=daily["date"], y=daily["low_cm"], mode="lines", line=dict(width=0),
                    fill="tonexty", fillcolor="rgba(46,134,193,0.25)", name="Likely range (80%)")
    fig.add_scatter(x=daily["date"], y=daily["expected_cm"], mode="lines+markers",
                    line=dict(color=config.BRAND_BLUE, width=3), name="Expected snow depth")
    fig.add_hline(y=config.GOOD_SNOW_CM, line_dash="dash", line_color=config.RED,
                  annotation_text=f"{config.GOOD_SNOW_CM} cm threshold", annotation_position="top left")
    fig.update_layout(title="Expected snow depth per day", yaxis_title="cm")
    return _style(fig)


# ------------------------------------------------------------------- model page
def walk_forward_timeline(results: pd.DataFrame) -> go.Figure:
    """Training (dark) and test (light) periods of each validation round."""
    fig = go.Figure()
    for i, (_, r) in enumerate(results.iterrows()):
        t0, t1 = (int(x) for x in r["train_period"].split("-"))
        s0, s1 = (int(x) for x in r["test_period"].split("-"))
        fig.add_bar(y=[r["round"]], x=[t1 - t0 + 1], base=[t0], orientation="h",
                    marker_color=config.BRAND_BLUE, name="Train", legendgroup="train",
                    showlegend=(i == 0))
        fig.add_bar(y=[r["round"]], x=[s1 - s0 + 1], base=[s0], orientation="h",
                    marker_color=config.AMBER, name="Test", legendgroup="test", showlegend=(i == 0))
    fig.update_layout(barmode="overlay", yaxis=dict(autorange="reversed"),
                      xaxis=dict(range=[1950, 2026], title="Year"), title="Walk-forward validation")
    return _style(fig, height=300)


def model_vs_baseline_chart(results: pd.DataFrame, model_col: str, baseline_col: str, title: str) -> go.Figure:
    """Grouped bars: model versus simple historical baseline, per round."""
    fig = go.Figure()
    fig.add_bar(x=results["round"], y=results[model_col], name="Model", marker_color=config.BRAND_BLUE)
    fig.add_bar(x=results["round"], y=results[baseline_col], name="Historical baseline",
                marker_color=config.GREY)
    fig.update_layout(barmode="group", title=title)
    return _style(fig)


def future_range_chart(outlook: pd.DataFrame) -> go.Figure:
    """Range band of good ski weeks per season, per decade (illustration)."""
    fig = go.Figure()
    fig.add_scatter(x=outlook["decade"], y=outlook["high_weeks"], mode="lines", line=dict(width=0),
                    showlegend=False, hoverinfo="skip")
    fig.add_scatter(x=outlook["decade"], y=outlook["low_weeks"], mode="lines", line=dict(width=0),
                    fill="tonexty", fillcolor="rgba(46,134,193,0.25)", name="Range across climate models")
    fig.add_scatter(x=outlook["decade"], y=outlook["median_weeks"], mode="lines+markers",
                    line=dict(color=config.BRAND_BLUE, width=3), name="Median")
    fig.update_layout(title="Good ski weeks per season (illustration)", yaxis_title="weeks")
    return _style(fig, height=360)
