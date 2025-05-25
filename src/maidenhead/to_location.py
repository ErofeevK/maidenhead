from __future__ import annotations
import functools


def to_location(maiden: str, center: bool = False) -> tuple[float, float]:
    """
    convert Maidenhead grid to latitude, longitude

    Parameters
    ----------

    maiden : str
        Maidenhead grid locator

    center : bool
        If true, return the center of provided maidenhead grid square, instead of default south-west corner
        Default value = False needed to maidenhead full backward compatibility of this module.

    Returns
    -------

    latLon : tuple of float
        Geographic latitude, longitude
    """

    maiden = maiden.strip().upper()
    N = len(maiden)
    if N < 2 or N % 2:
        raise ValueError("Maidenhead locator requires even number of characters")

    precision = N//2

    def cvt(x: str) -> int: return ord(x) - ord('A')

    cvts = [cvt if not (i % 2) else lambda x: int(x) for i in range(precision)]
    weights = [24 if i % 2 else 10 for i in range(precision - 1)] + [1]

    def convert(maiden: str) -> tuple[int, int]:
        val = [c(v) for c, v in zip(cvts, maiden)]
        if any(0 > v >= 24 for v in val):
            raise ValueError("Locator uses A through X characters")
        if val[0] >= 18:
            raise ValueError("Locator uses A through R characters for the first pair")
        return functools.reduce(lambda ac, v: ((ac[0]+v[0])*v[1], ac[1]*v[1]), list(zip(val, weights)), (0, 1))

    lat_nom, lat_den = convert(maiden[1::2])
    lon_nom, lon_den = convert(maiden[::2])

    center_offset_lat = 5 if center else 0
    center_offset_lon = 10 if center else 0

    lat = (10 * (lat_nom - 9 * lat_den) + center_offset_lat) / lat_den
    lon = (20 * (lon_nom - 9 * lon_den) + center_offset_lon) / lon_den

    return (lat, lon)
