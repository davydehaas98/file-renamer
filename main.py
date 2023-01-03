import logging
import os.path
import argparse
import pathlib
import ffmpeg
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener


def rename_file(old_path: Path, date_taken: str, index: int):
    new_path = Path(f"{old_path.parent}/{date_taken}_{index:04d}{old_path.suffix.lower()}")
    if old_path.name != new_path.name:
        old_path.rename(new_path)
        logging.info(f"'{old_path.name}' renamed to '{new_path.name}'.")
    else:
        logging.info(f"'{old_path.name}' already has the correct name.")


def retrieve_meta_data(file_path: Path, index: int):
    logging.debug(f"Retrieving metadata from file '{file_path}'.")
    suffix = file_path.suffix.lower()
    match suffix:
        case ".jpg" | ".jpeg" | ".png" | ".heic":
            with Image.open(file_path) as image:
                exif = {}
                for tag, value in image.getexif().items():
                    if tag in TAGS:
                        exif[TAGS[tag]] = value
                date_taken = exif.get("DateTime").replace(':', '-').replace(' ', '_')
            if date_taken is not None:
                rename_file(file_path, date_taken, index)
            else:
                logging.warning(f"'{file_path}' has no date taken, skipping..")
        case ".cr3":
            logging.warning(f"'{suffix}' is not yet supported, skipping..")
            # image = Image.open(file_path)
            # logging.debug(image.getexif().items())
        case ".mov":
            probe = ffmpeg.probe(file_path)
            date_taken = probe["streams"][0]["tags"]["creation_time"].replace(':', '-').replace('T', '_').split(".")[0]
            if date_taken is not None:
                rename_file(file_path, date_taken, index)
            else:
                logging.warning(f"'{file_path}' has no date taken, skipping..")
        case _:
            logging.warning(f"'{suffix}' is not supported, skipping..")


def run(dir_path: Path):
    logging.info(f"Renaming files under '{dir_path}'.")
    paths = sorted(Path(dir_path).iterdir(), key=os.path.getmtime)
    index = 1
    register_heif_opener()
    for path in paths:
        if path.is_file():
            retrieve_meta_data(path, index)
            index += 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="Source directory path")
    path = parser.parse_args().path
    if path is None:
        path = pathlib.Path.cwd()

    run(path)
