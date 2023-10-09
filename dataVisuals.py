import pandas as pd
import numpy as np
import plotly.express as px


def plotly_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_title: str,
    y_title: str,
    legend_title: str,
    color=None | str,
):
    lineChart = px.line(df, x=x, y=y, color=color, markers=True)
    lineChart.update_layout(
        title_text=f"<b>{title}</b>",
        xaxis_title_text=f"<b>{x_title}</b>",
        yaxis_title_text=f"<b>{y_title}</b>",
        legend_title=f"{legend_title}",
        xaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        font=dict(size=18, color="#65C4E0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    lineChart.update_xaxes(tickangle=45)
    return lineChart


def plotly_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_title: str,
    y_title: str,
):
    """
    Produce a barChart by plotly
    df is filtrable from the input it self.
    """
    barChart = px.histogram(df, x=x, y=y)
    barChart.update_layout(
        title_text=f"<b>{title}</b>",
        xaxis_title_text=f"<b>{x_title}</b>",
        yaxis_title_text=f"<b>{y_title}</b>",
        legend_title="",
        xaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        font=dict(size=18, color="#65C4E0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    barChart.update_xaxes(tickangle=45)
    return barChart


def plotly_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    legend_title: str,
):
    pieChart = px.pie(
        df,
        names=names,
        values=values,
    )
    pieChart.update_layout(
        legend_title=f"<b>{legend_title}</b>",
        title_text=f"<b>{title}</b>",
        title_font=dict(size=30, color="#65C4E0"),
        font=dict(size=18, color="#65C4E0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    pieChart.update_traces(
        textposition="auto",
        textinfo="percent+label",
        textfont_size=14,
        texttemplate="<b>%{label}<br>%{percent}</b>",
    )
    return pieChart


def plotly_box_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_title: str,
    y_title: str,
):
    boxplot = px.box(
        data_frame=df,
        x=x,
        y=y,
        title=title,
        boxmode="group",
    )
    boxplot.update_layout(
        title_text=f"<b>{title}</b>",
        xaxis_title_text=f"<b>{x_title}</b>",
        yaxis_title_text=f"<b>{y_title}</b>",
        legend_title="",
        xaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        yaxis=dict(
            tickfont=dict(
                family="Arial",
                size=15,
                color="white",
            ),
        ),
        font=dict(size=18, color="#65C4E0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return boxplot


####
def table_without_filters(df, dbc):
    return dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        color="cyborg",
        class_name="dbc",
    )
