from textwrap import dedent
from dash import html, dcc
import dash_bootstrap_components as dbc


# Display utility functions
def _merge(a, b):
    return dict(a, **b)


def _omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


# Custom Display Components
def Card(children, **kwargs):
    return html.Section(className="card", children=children, **_omit(["style"], kwargs))


def FormattedSlider(**kwargs):
    return html.Div(
        style=kwargs.get("style", {}), children=dcc.Slider(**_omit(["style"], kwargs))
    )


def NamedSlider(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[
            html.P(f"{name}:"),
            html.Div(style={"margin-left": "6px"}, children=dcc.Slider(**kwargs)),
        ],
    )


def NamedDropdown(name, **kwargs):
    return html.Div(
        children=[
            html.Div(children=f"{name}:", style={
                "margin-bottom": "2px",
                "margin-left": "10px",
                }),
            dcc.Dropdown(**kwargs,className="text-center p-1"),
        ],
    )


def NamedRadioItems(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[html.P(children=f"{name}:"), dcc.RadioItems(**kwargs)],
    )


def NamedDisabledInputItem(name, **kwargs):
    return dbc.InputGroup(
        [
            dbc.InputGroupText(f"{name} :", className="bg-primary text-left text-white p-1"),
            dbc.Input(**kwargs, disabled=True, className="text-left p-1 bg-secondary"),
        ],
        className="mb-1",
        size="sm",
    )


# # Non-generic
# def DemoDescription(filename, strip=False):
#     with open(filename, "r") as file:
#         text = file.read()

#     if strip:
#         text = text.split("<Start Description>")[-1]
#         text = text.split("<End Description>")[0]

#     return html.Div(
#         className="row",
#         style={
#             "padding": "15px 30px 27px",
#             "margin": "45px auto 45px",
#             "width": "80%",
#             "max-width": "1024px",
#             "borderRadius": 5,
#             "border": "thin lightgrey solid",
#             "font-family": "Roboto, sans-serif",
#         },
#         children=dcc.Markdown(dedent(text)),
#     )
