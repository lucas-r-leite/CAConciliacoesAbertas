from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import conciliacaoMesOpen as cc

app = Dash(__name__)
df = cc.main()
# df = pd.read_excel("Conciliacao_Abertas_Mes.xlsx")

# Get unique values from the "start_date" column
unique_dates = df["start_date"].unique()

# Create options for the dropdown based on unique dates
date_options = [{"label": date, "value": date} for date in unique_dates]

app.layout = html.Div(
    style={"backgroundColor": "#f0f0f0"},
    children=[
        html.Div(
            [
                # html.Img(src="your_image_url.jpg", style={'width': '100px', 'height': '100px'}),
                html.H3("Asset Gestão Financeira", style={"text-align": "center"}),
            ]
        ),
        html.H4("Conciliações Abertas"),
        html.P("Select date:"),
        dcc.Dropdown(
            id="dropdown",
            options=date_options,
            value=unique_dates[0],
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ],
)


@app.callback(Output("graph", "figure"), Input("dropdown", "value"))
def display_date(selected_date):
    filtered_df = df[df["start_date"] == selected_date]
    fig = px.bar(
        filtered_df,
        x="NomeCliente",
        y="total",
        color="Nome do Banco",  # Stack by "Nome do Banco" (Bank Name)
        barmode="stack",  # Set barmode to "stack" for a stacked bar chart
        labels={"total": "Conciliações Abertas", "NomeCliente": "Clientes"},
    )
    return fig


if __name__ == "__main__":
    app.run_server()
