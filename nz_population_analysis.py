"""
New Zealand Population Trend Analysis
Data Source: Stats NZ (https://www.stats.govt.nz)
Author: Jina Lee
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── 1. Data ──────────────────────────────────────────────────────────────────
# Source: Stats NZ estimated resident population (annual, June year)
data = {
    "Year": list(range(2000, 2024)),
    "Total_Population": [
        3857600, 3880500, 3939900, 4009200, 4061100,
        4098100, 4140300, 4180900, 4228700, 4266900,
        4320500, 4384800, 4433000, 4477800, 4509700,
        4528600, 4574200, 4692700, 4885500, 4917000,
        5084300, 5123800, 5099900, 5123400
    ],
    "Auckland_Population": [
        1169600, 1187300, 1212500, 1243700, 1273800,
        1299600, 1326800, 1354500, 1385700, 1413100,
        1454800, 1495700, 1534600, 1571100, 1600300,
        1614100, 1638400, 1693200, 1756400, 1766900,
        1841300, 1868300, 1844900, 1858800
    ]
}

df = pd.DataFrame(data)
df["Other_NZ"] = df["Total_Population"] - df["Auckland_Population"]
df["Auckland_Share_pct"] = (df["Auckland_Population"] / df["Total_Population"] * 100).round(1)
df["YoY_Growth"] = df["Total_Population"].pct_change() * 100

# ── 2. Plot ───────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("New Zealand Population Trend Analysis (2000–2023)",
             fontsize=16, fontweight="bold", y=1.01)

BLUE   = "#2E75B6"
ORANGE = "#ED7D31"
GREEN  = "#70AD47"

# ── Chart 1: Total population ─────────────────────────────────────────────
ax1 = axes[0, 0]
ax1.plot(df["Year"], df["Total_Population"] / 1e6,
         color=BLUE, linewidth=2.5, marker="o", markersize=4)
ax1.fill_between(df["Year"], df["Total_Population"] / 1e6,
                 alpha=0.15, color=BLUE)
ax1.set_title("Total Population", fontweight="bold")
ax1.set_ylabel("Population (millions)")
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1fM"))
ax1.set_xlim(2000, 2023)

# ── Chart 2: Auckland vs Rest of NZ ──────────────────────────────────────
ax2 = axes[0, 1]
ax2.stackplot(df["Year"],
              df["Auckland_Population"] / 1e6,
              df["Other_NZ"] / 1e6,
              labels=["Auckland", "Rest of NZ"],
              colors=[BLUE, ORANGE], alpha=0.8)
ax2.set_title("Auckland vs Rest of New Zealand", fontweight="bold")
ax2.set_ylabel("Population (millions)")
ax2.legend(loc="upper left", fontsize=9)
ax2.set_xlim(2000, 2023)

# ── Chart 3: Auckland share % ─────────────────────────────────────────────
ax3 = axes[1, 0]
ax3.bar(df["Year"], df["Auckland_Share_pct"],
        color=BLUE, alpha=0.75, edgecolor="white")
ax3.axhline(df["Auckland_Share_pct"].mean(), color=ORANGE,
            linestyle="--", linewidth=1.5, label=f"Average: {df['Auckland_Share_pct'].mean():.1f}%")
ax3.set_title("Auckland's Share of NZ Population (%)", fontweight="bold")
ax3.set_ylabel("Share (%)")
ax3.set_ylim(30, 40)
ax3.legend(fontsize=9)
ax3.set_xlim(1999, 2024)

# ── Chart 4: Year-on-year growth rate ────────────────────────────────────
ax4 = axes[1, 1]
colors = [GREEN if v >= 0 else "#FF6B6B" for v in df["YoY_Growth"].fillna(0)]
ax4.bar(df["Year"], df["YoY_Growth"].fillna(0),
        color=colors, alpha=0.8, edgecolor="white")
ax4.axhline(0, color="black", linewidth=0.8)
ax4.set_title("Year-on-Year Population Growth Rate (%)", fontweight="bold")
ax4.set_ylabel("Growth Rate (%)")
ax4.set_xlim(1999, 2024)

# Annotate COVID dip
ax4.annotate("COVID-19\nborder closure",
             xy=(2021, df.loc[df["Year"] == 2021, "YoY_Growth"].values[0]),
             xytext=(2018, -0.8),
             arrowprops=dict(arrowstyle="->", color="gray"),
             fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("nz_population_analysis.png", dpi=150, bbox_inches="tight")
print("Chart saved successfully!")

# ── 3. Key insights ───────────────────────────────────────────────────────
print("\n📊 Key Insights:")
print(f"  • 2000–2023 total growth: {((df['Total_Population'].iloc[-1] / df['Total_Population'].iloc[0]) - 1) * 100:.1f}%")
print(f"  • Peak growth year: {df.loc[df['YoY_Growth'].idxmax(), 'Year']} "
      f"({df['YoY_Growth'].max():.2f}%)")
print(f"  • Auckland share range: {df['Auckland_Share_pct'].min()}% – {df['Auckland_Share_pct'].max()}%")
print(f"  • Population decline year: {df.loc[df['YoY_Growth'] < 0, 'Year'].values} (COVID impact)")
