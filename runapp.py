from dash import Dash, html, Input, Output, State
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from mainLayout import root_layout
import dataFunctions
import dataVisuals
from dataReady import df, df_grouped, customer_segments_df

app = Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP])
load_figure_template("cybrog")

app.layout = dbc.Container(
    children=[*root_layout],
    fluid=True,
    className="dbc",
)


@app.callback(
    Output("banner_title", "children"),
    Output("filter_year_dropdown", "options"),
    Output("filter_region_dropdown", "options"),
    Input("allTabs", "active_tab"),
)
def banner_title_maker(active_tab):
    if not active_tab:
        raise PreventUpdate
    tab_suffix = int(active_tab[-1])
    if tab_suffix == 0:
        return "Product Performance", df["Year"].unique(), df["Region"].unique()
    if tab_suffix == 1:
        return "Customers Segments", df["Year"].unique(), df["Region"].unique()


@app.callback(
    Output("filter_country_dropdown", "options"),
    Input(
        "filter_region_dropdown",
        "value",
    ),
)
def country_dropdown(region):
    if not region:
        raise PreventUpdate
    return df.query("Region == @region")["Country"].unique()


# Product Performance Callbacks


@app.callback(
    Output("productPerformanceTabVisual1", "figure"),
    Output("productPerformanceTabVisual2", "figure"),
    State("filter_year_dropdown", "value"),
    State("filter_region_dropdown", "value"),
    State("filter_country_dropdown", "value"),
    Input("filter_button", "n_clicks"),
)
def product_performance_first_column(year, region, country, filter_button):
    _df = df_grouped.copy()
    if year != None:
        _df = _df.query("Year == @year")
    if region != None:
        _df = _df.query("Region == @region")
    if country != None:
        _df = _df.query("Country == @country")
    _product_list_visual1 = dataFunctions.top_products_by_quantity(_df)
    visual1 = dataVisuals.plotly_bar_chart(
        df=_df.query("ProductName in @_product_list_visual1")
        .groupby("ProductName", as_index=False)["Quantity"]
        .sum()
        .sort_values(by=["Quantity"], ascending=False),
        x="ProductName",
        y="Quantity",
        title="Top 10 Products by Quantity",
        x_title="",
        y_title="Total Quantity",
    )

    _product_list_visual2 = dataFunctions.top_product_by_revenue(_df)
    visual2 = dataVisuals.plotly_bar_chart(
        df=_df.query("ProductName in @_product_list_visual2")
        .groupby("ProductName", as_index=False)["totalPriceSold"]
        .sum()
        .sort_values(by=["totalPriceSold"], ascending=False),
        x="ProductName",
        y="totalPriceSold",
        x_title="",
        y_title="Total Revenue",
        title="Top 10 Products by Revenue",
    )
    return visual1, visual2


@app.callback(
    Output("productPerformanceTabVisual3", "figure"),
    Output("productPerformanceTabVisual4", "figure"),
    State("filter_year_dropdown", "value"),
    Input("filter_button", "n_clicks"),
)
def product_performance_scound_column(year, filter_button):
    _df = df.copy()
    if year != None:
        _df = _df.query("Year == @year")
    _df_visual = dataFunctions.region_dataframe(_df)
    _df_visual_for_rest_of_world = _df_visual.copy()
    _df_visual_for_rest_of_world["Region"] = _df_visual_for_rest_of_world[
        "Region"
    ].apply(lambda x: x if x == "Europe" else "Rest of The World")
    visual1 = dataVisuals.plotly_pie_chart(
        df=_df_visual_for_rest_of_world,
        names="Region",
        values="tot_amount",
        title="Revenue by Regions",
        legend_title="Regions",
    )
    viusal2 = dataVisuals.plotly_pie_chart(
        df=_df_visual,
        names="Region",
        values="mean_amount",
        title="Mean Revenue by Regions",
        legend_title="Regions",
    )
    return visual1, viusal2


@app.callback(
    Output("productPerformanceTabMatrix1", "children"),
    Output("productPerformanceTabMatrixHeader", "children"),
    State("filter_year_dropdown", "value"),
    State("filter_region_dropdown", "value"),
    State("filter_country_dropdown", "value"),
    Input("productPerformanceTabSuggestedBundles", "value"),
    Input("filter_button", "n_clicks"),
)
def product_performance_table(year, region, country, radio_button_input, n_clicks):
    _df = df.copy()
    _df_suggested = df.copy()
    if year != None:
        _df = _df.query("Year == @year")
        _df_suggested = _df_suggested.query("Year == @year")
    if region != None:
        _df_suggested = _df_suggested.query("Region == @region")
    if country != None:
        _df_suggested = _df_suggested.query("Country == @country")
    _df_visual = dataFunctions.region_dataframe(_df)
    if radio_button_input == "RC":
        table = dataVisuals.table_without_filters(
            df=_df_visual.rename(
                {
                    "tot_amount": "Total Revenue",
                    "mean_amount": "Mean Revenue",
                    "n_Transactions": "# Transactions",
                    "mean_Quantity": "Mean Quantity",
                },
                axis=1,
            ),
            dbc=dbc,
        )
        table_header = f"Region performance in {year if year != None else 'All years'}"
    if radio_button_input == "SB":
        transactions_ids = list(_df_suggested["TransactionNo"].unique())
        table = dataVisuals.table_without_filters(
            df=dataFunctions.items_bundles(transactions_ids), dbc=dbc
        )
        year_title = year if year != None else "All Years"
        region_title = region if region != None else "All Regions"
        country_title = country if country != None else "All Countries"
        table_header = (
            f"Bundles suggestion for {region_title} in {country_title} -- {year_title}"
        )
    return table, table_header


# Customer Segments Callbacks

@app.callback(
    Output("userClassificationTabVisual1", "figure"),
    Output("userClassificationTabVisual2", "figure"),
    State("filter_year_dropdown", "value"),
    State("filter_region_dropdown", "value"),
    State("filter_country_dropdown", "value"),
    Input("filter_button", "n_clicks"),
)
def user_classification_first_column_visuals(year, region, country, n_clicks):
    _df = df.copy()
    if year != None:
        _df = _df.query("Year == @year")
    if region != None:
        _df = _df.query("Region == @region")
    if country != None:
        _df = _df.query("Country == @country")
    customers_ids = _df["CustomerNo"].unique()
    _df = customer_segments_df.query("CustomerNo in @customers_ids")
    visual1 = dataVisuals.plotly_box_plot(
        df=_df,
        x="Rank",
        y="totalQuantity",
        title="by Quantity",
        x_title="",
        y_title="Total Quantity",
    )

    visual2 = dataVisuals.plotly_box_plot(
        df=_df,
        x="Rank",
        y="totalPriceSold",
        title="by Revenue",
        x_title="",
        y_title="Total Revenue",
    )
    return visual1, visual2


@app.callback(
    Output("userClassificationTabVisual3", "figure"),
    Output("userClassificationTabVisual4", "figure"),
    State("filter_year_dropdown", "value"),
    State("filter_region_dropdown", "value"),
    State("filter_country_dropdown", "value"),
    Input("filter_button", "n_clicks"),
)
def user_classification_secound_column_visuals(year, region, country, n_clicks):
    _df = df.copy()
    if year != None:
        _df = _df.query("Year == @year")
    if region != None:
        _df = _df.query("Region == @region")
    if country != None:
        _df = _df.query("Country == @country")
    customers_ids = _df["CustomerNo"].unique()
    _df = customer_segments_df.query("CustomerNo in @customers_ids")
    visual1 = dataVisuals.plotly_bar_chart(
        df=_df.groupby("Rank", as_index=False)["totalQuantity"]
        .sum()
        .sort_values(by=["totalQuantity"], ascending=False),
        x="Rank",
        y="totalQuantity",
        title="by Quantity",
        x_title="",
        y_title="",
    )

    visual2 = dataVisuals.plotly_pie_chart(
        df=_df.groupby("Rank", as_index=False)["totalPriceSold"]
        .sum()
        .sort_values(by=["totalPriceSold"], ascending=False),
        names="Rank",
        values="totalPriceSold",
        title="by Revenue",
        legend_title="Ranks",
    )
    return visual1, visual2


#
##
####
#####
if __name__ == "__main__":
    app.run_server(port=2055, debug=True)
