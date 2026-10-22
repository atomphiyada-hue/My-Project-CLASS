import os
import gspread
from dash import Dash, html
import dash_ag_grid as dag
from dotenv import load_dotenv
from dash import Dash, html, dcc, Input, Output, State, no_update

load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")
gc = gspread.service_account(filename="credentials.json")
ws = gc.open_by_key(SHEET_ID).sheet1

COLS = [{"field": "Student ID"}, {"field": "Student Name"}, {"field": "Student Year"}]


def serve_layout():
    rows = ws.get_all_records()
    return [
        html.H3("Student List"),
        dag.AgGrid(id="table", rowData=rows, columnDefs=COLS),
        dcc.Input(id="in-id", placeholder="student_id"),
        dcc.Input(id="in-name", placeholder="name"),
        dcc.Input(id="in-nick", placeholder="nickname"),
        html.Button("Add student", id="btn-add"),
        html.Div(id="msg"),
    ]


app = Dash()
app.layout = serve_layout

@app.callback(
    Output("table", "rowData"),
    Output("msg", "children"),
    Input("btn-add", "n_clicks"),
    State("in-id", "value"),
    State("in-name", "value"),
    State("in-nick", "value"),
    prevent_initial_call=True,
)
def add_student(n_clicks, sid, name, nick):
    if not (sid and name and nick):
        return no_update, "Please fill all fields"
    ws.append_row([sid, name, nick])
    return ws.get_all_records(), "Added!"

if __name__ == "__main__":
    app.run(debug=True)