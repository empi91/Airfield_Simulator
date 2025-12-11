import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

x_eye = -1.25
y_eye = 2
z_eye = 0.5

plane_data = {
    "plane_id": ["PLANE_001", "PLANE_002"],
    "x": [1005, 2503],
    "y": [2007, 2000],
    "z": [2000, 3500],
    "fuel": [35, 178.2],
}

df = pd.DataFrame(plane_data)
print(df)


fig = px.scatter_3d(
    plane_data,
    x="x",
    y="y",
    z="z",
    color="fuel",
    opacity=0.7,
    width=2000,
    height=1000,
    range_x=[10000, 0],
    range_y=[10000, 0],
    range_z=[0, 5000],
)


pio.show(fig)
