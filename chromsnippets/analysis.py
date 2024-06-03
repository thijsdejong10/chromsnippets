import pandas as pd
from scipy.signal import find_peaks
import numpy as np
from scipy.sparse import find
import seaborn as sns
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel
from lmfit import Model
from typing import Callable


def chromatogram_extract_peaks(
    data_group: pd.DataFrame,
    find_peaks_kwargs: dict = dict(),
    x_axis: str = "time",
    y_axis: str = "intensity",
    decimals: int = 2,
) -> pd.DataFrame:
    """
    Extract peaks from a single chromatogram or trace and return them as a peak table.
    Designed to also be usable in a grouby call.
    """
    idx, properties = find_peaks(data_group[y_axis], **find_peaks_kwargs)
    peaks = pd.DataFrame(
        {
            "indices": idx,
            "intensity": data_group[y_axis].iloc[idx],
            x_axis: data_group[x_axis].iloc[idx],
            **properties,
        }
    )
    return peaks


def series_extract_peaks(
    data: pd.DataFrame,
    groups: str | list[str] = "sample_name",
    find_peaks_kwargs: dict = dict(),
    x_axis: str = "time",
    y_axis: str = "intensity",
) -> pd.DataFrame:
    # TODO: rounding
    peaks = data.groupby(groups).apply(
        chromatogram_extract_peaks,
        find_peaks_kwargs=find_peaks_kwargs,
        y_axis=y_axis,
        x_axis=x_axis,
        include_groups=True,
    )
    peaks = peaks.reset_index(groups).reset_index(drop=True)
    return peaks


def bin_peaks(
    peaks: pd.DataFrame, threshold: float, y_axis: str = "time"
) -> tuple[pd.DataFrame, dict[float, float]]:
    # TODO: rounding
    peaks.sort_values(by=y_axis, inplace=True)
    np.cumsum(peaks[y_axis].diff() > 1)
    diff = peaks[y_axis].diff().fillna(0)
    bins = (diff > threshold).cumsum()
    bin_avg = peaks.groupby(bins)[y_axis].transform("mean")
    peaks["bin_label"] = bin_avg
    bin_mapping = dict(zip(peaks[y_axis].values, bin_avg))
    return peaks, bin_mapping


def assign_peaks(peaks: pd.DataFrame, assignments: pd.DataFrame) -> pd.DataFrame:
    return peaks
