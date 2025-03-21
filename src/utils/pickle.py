import gzip
import logging
import pathlib
import pickle
import shutil
from os import PathLike
from typing import Any, Union

import pandas as pd

from .md5checksum import md5
from .md5checksum import read_checksum as _read_checksum
from .md5checksum import write_checksum as _write_checksum

logger = logging.getLogger("ailab.process.pickle")

FilePath = Union[str, PathLike[str]]


def save(
        data: Union[pd.DataFrame, Any],
        file_path: FilePath,
        write_checksum: bool = False,
        protocol: int = pickle.HIGHEST_PROTOCOL,
        **kwargs: Any,
) -> None:
    """
    Saves the given data to a pickle file. Dump to .tmp file first and rename it to the original file
    Create parent directory if it does not exist
    """
    _filepath: pathlib.Path
    if isinstance(file_path, pathlib.Path):
        _filepath = file_path
    else:
        _filepath = pathlib.Path(file_path)

    tmp_filename = _filepath.with_suffix(_filepath.suffix + ".tmp")

    if not _filepath.parent.exists():
        logger.warning(f"Directory '{_filepath.parent}' does not exist. Creating...")
        _filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        if isinstance(data, pd.DataFrame):
            if _filepath.suffix == ".gz":
                data.to_pickle(tmp_filename, compression="gzip", protocol=protocol, **kwargs)
            elif _filepath.suffix == ".pkl":
                data.to_pickle(tmp_filename, protocol=protocol, **kwargs)
            elif _filepath.suffix == ".parquet":
                data.to_parquet(tmp_filename, **kwargs)
            elif _filepath.suffix == ".csv":
                data.to_csv(tmp_filename, **kwargs)
            elif _filepath.suffix == ".json":
                data.to_json(tmp_filename, **kwargs)
            else:
                raise ValueError(f"Unsupported file type '{_filepath.suffix}'")
        else:
            if _filepath.suffix == ".pkl":
                with open(tmp_filename, "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            elif _filepath.suffix == ".gz":
                with gzip.open(tmp_filename, "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            elif _filepath.suffix == ".txt":
                with open(tmp_filename, "w") as file:
                    file.write(data)
            else:
                with open(tmp_filename, "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

        # rename files -> atomic
        shutil.move(tmp_filename, file_path)

        # write checksum
        if write_checksum:
            _write_checksum(str(file_path), str(_filepath.with_suffix(_filepath.suffix + ".checksum")))

    except BaseException as e:
        logger.error(f"Failed to save '{_filepath}', deleting tmp file '{tmp_filename}'")
        tmp_filename.unlink(missing_ok=True)
        logger.exception(e)
        raise e


def load(file_path: FilePath, read_checksum: bool = False) -> Any:
    """
    Loads data from a pickle file.

    Args:
        file_path (str): The name of the pickle file.
        read_checksum (bool)
    Returns:
        Any: The loaded data.
    """
    _filepath: pathlib.Path
    if isinstance(file_path, pathlib.Path):
        _filepath = file_path
    else:
        _filepath = pathlib.Path(file_path)

    if _filepath.suffix == ".gz":
        with gzip.open(_filepath, "rb") as file:
            data = pickle.load(file)
    elif _filepath.suffix == ".pkl":
        with open(_filepath, "rb") as file:
            data = pickle.load(file)
    elif _filepath.suffix == ".parquet":
        data = pd.read_parquet(_filepath)
    elif _filepath.suffix == ".csv":
        data = pd.read_csv(_filepath)
    elif _filepath.suffix == ".json":
        data = pd.read_json(_filepath)
    elif _filepath.suffix == ".txt":
        with open(_filepath, "r") as file:
            data = file.read()
    else:
        raise ValueError(f"Unsupported loading file type '{_filepath.suffix}'")

    # checksum
    if read_checksum:
        checksum_file_path = _filepath.with_suffix(_filepath.suffix + ".checksum")
        if not checksum_file_path.exists():
            logger.error(f"Checksum file not found: {_filepath}")
            return data
        data_checksum: str = _read_checksum(str(checksum_file_path))
        if data_checksum != md5(str(_filepath)):
            logger.error(f"Checksum failed: {_filepath}")

    return data
