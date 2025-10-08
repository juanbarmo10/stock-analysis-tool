import yfinance as yf


def get_fundamentals_yf(symbol, mode="summary"):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    if mode == "summary":
        return {
        "symbol": symbol,
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
        }  # versión 1 compacta
    elif mode == 'full':
        return {
            "symbol": symbol,
            "info": info,
            "financials": ticker.financials.to_dict(),
            "balance": ticker.balance_sheet.to_dict(),
            "cashflow": ticker.cashflow.to_dict(),
        }
    
