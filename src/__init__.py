from pprint import pprint
from src.screener import Screener
from src.ticker import Ticker


def main():
    screener = Screener()
    screener.scrape()

    res = screener.query(
        [
            ("defaultKeyStatistics.forwardPE.raw", "lt", 15),
            ("defaultKeyStatistics.pegRatio.raw", "gt", 10),
            ("summaryDetail.dividendYield.raw", "gt", 0.05),
        ]
    )

    for s in res:
        t = Ticker(s)
        print(s)
        print("PE: ", t.get_pe_ratio())
        print("PEG: ", t.get_peg_ratio())
        print("DivYield: ", t.get_dividend_yield())


if __name__ == "__main__":
    main()
