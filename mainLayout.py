from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# from dash_bootstrap_templates import load_figure_template
import pandas as pd

from utils import dash_reusable_components as drc
from utils import layout_reusable_components as lrc
from productPerformanceTab import layout as productPerformanceLayout
from userClassificationTab import layout as userClassificationLayout

app = Dash(__name__)

filter_column = dbc.Card(
    dbc.Row(
        dbc.Col(
            [
                drc.NamedDropdown(
                    "Year", id="filter_year_dropdown"
                ),
                drc.NamedDropdown(
                    "Region",
                    id="filter_region_dropdown",
                ),
                drc.NamedDropdown(
                    "Country",
                    id="filter_country_dropdown",
                ),
                dbc.Button(
                    "Filter",
                    className="d-grid gap-2 col-6 mx-auto my-1",
                    size="sm",
                    id="filter_button",
                ),
            ]
        )
    )
)

productPerformanceTab = dbc.Tab(productPerformanceLayout, label="Product Performance")
userClassificationTab = dbc.Tab(userClassificationLayout, label="Customers Segments")

allTabs = dbc.Tabs(
    [
        productPerformanceTab,
        userClassificationTab,
    ],
    id="allTabs",
)


main_inner_layout = dbc.Row(
    [
        dbc.Col([filter_column], width=2),
        dbc.Col([allTabs], width=10),
    ]
)


root_layout = [
    lrc.DashboardBanner(app, "grinta-logo.png"),
    main_inner_layout,
    lrc.DashboardFooter(app, "textlesslogo.png"),
]
