from typing import List, Tuple, Generator
from subprocess import Popen, PIPE
import os
from pytickersymbols import PyTickerSymbols
from os import walk
import json
from src.utils import safeget


class Screener:
    def __init__(self, cache_folder: str = "./cache") -> None:
        self.markets = PyTickerSymbols()

        self.cache_folder = cache_folder
        self.scraper_executable = "./scraper"

    def get_ftse_100(self) -> List[str]:
        def extracy_symbol(universe):
            for ticker in universe:
                for s in ticker["symbols"]:
                    if s["currency"] == "GBP":
                        yield s["yahoo"]

        return list(
            extracy_symbol([s for s in self.markets.get_stocks_by_index("FTSE 100")])
        )

    def get_snp_500(self) -> List[str]:
        return [s["symbol"] for s in self.markets.get_stocks_by_index("S&P 500")]

    def scrape(self) -> bool:
        stocks = self.get_ftse_100() + self.get_snp_500()

        my_env = os.environ.copy()
        my_env["CACHE_PATH"] = self.cache_folder
        process = Popen(
            self.scraper_executable + " " + " ".join(stocks),
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
            env=my_env,
        )
        (output, err) = process.communicate()
        return process.wait() == 0

    def get_cached_files(self) -> Generator:
        for _, _, filenames in walk(self.cache_folder):
            for f in filenames:
                yield f"{self.cache_folder}/{f}"

    def query(self, queries: List[Tuple]) -> List[str]:
        results = []
        for q in queries:
            if len(results) == 0:
                files = list(self.get_cached_files())
            else:
                files = [f"{self.cache_folder}/ticker_{f}.json" for f in results]

            results = []
            for f in files:
                with open(f, "r") as o:
                    ticker = json.load(o)

                    symbol = safeget(
                        ticker,
                        "quoteSummary",
                        "result",
                        0,
                        "quoteType",
                        "symbol",
                    )
                    val = safeget(ticker, "quoteSummary", "result", 0, *q[0].split("."))
                    if val is None:
                        continue

                    match q[1]:
                        case "gt":
                            if val > q[2]:
                                results.append(symbol)
                        case "lt":
                            if val < q[2]:
                                results.append(symbol)
                        case "eq":
                            if val == q[2]:
                                results.append(symbol)
                        case "in":
                            if val in q[2]:
                                results.append(symbol)

        return results
