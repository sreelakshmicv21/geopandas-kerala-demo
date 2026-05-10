import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl

# # --- Global settings to remove scientific notation ---
mpl.rcParams['axes.formatter.useoffset'] = False
mpl.rcParams['axes.formatter.use_mathtext'] = False

# Read shapefiles (use raw string for Windows paths)
road = gpd.read_file(r"..\Data\kerala_highway\kerala_highway.shp")
district = gpd.read_file(r"..\Data\district\district.shp")

# # Inspect data
print("Roads CRS:", road.crs)
print("Districts CRS:", district.crs)
print("Roads head:\n", road.head(5))
print("Districts head:\n", district.head(5))

# # Reproject to projected CRS (UTM zone for Kerala ~ EPSG:32643)
road_proj = road.to_crs(epsg=32643)
district_proj = district.to_crs(epsg=32643)

# --- Plot roads ---
road_proj.plot(color="red", figsize=(10,6))
plt.title("Kerala Roads")
plt.ticklabel_format(style="plain")
plt.savefig("road_plot.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Buffer roads (4000 m) ---
buffered = road_proj.buffer(4000)
ax = road_proj.plot(color="blue", linewidth=0.5, figsize=(10,6))
buffered.plot(ax=ax, color="red", alpha=0.5)
plt.title("Buffered Roads (4000 m)")
plt.ticklabel_format(style="plain")
plt.savefig("buffer_plot.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Spatial Join (tag roads with districts) ---
joined = gpd.sjoin(road_proj, district_proj, how="left")
joined = joined.drop(columns=["index_right"])
ax = joined.plot(column="DISTRICT", legend=True, figsize=(10,6))
plt.title("Roads by District")
plt.ticklabel_format(style="plain")
plt.savefig("spatial_join.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Filter Kozhikode district ---
kozhikode = district_proj[district_proj["DISTRICT"] == "Kozhikode"]
kozhikode.plot(edgecolor="black", facecolor="lightblue", figsize=(10,6))
plt.title("Kozhikode District Boundary")
plt.ticklabel_format(style="plain")
plt.savefig("kozhikode_boundary.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Roads clipped to Kozhikode ---
inter = gpd.overlay(road_proj, kozhikode, how="intersection")
inter.plot(color="green", figsize=(10,6))
plt.title("Roads inside Kozhikode")
plt.ticklabel_format(style="plain")
plt.savefig("intersection.png", dpi=300, bbox_inches="tight")
plt.show()

# --- Dissolve (merge districts by state name) ---
dissolved = district_proj.dissolve(by="ST_NM", as_index=False)
dissolved.plot(edgecolor="black", facecolor="lightgrey", figsize=(10,6))
plt.title("Kerala State Boundary (Dissolved)")
plt.ticklabel_format(style="plain")
plt.savefig("dissolve.png", dpi=300, bbox_inches="tight")
plt.show()

