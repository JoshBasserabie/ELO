import urllib.request
from zipfile import ZipFile
import os
import constants

GAME_FIELDS = [
    "WhiteFideId",
    "BlackFideId",
    "White",
    "Black",
    "WhiteElo",
    "BlackElo",
    ]

SCORE_CONVERSION = {
        "1/2-1/2": 0.5,
        "1-0": 1,
        "0-1": 0
    }

PGN_URL = "https://theweekinchess.com/zips/twic{id}g.zip"
PGN_ZIP_PATH = "PGN_zips/{id}.zip"
PGN_PATH = "PGNs/"
UNZIP_PATH = PGN_PATH + "{id}/"
PGN_NAME = "twic{id}.pgn"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"


def download_PGNs(start=constants.PGN_DEFAULT_START, end=constants.PGN_DEFAULT_END):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]
    urllib.request.install_opener(opener)

    for i in range(start, end):
        url = PGN_URL.format(id=i)
        path = PGN_ZIP_PATH.format(id=i)
        urllib.request.urlretrieve(url, path)

def unzip_PGNs(start=constants.PGN_DEFAULT_START, end=constants.PGN_DEFAULT_END):
    for i in range(start, end):
        zip_path = PGN_ZIP_PATH.format(id=i)
        path = UNZIP_PATH.format(id=i)
        file_name = PGN_NAME.format(id=i)
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(path)
            os.rename(path + file_name, PGN_PATH + file_name)
            os.rmdir(path)

def extract_PGN_data(id):
    result = []
    current = {}
    full_path = PGN_PATH + PGN_NAME.format(id=id)
    with open(full_path, encoding="utf8", errors="replace") as file:
        for line in file:
            line = line.rstrip()
            if len(line) > 1:
                if line[0] == "[" and line[-1] == "]":
                    line = line[1:-1]
                    line = line.replace('"', '')
                    key, value = line.split(" ")[0], " ".join(line.split(" ")[1:])
                    if key == "Result":
                        try:
                            current["WhiteScore"] = SCORE_CONVERSION[value]
                        except KeyError:
                            pass
                    if key in GAME_FIELDS:
                        current[key] = value
                    if key == "Event":
                        if len(current) == len(GAME_FIELDS + ["WhiteScore"]):
                            result = result + [current]
                        current = {}
    return result
