from typing import List, Sequence, Tuple, TypeVar, overload

_T = TypeVar("_T")


@overload
def chunk(seq: List[_T], size: int) -> List[List[_T]]: ...


@overload
def chunk(seq: Tuple[_T, ...], size: int) -> List[List[_T]]: ...


@overload
def chunk(seq: Sequence[_T], size: int) -> List[List[_T]]: ...


def chunk(seq: Sequence[_T], size: int) -> Sequence[Sequence[_T]]:
    """
    Splits a sequence into chunks of a specified size.

    Args:
        seq (Sequence[Any]): The sequence to be chunked.
        size (int): The size of each chunk.

    Returns:
        Sequence[Sequence[Any]]: A list of lists, each containing a chunk of the sequence.

    Example:
        >>> seq = [1, 2, 3, 4, 5]
        >>> size = 2
        >>> chunk(seq, size)
        [[1, 2], [3, 4], [5]]
    """
    return [seq[pos: pos + size] for pos in range(0, len(seq), size)]
