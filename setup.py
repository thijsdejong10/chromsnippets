from setuptools import setup

setup(
    name="chromsnippet",
    version="0.0.0",
    author=["Thijs de Jong"],
    packages=["chromsnippet"],
    install_requires=[
        "rainbow-api >= 1.0.6",
        "numpy >= 1.26.6",
        "scipy >= 1.12.0",
        "pandas >= 2.2.1",
        "matplotlib >= 3.8.3",
        "seaborn >= 0.13.2",
        "plotly >= 5.19.0",
    ],
)
