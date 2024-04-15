import pandas as pd
from scipy.signal import find_peaks
import numpy as np


def chromatogram_extract_peaks(
    data_group: pd.DataFrame, find_peaks_kwargs: dict = dict(), y_axis: str = "time"
) -> pd.DataFrame:
    """
    Extract peaks from a single chromatogram or trace and return them as a peak table.
    Designed to also be usable in a grouby call.
    """
    idx, properties = find_peaks(data_group.intensity, **find_peaks_kwargs)
    peaks = pd.DataFrame(
        {
            "indices": idx,
            "intensity": data_group.intensity.iloc[idx],
            y_axis: data_group[y_axis].iloc[idx],
            **properties,
        }
    )
    return peaks


def series_extract_peaks(
    data: pd.DataFrame, groups: str | list[str] = "sample_name", y_axis: str = "time"
) -> pd.DataFrame:
    # TODO: rounding
    peaks = data.groupby(groups).apply(chromatogram_extract_peaks, y_axis=y_axis)
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
