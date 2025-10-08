# import yfinance as yf
# import numpy as np

# def obtener_metricas(ticker, mode='summary'):
#     t = yf.Ticker(ticker)
    
#     fin = t.financials
#     bal = t.balance_sheet
#     cf = t.cashflow
    
#     metricas = {}
    
#     def safe_get(df, posibles):
#         """Busca la primera fila existente de una lista de posibles nombres."""
#         for name in posibles:
#             if name in df.index:
#                 return df.loc[name].dropna().iloc[0]
#         return np.nan
    
#     # ======== Métricas básicas ========
#     net_income = safe_get(fin, [
#         "Net Income", 
#         "Net Income From Continuing Operation Net Minority Interest",
#         "Net Income Common Stockholders"
#     ])
    
#     ebitda = safe_get(fin, ["EBITDA", "Normalized EBITDA"])
#     total_debt = safe_get(bal, ["Total Debt", "Total Liabilities Net Minority Interest"])
#     free_cf = safe_get(cf, ["Free Cash Flow"])
    
#     metricas["Net Income"] = net_income
#     metricas["EBITDA"] = ebitda
#     metricas["Total Debt"] = total_debt
#     metricas["Free Cash Flow"] = free_cf
    
#     # ======== Ratios adicionales si mode='full' ========
#     if mode == 'full':
#         # Buscar otras posibles variables
#         total_assets = safe_get(bal, ["Total Assets"])
#         current_assets = safe_get(bal, ["Current Assets"])
#         current_liab = safe_get(bal, ["Current Liabilities"])
#         shares_out = safe_get(bal, ["Ordinary Shares Number", "Share Issued"])
        
#         # Ratios financieros
#         if all(np.isfinite([net_income, ebitda, total_debt])):
#             metricas["Debt/EBITDA"] = total_debt / ebitda if ebitda else np.nan
        
#         if all(np.isfinite([net_income, total_assets])):
#             metricas["ROA"] = net_income / total_assets if total_assets else np.nan
        
#         if all(np.isfinite([current_assets, current_liab])):
#             metricas["Current Ratio"] = current_assets / current_liab if current_liab else np.nan
        
#         if np.isfinite(free_cf) and np.isfinite(shares_out):
#             metricas["FCF per Share"] = free_cf / shares_out
        
#     return metricas

# fundamentals/metrics.py
# import pandas as pd
# import numpy as np
# import yfinance as yf

# def safe_get(df, posibles):
#     """Busca la primera fila existente de una lista de posibles nombres."""
#     if df is None or df.empty:
#         return np.nan
#     for name in posibles:
#         if name in df.index:
#             vals = df.loc[name].dropna()
#             if not vals.empty:
#                 return vals.iloc[0]
#     return np.nan


# def calculate_growth_ratio(financials: dict, possible_fields):
#     """Calcula el crecimiento promedio de alguno de los posibles campos."""
#     try:
#         df = pd.DataFrame(financials).T
#         df = df.sort_index()

#         field = next((f for f in possible_fields if f in df.columns), None)
#         if not field:
#             return None

#         growth = df[field].pct_change().replace([np.inf, -np.inf], np.nan).dropna().mean()
#         return float(growth)
#     except Exception:
#         return None


# def compute_metrics(ticker, mode="summary"):
#     t = yf.Ticker(ticker)

#     info = t.info or {}
#     fin = t.financials
#     bal = t.balance_sheet
#     cf = t.cashflow

#     metricas = {}

#     # --- Variables base ---
#     net_income = safe_get(fin, [
#         "Net Income", 
#         "Net Income From Continuing Operation Net Minority Interest",
#         "Net Income Common Stockholders"
#     ])
#     ebitda = safe_get(fin, ["EBITDA", "Normalized EBITDA"])
#     total_debt = safe_get(bal, ["Total Debt", "Total Liabilities Net Minority Interest"])
#     total_assets = safe_get(bal, ["Total Assets"])
#     current_assets = safe_get(bal, ["Current Assets"])
#     current_liab = safe_get(bal, ["Current Liabilities"])
#     shares_out = safe_get(bal, ["Ordinary Shares Number", "Share Issued"])
#     free_cf = safe_get(cf, ["Free Cash Flow", "FreeCashFlow", "Operating Cash Flow"])

#     # --- Métricas básicas (summary) ---
#     metricas.update({
#         "Net Income": net_income,
#         "EBITDA": ebitda,
#         "Total Debt": total_debt,
#         "Free Cash Flow": free_cf,
#     })

#     # --- Métricas extendidas (full) ---
#     if mode == "full":
#         # Ratios financieros
#         metricas["Debt/EBITDA"] = total_debt / ebitda if ebitda else np.nan
#         metricas["ROA"] = net_income / total_assets if total_assets else np.nan
#         metricas["Current Ratio"] = current_assets / current_liab if current_liab else np.nan
#         metricas["FCF per Share"] = free_cf / shares_out if shares_out else np.nan

#         # Growth ratios
#         financials_dict = fin.to_dict() if fin is not None else {}
#         cashflow_dict = cf.to_dict() if cf is not None else {}

#         net_income_growth = calculate_growth_ratio(financials_dict, [
#             "Net Income", "Net Income Common Stockholders",
#             "Net Income From Continuing Operation Net Minority Interest"
#         ])
#         revenue_growth = calculate_growth_ratio(financials_dict, ["Total Revenue", "Revenue"])
#         fcf_growth = calculate_growth_ratio(cashflow_dict, ["Free Cash Flow", "FreeCashFlow", "Operating Cash Flow"])

#         metricas["Net Income Growth"] = net_income_growth
#         metricas["Revenue Growth"] = revenue_growth
#         metricas["FCF Growth"] = fcf_growth

#         # Score fundamental (condiciones tipo "quality score")
#         score = 0
#         reasons = []

#         pe = info.get("trailingPE")
#         roe = info.get("returnOnEquity")
#         profit_margin = info.get("profitMargins")
#         debt_to_equity = info.get("debtToEquity")

#         if pe and pe < 20:
#             score += 1; reasons.append("PE < 20")

#         if roe and roe > 0.1:
#             score += 1; reasons.append("ROE > 10%")

#         if profit_margin and profit_margin > 0.08:
#             score += 1; reasons.append("Margen de beneficio > 8%")

#         if debt_to_equity and debt_to_equity < 100:
#             score += 1; reasons.append("Deuda razonable")

#         if net_income_growth and net_income_growth > 0.05:
#             score += 1; reasons.append("Crecimiento de utilidades > 5%")

#         if revenue_growth and revenue_growth > 0.05:
#             score += 1; reasons.append("Crecimiento de ingresos > 5%")

#         if fcf_growth and fcf_growth > 0:
#             score += 1; reasons.append("Crecimiento del flujo de caja libre positivo")

#         metricas["Score"] = score
#         metricas["Reasons"] = reasons

#     return metricas


# fundamentals/metrics.py
import pandas as pd
import numpy as np
import yfinance as yf


def safe_get(df, posibles):
    """Busca la primera fila existente de una lista de posibles nombres."""
    if df is None or df.empty:
        return np.nan
    for name in posibles:
        if name in df.index:
            vals = df.loc[name].dropna()
            if not vals.empty:
                return vals.iloc[0]
    return np.nan


def calculate_growth_ratio(financials: dict, possible_fields):
    """Calcula el crecimiento promedio de alguno de los posibles campos."""
    try:
        df = pd.DataFrame(financials).T
        df = df.sort_index()

        field = next((f for f in possible_fields if f in df.columns), None)
        if not field:
            return None

        growth = df[field].pct_change().replace([np.inf, -np.inf], np.nan).dropna().mean()
        return float(growth)
    except Exception:
        return None


def compute_metrics(ticker, mode="summary"):
    t = yf.Ticker(ticker)
    info = t.info or {}

    # DataFrames financieros
    fin = t.financials
    bal = t.balance_sheet
    cf = t.cashflow

    # --- Modo summary: métricas básicas ---
    if mode == "summary":
        summary = {
            "symbol": ticker,
            "CompanyName": info.get("longName"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "MarketCap": info.get("marketCap"),
            "Price": info.get("currentPrice"),
            "PE": info.get("trailingPE"),
            "ForwardPE": info.get("forwardPE"),
            "PB": info.get("priceToBook"),
            "PS": info.get("priceToSalesTrailing12Months"),
            "ROE": info.get("returnOnEquity"),
            "ROA": info.get("returnOnAssets"),
            "DebtToEquity": info.get("debtToEquity"),
            "ProfitMargin": info.get("profitMargins"),
            "OperatingMargin": info.get("operatingMargins"),
            "GrossMargin": info.get("grossMargins"),
            "RevenueGrowth": info.get("revenueGrowth"),
            "EarningsGrowth": info.get("earningsGrowth"),
            "FCF": info.get("freeCashflow"),
        }
        return summary

    # --- Modo full: ratios + score + crecimientos + dataframes ---
    elif mode == "full":
        metricas = {}

        # Extraer variables clave
        net_income = safe_get(fin, [
            "Net Income",
            "Net Income From Continuing Operation Net Minority Interest",
            "Net Income Common Stockholders"
        ])
        ebitda = safe_get(fin, ["EBITDA", "Normalized EBITDA"])
        total_debt = safe_get(bal, ["Total Debt", "Total Liabilities Net Minority Interest"])
        total_assets = safe_get(bal, ["Total Assets"])
        current_assets = safe_get(bal, ["Current Assets"])
        current_liab = safe_get(bal, ["Current Liabilities"])
        shares_out = safe_get(bal, ["Ordinary Shares Number", "Share Issued"])
        free_cf = safe_get(cf, ["Free Cash Flow", "FreeCashFlow", "Operating Cash Flow"])

        # Ratios
        metricas.update({
            "Net Income": net_income,
            "EBITDA": ebitda,
            "Total Debt": total_debt,
            "Free Cash Flow": free_cf,
            "Debt/EBITDA": total_debt / ebitda if ebitda else np.nan,
            "ROA": net_income / total_assets if total_assets else np.nan,
            "Current Ratio": current_assets / current_liab if current_liab else np.nan,
            "FCF per Share": free_cf / shares_out if shares_out else np.nan,
        })

        # Crecimientos
        financials_dict = fin.to_dict() if fin is not None else {}
        cashflow_dict = cf.to_dict() if cf is not None else {}

        net_income_growth = calculate_growth_ratio(financials_dict, [
            "Net Income", "Net Income Common Stockholders",
            "Net Income From Continuing Operation Net Minority Interest"
        ])
        revenue_growth = calculate_growth_ratio(financials_dict, ["Total Revenue", "Revenue"])
        fcf_growth = calculate_growth_ratio(cashflow_dict, ["Free Cash Flow", "FreeCashFlow", "Operating Cash Flow"])

        metricas["Net Income Growth"] = net_income_growth
        metricas["Revenue Growth"] = revenue_growth
        metricas["FCF Growth"] = fcf_growth

        # Score
        score = 0
        reasons = []

        pe = info.get("trailingPE")
        roe = info.get("returnOnEquity")
        profit_margin = info.get("profitMargins")
        debt_to_equity = info.get("debtToEquity")

        if pe and pe < 20:
            score += 1; reasons.append("PE < 20")

        if roe and roe > 0.1:
            score += 1; reasons.append("ROE > 10%")

        if profit_margin and profit_margin > 0.08:
            score += 1; reasons.append("Margen de beneficio > 8%")

        if debt_to_equity and debt_to_equity < 100:
            score += 1; reasons.append("Deuda razonable")

        if net_income_growth and net_income_growth > 0.05:
            score += 1; reasons.append("Crecimiento de utilidades > 5%")

        if revenue_growth and revenue_growth > 0.05:
            score += 1; reasons.append("Crecimiento de ingresos > 5%")

        if fcf_growth and fcf_growth > 0:
            score += 1; reasons.append("Crecimiento del flujo de caja libre positivo")

        metricas["Score"] = score
        metricas["Reasons"] = reasons

        # Añadir los dataframes completos para visualizaciones futuras
        metricas["financials"] = fin
        metricas["balance"] = bal
        metricas["cashflow"] = cf

        return metricas
