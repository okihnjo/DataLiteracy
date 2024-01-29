import datetime as dt
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.api.types import is_object_dtype
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from tueplots import bundles, cycler
from tueplots.constants.color import palettes

plt.rcParams.update({"figure.dpi": 150})

plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=True))
plt.rcParams.update(
    cycler.cycler(color=palettes.tue_plot)  # marker=marker_constants.o_sized,
)

df = pd.read_csv(
    "../data/testlizenz-tuebingen-dataliteracy4students_rt_stuttgart/testlizenz-tuebingen-dataliteracy4students_1706088512814.csv",
    sep=";",
    encoding="unicode_escape",
)
# include year column
df["year"] = df["startdate"].str[:4]
df["endyear"] = df["enddate"].str[:4]
df["month"] = pd.DatetimeIndex(df["startdate"]).month
df = df[df["oadr_ort"] == "Tübingen"]
oadr_u2 = df["oadr_u2"].unique().tolist()
cleaned_oadr_2 = [x for x in oadr_u2 if x == x]
df_w_loc = df[df["oadr_u2"].notna()]
df_wo_loc = df[df["oadr_u2"].isna()]
for column in df.columns:
    if is_object_dtype(df[column]):
        if df[column].str.contains(",").any():
            df[column] = df[column].str.replace(",", ".").astype(float)
            df_w_loc[column] = df_w_loc[column].str.replace(",", ".").astype(float)
interesting_regions = df_w_loc["oadr_u2"].unique().tolist()
interesting_regions = [x for x in interesting_regions if x == x]
df_w_loc["year_month"] = (
    df_w_loc["year"].astype(str) + "-" + df_w_loc["month"].astype(str).str.zfill(2)
)
df_w_loc = df_w_loc.sort_values(by=["year_month"])
df_w_loc_interesting = df_w_loc[df_w_loc["oadr_u2"].isin(interesting_regions)]
df_w_loc_interesting_copy = df_w_loc_interesting.copy()
df_w_loc_interesting_copy["startdate"] = pd.to_datetime(
    df_w_loc_interesting_copy["startdate"]
)
df_w_loc_interesting_copy["startdate_ordinal"] = df_w_loc_interesting_copy[
    "startdate"
].map(dt.datetime.toordinal)
lg_df = pd.DataFrame(columns=["oadr_u2", "r_sq", "intercept", "slope", "p_val"])
df_w_loc_interesting_copy = df_w_loc_interesting_copy.sort_values(
    by=["oadr_u2", "startdate_ordinal"]
)
selected_regions = ["Feuerhägle/Mühlenviertel", "Au/Unterer Wert/Französiches Viertel"]
for i in selected_regions:
    x = df_w_loc_interesting_copy.loc[
        df_w_loc_interesting_copy["oadr_u2"] == i, "startdate_ordinal"
    ]
    y = df_w_loc_interesting_copy.loc[
        df_w_loc_interesting_copy["oadr_u2"] == i, "kstn_miete_kalt_pqm"
    ]
    test_result = linregress(x=x, y=y)
    print(test_result)
    x = x.values.reshape(-1, 1)
    print(i)
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    intercept = model.intercept_
    slope = model.coef_[0]
    lg_df = lg_df._append(
        {
            "oadr_u2": i,
            "r_sq": r_sq,
            "intercept": intercept,
            "slope": slope,
            "p_val": test_result.pvalue,
        },
        ignore_index=True,
    )
lg_df.sort_values(by=["slope"])

df_complete = df[df["kstn_miete_kalt_pqm"].notna()]
df_complete["startdate"] = pd.to_datetime(df_complete["startdate"])
df_complete["startdate_ordinal"] = df_complete["startdate"].map(dt.datetime.toordinal)
df_complete = df_complete.sort_values(by=["startdate_ordinal"])
x = df_complete["startdate_ordinal"]
y = df_complete["kstn_miete_kalt_pqm"]
model = linregress(x=x, y=y)
tue_slope = model.slope
tue_intercept = model.intercept

# Assuming 'df_w_loc_interesting_copy', 'lg_df', and 'df_complete' are predefined DataFrames
selected_regions = ["Feuerhägle/Mühlenviertel", "Au/Unterer Wert/Französiches Viertel"]

# Creating the plot
fig, ax = plt.subplots()
scatter_plots = []  # To store scatter plot handles for the legend

for region in selected_regions:
    # Filter data for the selected region
    region_data = df_w_loc_interesting_copy[
        df_w_loc_interesting_copy["oadr_u2"] == region
    ]

    # Creating scatter plot for the selected region
    scatter = ax.scatter(
        region_data["startdate_ordinal"],
        region_data["kstn_miete_kalt_pqm"],
        label=region,
        marker=".",
        alpha=0.5,
        vmin=date(2012, 1, 1).toordinal(),
        vmax=date(2023, 12, 31).toordinal(),
    )
    scatter_plots.append(scatter)

    # Calculating and plotting the regression line for each region
    slope = lg_df.loc[lg_df["oadr_u2"] == region, "slope"].values[0]
    intercept = lg_df.loc[lg_df["oadr_u2"] == region, "intercept"].values[0]
    x = np.array(
        [region_data["startdate_ordinal"].min(), region_data["startdate_ordinal"].max()]
    )
    y = slope * x + intercept
    ax.plot(x, y)

# Adding the overall regression line for 'All data'

from tueplots.constants.color import palettes, rgb

x_tue = np.array(
    [df_complete["startdate_ordinal"].min(), df_complete["startdate_ordinal"].max()]
)
y_tue = tue_slope * x_tue + tue_intercept
(line_all_data,) = ax.plot(x_tue, y_tue, color=rgb.tue_gold, label="Tübingen")

# Formatting the plot
ax.set_title("Scatter Plot And Regression For Selected Regions")
ax.set_ylabel("Cold Rent Per m² in €")
plt.xlim(date(2012, 1, 1).toordinal(), date(2023, 12, 31).toordinal())
new_labels = [date.fromordinal(int(item)) for item in ax.get_xticks()]
ax.set_xticklabels(new_labels, rotation=25)  # rotation = 45
# Creating custom legend for scatter plots and the 'All data' regression line
scatter_plots.append(line_all_data)
ax.legend(handles=scatter_plots, labels=selected_regions + ["Tübingen"])
plt.grid()
# plt.tight_layout()
# plt.show()
plt.savefig("linreg.pdf")
