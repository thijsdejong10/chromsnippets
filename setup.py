from setuptools import setup

setup(
    name="chromsnippets",
    version="0.0.0",
    author=["Thijs de Jong"],
    packages=["chromsnippets"],
    install_requires=[
        "rainbow-api >= 1.0.6",
        "numpy >= 1.26.4",
        "scipy >= 1.12.0",
        "pandas >= 2.2.1",
        "matplotlib >= 3.8.3",
        "seaborn >= 0.13.2",
        "plotly >= 5.19.0",
    ],
)
