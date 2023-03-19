from typing import Tuple, List

from src.ticker import Ticker
from src.yahoo_finance import YahooFinance
from src.utils import safeget


class Financial(Ticker):
    def __init__(self, symbol: str, yahoo_finance: YahooFinance = None) -> None:
        super().__init__(symbol, yahoo_finance)

    def get_income_statements_titles(self) -> List[Tuple[str, str]]:
        return [
            ("Total revenue", "total_revenue"),
            ("Operating expenses", None),
            ("Selling general and administrative", "selling_general_administrative"),
            ("Total operating expenses", "total_operating_expenses"),
            ("Interest expense", "interest_expense"),
            ("Income before tax", "income_before_tax"),
            ("Income tax expense", "income_tax_expense"),
            ("Income from continuing operations", "net_income_from_continuing_ops"),
            ("Net income", "net_income"),
            (
                "Net income available to common shareholders",
                "net_income_applicable_to_common_shares",
            ),
            ("Basic EPS", None),
            ("Diluted EPS", None),
            ("Basic average shares", None),
            ("Diluted average shares", None),
        ]

    def get_income_statements(self) -> dict | None:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        statements = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "incomeStatementHistory",
            "incomeStatementHistory",
        )

        if statements is None:
            return None

        res = []
        for s in statements:
            res.append(
                {
                    "date": safeget(s, "endDate", "fmt"),
                    "total_revenue": safeget(s, "totalRevenue", "raw"),
                    "cost_of_revenue": safeget(s, "costOfRevenue", "raw"),
                    "gross_profit": safeget(s, "grossProfit", "raw"),
                    "research_development": safeget(s, "researchDevelopment", "raw"),
                    "selling_general_administrative": safeget(
                        s, "sellingGeneralAdministrative", "raw"
                    ),
                    "total_operating_expenses": safeget(
                        s, "totalOperatingExpenses", "raw"
                    ),
                    "operating_income": safeget(s, "operatingIncome", "raw"),
                    "total_other_income_expense_net": safeget(
                        s, "totalOtherIncomeExpenseNet", "raw"
                    ),
                    "ebit": safeget(s, "ebit", "raw"),
                    "interest_expense": safeget(s, "interestExpense", "raw"),
                    "income_before_tax": safeget(s, "incomeBeforeTax", "raw"),
                    "income_tax_expense": safeget(s, "incomeTaxExpense", "raw"),
                    "net_income_from_continuing_ops": safeget(
                        s, "netIncomeFromContinuingOps", "raw"
                    ),
                    "net_income": safeget(s, "netIncome", "raw"),
                    "net_income_applicable_to_common_shares": safeget(
                        s, "netIncomeApplicableToCommonShares", "raw"
                    ),
                }
            )

        return res

    def get_balance_sheets(self) -> dict | None:
        if self.ticker_info is None:
            self.ticker_info = self.yf.get_ticker_info(self.symbol)

        statements = safeget(
            self.ticker_info,
            "quoteSummary",
            "result",
            0,
            "balanceSheetHistory",
            "balanceSheetStatements",
        )

        if statements is None:
            return None

        res = []
        for s in statements:
            res.append(
                {
                    "date": safeget(s, "endDate", "fmt"),
                    "cash": safeget(s, "cash", "raw"),
                    "short_term_investments": safeget(s, "shortTermInvestments", "raw"),
                    "net_receivables": safeget(s, "netReceivables", "raw"),
                    "inventory": safeget(s, "inventory", "raw"),
                    "other_current_assets": safeget(s, "otherCurrentAssets", "raw"),
                    "total_current_assets": safeget(s, "totalCurrentAssets", "raw"),
                    "long_term_investments": safeget(s, "longTermInvestments", "raw"),
                    "property_plant_equipment": safeget(
                        s, "propertyPlantEquipment", "raw"
                    ),
                    "other_assets": safeget(s, "otherAssets", "raw"),
                    "total_assets": safeget(s, "totalAssets", "raw"),
                    "accounts_payable": safeget(s, "accountsPayable", "raw"),
                    "short_long_term_debt": safeget(s, "shortLongTermDebt", "raw"),
                    "other_current_liab": safeget(s, "otherCurrentLiab", "raw"),
                    "long_term_debt": safeget(s, "longTermDebt", "raw"),
                    "other_liab": safeget(s, "otherLiab", "raw"),
                    "total_current_liabilities": safeget(
                        s, "totalCurrentLiabilities", "raw"
                    ),
                    "total_liab": safeget(s, "totalLiab", "raw"),
                    "common_stock": safeget(s, "commonStock", "raw"),
                    "retained_earnings": safeget(s, "retainedEarnings", "raw"),
                    "treasury_stock": safeget(s, "treasuryStock", "raw"),
                    "other_stockholder_equity": safeget(
                        s, "otherStockholderEquity", "raw"
                    ),
                    "total_stockholder_equity": safeget(
                        s, "totalStockholderEquity", "raw"
                    ),
                    "net_tangible_assets": safeget(s, "netTangibleAssets", "raw"),
                }
            )

        return res

    def get_cash_flows(self) -> dict | None:
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

        if statements is None:
            return None

        res = []
        for s in statements:
            res.append(
                {
                    "date": safeget(s, "endDate", "fmt"),
                    "net_income": safeget(s, "netIncome", "raw"),
                    "depreciation": safeget(s, "depreciation", "raw"),
                    "change_to_net_income": safeget(s, "changeToNetincome", "raw"),
                    "change_to_account_receivables": safeget(
                        s, "changeToAccountReceivables", "raw"
                    ),
                    "change_to_liabilities": safeget(s, "changeToLiabilities", "raw"),
                    "change_to_inventory": safeget(s, "changeToInventory", "raw"),
                    "change_to_operating_activities": safeget(
                        s, "changeToOperatingActivities", "raw"
                    ),
                    "total_cash_from_operating_activities": safeget(
                        s, "totalCashFromOperatingActivities", "raw"
                    ),
                    "capital_expenditures": safeget(s, "capitalExpenditures", "raw"),
                    "investments": safeget(s, "investments", "raw"),
                    "other_cashflows_from_investing_activities": safeget(
                        s, "otherCashflowsFromInvestingActivities", "raw"
                    ),
                    "total_cashflows_from_investing_activities": safeget(
                        s, "totalCashflowsFromInvestingActivities", "raw"
                    ),
                    "dividends_paid": safeget(s, "dividendsPaid", "raw"),
                    "net_borrowings": safeget(s, "netBorrowings", "raw"),
                    "other_cashflows_from_financing_activities": safeget(
                        s, "otherCashflowsFromFinancingActivities", "raw"
                    ),
                    "total_cash_from_financing_activities": safeget(
                        s, "totalCashFromFinancingActivities", "raw"
                    ),
                    "change_in_cash": safeget(s, "changeInCash", "raw"),
                    "repurchase_of_stock": safeget(s, "repurchaseOfStock", "raw"),
                }
            )

        return res


if __name__ == "__main__":
    from pprint import pprint

    f = Financial("AAPL")
    pprint(f.get_income_statements())
