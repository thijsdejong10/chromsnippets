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


def normalize_to_is(data: pd.DataFrame, lower_bound: float, upper_bound: float):
    data.intensity = (
        data.groupby("sample_name")
        .apply(
            lambda x: x.intensity
            / x[x.time.between(lower_bound, upper_bound)].intensity.max(),
            include_groups=True,
        )
        .values
    )
    return data

def bin_peaks(
    peaks: pd.DataFrame,
    threshold: float,
    bin_axis: str = "time",
    return_label: str = "bin_label",
    plot: bool = False,
) -> tuple[pd.DataFrame, dict[float, float]]:
    # TODO: rounding
    peaks.sort_values(by=bin_axis, inplace=True)
    np.cumsum(peaks[bin_axis].diff() > 1)
    diff = peaks[bin_axis].diff().fillna(0)
    bins = (diff > threshold).cumsum()
    bin_avg = peaks.groupby(bins)[bin_axis].transform("mean")
    peaks[return_label] = bin_avg
    bin_mapping = dict(zip(peaks[bin_axis].values, bin_avg))
    peaks.sort_index(inplace=True)
    return peaks, bin_mapping


def deconvolute_peaks(
    data: pd.DataFrame,
    y: str = "intensity",
    x: str = "time",
    number_of_peaks: int = 1,
    fit_parameters: dict[str, float | dict[str, float]] = dict(),
    baseline: Model = Model(lambda x, baseline: x + baseline, prefix="bl_"),
):
    """
    Fit parameters should be a dictionary that is valid as an in put to the gaussian model,
    either {"g1_center":500}, or {"g1_center":{"value":100,"min":2}}
    """
    model = baseline
    for i in range(1, number_of_peaks + 1):
        model += GaussianModel(prefix=f"g{i}_")
    params = model.make_params(**fit_parameters)
    result = model.fit(data[y], params, x=data[x])


def assign_peaks(peaks: pd.DataFrame, assignments: pd.DataFrame) -> pd.DataFrame:
    return peaks
