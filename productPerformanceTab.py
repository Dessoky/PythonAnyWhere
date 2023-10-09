from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

import iconsVisuals

# from dash_bootstrap_templates import load_figure_template


visuals_column = dbc.Card(
    [
        dbc.Row(html.Div(dcc.Graph(id="productPerformanceTabVisual1"))),
        dbc.Row(html.Div(dcc.Graph(id="productPerformanceTabVisual2"))),
    ]
)

matrix_column = dbc.Card(
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([dcc.Graph(id="productPerformanceTabVisual3")], width=6),
                    dbc.Col([dcc.Graph(id="productPerformanceTabVisual4")], width=6),
                ]
            ),
            dbc.Row(
                dbc.RadioItems(
                    options=[
                        {
                            "label": iconsVisuals.icon_maker(
                                iconsVisuals.table,
                                "Region Census",
                            ),
                            "value": "RC",
                        },
                        {
                            "label": iconsVisuals.icon_maker(
                                iconsVisuals.ads,
                                "Suggested Bundles",
                            ),
                            "value": "SB",
                        },
                    ],
                    value="RC",
                    id="productPerformanceTabSuggestedBundles",
                    inline=True,
                    className="d-flex justify-content-center",
                )
            ),
            dbc.Row(
                [
                    dcc.Loading(
                        html.Div(
                            id="productPerformanceTabMatrixHeader",
                            className="text-white text-center bg-primary",
                        )
                    ),
                    dcc.Loading(
                        html.Div(
                            ["Todo Add Matrix"],
                            id="productPerformanceTabMatrix1",
                            className="text-center",
                        ),
                        type="circle",
                    ),
                ]
            ),
        ]
    )
)


layout = dbc.Row(
    [
        dbc.Col([visuals_column], width=6),
        dbc.Col([matrix_column], width=6),
    ]
)
