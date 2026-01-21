import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("output.csv")

# -----------------------------
# Theme configuration
# -----------------------------
BACKGROUND_COLOR = "#0b1116"
BAR_COLOR = "#5ea8ff"
TEXT_COLOR = "#e6eef8"
AXES_COLOR = "#9fb0c9"
'''
BACKGROUND_COLOR = "#ffffff"
BAR_COLOR = "#0b6df2"
TEXT_COLOR = "#0b1720"
AXES_COLOR = "#536070"
'''
'''
BACKGROUND_COLOR = "#000000"
BAR_COLOR = "#ffff00"
TEXT_COLOR = "#ffffff"
AXES_COLOR = "#ffffff"
'''

plt.rcParams.update({
    "figure.facecolor": BACKGROUND_COLOR,
    "axes.facecolor": BACKGROUND_COLOR,
    "axes.edgecolor": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR
})

# -----------------------------
# Helper function for barh plots
# -----------------------------
def barh_chart(series, title, xlabel, ylabel, yTickSize=10):
    fig, ax = plt.subplots()
    series.plot(kind="barh", ax=ax, color=BAR_COLOR)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="y", labelsize=yTickSize)

    for spine in ax.spines.values():
        spine.set_color(AXES_COLOR)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.tight_layout()
    plt.show()


# -----------------------------
# 1. Age distribution
# -----------------------------
age_counts = (
    df["AgeRange"]
    .fillna("Unknown")
    .value_counts()
    .sort_index()
)

barh_chart(
    age_counts,
    "Age Distribution",
    "Count",
    "Age Range"
)


# -----------------------------
# 2. Pay Plan distribution
# -----------------------------
payplan_counts = (
    df["PayPlan"]
    .fillna("Unknown")
    .value_counts()
    .sort_values()
    .iloc[::-1]
)

barh_chart(
    payplan_counts,
    "Pay Plan Distribution",
    "Count",
    "Pay Plan",
    yTickSize=6
)


# -----------------------------
# 3. Service Range distribution
# -----------------------------
service_range_order = [
    "UNSP", "< 1", "1-2",
    "3-4", "5-9", "10-14",
    "15-19", "20-24", "25-29",
    "30-34"
]

service_counts = (
    df["ServiceRange"]
    .fillna("Unknown")
    .value_counts()
    .reindex(service_range_order)
    .dropna()
)

barh_chart(
    service_counts,
    "Service Range Distribution",
    "Count",
    "Service Range"
)


# -----------------------------
# 4. Component distribution (PIE CHART)
# -----------------------------
component_counts = (
    df["Component"]
    .fillna("Unknown")
    .value_counts()
)

def autopct_if_large(pct):
    return f"{pct:.1f}%" if pct >= 1 else ""

fig, ax = plt.subplots()
ax.pie(
    component_counts,
    labels=[
        label if pct >= 1 else ""
        for label, pct in zip(
            component_counts.index,
            component_counts / component_counts.sum() * 100
        )
    ],
    autopct=autopct_if_large,
    startangle=90,
    textprops={"color": TEXT_COLOR}
)

ax.set_title("Component Distribution")
ax.axis("equal")
fig.patch.set_facecolor(BACKGROUND_COLOR)

plt.tight_layout()
plt.show()
