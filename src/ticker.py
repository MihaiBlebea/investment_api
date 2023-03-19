from typing import Dict
from src.utils import safeget
from src.yahoo_finance import YahooFinance
from datetime import datetime
from src.utils import calc_percentage_diff


class Ticker:
    ticker_info = None

    historic_prices = None

    historic_dividends = None

    def __init__(self, symbol: str, yahoo_finance: YahooFinance = None) -> None:
        self.symbol = symbol
        self.yf = YahooFinance() if yahoo_finance is None else yahoo_finance

    def get_company_name(self) -> str:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "quoteType",
            "shortName",
        )

    def get_dividend_yield(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "trailingAnnualDividendYield",
            "raw",
        )

    def get_industry(self) -> str:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "assetProfile",
            "industry",
        )

    def get_sector(self) -> str:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "assetProfile",
            "sector",
        )

    def get_exchange_name(self) -> str:
        return safeget(
            self.ticker_info, "quoteSummary", "result", 0, "price", "exchange"
        )

    def get_dividend_yield(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        div_yield = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "dividendYield",
            "raw",
        )

        return div_yield if div_yield is not None else 0

    def get_beta(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "defaultKeyStatistics",
            "beta",
            "raw",
        )

    def get_market_cap(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "marketCap",
            "raw",
        )

    def get_pe_ratio(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "trailingPE",
            "raw",
        )

    def get_debt_to_equity(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        res = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "financialData",
            "debtToEquity",
            "raw",
        )
        return res / 100 if res is not None else None

    def get_eps_ratio(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "defaultKeyStatistics",
            "trailingEps",
            "raw",
        )

    def get_current_price(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        price = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "price",
            "regularMarketPrice",
            "raw",
        )

        # Price for London stock exchange is calculated in penny
        return price / 100 if self.get_exchange_name() == "LSE" else price

    def get_currency(self) -> str:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "currency",
        )

    def get_yearly_ratios(self) -> list:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        statements = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "cashflowStatementHistory",
            "cashflowStatements",
        )

        return [
            {
                "date": safeget(sts, "endDate", "fmt"),
                "year": datetime.fromtimestamp(safeget(sts, "endDate", "raw")).year,
                "net_income": safeget(sts, "netIncome", "raw"),
                "dividends_paid": abs(safeget(sts, "dividendsPaid", "raw")),
                "payout_ratio": abs(safeget(sts, "dividendsPaid", "raw"))
                / safeget(sts, "netIncome", "raw"),
                "dividend_cover": safeget(sts, "netIncome", "raw")
                / abs(safeget(sts, "dividendsPaid", "raw")),
            }
            for sts in statements
        ]

    def current_year_div_per_share(self) -> float:
        yearly_dividends = self.get_dividends_per_year()
        dividend_growth = self.get_yearly_dividend_growth(5)
        last_year_div_amount = list(yearly_dividends.values())[-1]

        return last_year_div_amount + (last_year_div_amount * dividend_growth)

    def get_dividends_per_year(self) -> Dict[int, float]:
        if self.historic_dividends is None:
            self.historic_dividends = self.yf.get_historic_dividends(self.symbol)

        current_year = datetime.now().year
        dividends = {}
        for d in self.historic_dividends:
            dt = datetime.fromtimestamp(d["date"])
            if dt.year == current_year:
                continue

            if dt.year not in dividends:
                dividends[dt.year] = 0

            dividends[dt.year] += d["amount"]

        return dividends

    def get_yearly_dividend_growth(self, last_years: int = None) -> float:
        dividends = list(self.get_dividends_per_year().values())

        if last_years is not None:
            dividends = dividends[-last_years:]
            initial = None
            total_growth = 0

        for i, div in enumerate(dividends):
            if i == 0:
                initial = div
                continue

            total_growth += calc_percentage_diff(initial, div)

            initial = div

        return round(total_growth / len(dividends), 4)

    def get_trailing_average_div_yield(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        trailing_div_yield = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "summaryDetail",
            "fiveYearAvgDividendYield",
            "raw",
        )

        if trailing_div_yield is None:
            return 0

        return float(trailing_div_yield) / 100

    def get_cadi(self) -> int:
        divs = list(self.get_dividends_per_year().values())
        divs.reverse()
        cadi = 0

        for i in range(len(divs)):
            cadi += 1

            if i + 1 == len(divs):
                break

            if divs[i] < divs[i + 1]:
                break

        return cadi

    def get_peg_ratio(self) -> float:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "defaultKeyStatistics",
            "pegRatio",
            "raw",
        )

    def get_ex_dividend_date(self, fmt: bool = False) -> int:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "calendarEvents",
            "exDividendDate",
            "fmt" if fmt else "raw",
        )

    def get_next_dividend_date(self, fmt: bool = False) -> int:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        return safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "calendarEvents",
            "dividendDate",
            "fmt" if fmt else "raw",
        )

    def dividend_discount_model(self, ror: float = 0.1) -> float:
        current_dividend = self.get_dividend_yield() * self.get_current_price() / 100
        return current_dividend / (ror - self.get_yearly_dividend_growth(10))

    def dividend_discount_model_v2(
        self, ror: float = 0.1, hold_years: int = 10
    ) -> float:
        current_dividend = self.get_dividend_yield() * self.get_current_price() / 100
        discounted_dividends = []
        for i in range(hold_years):
            # print(i)
            cv = current_dividend + (current_dividend * i) / (1 + ror) ** i
            discounted_dividends.append(cv)

        selling_price = self.get_current_price() / 100 + (
            self.get_current_price() / 100 * ror
        )
        discounted_selling_price = selling_price / (1 + ror) ** hold_years
        return sum(discounted_dividends) + discounted_selling_price

    def ratios_valuation_model(self) -> float:
        peg = self.get_peg_ratio()
        if peg is None:
            return None

        peg = peg / 100

        return self.get_eps_ratio() * (1 + peg) * self.get_pe_ratio()


if __name__ == "__main__":
    from pprint import pprint

    yf = YahooFinance()

    tkr = Ticker("AAPL", yf)

    pprint(tkr.ratios_valuation_model())

    # pprint(tkr.get_next_dividend_date(True))

    # pprint(tkr.dividend_discount_model(0.1))

    pprint(tkr.get_current_price())

    # pprint(tkr.dividend_discount_model_v2())
