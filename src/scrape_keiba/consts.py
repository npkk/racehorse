import logging
from enum import Enum

RACE_RESULT_COLUMNS = [
    "race_id",
    "final_position",
    "bracket_number",
    "gate_number",
    "horse_id",
    "sex",
    "age",
    "weight",
    "jockey_id",
    "finish_time",
    "margin",
    "favority",
    "win_odds",
    "last_three_farlongs_time",
    "position",
    "trainer_id",
    "horse_weight",
]


class HorseSex(Enum):
    SIRE = 0
    MARE = 1
    TRICK = 2


JPHS_TO_HS = {
    "牡": HorseSex.SIRE,
    "牝": HorseSex.MARE,
    "セ": HorseSex.TRICK,
}

LOGLEVEL_DICT = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}
