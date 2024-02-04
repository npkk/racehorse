import logging
import os
import pathlib
from collections.abc import Generator

from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
from pandas import DataFrame, concat
from tqdm import trange

from . import consts, settings, util

# TODO remove consts for test
URL = "https://race.netkeiba.com/race/result.html?race_id=202308030211"


def url_generate() -> Generator[str, None, None]:
    if settings.mode != "PROD":
        yield URL
    else:
        year_start = get_resume(0, 4, 2010)
        place_start = get_resume(4, 6, 11)
        kai_start = get_resume(6, 8, 11)
        day_start = get_resume(8, 10, 11)
        race_start = get_resume(10, 12, 13)
        for year_num in trange(year_start, 2023):
            for place_num in range(place_start, 11):
                for kai_num in range(kai_start, 11):
                    for day_num in range(day_start, 11):
                        for race_num in range(race_start, 13):
                            yield f"https://race.netkeiba.com/race/result.html?race_id={year_num:04d}{place_num:02d}{kai_num:02d}{day_num:02d}{race_num:02d}"


def get_resume(start: int, end: int, default: int) -> int:
    return (
        int(settings.resume_race_id[start:end])
        if settings.resume_race_id is not None
        else default
    )


def process_line(tr: Tag) -> DataFrame | None:
    """Process tr to DataFrame."""
    linedata = []
    for idx, td in enumerate(tr.select("td")):
        if idx == 3:
            # horse_name to horse_id
            linedata.append(td.select_one("a").attrs["href"].rsplit("/", 1)[-1].strip())
        elif idx == 4:
            # ex. 牡2 to 牡, 2
            linedata.append(consts.JPHS_TO_HS[td.text.strip()[0]].value)
            linedata.append(td.text.strip()[1:])
        elif idx in [6, 13]:
            # jockey and trainer
            if td.select_one("a") is None:
                linedata.append(td.text.strip())
            else:
                linedata.append(
                    td.select_one("a").attrs["href"].rsplit("/", 2)[-2].strip(),
                )
        elif idx == 14:
            linedata.append(td.text.strip().split("(")[0])
        else:
            linedata.append(td.text.strip())
    line = DataFrame(
        [linedata],
        columns=list(consts.RACE_RESULT_COLUMNS[1:]),
    )
    logging.debug(f"line_generated: {line}")

    return line


def item_process(df: DataFrame, race_id: str) -> None:
    """Process DataFrame to output."""
    df.to_csv(pathlib.Path(settings.csv_dir, f"{race_id}.csv"), index=False)


def table_generate(soup: BeautifulSoup, race_id: str) -> DataFrame | None:
    """Process soup to DataFrame"""
    race_result = soup.select_one("table.RaceTable01")
    logging.debug(f"race_result: {race_result}")
    if race_result is None:
        return None

    target_df = DataFrame([], columns=list(consts.RACE_RESULT_COLUMNS[1:]))

    for tr_tag in race_result.select("tr.HorseList"):
        tag_df = process_line(tr_tag)
        logging.debug(f"tag_df: {tag_df}")
        if tag_df is not None:
            target_df = concat([target_df, tag_df], axis=0)

    target_df["race_id"] = race_id

    logging.debug(f"table_generated: {target_df}")
    return target_df


def run() -> None:
    for url in url_generate():
        race_id = url.rsplit("=", 1)[-1]
        soup = util.get_soup(url)
        race_result = table_generate(soup, race_id)
        if race_result is None:
            continue
        item_process(race_result, race_id)


if __name__ == "__main__":
    load_dotenv()
    if settings.loglevel is not None:
        logging.basicConfig(level=consts.LOGLEVEL_DICT[os.environ["LOGLEVEL"]])
    run()
