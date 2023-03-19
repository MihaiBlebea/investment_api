from flask import jsonify

from src.ticker import Ticker


def get_ratios(symbol: str):
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        t = Ticker(symbol)
        return (
            jsonify(
                {
                    "status": "OK",
                    "data": {
                        "dividend_yield": t.get_dividend_yield(),
                        "current_price": t.get_current_price(),
                        "current_dividend_amount": t.current_year_div_per_share(),
                        "dividend_growth": t.get_yearly_dividend_growth(5),
                        "dividend_ratios_per_year": t.get_yearly_ratios(),
                        "cadi": t.get_cadi(),
                        "beta": t.get_beta(),
                        "pe_ratio": t.get_pe_ratio(),
                        "eps_ratio": t.get_eps_ratio(),
                        "peg_ratio": t.get_peg_ratio(),
                        "market_cap": t.get_market_cap(),
                        "debt_to_equity": t.get_debt_to_equity(),
                        "intrinsec_value": t.ratios_valuation_model(),
                    },
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500


def get_company(symbol: str) -> None:
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        t = Ticker(symbol)
        return (
            jsonify(
                {
                    "status": "OK",
                    "data": {
                        "company_name": t.get_company_name(),
                        "industry": t.get_industry(),
                        "sector": t.get_sector(),
                    },
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500


def get_dividends(symbol: str):
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        t = Ticker(symbol)
        return jsonify({"status": "OK", "data": t.get_dividends_per_year()}), 200
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500
