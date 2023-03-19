from flask import jsonify

from src.financial import Financial


def get_income_statements(symbol: str):
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        f = Financial(symbol)
        return (
            jsonify(
                {
                    "status": "OK",
                    "data": f.get_income_statements(),
                    "title": f.get_income_statements_titles(),
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500


def get_balance_sheets(symbol: str):
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        f = Financial(symbol)
        return (
            jsonify(
                {
                    "status": "OK",
                    "data": f.get_balance_sheets(),
                    # "title": f.get_income_statements_titles(),
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500


def get_cash_flows(symbol: str):
    try:
        assert isinstance(symbol, str), "Symbol must be a type string."
        f = Financial(symbol)
        return (
            jsonify(
                {
                    "status": "OK",
                    "data": f.get_cash_flows(),
                    # "title": f.get_income_statements_titles(),
                }
            ),
            200,
        )
    except Exception as err:
        return jsonify({"status": "ERROR", "error": str(err)}), 500
