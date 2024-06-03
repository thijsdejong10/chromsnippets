import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
from pathlib import Path
from typing import Optional


def plot_signal_and_peaks_interactive(
    signal: pd.DataFrame,
    peaks: pd.DataFrame,
    x: str = "time",
    y_signal: str = "intensity",
    y_peaks: str = "intensity",
    opacity: float = 0.8,
    show: bool = True,
    save_path: Optional[Path] = None,
):
    csequence = [f"{rgb[:-1]},{opacity})" for rgb in px.colors.qualitative.Set3]
    fig = px.line(
        signal,
        x=x,
        y=y_signal,
        color="sample_name",
        color_discrete_sequence=csequence,
    )

    [
        fig.add_trace(d)
        for d in px.scatter(
            peaks,
            x=x,
            y=y_peaks,
            color="sample_name",
            color_discrete_sequence=csequence,
        ).data
    ]
    if show:
        fig.show()
    if save_path:
        fig.write_html(save_path)


def plot_peak_distribution(
    data: pd.DataFrame,
    peaks: pd.DataFrame,
    binwidth: float,
    x: str = "time",
    y: str = "intenisty",
    palette: str = "Set2",
    show: bool = True,
    save_path: Optional[Path] = None,
):
    # NOTE: might be nice to get an interactive plotly version of this as well, but that is a bit too much effort at this point
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    sns.histplot(
        data=peaks,
        x=x,
        binwidth=binwidth,
        element="step",
        hue="bin_label",
        palette=palette,
        ax=ax,
    )
    sns.lineplot(data=data, x=x, y=y, hue="sample_name", ax=ax2)
    if show:
        plt.show()
    if save_path:
        fig.savefig(save_path)
