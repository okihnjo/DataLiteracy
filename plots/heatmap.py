import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from pandas.api.types import is_object_dtype
from tueplots import bundles

pd.set_option("display.max_columns", None)


df = pd.read_csv(
    "../data/testlizenz-tuebingen-dataliteracy4students_1706200535571/testlizenz-tuebingen-dataliteracy4students_1706200535571.csv",
    sep=";",
    encoding="unicode_escape",
)
df["year"] = pd.to_datetime(df["startdate"]).dt.year
df["month"] = pd.to_datetime(df["startdate"]).dt.month

# Cleaning process
df_total_oadr_u1 = df.groupby(["oadr_u1"]).size().reset_index(name="count")
df_total_oadr_u1_count = df["oadr_u1"].isnull().sum()
print(f"Total number of OADR_U1: {df_total_oadr_u1['count'].sum()}")
print(f"Total number of OADR_U1 with no value: {df_total_oadr_u1_count}")
df.groupby(["oadr_u1"]).size().reset_index(name="count")

df_total_oadr_u2 = df.groupby(["oadr_u2"]).size().reset_index(name="count")
df_total_oadr_u2_count = df["oadr_u2"].isnull().sum()
print(f"Total number of OADR_U2: {df_total_oadr_u2['count'].sum()}")
print(f"Total number of OADR_U2 with no value: {df_total_oadr_u2_count}")
df.groupby(["oadr_u2"]).size().reset_index(name="count")

df_w_loc = df[df["oadr_u1"].notna()]
df_wo_loc = df[df["oadr_u1"].isna()]
print(f"Total number of rows with location: {df_w_loc.shape[0]}")
print(f"Total number of rows without location: {df_wo_loc.shape[0]}")

for column in df.columns:
    if is_object_dtype(df[column]):
        if df[column].str.contains(",").any():
            df[column] = df[column].str.replace(",", ".").astype(float)
            df_w_loc[column] = df_w_loc[column].str.replace(",", ".").astype(float)

path_tue_shp = "../data/KLGL_Stadtteile_Shape/KLGL_Stadtteile_Shape.shp"
tuebingen_gdf = gpd.read_file(path_tue_shp)
# df_kauf = (
#     df_w_loc[df_w_loc["nachfrageart"] == "kauf"]
#     .groupby(["oadr_u2"])
#     .size()
#     .reset_index(name="count_kauf")
# )
df_miete = (
    df_w_loc[df_w_loc["nachfrageart"] == "miete"]
    .groupby(["oadr_u2"])
    .size()
    .reset_index(name="count_miete")
)

# https://www.tuebingen.de/Dateien/einwohner_stadtteile_Jahresvergleich.pdf
data = {
    "region": [
        "Zentrum",
        "Universität",
        "Wanne",
        "Schönblick/Waldhäuser Ost",
        "Österberg/Gartenstraße",
        "Au/Unterer Wert/Französiches Viertel",
        "Südstadt",
        "Weststadt",
        "Lustnau-Zentrum/Herrlesberg/Stäudach",
        "Denzenberg/Sand",
        "Neuhalde",
        "Aeule",
        "De-Zentrum",
        "Feuerhägle/Mühlenviertel",
        "Gartenstadt",
        "Bebenhausen",
        "Pfrondorf",
        "Weilheim",
        "Kilchberg",
        "Bühl",
        "Hirschau",
        "Unterjesingen",
        "Hagelloch",
        "Gesamt",
    ],
    "2016": [
        6430,
        8242,
        5384,
        9779,
        2509,
        3656,
        10459,
        8519,
        5908,
        2421,
        1261,
        985,
        1863,
        4484,
        494,
        343,
        3343,
        1498,
        1252,
        2114,
        3289,
        2580,
        1713,
        88526,
    ],
    "2017": [
        6503,
        8299,
        5370,
        9878,
        2580,
        3832,
        10484,
        8622,
        5950,
        2438,
        1287,
        988,
        1860,
        4857,
        496,
        328,
        3360,
        1468,
        1271,
        2125,
        3288,
        2624,
        1702,
        89610,
    ],
    "2018": [
        6479,
        8524,
        5359,
        9838,
        2580,
        4248,
        10518,
        8687,
        5957,
        2479,
        1318,
        995,
        1888,
        5191,
        473,
        338,
        3363,
        1445,
        1299,
        2145,
        3304,
        2627,
        1709,
        90764,
    ],
    "2019": [
        6516,
        8618,
        5528,
        9968,
        2632,
        4678,
        10618,
        8778,
        6037,
        2499,
        1315,
        984,
        1846,
        5110,
        473,
        326,
        3348,
        1467,
        1295,
        2172,
        3276,
        2640,
        1715,
        91839,
    ],
    "2020": [
        6371,
        8445,
        5469,
        9772,
        2685,
        4997,
        10519,
        8607,
        5910,
        2550,
        1320,
        977,
        1810,
        4806,
        463,
        333,
        3319,
        1446,
        1287,
        2154,
        3297,
        2627,
        1713,
        90877,
    ],
    "2021": [
        6501,
        8593,
        5541,
        9959,
        2708,
        5291,
        10578,
        8708,
        5930,
        2605,
        1300,
        958,
        1789,
        5061,
        457,
        336,
        3315,
        1443,
        1274,
        2171,
        3359,
        2566,
        1727,
        92170,
    ],
    "2022": [
        6540,
        8568,
        5665,
        10004,
        2707,
        5272,
        10616,
        8828,
        5952,
        2586,
        1287,
        1033,
        1780,
        5206,
        459,
        322,
        3348,
        1475,
        1266,
        2182,
        3384,
        2567,
        1753,
        92800,
    ],
}

# Erstellen des DataFrames
df_people = pd.DataFrame(data)
df_people = df_people.set_index("region")
# calculate mean from 2016 to 2022
mean_pop = df_people.mean(axis=1).round(0).astype(int)
# print(mean_pop)


shp_dict = {
    "Universität": 22,
    "Schönblick/Waldhäuser Ost": 9,
    "Zentrum": 20,
    "Bühl": 3,
    "Südstadt": 0,
    "Hagelloch": 10,
    "Kilchberg": 1,
    "Au/Unterer Wert/Französiches Viertel": 19,
    "Weststadt": 21,
    "Bebenhausen": 12,
    "Hirschau": 15,
    "Österberg/Gartenstraße": 4,
    "Pfrondorf": 17,
    "Wanne": 6,
    "Unterjesingen": 18,
    "Feuerhägle/Mühlenviertel": 7,
    "Lustnau-Zentrum/Herrlesberg/Stäudach": 11,
    "De-Zentrum": 2,
    "Aeule": 8,
    "Weilheim": 16,
    "Denzenberg/Sand": 5,
    "Gartenstadt": 13,
    "Neuhalde": 14,
}
sorted_dict = dict(sorted(shp_dict.items(), key=lambda item: item[1]))
tuebingen_gdf["region"] = sorted_dict.keys()
# tuebingen_gdf = tuebingen_gdf.join(df_kauf.set_index("oadr_u2"), on="region")
tuebingen_gdf = tuebingen_gdf.join(df_miete.set_index("oadr_u2"), on="region")
tuebingen_gdf = tuebingen_gdf.join(mean_pop.rename("population"), on="region")

# ratio
tuebingen_gdf["ratio"] = tuebingen_gdf["count_miete"] / tuebingen_gdf["population"]

# rent
from tueplots.constants.color import palettes, rgb

colors = [(1, 1, 1), rgb.tue_gold, rgb.tue_red]
cmap_white_yellow_red = LinearSegmentedColormap.from_list(
    "white_yellow_red", colors, N=256
)
cmap_white_silver_blue = LinearSegmentedColormap.from_list(
    "white_silver_blue", [(1,1,1), rgb.tue_gray, rgb.tue_blue], N=256
)

short_labels = {
    "Südstadt": "Süd",
    "Kilchberg": "Kil",
    "De-Zentrum": "DZ",
    "Bühl": "Bhl",
    "Österberg/Gartenstraße": "Ö",
    "Denzenberg/Sand": "S",
    "Wanne": "Wanne",
    "Feuerhägle/Mühlenviertel": "F",
    "Aeule": "a",
    "Schönblick/Waldhäuser Ost": "WHO",
    "Hagelloch": "Hgl",
    "Lustnau-Zentrum/Herrlesberg/Stäudach": "Lust",
    "Bebenhausen": "Bbh",
    "Gartenstadt": "Gst",
    "Neuhalde": "Neu",
    "Hirschau": "Hrsch",
    "Weilheim": "Wh",
    "Pfrondorf": "Pfr",
    "Unterjesingen": "Ujsg",
    "Au/Unterer Wert/Französiches Viertel": "FV",
    "Zentrum": "Z",
    "Weststadt": "Wstd",
    "Universität": "Uni",
}


plt.rcParams.update(bundles.icml2022(column="half", nrows=3))
plt.rcParams["axes.titlesize"] = 7
# Create a larger plot with a specified size
fig, axs = plt.subplots(2, 1)
from matplotlib.colors import LogNorm

# Plot the GeoDataFrame with a heatmap based on density values using the custom colormap
tuebingen_gdf.plot(
    ax=axs[0],
    cmap=cmap_white_yellow_red,
    edgecolor=rgb.tue_dark,
    column="count_miete",
    legend=True,
    norm=LogNorm(
        vmin=10,  # tuebingen_gdf["count_miete"].min(),
        vmax=tuebingen_gdf["count_miete"].max(),
    ),  # Set norm to LogNorm for logarithmic scale
)

# print("Min count_miete:", tuebingen_gdf[tuebingen_gdf["count_miete"] == tuebingen_gdf["count_miete"].min()])
# print("Max count_miete:", tuebingen_gdf[tuebingen_gdf["count_miete"] == tuebingen_gdf["count_miete"].max()])


# Plot the GeoDataFrame with a heatmap based on density values using the custom colormap
tuebingen_gdf.plot(
    ax=axs[1],
    cmap=cmap_white_silver_blue,
    edgecolor=rgb.tue_dark,
    column="ratio",
    legend=True,
    # norm=LogNorm(
    #     vmin=tuebingen_gdf["ratio"].min(), vmax=tuebingen_gdf["ratio"].max()
    # ),  # Set norm to LogNorm for logarithmic scale
)
# Add labels for each region
for idx, row in tuebingen_gdf.iterrows():
    short_label = short_labels.get(
        row["region"], row["region"]
    )  # Use the short label if available
    x, y = row["geometry"].centroid.coords[0]
    # negative y = south
    # negative x = west
    match row["region"]:
        case "Wanne":
            x, y = x - 100, y + 300
        case "Hagelloch":
            x, y = x, y - 700
        case "Neuhalde":
            x, y = x - 250, y - 1500
        case "Denzenberg/Sand":
            x, y = x, y - 300
        case "Universität":
            x, y = x + 300, y - 500
        case "Zentrum":
            x, y = x, y - 200
        case "Feuerhägle/Mühlenviertel":
            x, y = x - 100, y
        case "Schönblick/Waldhäuser Ost":
            x, y = x + 200, y
        case "Österberg/Gartenstraße":
            x, y = x, y - 100
        case "De-Zentrum":
            x, y = x - 300, y
        case "Au/Unterer Wert/Französiches Viertel":
            x, y = x + 150, y
        case "Lustnau-Zentrum/Herrlesberg/Stäudach":
            x, y = x - 100, y
        case "Aeule":
            x, y = x + 70, y - 75
        case "Gartenstadt":
            x, y = x - 100, y
        case _:
            x, y = x, y
    axs[0].annotate(short_label, xy=(x, y), ha="center", color="black", fontsize=7)
    axs[1].annotate(short_label, xy=(x, y), ha="center", color="black", fontsize=7)


# Add labels and legend
axs[0].set_title("Rental Offers From 2012/01 To 2023/12")
axs[1].set_title("Rental Offers Per Inhabitant From 2012/01 To 2023/12")

# Hide X and Y axes label marks
# axs.xaxis.set_tick_params(labelbottom=False)
# axs.yaxis.set_tick_params(labelleft=False)

# # Hide X and Y axes tick marks
# axs.set_xticks([])
# axs.set_yticks([])
axs[0].set_axis_off()
axs[1].set_axis_off()

# Now we will create the legend for the short labels manually.
# We create a list of patches for the legend
import matplotlib.patches as mpatches

legend_patches = [
    mpatches.Patch(color="grey", label=f"{short}: {region}")
    for region, short in short_labels.items()
]


# Add the building marker to your list of legend patches

# plt.legend(
#     handles=legend_patches
# )  # , bbox_to_anchor=(1.45, 1), loc=2, borderaxespad=0.0)


# Show the plot
plt.savefig("heatmap_miete.pdf")
