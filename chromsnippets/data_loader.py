import rainbow as rb
from pathlib import Path
import numpy as np
import pandas as pd
from functools import partial
import multiprocessing


def load_fid(
    directory: rb.DataDirectory,
    solvent_cutoff: float = 2.7,
    set_intensity_zero: bool = False,
) -> pd.DataFrame:
    """
    Use rainbow-api to read in FID data. Optionally cut off the solvent peak, and set the minimum to zero.
    """
    if "FID" not in directory.by_detector:
        print(f"No FID data detected, skipping load_fid for {directory.name}")

    # fid_data = directory.get_file(str(directory.by_detector["FID"][0]))
    fid_data = directory.by_detector["FID"][0]
    fid_df = pd.DataFrame(
        {
            "sample": directory.name.split(".")[0],
            "time": fid_data.xlabels,
            "intensity": fid_data.data.reshape(-1),
        }
    )
    fid_df = fid_df[fid_df.time > solvent_cutoff]
    if set_intensity_zero:
        fid_df.intensity = fid_df.intensity - min(fid_df.intensity)

    return fid_df


def load_ms(directory: rb.DataDirectory) -> pd.DataFrame:
    """
    Use rainbow-api to read in a data.ms file.
    Setting the precision for the mass should be done when creating the directory itself.
    """
    if "MS" not in directory.by_detector:
        print(f"No ms data detected, skipping load_ms for {directory.name}")
    ms_data = directory.by_detector["MS"][0]
    ms_df = pd.DataFrame(
        {
            "sample": directory.name.split(".")[0],
            "time": np.repeat(ms_data.xlabels, len(ms_data.ylabels)),
            "mz": np.tile(ms_data.ylabels, len(ms_data.xlabels)),
            "intensity": ms_data.data.flatten(),
        }
    )

    ms_df = ms_df[ms_df.intensity != 0]

    ms_df.reset_index(drop=True, inplace=True)

    return ms_df


def load_folder_fid(
    data_directory: Path,
    load_fid_kwargs: dict = dict(),
) -> pd.DataFrame:
    files = data_directory.glob("*.D")
    files = [f.__str__() for f in files]
    pool = multiprocessing.Pool()
    # rb_directories = map(rb.read,files)
    rb_directories = pool.map(partial(rb.read), files)
    fid_data = pd.concat(pool.map(partial(load_fid, **load_fid_kwargs), rb_directories))
    fid_data.reset_index(drop=True, inplace=True)
    fid_data["sample"] = fid_data["sample"].astype("category")
    return fid_data


def load_folder_ms(
    data_directory: Path,
    prec: int = 1,
) -> pd.DataFrame:
    files = data_directory.glob("*.D")
    files = [f.__str__() for f in files]
    pool = multiprocessing.Pool()
    # rb_directories = map(rb.read,files)
    rb_directories = pool.map(partial(rb.read, prec=prec), files)
    ms_data = pd.concat(pool.map(load_ms, rb_directories))
    ms_data.reset_index(drop=True, inplace=True)
    ms_data["sample"] = ms_data["sample"].astype("category")
    return ms_data
