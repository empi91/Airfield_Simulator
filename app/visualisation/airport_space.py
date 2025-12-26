import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import Dash, Input, Output, dcc, html

# app.layout = html.Div(
#     children=[
#         html.Div(
#             children=[
#                 html.Div(
#                     children=[
#                         html.Div(children="Region", className="menu-title"),
#                         dcc.Dropdown(
#                             id="region-filter",
#                             options=[
#                                 {"label": region, "value": region}
#                                 for region in regions
#                             ],
#                             value="Albany",
#                             clearable=False,
#                             className="dropdown",
#                         ),
#                     ]
#                 ),
#                 html.Div(
#                     children=[
#                         html.Div(children="Type", className="menu-title"),
#                         dcc.Dropdown(
#                             id="type-filter",
#                             options=[
#                                 {
#                                     "label": avocado_type.title(),
#                                     "value": avocado_type,
#                                 }
#                                 for avocado_type in avocado_types
#                             ],
#                             value="organic",
#                             clearable=False,
#                             searchable=False,
#                             className="dropdown",
#                         ),
#                     ],
#                 ),
#                 html.Div(
#                     children=[
#                         html.Div(
#                             children="Date Range", className="menu-title"
#                         ),
#                         dcc.DatePickerRange(
#                             id="date-range",
#                             min_date_allowed=data["Date"].min().date(),
#                             max_date_allowed=data["Date"].max().date(),
#                             start_date=data["Date"].min().date(),
#                             end_date=data["Date"].max().date(),
#                         ),
#                     ]
#                 ),
#             ],
#             className="menu",
#         ),
#     ]
# )


class WebLayout:
    def __init__(self):
        self.app = self.create_app()
        self.register_callbacks()

    def create_app(self):
        app = Dash(__name__)
        app.title = "Airport Simulator"
        app.layout = html.Div(
            children=[
                html.Div(
                    # HEADER
                    children=[
                        html.H1(children="Airport Simulator", className="header-title"),
                        html.P(
                            children=(
                                "Real time airport control tower simulation"
                                "Up to 100 planes trying to land simultanously,"
                                "without crashing at each other, before run out of fuel"
                            ),
                            className="header-description",
                        ),
                    ],
                    className="header",
                ),
                html.Div(
                    # REAL TIME DATA: planes_flying, planes_landed, planes_crashed
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children="PLANES FLYING:", className="data-label"
                                ),
                                html.Div(children="1", className="data-value"),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children="PLANES LANDED:", className="data-label"
                                ),
                                html.Div(children="0", className="data-value"),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    children="PLANES CRASHED:", className="data-label"
                                ),
                                html.Div(children="0", className="data-value"),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    # REAL TIME 3D PLANES PLOT
                    children=[html.Div(children=dcc.Graph(id="planes-graph"))]
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=2000,  # Update every 2 seconds (2000 milliseconds)
                    n_intervals=0,
                ),
            ]
        )
        return app

    def register_callbacks(self):
        @self.app.callback(
            Output("planes-graph", "figure"),
            Input("interval-component", "n_intervals"),
        )
        def update_graph(n):
            # Import here to avoid circular imports
            from app.database import Database

            db = Database()
            planes = db.get_all_planes()

            plane_dict = {
                "plane_id": [],
                "x": [],
                "y": [],
                "z": [],
                "fuel": [],
            }

            for plane in planes:
                plane_dict["plane_id"].append(plane.plane_id)
                plane_dict["x"].append(plane.x_pos)
                plane_dict["y"].append(plane.y_pos)
                plane_dict["z"].append(plane.z_pos)
                plane_dict["fuel"].append(plane.fuel_left)

            scatter_figure = px.scatter_3d(
                data_frame=plane_dict,
                x="x",
                y="y",
                z="z",
                color="fuel",
                hover_data=["plane_id"],
                opacity=0.7,
                width=2000,
                height=1000,
                range_x=[10000, 0],
                range_y=[10000, 0],
                range_z=[0, 5000],
            )
            return scatter_figure

    def run(self, debug=True, port=8050):
        self.app.run(debug=debug, port=port)
