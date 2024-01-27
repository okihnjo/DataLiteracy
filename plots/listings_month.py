import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tueplots import bundles, cycler, markers
from tueplots.constants import markers as marker_constants
from tueplots.constants.color import palettes, rgb

# Increase the resolution of all the plots below
plt.rcParams.update({"figure.dpi": 150})

plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=True))
plt.rcParams.update(
    cycler.cycler(color=palettes.tue_plot)  # marker=marker_constants.o_sized,
)

df = pd.read_csv(
    "../data/testlizenz-tuebingen-dataliteracy4students_1700939273256.csv",
    sep=";",
    header=0,
    encoding="unicode_escape",
    decimal=",",
)
print(df.columns)
df = df[df["nachfrageart"]=="miete"]
df["year"] = df["startdate"].str[:4]
df["month"] = pd.DatetimeIndex(df["startdate"]).month
df["year_removed"] = df["enddate"].str[:4]
df["month_removed"] = pd.DatetimeIndex(df["enddate"]).month
monthly_counts = df.groupby(["year", "month"]).size().reset_index(name="count")
monthly_counts_summed = (
    monthly_counts.groupby("month")["count"].sum().reset_index(name="total_count")
)
monthly_removed_counts = (
    df.groupby(["year_removed", "month_removed"])
    .size()
    .reset_index(name="removed_count")
)
monthly_removed_counts_summed = (
    monthly_removed_counts.groupby("month_removed")["removed_count"]
    .sum()
    .reset_index(name="total_removed_count")
)

months = monthly_counts_summed["month"]
bar_width = 0.4
bar_positions_added = months - bar_width / 2
bar_positions_removed = months + bar_width / 2

plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=True))

plt.bar(
    bar_positions_added,
    monthly_counts_summed["total_count"],
    width=bar_width,
    color=rgb.tue_gold,
    # alpha=0.7,
    label="Added",
)
plt.bar(
    bar_positions_removed,
    monthly_removed_counts_summed["total_removed_count"],
    width=bar_width,
    color=rgb.tue_blue,
    # alpha=0.7,
    label="Removed",
)

plt.title("Amount Of Flats Listed And Removed Per Month Over 10 Years")
plt.xlabel("Months")
plt.ylabel("Total Number of Flats")
plt.xticks(
    months,
    [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
)

plt.legend(loc="lower right")
plt.savefig("listings_month.pdf")
print(df.shape)
