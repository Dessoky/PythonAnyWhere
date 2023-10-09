from dash import dcc, html
import dash_bootstrap_components as dbc


def DashboardBanner(app, image_path):
    return dbc.Row(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src=app.get_asset_url(image_path),
                                    className="img-fluid rounded-start",
                                    style={"width": "inherit"},
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H1(
                                            id="banner_title",
                                            className="card-title",
                                            style={
                                                "color": "gold",
                                            },
                                        ),
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3 bg-secoundry",
                # style={"background-color": "#c19c60"},
            )
        ]
    )


def DashboardFooter(app,image_path):
    return dbc.Row(
        [
            html.Footer(
                children=[
                    dcc.Markdown(
                        "#### **Data Analysis Team**",
                        className="text-white",
                    ),
                    dbc.CardImg(
                        src=app.get_asset_url(image_path),
                        className="img-fluid rounded-start mb-2",
                        style={"width": "20%"},
                    ),
                ],
                className="mt-3 text-center",
                # style={"background-color": "#c19c60"},
            )
        ]
    )
