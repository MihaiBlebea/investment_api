from typing import List
from pathlib import Path
import json
import time
import os
from currency_converter import CurrencyConverter, SINGLE_DAY_ECB_URL
from datetime import datetime

# TODO: Update SSL cert for currency converter
# cc = CurrencyConverter(SINGLE_DAY_ECB_URL)


DETA_DRIVER_NAME = "dividend-calculator"


def safeget(dct: dict, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def calc_percentage_diff(initial: float, current: float) -> float:
    return abs(initial - current) / current


def cache_factory(cache_dir: str, file_prefix: str, ttl_sec: int):
    def cache(func):
        def wrapper(*args, **kwargs):
            args_params = [str(argv) for argv in args[1:]]
            kwargs_params = [str(argv) for argv in list(kwargs.values())]

            file_sufix = "_".join(args_params + kwargs_params)

            Path(cache_dir).mkdir(parents=True, exist_ok=True)

            cache_file_path = Path(f"{cache_dir}/{file_prefix}_{file_sufix}.json")

            if cache_file_path.is_file():
                now = int(time.time())
                created_at = int(cache_file_path.stat().st_mtime)

                if now < created_at + ttl_sec:
                    with open(cache_file_path, "r") as file:
                        return json.loads(file.read())

            print(f"Fetching {cache_file_path} from source")
            result = func(*args, **kwargs)

            with open(cache_file_path, "w") as file:
                file.write(json.dumps(result, indent=4, ensure_ascii=False))

            return result

        return wrapper

    return cache


def growth_in_percentage(data: List[float]) -> List[float]:
    initial = data[0]
    res = [0]
    for d in data[1:]:
        res.append(calc_percentage_diff(initial, d))

    return res


def to_GBP(amount: float, from_currency: str) -> float:
    if from_currency == "GBp":
        return amount / 100

    return amount

    # TODO: enable currency converter after fixing the SSL cert issue
    # return cc.convert(amount, from_currency, "GBP")


def to_percentage(value: float) -> str:
    return f"{round(value * 100, 2)}%"


def to_gbp_fmt(value: float) -> str:
    value: str = "{:20,.2f}".format(value).strip()
    if ".00" in value:
        value = value.replace(".00", "")

    return "£" + value


def to_int(value: float) -> int:
    return int(value)


def to_date(value: int) -> str:
    if value is None:
        return ""
    return datetime.fromtimestamp(value).strftime("%d-%m-%Y")
