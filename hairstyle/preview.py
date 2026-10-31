"""Procedural silhouettes on a generic head, not a personalized virtual try-on."""
import numpy as np
import plotly.graph_objects as go

def make_preview(style: dict, color: str = "#352820") -> go.Figure:
    theta, phi = np.meshgrid(np.linspace(0, 2*np.pi, 64), np.linspace(0, np.pi, 40))
    x = .78*np.sin(phi)*np.cos(theta)
    y = .68*np.sin(phi)*np.sin(theta)
    z = 1.05*np.cos(phi)
    fig = go.Figure(go.Surface(x=x, y=y, z=z, showscale=False,
                               colorscale=[[0, "#D5B89D"], [1, "#D5B89D"]],
                               hoverinfo="skip"))
    volume = style["preview"]["volume"]
    drop = style["preview"]["drop"]
    # Front (+y) leaves the face exposed; sides/back extend with length.
    angle = np.linspace(0, 2*np.pi, 64)
    cutoff = 1.25 + drop*(1-np.maximum(np.sin(angle), 0))
    t, a = np.meshgrid(np.linspace(0, 1, 32), angle, indexing="ij")
    p = t * cutoff
    ripple = style["preview"]["texture"] * np.sin(12*a)*np.sin(9*p)
    radius = 1 + volume + ripple
    fig.add_trace(go.Surface(
        x=.80*radius*np.sin(p)*np.cos(a),
        y=.70*radius*np.sin(p)*np.sin(a),
        z=1.08*np.cos(p) + volume,
        colorscale=[[0, color], [1, color]], showscale=False, hoverinfo="skip"))
    # Eyes and nose establish the front orientation.
    fig.add_trace(go.Scatter3d(x=[-.25, .25, 0], y=[.635, .635, .74],
                              z=[.20, .20, -.05], mode="markers",
                              marker=dict(size=[4, 4, 5], color="#493A32"),
                              hoverinfo="skip", showlegend=False))
    fig.update_layout(
        height=430, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="#FBF8F3", uirevision=style["id"],
        scene=dict(xaxis=dict(visible=False, range=[-1.5,1.5]),
                   yaxis=dict(visible=False, range=[-1.5,1.5]),
                   zaxis=dict(visible=False, range=[-1.4,1.7]),
                   aspectmode="data", camera=dict(eye=dict(x=1.2,y=2,z=.5))))
    return fig
