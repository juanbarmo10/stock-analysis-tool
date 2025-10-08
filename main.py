

#%%

# main.py
from fundamentals.metrics import compute_metrics
import pandas as pd

ticker = "NVO"

print("=== SUMMARY ===")
summary = compute_metrics(ticker, mode="summary")
for k, v in summary.items():
    print(f"{k}: {v}")

print("\n=== FULL ===")
full = compute_metrics(ticker, mode="full")
for k, v in full.items():
    if k not in ["financials", "balance", "cashflow"]:
        print(f"{k}: {v}")

# Ejemplo de uso de los DataFrames
fin = full["financials"]
print("\n=== Financials DataFrame ===")
print(fin.head())

bal = full["balance"]
cf = full["cashflow"]

#%%

from fundamentals.metrics import compute_metrics
from fundamentals.visualize import plot_financials, plot_balance, plot_cashflow

ticker = "NBIS"
mode = "full"

data = compute_metrics(ticker, mode=mode)

print(f"📊 {ticker} Summary:")
for k, v in data.items():
    if not isinstance(v, (dict, type(None))):
        print(f"{k}: {v}")

if mode == "full":
    fin = data["financials"]
    bal = data["balance"]
    cf = data["cashflow"]

    # Mostrar y guardar gráficas
    plot_financials(fin, ticker, save=True)
    plot_balance(bal, ticker, save=True)
    plot_cashflow(cf, ticker, save=True)
