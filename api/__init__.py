import os
from flask import Flask

from api.indicators_controller import get_ratios, get_company, get_dividends
from api.financials_controller import (
    get_income_statements,
    get_balance_sheets,
    get_cash_flows,
)


# Initiate the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


API_V1 = "/api/v1"


app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/ratios", methods=["GET"], view_func=get_ratios
)

app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/company", methods=["GET"], view_func=get_company
)

app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/dividends", methods=["GET"], view_func=get_dividends
)

app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/income-statements",
    methods=["GET"],
    view_func=get_income_statements,
)

app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/balance-sheets",
    methods=["GET"],
    view_func=get_balance_sheets,
)

app.add_url_rule(
    f"{API_V1}/ticker/<symbol>/cash-flows",
    methods=["GET"],
    view_func=get_cash_flows,
)

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8085,
        # ssl_context="adhoc"
    )
