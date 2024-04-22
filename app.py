
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Initialize the Dash app with external stylesheets for Google Fonts
app = Dash(__name__, external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap',
    'https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;700&display=swap'
])

# Load data (ensure you replace 'data.csv' with your actual data file)
df = pd.read_csv('data.csv', index_col='index')

# Sample graphs (adjust these to your actual data)
total_patients_graph = px.bar(x=["Total Patients"], y=[len(df)], title="Total Number of Patients")
illness_distribution_graph = px.pie(names=['Disease A', 'Disease B'], values=[10, 90], title="Distribution of Illnesses")

# Styles using the imported fonts
styles = {
    'container': {
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center',
        'alignItems': 'center',
        'backgroundColor': '#ECECEC'  # Light gray background
    },
    'box': {
        'width': '300px',
        'height': '200px',
        'margin': '10px',
        'padding': '10px',
        'border': '1px solid #474787',
        'borderRadius': '5px',
        'backgroundColor': '#AAABB8',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center',
        'textAlign': 'center',
        'fontFamily': 'Source Sans Pro, sans-serif'  # Paragraph font
    },
    'title': {
        'fontFamily': 'Playfair Display, serif',  # Title font
        'color': '#2C2C54',
        'textAlign': 'center',
        'marginBottom': '20px'
    },
    'text': {
        'fontFamily': 'Source Sans Pro, sans-serif',
        'textAlign': 'center',
        'color': '#474787'
    },
    'half': {
        'width': '50%',
        'display': 'inline-block'
    }
}

# Layout configuration using styles
app.layout = html.Div([
    html.H1('Health Dashboard', style=styles['title']),
    html.Div([
        html.Div([
            html.H2('General Statistics', style=styles['title']),
            dcc.Graph(figure=total_patients_graph),
            dcc.Graph(figure=illness_distribution_graph)
        ], style=styles['half']),
        
        html.Div([
            html.H2('Patient Details and Lab Results', style=styles['title']),
            dcc.Dropdown(
                id='patient-dropdown',
                options=[{'label': row['name'], 'value': idx} for idx, row in df.iterrows()],
                value=df.index[0]
            ),
            html.Div(id='patient-details', style=styles['container']),
            dcc.Graph(id='lab-results-graph')
        ], style=styles['half']),
    ], style={'display': 'flex', 'flexWrap': 'wrap'})
])

@app.callback(
    [Output('patient-details', 'children'),
     Output('lab-results-graph', 'figure')],
    [Input('patient-dropdown', 'value')]
)
def update_patient_details(selected_patient_index):
    patient = df.loc[selected_patient_index]
    details = [
        html.Div(style=styles['box'], children=[
            html.H3("Identification Information", style=styles['text']),
            html.P(f"Name: {patient['name'].replace(';', ', ')}"),
            html.P(f"Date of Birth: {patient['dob'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Medical Conditions", style=styles['text']),
            html.P(f"Conditions: {patient['conditions'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Medication List", style=styles['text']),
            html.P(f"💊 Medications: {patient['medications'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Treatment Records", style=styles['text']),
            html.P(f"🏋️ Treatments: {patient['treatments'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Progress Notes", style=styles['text']),
            html.P(f"🦵 Progress Notes: {patient['progress_notes'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Immunization Records", style=styles['text']),
            html.P(f"💉 Vaccines: {patient['vaccines'].replace(';', ', ')}")
        ]),
        html.Div(style=styles['box'], children=[
            html.H2("Consent and Authorization Forms", style=styles['text']),
            html.P(f"📝 Consents: {patient['consents'].replace(';', ', ')}")
        ])    ]
    # Assuming data for plotting exists, modify according to your dataset
    lab_results_graph = px.bar(x=["Sample Data"], y=[100], title="Sample Lab Result")
    lab_results_graph.update_layout(
        font=dict(family='Source Sans Pro, sans-serif'),
        title_font=dict(family='Playfair Display, serif', size=20)
    )
    return details, lab_results_graph

if __name__ == '__main__':
    app.run_server(debug=True)
