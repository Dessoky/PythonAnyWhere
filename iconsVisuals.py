from dash import html


def icon_maker(bootstrap_icon, label):
    return html.Div(
        [html.I(className=f"{bootstrap_icon} pe-1"), label],
    )


list_numeric = "bi bi-list-ol"
ads = "bi bi-badge-ad"
table = "bi bi-table"
