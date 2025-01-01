import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Connexion à la base de données
engine = create_engine('mysql+pymysql://root:@localhost/e_commerce')

# Requêtes SQL
main_query = """
SELECT 
    c.id AS client_id, c.nom AS nom, c.prenoms AS prenoms, c.sexe AS sexe,
    dc.id AS detailcommande_id, dc.date_commande, dc.Ville_de_residence AS ville_residence,
    co.produit_id, p.nom AS produit_nom, p.categorie, p.stock,
    pa.mode_paiement_id, mp.type_paiement,
    co.nombre_article, p.prix,
    v.lat, v.lng
FROM 
    Client c
JOIN 
    Commande co ON c.id = co.client_id
JOIN 
    DetailCommande dc ON co.commande_id = dc.id
JOIN 
    Produit p ON co.produit_id = p.id
JOIN 
    Paiement pa ON dc.id = pa.commande_id
JOIN 
    ModePaiement mp ON pa.mode_paiement_id = mp.id
LEFT JOIN
    Ville v ON dc.Ville_de_residence = v.city
"""

stock_query = """
SELECT nom, stock, categorie
FROM Produit
ORDER BY stock DESC
LIMIT 5
"""

low_stock_query = """
SELECT nom, stock, categorie
FROM Produit
WHERE stock > 0
ORDER BY stock ASC
LIMIT 5
"""

# Chargement des données
df = pd.read_sql(main_query, engine)
top_stock_df = pd.read_sql(stock_query, engine)
low_stock_df = pd.read_sql(low_stock_query, engine)

# Préparation des données
df['date_commande'] = pd.to_datetime(df['date_commande'])
df['montant'] = df['nombre_article'] * df['prix']

# Initialisation de l'application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Styles personnalisés
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#2ecc71',
    'warning': '#f1c40f',
    'danger': '#e74c3c',
    'light': '#ecf0f1',
    'dark': '#2c3e50'
}

# Layout principal
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Tableau de Bord', value='tab-1'),
        dcc.Tab(label='Données Détaillées', value='tab-2'),
    ]),
    
    # Contenu principal
    html.Div([
        # Sidebar pour les filtres
        html.Div([
            html.H3("Filtres", style={'color': COLORS['light'], 'marginBottom': '20px'}),
            
            # Filtre de date
            html.Div([
                html.Label('Période', style={'color': COLORS['light']}),
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=df['date_commande'].min(),
                    max_date_allowed=df['date_commande'].max(),
                    start_date=df['date_commande'].min(),
                    end_date=df['date_commande'].max(),
                    style={'backgroundColor': COLORS['light']}
                ),
            ], style={'marginBottom': '20px'}),
            
            # Filtre de catégorie
            html.Div([
                html.Label('Catégorie', style={'color': COLORS['light']}),
                dcc.Dropdown(
                    id='categorie-filter',
                    options=[{'label': cat, 'value': cat} for cat in df['categorie'].unique()],
                    multi=True,
                    placeholder="Sélectionner les catégories",
                    style={'backgroundColor': COLORS['light']}
                ),
            ], style={'marginBottom': '20px'}),
            
            # Filtre de ville
            html.Div([
                html.Label('Ville', style={'color': COLORS['light']}),
                dcc.Dropdown(
                    id='ville-filter',
                    options=[{'label': ville, 'value': ville} 
                            for ville in df['ville_residence'].unique()],
                    multi=True,
                    placeholder="Sélectionner les villes",
                    style={'backgroundColor': COLORS['light']}
                ),
            ], style={'marginBottom': '20px'}),
            
            # Filtre de paiement
            html.Div([
                html.Label('Mode de paiement', style={'color': COLORS['light']}),
                dcc.Dropdown(
                    id='paiement-filter',
                    options=[{'label': mode, 'value': mode} 
                            for mode in df['type_paiement'].unique()],
                    multi=True,
                    placeholder="Sélectionner les modes de paiement",
                    style={'backgroundColor': COLORS['light']}
                ),
            ], style={'marginBottom': '20px'}),
            
        ], style={
            'width': '200px',
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'bottom': '0',
            'backgroundColor': COLORS['secondary'],
            'padding': '20px',
            'boxShadow': '2px 0 5px rgba(0,0,0,0.1)'
        }),
        
        # Contenu principal
        html.Div(id='main-content', style={
            'marginLeft': '250px',
            'padding': '20px'
        })
    ]),
])

# Callbacks
@app.callback(
    Output('main-content', 'children'),
    [Input('tabs', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('categorie-filter', 'value'),
     Input('ville-filter', 'value'),
     Input('paiement-filter', 'value')]
)
def update_content(tab, start_date, end_date, categories, villes, paiements):
    filtered_df = df.copy()
    
    # Application des filtres
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date_commande'] >= start_date) &
            (filtered_df['date_commande'] <= end_date)
        ]
    if categories:
        filtered_df = filtered_df[filtered_df['categorie'].isin(categories)]
    if villes:
        filtered_df = filtered_df[filtered_df['ville_residence'].isin(villes)]
    if paiements:
        filtered_df = filtered_df[filtered_df['type_paiement'].isin(paiements)]
    
    if tab == 'tab-1':
        return create_dashboard_layout(filtered_df)
    else:
        return create_data_view_layout(filtered_df)

def create_dashboard_layout(filtered_df):
    # Calcul des KPIs
    total_ventes = filtered_df['montant'].sum()
    nb_commandes = filtered_df['detailcommande_id'].nunique()
    panier_moyen = total_ventes / nb_commandes if nb_commandes > 0 else 0
    nb_clients = filtered_df['client_id'].nunique()
    
    return html.Div([
        # KPIs
        html.Div([
            create_kpi_card("Ventes Totales", f"{total_ventes:,.0f} FCFA", COLORS['accent']),
            create_kpi_card("Commandes", f"{nb_commandes:,}", COLORS['success']),
            create_kpi_card("Panier Moyen", f"{panier_moyen:,.0f} FCFA", COLORS['warning']),
            create_kpi_card("Clients Uniques", f"{nb_clients:,}", COLORS['danger'])
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
        
        # Première ligne de graphiques
        html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_map_figure(filtered_df),
                    style={'height': '400px'}
                )
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(
                    figure=create_sales_evolution(filtered_df),
                    style={'height': '400px'}
                )
            ], style={'width': '50%', 'display': 'inline-block'})
        ]),
        
        # Deuxième ligne de graphiques
        html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_category_pie(filtered_df),
                    style={'height': '400px'}
                )
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(
                    figure=create_payment_distribution(filtered_df),
                    style={'height': '400px'}
                )
            ], style={'width': '50%', 'display': 'inline-block'})
        ]),
        
        # Stock Dashboard
        html.Div([
            html.Div([
                html.H3("Top 5 Stocks les plus élevés"),
                create_stock_table(top_stock_df)
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            html.Div([
                html.H3("Top 5 Stocks les plus faibles"),
                create_stock_table(low_stock_df)
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])

def create_data_view_layout(filtered_df):
    return html.Div([
        html.H1("Données Détaillées", 
                style={'textAlign': 'center', 'color': COLORS['primary']}),
        
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': 'Date', 'id': 'date_commande'},
                {'name': 'Client', 'id': 'nom'},
                {'name': 'Produit', 'id': 'produit_nom'},
                {'name': 'Catégorie', 'id': 'categorie'},
                {'name': 'Ville', 'id': 'ville_residence'},
                {'name': 'Quantité', 'id': 'nombre_article'},
                {'name': 'Montant', 'id': 'montant'},
            ],
            data=filtered_df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
            },
            style_header={
                'backgroundColor': COLORS['light'],
                'fontWeight': 'bold',
            },
            filter_action='native',
            sort_action='native',
            page_action='native',
        )
    ])

# Fonctions utilitaires pour les visualisations
def create_map_figure(df):
    return px.scatter_mapbox(
        df.drop_duplicates('ville_residence'),
        lat='lat',
        lon='lng',
        size='montant',
        color='montant',
        hover_name='ville_residence',
        zoom=6,
        title='Répartition géographique des ventes',
    ).update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":30,"l":0,"b":0}
    )

def create_sales_evolution(df):
    daily_sales = df.groupby('date_commande')['montant'].sum().reset_index()
    return px.line(
        daily_sales,
        x='date_commande',
        y='montant',
        title='Évolution des ventes'
    ).update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

def create_category_pie(df):
    category_sales = df.groupby('categorie')['montant'].sum()
    return px.pie(
        values=category_sales.values,
        names=category_sales.index,
        title='Répartition des ventes par catégorie'
    )

def create_payment_distribution(df):
    payment_data = df.groupby('type_paiement')['montant'].sum()
    return px.bar(
        x=payment_data.index,
        y=payment_data.values,
        title='Distribution des modes de paiement'
    )

def create_kpi_card(title, value, color):
    return html.Div([
        html.H4(title, style={'color': COLORS['dark'], 'marginBottom': '5px'}),
        html.H2(value, style={'color': color, 'margin': '0'})
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'width': '23%',
        'textAlign': 'center'
    })

def create_stock_table(df):
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'name': 'Produit', 'id': 'nom'},
            {'name': 'Stock', 'id': 'stock'},
            {'name': 'Catégorie', 'id': 'categorie'}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
        },
        style_header={
            'backgroundColor': COLORS['light'],
            'fontWeight': 'bold',
        }
    )

# Style CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard E-commerce</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                background-color: #f5f6fa;
                margin: 0;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)