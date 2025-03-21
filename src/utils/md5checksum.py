import hashlib


def md5(file_name: str) -> str:
    """
    Calculate the MD5 hash of a file.

    Args:
        file_name (str): The name of the file to calculate the MD5 hash for.

    Returns:
        str: The MD5 hash of the file.
    """
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def write_checksum(file_path: str, file_path_checksum: str) -> None:
    """
    Generate a checksum for a given file and write it to another file.

    Args:
        file_path (str): The path to the file for which the checksum needs to be generated.
        file_path_checksum (str): The path to the file where the checksum will be written.

    Returns:
        None
    """
    md5_checksum = md5(file_path)
    with open(file_path_checksum, "w") as file:
        file.write(md5_checksum)


def read_checksum(file_path_checksum: str) -> str:
    """
    Reads the contents of a file and returns the checksum.

    Args:
        file_path_checksum (str): The path to the file containing the checksum.

    Returns:
        str: The checksum read from the file.
    """
    with open(file_path_checksum, 'r') as file:
        data = file.read().replace('\n', '')
    return data.strip()
