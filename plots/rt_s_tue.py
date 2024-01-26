import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tueplots import bundles, cycler, markers
from tueplots.constants import markers as marker_constants
from tueplots.constants.color import palettes

# Increase the resolution of all the plots below
plt.rcParams.update({"figure.dpi": 150})

plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=True))
plt.rcParams.update(
    cycler.cycler(color=palettes.tue_plot)  # marker=marker_constants.o_sized,
)

df_var = pd.read_csv("../data/df_var.csv", sep=",", header=0)


# Assuming df_var is your DataFrame
# Get unique values for 'oadr_ort' for coloring and legend
# unique_oadr_ort = df_var["oadr_ort"].unique()
# colors = plt.cm.viridis(np.linspace(0, 1, len(unique_oadr_ort)))
# oadr_ort_color = dict(zip(unique_oadr_ort, colors))

# Plotting each group
for oadr_ort, group_data in df_var.groupby("oadr_ort"):
    plt.plot(
        group_data["startyear"],
        group_data["kstn_miete_kalt_pqm"],
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
plt.xlabel("Year-Month")
plt.ylabel("Mean Rent per Square Meter")

# plt.xticks(rotation=45)
plt.xlim(2012, 2023)
plt.legend(loc="lower right", ncol=1)  # title = 'city'
plt.grid(True)

# Show the plot
plt.savefig("rt_s_tue.pdf")
