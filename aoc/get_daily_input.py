"""
Fetch, cache, and access your input data from Advent of Code
https://adventofcode.com
"""

import os
import sys

from typing import Iterable
from urllib.request import Request, urlopen

URL_TEMPLATE = "https://adventofcode.com/{year}/day/{day}/input"
DEFAULT_SESSION = os.environ.get("AOC_SESSION")
DEFAULT_USERAGENT = os.environ.get("AOC_USERAGENT")
CACHE_DIRECTORY = ".aoccache"


def _cache_filename(year: int, day: int) -> str:
    return os.path.join(CACHE_DIRECTORY, str(year), f"{day}.txt")


def download_daily_input(
    year: int, day: int,
    session_id: str = DEFAULT_SESSION, useragent: str = DEFAULT_USERAGENT
) -> None:
    """
    Download specified day's input into the cache directory
    """
    with urlopen(Request(
            url=URL_TEMPLATE.format(year=year, day=day),
            headers={"Cookie": f"session={session_id}",
                     "User-Agent": useragent}
    )) as response:
        if response.status == 200:
            os.makedirs(os.path.join(CACHE_DIRECTORY, str(year)), exist_ok=True)
            with open(_cache_filename(year, day), mode="wt", encoding="ascii") as outfile:
                for line in response:
                    outfile.write(line.decode())


def get_daily_input(
    year: int, day: int,
    session_id: str = DEFAULT_SESSION, force_download: bool = False
) -> Iterable[str]:
    """
    Yield lines from the day's input set
    """
    if force_download or not os.path.exists(_cache_filename(year, day)):
        download_daily_input(year, day, session_id)
    with open(_cache_filename(year, day), mode="rt", encoding="ascii") as infile:
        return map(lambda l: l.rstrip("\n"), infile)


def main() -> None:
    """
    Download to cached based on command-line arguments
    """
    year, day = (sys.argv + [2015, 1])[1:3]
    print(f"Fetching {year} day {day}")
    get_daily_input(int(year), int(day))


if __name__ == "__main__":
    main()
