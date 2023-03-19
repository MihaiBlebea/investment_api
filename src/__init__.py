from pprint import pprint
from src.screener import Screener
from src.ticker import Ticker

from pandas import DataFrame


def main():
    screener = Screener()
    # screener.get_snp_500()
    screener.scrape()

    res = screener.query(
        [
            # ("defaultKeyStatistics.trailingPE.raw", "lt", 15),
            # ("defaultKeyStatistics.pegRatio.raw", "gt", 10),
            # ("summaryDetail.dividendYield.raw", "gt", 0.05),
            ("assetProfile.sector", "eq", "Financial Services"),
            ("assetProfile.industry", "in", ["Banks—Regional", "Banks—Diversified"]),
        ]
    )

    data = []
    for s in res:
        t = Ticker(s)

        data.append(
            [
                s,
                round(t.get_pe_ratio(), 2),
                t.get_peg_ratio(),
                t.get_dividend_yield(),
                t.get_profit_margin(),
            ]
        )

    df = DataFrame(
        data=data, columns=["symbol", "PE", "PEG", "DivYield", "ProfitMargins"]
    )

    df = df.sort_values("ProfitMargins", ignore_index=True, ascending=False)

    print(df)


if __name__ == "__main__":
    main()
