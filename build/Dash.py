import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import base64
import io

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

# Requêtes SQL (garder les requêtes existantes et ajouter)
product_performance_query = """
SELECT 
    p.nom AS produit_nom,
    COUNT(co.produit_id) as nombre_commandes,
    SUM(co.nombre_article) as total_articles_vendus
FROM 
    Produit p
LEFT JOIN 
    Commande co ON p.id = co.produit_id
GROUP BY 
    p.id, p.nom
ORDER BY 
    nombre_commandes DESC
"""

# Chargement des données
df = pd.read_sql(main_query, engine)
top_stock_df = pd.read_sql(stock_query, engine)
low_stock_df = pd.read_sql(low_stock_query, engine)
product_performance_df = pd.read_sql(product_performance_query, engine)
product_performance_df['produit_nom'] = product_performance_df['produit_nom'].str.slice(0, 30) #Couper les noms des produits

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
        dcc.Tab(label='Prédictions des Ventes', value='tab-3'),
        dcc.Tab(label='Segmentation Clients', value='tab-4'),
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
        html.Div(id='main-content', style={'marginLeft': '250px', 'padding': '20px'})
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
    
    # Application des filtres existants
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
    elif tab == 'tab-2':
        return create_data_view_layout(filtered_df)
    elif tab == 'tab-3':
        return create_predictions_layout(filtered_df)
    else:
        return create_segmentation_layout(filtered_df)

def create_dashboard_layout_original(filtered_df):
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
    payment_data = df.groupby('type_paiement')['montant'].sum().reset_index()
    return px.bar(
        payment_data,
        x='type_paiement',
        y='montant',
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
        'width': '20%',
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

# Fonction pour créer le graphique des performances produits
def create_product_performance_charts():
    # Top 10 produits les plus commandés
    top_products = product_performance_df.nlargest(10, 'nombre_commandes')
    top_products_fig = px.bar(
        top_products,
        x='produit_nom',
        y='nombre_commandes',
        title='Top 10 des produits les plus commandés'
    ).update_layout(xaxis={'tickangle': 45})

    # Top 10 produits les moins commandés
    bottom_products = product_performance_df.nsmallest(10, 'nombre_commandes')
    bottom_products_fig = px.bar(
        bottom_products,
        x='produit_nom',
        y='nombre_commandes',
        title='Top 10 des produits les moins commandés'
    ).update_layout(xaxis={'tickangle': 45})

    return html.Div([
        html.Div([dcc.Graph(figure=top_products_fig)], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(figure=bottom_products_fig)], style={'width': '50%', 'display': 'inline-block'})
    ])

# Mise à jour du layout du tableau de bord
def create_dashboard_layout(filtered_df):
    # Garder le layout existant et ajouter les nouveaux graphiques
    existing_layout = create_dashboard_layout_original(filtered_df)
    product_performance = create_product_performance_charts()
    
    return html.Div([
        existing_layout,
        html.H3("Performance des Produits"),
        product_performance
    ])

# Fonction pour l'export des données
def create_download_buttons():
    return html.Div([
        html.Button("Exporter en CSV", id='btn-csv'),
        dcc.Download(id="download-dataframe-csv"),
    ], style={'margin': '10px 0'})

# Callbacks pour l'export
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-csv", "n_clicks"),
    prevent_initial_call=True,
)
def export_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "data.csv")


# Mise à jour du layout des données détaillées
def create_data_view_layout(filtered_df):
    return html.Div([
        html.H1("Données Détaillées", style={'textAlign': 'center', 'color': COLORS['primary']}),
        create_download_buttons(),
        dash_table.DataTable(
            id='data-table',
            columns=[{'name': i, 'id': i} for i in filtered_df.columns],
            data=filtered_df.to_dict('records'),
            page_size=10,
            filter_action='native',
            sort_action='native',
            style_table={'overflowX': 'auto'},
            export_format='csv'
        )
    ])

# Layout pour les prédictions
def create_predictions_layout(df):
    return html.Div([
        html.H1("Prédictions des Ventes", style={'textAlign': 'center'}),
        html.Div([
            html.H3("Sélectionner la période de prédiction"),
            dcc.Dropdown(
                id='prediction-horizon',
                options=[
                    {'label': '7 jours', 'value': 7},
                    {'label': '30 jours', 'value': 30},
                    {'label': '90 jours', 'value': 90},
                ],
                value=30
            ),
            html.Button('Générer Prédictions', id='generate-predictions', n_clicks=0),
            dcc.Graph(id='prediction-graph')
        ])
    ])

# Layout pour la segmentation
def create_segmentation_layout(df):
    return html.Div([
        html.H1("Segmentation des Clients", style={'textAlign': 'center'}),
        html.Div([
            html.H3("Paramètres de Segmentation"),
            dcc.Dropdown(
                id='n-clusters',
                options=[{'label': f'{i} segments', 'value': i} for i in range(2, 11)],
                value=4
            ),
            html.Button('Générer Segmentation', id='generate-segments', n_clicks=0),
            dcc.Graph(id='segmentation-graph'),
            html.Div(id='segment-descriptions')
        ])
    ])


# Fonction améliorée pour les prédictions
def prepare_features_for_prediction(df):
    """Prépare les features avancées pour la prédiction"""
    daily_sales = df.groupby('date_commande')['montant'].sum().reset_index()
    daily_sales = daily_sales.set_index('date_commande').asfreq('D').reset_index()
    daily_sales['montant'] = daily_sales['montant'].fillna(0)
    
    # Features temporelles avancées
    daily_sales['day_of_week'] = daily_sales['date_commande'].dt.dayofweek
    daily_sales['month'] = daily_sales['date_commande'].dt.month
    daily_sales['day_of_month'] = daily_sales['date_commande'].dt.day
    daily_sales['is_weekend'] = daily_sales['day_of_week'].isin([5, 6]).astype(int)
    
    # Moyennes mobiles
    daily_sales['rolling_mean_7d'] = daily_sales['montant'].rolling(window=7, min_periods=1).mean()
    daily_sales['rolling_mean_30d'] = daily_sales['montant'].rolling(window=30, min_periods=1).mean()
    
    # Lag features
    for lag in [1, 7, 14, 30]:
        daily_sales[f'lag_{lag}d'] = daily_sales['montant'].shift(lag).fillna(0)
    
    return daily_sales

def train_prediction_model(daily_sales):
    """Entraîne un modèle de prédiction plus sophistiqué"""
    from xgboost import XGBRegressor
    
    feature_columns = [
        'day_of_week', 'month', 'day_of_month', 'is_weekend',
        'rolling_mean_7d', 'rolling_mean_30d',
        'lag_1d', 'lag_7d', 'lag_14d', 'lag_30d'
    ]
    
    # Préparation des données
    X = daily_sales[feature_columns].iloc[30:]  # Commence après 30 jours pour avoir toutes les features
    y = daily_sales['montant'].iloc[30:]
    
    # Division train/test
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Entraînement du modèle
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    return model, feature_columns

@app.callback(
    Output('prediction-graph', 'figure'),
    [Input('generate-predictions', 'n_clicks'),
     Input('prediction-horizon', 'value')],
    [State('date-range', 'start_date'),
     State('date-range', 'end_date')]
)

def update_predictions(n_clicks, horizon, start_date, end_date):
    if n_clicks == 0:
        return {}
        
    # Préparation des données
    daily_sales = prepare_features_for_prediction(df)
    model, feature_columns = train_prediction_model(daily_sales)
    
    # Génération des prédictions futures
    last_date = daily_sales['date_commande'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=horizon)
    future_data = pd.DataFrame({'date_commande': future_dates})
    
    # Création des features pour les données futures
    future_data['day_of_week'] = future_data['date_commande'].dt.dayofweek
    future_data['month'] = future_data['date_commande'].dt.month
    future_data['day_of_month'] = future_data['date_commande'].dt.day
    future_data['is_weekend'] = future_data['day_of_week'].isin([5, 6]).astype(int)
    
    # Simulation des moyennes mobiles et lags pour les prédictions futures
    last_values = daily_sales.tail(30)['montant'].values
    future_predictions = []
    
    for i in range(horizon):
        current_row = future_data.iloc[i:i+1].copy()
        
        # Calcul des moyennes mobiles
        current_row['rolling_mean_7d'] = np.mean(last_values[-7:])
        current_row['rolling_mean_30d'] = np.mean(last_values[-30:])
        
        # Calcul des lags
        current_row['lag_1d'] = last_values[-1]
        current_row['lag_7d'] = last_values[-7]
        current_row['lag_14d'] = last_values[-14]
        current_row['lag_30d'] = last_values[-30]
        
        # Prédiction
        pred = model.predict(current_row[feature_columns])[0]
        future_predictions.append(pred)
        
        # Mise à jour des dernières valeurs
        last_values = np.append(last_values[1:], pred)
    
    future_data['predicted_sales'] = future_predictions
    
    # Calcul de l'intervalle de confiance
    std_dev = np.std(daily_sales['montant'].tail(30))
    future_data['upper_bound'] = future_data['predicted_sales'] + 1.96 * std_dev
    future_data['lower_bound'] = future_data['predicted_sales'] - 1.96 * std_dev
    
    # Création du graphique
    fig = go.Figure()
    
    # Données historiques
    fig.add_trace(go.Scatter(
        x=daily_sales['date_commande'].tail(90),  # Affiche les 90 derniers jours
        y=daily_sales['montant'].tail(90),
        name='Ventes historiques',
        line=dict(color='blue')
    ))
    
    # Prédictions
    fig.add_trace(go.Scatter(
        x=future_data['date_commande'],
        y=future_data['predicted_sales'],
        name='Prédictions',
        line=dict(color='red', dash='dash')
    ))
    
    # Intervalle de confiance
    fig.add_trace(go.Scatter(
        x=future_data['date_commande'].tolist() + future_data['date_commande'].tolist()[::-1],
        y=future_data['upper_bound'].tolist() + future_data['lower_bound'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(231,234,241,0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Intervalle de confiance 95%'
    ))
    
    fig.update_layout(
        title='Prédiction des ventes avec intervalle de confiance',
        xaxis_title='Date',
        yaxis_title='Montant des ventes',
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

# Amélioration de la segmentation des clients
def prepare_customer_features(df):
    """Prépare des features plus avancées pour la segmentation"""
    # Calcul de la récence
    max_date = df['date_commande'].max()
    customer_last_purchase = df.groupby('client_id')['date_commande'].max()
    recency = (max_date - customer_last_purchase).dt.days
    
    # Agrégation des métriques par client
    customer_metrics = df.groupby('client_id').agg({
        'montant': ['sum', 'mean', 'std', 'count'],
        'nombre_article': ['sum', 'mean'],
        'detailcommande_id': 'nunique'
    })
    print(customer_metrics.columns)

    customer_metrics.columns = [
        'total_amount', 'avg_amount', 'std_amount', 'nb_transactions',
        'total_items', 'avg_items_per_order','commande_id'
    ]
    print(customer_metrics.columns)

    
    # Ajout de la récence
    customer_metrics['recency'] = recency
    
    # Calcul de métriques additionnelles
    customer_metrics['avg_amount_per_item'] = (
        customer_metrics['total_amount'] / customer_metrics['total_items']
    )
    
    # Fréquence des achats (en jours)
    customer_metrics['purchase_frequency'] = (
        customer_metrics['nb_transactions'] / 
        (customer_metrics['recency'] + 1)  # +1 pour éviter division par zéro
    )
    
    return customer_metrics

def perform_customer_segmentation(customer_metrics, n_clusters):
    """Réalise une segmentation plus sophistiquée des clients"""
    # Sélection des features pour la segmentation
    features_for_clustering = [
        'total_amount', 'avg_amount', 'nb_transactions',
        'recency', 'purchase_frequency', 'avg_items_per_order'
    ]
    
    # Standardisation
    scaler = StandardScaler()
    X = scaler.fit_transform(customer_metrics[features_for_clustering])
    
    # Application de K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    customer_metrics['Segment'] = kmeans.fit_predict(X)
    
    # Calcul des centres des clusters normalisés
    cluster_centers = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=features_for_clustering
    )
    
    return customer_metrics, cluster_centers

@app.callback(
    [Output('segmentation-graph', 'figure'),
     Output('segment-descriptions', 'children')],
    [Input('generate-segments', 'n_clicks'),
     Input('n-clusters', 'value')]
)
def update_segmentation(n_clicks, n_clusters):
    if n_clicks == 0:
        return {}, ""
    
    # Préparation des données
    customer_metrics = prepare_customer_features(df)
    segmented_customers, cluster_centers = perform_customer_segmentation(
        customer_metrics, n_clusters
    )
    
    # Création du graphique 2D
    fig = px.scatter(
        segmented_customers.reset_index(),
        x='total_amount',
        y='nb_transactions',
        color='Segment',
        title='Segmentation 2D des clients',
        labels={
            'total_amount': 'Montant total des achats',
            'nb_transactions': 'Nombre de transactions'
        }
    )
    
    # Caractérisation des segments
    segment_descriptions = []
    for segment in range(n_clusters):
        segment_data = segmented_customers[segmented_customers['Segment'] == segment]
        
        # Calcul des statistiques du segment
        stats = {
            'Taille du segment': len(segment_data),
            'Montant total moyen': segment_data['total_amount'].mean(),
            'Fréquence d\'achat': segment_data['purchase_frequency'].mean(),
            'Récence moyenne': segment_data['recency'].mean(),
            'Panier moyen': segment_data['avg_amount'].mean()
        }
        
        # Caractérisation du segment
        if stats['Montant total moyen'] > segmented_customers['total_amount'].quantile(0.75):
            segment_type = "Clients Premium"
        elif stats['Récence moyenne'] < segmented_customers['recency'].quantile(0.25):
            segment_type = "Clients Actifs"
        elif stats['Fréquence d\'achat'] > segmented_customers['purchase_frequency'].quantile(0.75):
            segment_type = "Clients Réguliers"
        elif stats['Récence moyenne'] > segmented_customers['recency'].quantile(0.75):
            segment_type = "Clients Inactifs"
        else:
            segment_type = "Clients Occasionnels"
        
        segment_descriptions.append(html.Div([ 
            html.H4(f'Segment {segment} - {segment_type}'),
            html.P(f"""
                Nombre de clients: {stats['Taille du segment']}
                Montant total moyen: {stats['Montant total moyen']:,.2f} FCFA
                Fréquence d'achat: {stats['Fréquence d\'achat']:.3f} commandes/jour
                Récence moyenne: {stats['Récence moyenne']:.1f} jours
                Panier moyen: {stats['Panier moyen']:,.2f} FCFA
            """)
        ]))
    
    return fig, html.Div(segment_descriptions)

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
