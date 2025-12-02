import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import os

# =============================
# CONFIGURAÇÃO INICIAL
# =============================
app = dash.Dash(__name__)
server = app.server

# =============================
# DADOS SIMULADOS
# =============================
def gerar_dados():
    """Gera dados simulados para o dashboard"""
    
    datas = pd.date_range(start='2024-01-01', end='2024-04-30', freq='D')
    regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D']
    
    np.random.seed(42)
    
    dados = {
        'Data': np.random.choice(datas, 500),
        'Região': np.random.choice(regioes, 500),
        'Produto': np.random.choice(produtos, 500),
        'Quantidade': np.random.randint(50, 300, 500),
        'Valor': np.random.uniform(1000, 10000, 500),
        'Status': np.random.choice(['Completo', 'Pendente'], 500, p=[0.9, 0.1])
    }
    
    df = pd.DataFrame(dados)
    df['Mês'] = df['Data'].dt.strftime('%B')
    df['Data_Formatada'] = df['Data'].dt.strftime('%d/%m/%Y')
    
    return df

df = gerar_dados()

# =============================
# CORES DO DESIGN SYSTEM
# =============================
COR_PRIMARIA = '#0078D4'
COR_SECUNDARIA = '#107c10'
COR_ALERTA = '#ffb900'
COR_PERIGO = '#d83b01'
COR_BG = '#f3f3f3'
COR_CARD = 'white'

# =============================
# COMPONENTES DOS GRÁFICOS
# =============================
def criar_grafico_evolucao(df_filtrado):
    """Gráfico de evolução de vendas"""
    df_dia = df_filtrado.groupby('Data_Formatada')['Valor'].sum().reset_index()
    df_dia = df_dia.sort_values('Data_Formatada')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_dia['Data_Formatada'],
        y=df_dia['Valor'],
        mode='lines+markers',
        line=dict(width=4, color=COR_PRIMARIA),
        marker=dict(size=8, color=COR_PRIMARIA, line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(0, 120, 212, 0.1)',
        name='Vendas',
        hovertemplate='<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='📈 Evolução de Vendas',
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        margin=dict(l=60, r=30, t=30, b=50),
        font=dict(family='Segoe UI, sans-serif', size=12),
        xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        hoverlabel=dict(bgcolor='white', font=dict(size=13), bordercolor=COR_PRIMARIA),
        showlegend=False,
        height=350
    )
    
    return fig

def criar_grafico_regioes(df_filtrado):
    """Gráfico de vendas por região"""
    df_regiao = df_filtrado.groupby('Região')['Valor'].sum().reset_index().sort_values('Valor', ascending=False)
    
    cores = [COR_PRIMARIA, '#1084D7', '#1890DB', '#209CDF', '#28A8E3']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_regiao['Região'],
        y=df_regiao['Valor'],
        marker=dict(color=cores[:len(df_regiao)]),
        hovertemplate='<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='📊 Vendas por Região',
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        margin=dict(l=60, r=30, t=30, b=50),
        font=dict(family='Segoe UI, sans-serif', size=12),
        xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        hoverlabel=dict(bgcolor='white', font=dict(size=13), bordercolor=COR_PRIMARIA),
        showlegend=False,
        height=350
    )
    
    return fig

def criar_grafico_produtos(df_filtrado):
    """Gráfico de distribuição por produto"""
    df_produto = df_filtrado.groupby('Produto')['Valor'].sum().reset_index()
    
    cores = [COR_PRIMARIA, '#1084D7', '#1890DB', '#209CDF']
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df_produto['Produto'],
        values=df_produto['Valor'],
        marker=dict(colors=cores),
        hovertemplate='<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='🍰 Distribuição por Produto',
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        margin=dict(l=30, r=30, t=30, b=30),
        font=dict(family='Segoe UI, sans-serif', size=12),
        height=350
    )
    
    return fig

def criar_grafico_performance(df_filtrado):
    """Gráfico de performance por região"""
    df_perf = df_filtrado.groupby('Região').agg({
        'Quantidade': 'sum'
    }).reset_index().sort_values('Quantidade', ascending=True)
    
    df_perf['Performance'] = (df_perf['Quantidade'] / df_perf['Quantidade'].max() * 100).round(0)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_perf['Região'],
        x=df_perf['Performance'],
        orientation='h',
        marker=dict(color=COR_SECUNDARIA),
        hovertemplate='<b>%{y}</b><br>%{x}% de performance<extra></extra>'
    ))
    
    fig.update_layout(
        title='📍 Performance por Região',
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        margin=dict(l=150, r=30, t=30, b=50),
        font=dict(family='Segoe UI, sans-serif', size=12),
        xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        hoverlabel=dict(bgcolor='white', font=dict(size=13), bordercolor=COR_PRIMARIA),
        showlegend=False,
        height=350
    )
    
    return fig

def criar_grafico_mensal(df_filtrado):
    """Gráfico comparativo mensal"""
    df_mensal = df_filtrado.groupby('Mês')['Valor'].sum().reset_index()
    
    meses_ordem = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_mensal['Mês'] = pd.Categorical(df_mensal['Mês'], categories=meses_ordem, ordered=True)
    df_mensal = df_mensal.sort_values('Mês')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_mensal['Mês'],
        y=df_mensal['Valor'],
        marker=dict(color=COR_PRIMARIA),
        hovertemplate='<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='📅 Comparativo Mensal',
        paper_bgcolor=COR_CARD,
        plot_bgcolor=COR_CARD,
        margin=dict(l=60, r=30, t=30, b=50),
        font=dict(family='Segoe UI, sans-serif', size=12),
        xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        hoverlabel=dict(bgcolor='white', font=dict(size=13), bordercolor=COR_PRIMARIA),
        showlegend=False,
        height=350
    )
    
    return fig

# =============================
# LAYOUT DO APP
# =============================
app.layout = html.Div([
    # HEADER
    html.Div([
        html.H1('📊 Dashboard de Vendas Premium', style={
            'margin': '0',
            'fontSize': '28px',
            'fontWeight': '600',
            'color': 'white'
        }),
        html.P('Análise em tempo real de vendas e performance', style={
            'fontSize': '14px',
            'opacity': '0.9',
            'marginTop': '5px'
        })
    ], style={
        'background': f'linear-gradient(135deg, {COR_PRIMARIA} 0%, #106EBE 100%)',
        'padding': '30px 40px',
        'color': 'white',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)'
    }),
    
    # CONTAINER PRINCIPAL
    html.Div([
        # FILTROS
        html.Div([
            html.Div([
                html.Label('Mês:', style={'fontWeight': '600', 'fontSize': '13px', 'marginRight': '10px', 'color': '#333'}),
                dcc.Dropdown(
                    id='mes-select',
                    options=[{'label': 'Todos', 'value': ''}] + 
                            [{'label': m, 'value': m} for m in sorted(df['Mês'].unique())],
                    value='',
                    style={'minWidth': '150px', 'width': '100%'}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'flex': '1', 'minWidth': '200px'}),
            
            html.Div([
                html.Label('Região:', style={'fontWeight': '600', 'fontSize': '13px', 'marginRight': '10px', 'color': '#333'}),
                dcc.Dropdown(
                    id='regiao-select',
                    options=[{'label': 'Todas', 'value': ''}] + 
                            [{'label': r, 'value': r} for r in sorted(df['Região'].unique())],
                    value='',
                    style={'minWidth': '150px', 'width': '100%'}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'flex': '1', 'minWidth': '200px'}),
            
            html.Div([
                html.Label('Produto:', style={'fontWeight': '600', 'fontSize': '13px', 'marginRight': '10px', 'color': '#333'}),
                dcc.Dropdown(
                    id='produto-select',
                    options=[{'label': 'Todos', 'value': ''}] + 
                            [{'label': p, 'value': p} for p in sorted(df['Produto'].unique())],
                    value='',
                    style={'minWidth': '150px', 'width': '100%'}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'flex': '1', 'minWidth': '200px'})
        ], style={
            'background': COR_CARD,
            'padding': '20px',
            'borderRadius': '8px',
            'marginBottom': '30px',
            'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.08)',
            'display': 'flex',
            'gap': '15px',
            'flexWrap': 'wrap',
            'alignItems': 'center'
        }),
        
        # KPIs
        html.Div([
            # KPI 1
            html.Div([
                html.Div('Vendas Totais', style={'fontSize': '13px', 'color': '#666', 'fontWeight': '600', 'textTransform': 'uppercase', 'marginBottom': '10px'}),
                html.Div(id='kpi-vendas', children='R$ 0,00', style={'fontSize': '32px', 'fontWeight': '700', 'color': COR_PRIMARIA, 'marginBottom': '8px'}),
                html.Div('↑ 12.5% vs. período anterior', style={'fontSize': '12px', 'color': '#999'})
            ], style={
                'background': COR_CARD,
                'padding': '25px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)',
                'borderLeft': f'4px solid {COR_PRIMARIA}',
                'transition': 'transform 0.3s ease'
            }),
            
            # KPI 2
            html.Div([
                html.Div('Quantidade Vendida', style={'fontSize': '13px', 'color': '#666', 'fontWeight': '600', 'textTransform': 'uppercase', 'marginBottom': '10px'}),
                html.Div(id='kpi-quantidade', children='0', style={'fontSize': '32px', 'fontWeight': '700', 'color': COR_SECUNDARIA, 'marginBottom': '8px'}),
                html.Div('↑ 8.3% vs. período anterior', style={'fontSize': '12px', 'color': '#999'})
            ], style={
                'background': COR_CARD,
                'padding': '25px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)',
                'borderLeft': f'4px solid {COR_SECUNDARIA}'
            }),
            
            # KPI 3
            html.Div([
                html.Div('Ticket Médio', style={'fontSize': '13px', 'color': '#666', 'fontWeight': '600', 'textTransform': 'uppercase', 'marginBottom': '10px'}),
                html.Div(id='kpi-ticket', children='R$ 0,00', style={'fontSize': '32px', 'fontWeight': '700', 'color': COR_ALERTA, 'marginBottom': '8px'}),
                html.Div('↑ 4.2% vs. período anterior', style={'fontSize': '12px', 'color': '#999'})
            ], style={
                'background': COR_CARD,
                'padding': '25px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)',
                'borderLeft': f'4px solid {COR_ALERTA}'
            }),
            
            # KPI 4
            html.Div([
                html.Div('Taxa Conversão', style={'fontSize': '13px', 'color': '#666', 'fontWeight': '600', 'textTransform': 'uppercase', 'marginBottom': '10px'}),
                html.Div(id='kpi-conversao', children='0%', style={'fontSize': '32px', 'fontWeight': '700', 'color': COR_PERIGO, 'marginBottom': '8px'}),
                html.Div('↓ -2.1% vs. período anterior', style={'fontSize': '12px', 'color': '#d83b01', 'fontWeight': '600'})
            ], style={
                'background': COR_CARD,
                'padding': '25px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)',
                'borderLeft': f'4px solid {COR_PERIGO}'
            })
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        }),
        
        # GRÁFICOS LINHA 1
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-evolucao')
            ], style={
                'background': COR_CARD,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)'
            }),
            
            html.Div([
                dcc.Graph(id='grafico-regioes')
            ], style={
                'background': COR_CARD,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)'
            })
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        }),
        
        # GRÁFICOS LINHA 2
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-produtos')
            ], style={
                'background': COR_CARD,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)'
            }),
            
            html.Div([
                dcc.Graph(id='grafico-performance')
            ], style={
                'background': COR_CARD,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)'
            })
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(500px, 1fr))',
            'gap': '20px',
            'marginBottom': '30px'
        }),
        
        # GRÁFICO COMPLETO
        html.Div([
            dcc.Graph(id='grafico-mensal')
        ], style={
            'background': COR_CARD,
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)',
            'marginBottom': '30px'
        }),
        
        # TABELA
        html.Div([
            html.H3('📋 Detalhes de Vendas', style={'marginBottom': '15px', 'paddingBottom': '10px', 'borderBottom': '1px solid #f0f0f0', 'color': '#333', 'marginTop': '0'}),
            html.Div(id='tabela-container', style={'overflowX': 'auto'})
        ], style={
            'background': COR_CARD,
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 1px 4px rgba(0, 0, 0, 0.08)'
        })
        
    ], style={
        'maxWidth': '1600px',
        'margin': '0 auto',
        'padding': '40px 20px'
    }),
    
    # FOOTER
    html.Div('© 2024 Dashboard Premium | Dados atualizados em tempo real', style={
        'textAlign': 'center',
        'padding': '20px',
        'color': '#999',
        'fontSize': '12px',
        'background': COR_BG
    })
    
], style={
    'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    'backgroundColor': COR_BG,
    'color': '#222',
    'margin': '0',
    'padding': '0'
})

# =============================
# CALLBACKS (INTERATIVIDADE)
# =============================
@callback(
    [Output('kpi-vendas', 'children'),
     Output('kpi-quantidade', 'children'),
     Output('kpi-ticket', 'children'),
     Output('kpi-conversao', 'children'),
     Output('grafico-evolucao', 'figure'),
     Output('grafico-regioes', 'figure'),
     Output('grafico-produtos', 'figure'),
     Output('grafico-performance', 'figure'),
     Output('grafico-mensal', 'figure'),
     Output('tabela-container', 'children')],
    [Input('mes-select', 'value'),
     Input('regiao-select', 'value'),
     Input('produto-select', 'value')]
)
def atualizar_dashboard(mes, regiao, produto):
    """Atualiza todo o dashboard baseado nos filtros"""
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if mes:
        df_filtrado = df_filtrado[df_filtrado['Mês'] == mes]
    if regiao:
        df_filtrado = df_filtrado[df_filtrado['Região'] == regiao]
    if produto:
        df_filtrado = df_filtrado[df_filtrado['Produto'] == produto]
    
    # Calcular KPIs
    total_vendas = df_filtrado['Valor'].sum()
    total_quantidade = df_filtrado['Quantidade'].sum()
    ticket_medio = total_vendas / total_quantidade if total_quantidade > 0 else 0
    
    taxa_conversao = (len(df_filtrado[df_filtrado['Status'] == 'Completo']) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
    
    # Formatar KPIs
    kpi_vendas = f'R$ {total_vendas:,.2f}'.replace(',', '.')
    kpi_quantidade = f'{total_quantidade:,.0f}'.replace(',', '.')
    kpi_ticket = f'R$ {ticket_medio:,.2f}'.replace(',', '.')
    kpi_conversao = f'{taxa_conversao:.1f}%'
    
    # Gerar gráficos
    fig_evolucao = criar_grafico_evolucao(df_filtrado) if len(df_filtrado) > 0 else go.Figure()
    fig_regioes = criar_grafico_regioes(df_filtrado) if len(df_filtrado) > 0 else go.Figure()
    fig_produtos = criar_grafico_produtos(df_filtrado) if len(df_filtrado) > 0 else go.Figure()
    fig_performance = criar_grafico_performance(df_filtrado) if len(df_filtrado) > 0 else go.Figure()
    fig_mensal = criar_grafico_mensal(df_filtrado) if len(df_filtrado) > 0 else go.Figure()
    
    # Gerar tabela
    df_tabela = df_filtrado.nlargest(10, 'Valor')[['Data_Formatada', 'Região', 'Produto', 'Quantidade', 'Valor', 'Status']]
    
    linhas_tabela = [
        html.Table([
            html.Thead(
                html.Tr([
                    html.Th('Data', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'}),
                    html.Th('Região', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'}),
                    html.Th('Produto', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'}),
                    html.Th('Quantidade', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'}),
                    html.Th('Valor (R$)', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'}),
                    html.Th('Status', style={'padding': '12px', 'textAlign': 'left', 'fontWeight': '600', 'borderBottom': f'2px solid {COR_PRIMARIA}', 'backgroundColor': '#f5f5f5'})
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(row['Data_Formatada'], style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                    html.Td(row['Região'], style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                    html.Td(row['Produto'], style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                    html.Td(f"{row['Quantidade']}", style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                    html.Td(f"R$ {row['Valor']:,.2f}".replace(',', '.'), style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'}),
                    html.Td(f"✓ {row['Status']}", style={'padding': '12px', 'borderBottom': '1px solid #f0f0f0'})
                ]) for _, row in df_tabela.iterrows()
            ])
        ], style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '13px'})
    ] if len(df_tabela) > 0 else [html.P('Nenhum dado encontrado', style={'textAlign': 'center', 'color': '#999', 'padding': '20px'})]
    
    return kpi_vendas, kpi_quantidade, kpi_ticket, kpi_conversao, fig_evolucao, fig_regioes, fig_produtos, fig_performance, fig_mensal, linhas_tabela

# =============================
# EXECUTAR APP
# =============================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=True, host='0.0.0.0', port=port)
