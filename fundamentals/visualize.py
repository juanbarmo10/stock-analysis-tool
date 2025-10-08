
#%%

import plotly.graph_objects as go
import os

def plot_financials(financials, ticker, save=False):
    if financials is None or financials.empty:
        print(f"⚠️ No financial data for {ticker}")
        return
    df = financials.T
    cols = [c for c in ["Total Revenue", "Net Income", "EBITDA"] if c in df.columns]
    if not cols:
        print(f"⚠️ No valid columns to plot for {ticker}")
        return

    fig = go.Figure()
    for c in cols:
        fig.add_trace(go.Bar(x=df.index, y=df[c], name=c))

    fig.update_layout(
        title=f"{ticker} — Ingresos y Utilidades",
        barmode='group',
        template='plotly_dark',
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    if save:
        os.makedirs("plots", exist_ok=True)
        fig.write_html(f"plots/{ticker}_financials.html")

    fig.show()


def plot_balance(balance, ticker, save=False):
    if balance is None or balance.empty:
        return
    df = balance.T
    cols = [c for c in ["Total Assets", "Total Liabilities Net Minority Interest"] if c in df.columns]
    if not cols:
        return
    fig = go.Figure()
    for c in cols:
        fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines+markers', name=c))
    fig.update_layout(
        title=f"{ticker} — Activos vs Pasivos",
        template='plotly_dark', height=400
    )

    if save:
        os.makedirs("plots", exist_ok=True)
        fig.write_html(f"plots/{ticker}_balance.html")

    fig.show()


def plot_cashflow(cf, ticker, save=False):
    if cf is None or cf.empty:
        return
    df = cf.T
    cols = [c for c in ["Operating Cash Flow", "Free Cash Flow"] if c in df.columns]
    if not cols:
        return
    fig = go.Figure()
    for c in cols:
        fig.add_trace(go.Bar(x=df.index, y=df[c], name=c))
    fig.update_layout(
        title=f"{ticker} — Flujo de Caja Operativo",
        template='plotly_dark',
        barmode='group', height=400
    )

    if save:
        os.makedirs("plots", exist_ok=True)
        fig.write_html(f"plots/{ticker}_cashflow.html")

    fig.show()
