import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_object_dtype
from tueplots import bundles, cycler
from tueplots.constants.color import palettes

# Increase the resolution of all the plots below
plt.rcParams.update({"figure.dpi": 150})

plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=True))
plt.rcParams.update(
    cycler.cycler(color=palettes.tue_plot)  # marker=marker_constants.o_sized,
)

df = pd.read_csv(
    "../data/testlizenz-tuebingen-dataliteracy4students_rt_stuttgart/testlizenz-tuebingen-dataliteracy4students_1706088512814.csv",
    sep=";",
    encoding="unicode_escape",
    header=0,
)
df_copy = df.copy()
for column in df.columns:
    if is_object_dtype(df[column]):
        if df[column].str.contains(",").any():
            df[column] = df[column].str.replace(",", ".").astype(float)
            df_copy[column] = df_copy[column].str.replace(",", ".").astype(float)

df_copy["endyear"] = pd.to_datetime(df_copy["enddate"]).dt.year
df_var = (
    df_copy.groupby(["oadr_ort", "endyear"])
    .agg(
        mean_pqm=("kstn_miete_kalt_pqm", "mean"),
        # median_pqm=("kstn_miete_kalt_pqm", "median"),
    )
    .reset_index()
)
df_var = df_var.sort_values(by=["oadr_ort", "endyear"], ascending=True)

# Assuming df_var is your DataFrame
# Get unique values for 'oadr_ort' for coloring and legend
# unique_oadr_ort = df_var["oadr_ort"].unique()
# colors = plt.cm.viridis(np.linspace(0, 1, len(unique_oadr_ort)))
# oadr_ort_color = dict(zip(unique_oadr_ort, colors))

# Plotting each group
for oadr_ort, group_data in df_var.groupby("oadr_ort"):
    plt.plot(
        group_data["endyear"],
        group_data["mean_pqm"],
        marker="o",
        markersize=3,
        # linewidth=1,
        label=oadr_ort,
        # color=oadr_ort_color[oadr_ort],
    )

    # Annotating each data point
    # for _, row in group_data.iterrows():
    #     if not pd.isna(row['percental_increase']):
    #         percent_text = f"{row['percental_increase'] * 100:.2f}%"
    #         x_offset = 0.1
    #         y_offset = 0.2
    #         if oadr_ort == "Stuttgart":
    #             y_offset = .5
    #         elif oadr_ort == "Tübingen":
    #             y_offset = -.3
    #         elif oadr_ort == "Reutlingen":
    #             y_offset = -.3

    #         plt.text(row['startyear'] + x_offset, row['kstn_miete_kalt_pqm'] + y_offset, percent_text,
    #                  horizontalalignment='left', color='black')

# Enhancing the plot
plt.title("Mean Rent per Square Meter Over Time")
plt.xlabel("Year")
plt.ylabel("Mean Rent per Square Meter")

# plt.xticks(rotation=45)
plt.xlim(2012, 2023)
plt.legend(loc="lower right", ncol=1)  # title = 'city'
plt.grid(True)

# Show the plot
plt.savefig("rt_s_tue.pdf")
