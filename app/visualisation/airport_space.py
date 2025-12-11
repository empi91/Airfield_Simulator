import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio


class PlanePlot:
    def __init__(self, planes: dict) -> None:
        self.planes = planes
        planes_df = pd.DataFrame(self.planes)
        # planes_df = pd.DataFrame(planes)
        self.draw_plot(planes_df)

    def draw_plot(self, planes):
        fig = px.scatter_3d(
            planes,
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


if __name__ == "__main__":
    plane_data: dict = {
        "plane_id": ["PLANE_001", "PLANE_002"],
        "x": [1005, 2503],
        "y": [2007, 2000],
        "z": [2000, 3500],
        "fuel": [35, 178.2],
    }
    plot = PlanePlot(plane_data)
