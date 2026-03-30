#!/usr/bin/env python3
"""
Generate charts and CSV exports for the MacBook local-LLM economics article.
Reads/writes data under repo root: data/, public/assets/economics-of-local-llms/
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
OUT_DIR = REPO_ROOT / "public" / "assets" / "economics-of-local-llms"

# Unified blue-forward publication palette (matches MMLU scatter aesthetic site-wide).
CHART_COLORS = {
    # Default seaborn categorical: blues first, one vermillion accent for contrast series.
    "categorical": [
        "#0072B2",
        "#2563eb",
        "#60a5fa",
        "#93c5fd",
        "#0ea5e9",
        "#D55E00",
        "#64748b",
        "#000000",
    ],
    "neutral": {
        "text": "#0f172a",
        "text_muted": "#475569",
        "text_dim": "#64748b",
        "edge": "#d0d0d0",
    },
    "positive": "#0072B2",
    "fit_no": "#f1f5f9",
    # Bandwidth heatmap: light → dark blue (same semantic as “faster = deeper blue”).
    "zone_slow": "#eff6ff",
    "zone_mid": "#93c5fd",
    "zone_fast": "#1d4ed8",
    "secondary_series": "#D55E00",
    "zero_line": "#b91c1c",
    "year_blues": ["#dbeafe", "#bfdbfe", "#93c5fd", "#3b82f6", "#1e40af"],
    "palettes": {
        "tier_traj": ["#0072B2", "#0369a1", "#0ea5e9", "#64748b"],
        "threshold_lines": ["#93c5fd", "#60a5fa", "#2563eb", "#1e3a8a"],
        "subscription_bars": ["#bfdbfe", "#93c5fd", "#60a5fa", "#2563eb"],
        "price_tier_lines": ["#bae6fd", "#7dd3fc", "#38bdf8", "#0284c7", "#0c4a6e"],
        "scenario_hues": ["#93c5fd", "#3b82f6", "#1e3a8a"],
        "air_pro": {"Air": "#60a5fa", "Pro": "#1e40af"},
        "headroom_pair": ["#0072B2", "#38bdf8"],
    },
}


def save_fig(fig: plt.Figure, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.svg"
    fig.savefig(path, format="svg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {path.relative_to(REPO_ROOT)}", file=sys.stderr)


def main() -> None:
    C = CHART_COLORS
    NN = C["neutral"]
    cat = C["categorical"]
    palettes = C["palettes"]

    sns.set_theme(
        style="whitegrid",
        palette=cat[:6],
        font_scale=1.05,
        rc={
            "figure.figsize": (12, 6),
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 12,
        },
    )

    # -----------------------------
    # Publication-facing knobs
    # -----------------------------
    OS_RESERVE_GIB = 3.5
    LIGHT_DEV_EXTRA_GIB = 2.5
    HEAVY_DEV_EXTRA_GIB = 6.5
    RUNTIME_MARGIN_GIB = 2.5

    hardware = pd.DataFrame(
        [
            {
                "machine": "MacBook Air M5",
                "tier": "Air",
                "memory_gib": 16,
                "bandwidth_gbps": 153,
                "price_aud": 1799,
                "price_basis": "Apple AU MacBook Air: from A$1,799",
                "source_url": "https://www.apple.com/au/macbook-air/",
            },
            {
                "machine": "MacBook Air M5",
                "tier": "Air",
                "memory_gib": 24,
                "bandwidth_gbps": 153,
                "price_aud": 2099,
                "price_basis": "Apple AU +A$300 memory upgrade from 16GB to 24GB",
                "source_url": "https://www.apple.com/au/macbook-air/",
            },
            {
                "machine": "MacBook Air M5",
                "tier": "Air",
                "memory_gib": 32,
                "bandwidth_gbps": 153,
                "price_aud": 2399,
                "price_basis": "Apple AU +A$600 memory upgrade from 16GB to 32GB",
                "source_url": "https://www.apple.com/au/macbook-air/",
            },
            {
                "machine": "MacBook Pro 14 M5",
                "tier": "Pro",
                "memory_gib": 16,
                "bandwidth_gbps": 153,
                "price_aud": 2699,
                "price_basis": "Apple AU MacBook Pro 14-inch: from A$2,699",
                "source_url": "https://www.apple.com/au/macbook-pro/",
            },
            {
                "machine": "MacBook Pro 14 M5",
                "tier": "Pro",
                "memory_gib": 24,
                "bandwidth_gbps": 153,
                "price_aud": 3252,
                "price_basis": (
                    "Apple US 14-inch M5 with 24GB unified memory: USD 2,049 list "
                    "(apple.com, Mar 2026); AUD placeholder; price_usd set to 2049 below"
                ),
                "source_url": "https://www.apple.com/shop/buy-mac/macbook-pro/14-inch-m5",
            },
            {
                "machine": "MacBook Pro 16 M5 Pro",
                "tier": "Pro",
                "memory_gib": 24,
                "bandwidth_gbps": 307,
                "price_aud": 4299,
                "price_basis": "Apple AU 16-inch with M5 Pro: from A$4,299",
                "source_url": "https://www.apple.com/au/macbook-pro/",
            },
            {
                "machine": "MacBook Pro 16 M5 Pro",
                "tier": "Pro",
                "memory_gib": 48,
                "bandwidth_gbps": 307,
                "price_aud": 4899,
                "price_basis": "Apple AU observed 48GB M5 Pro config at A$4,899",
                "source_url": "https://www.apple.com/au/macbook-pro/",
            },
            {
                "machine": "MacBook Pro 16 M5 Pro",
                "tier": "Pro",
                "memory_gib": 64,
                "bandwidth_gbps": 307,
                "price_aud": 5199,
                "price_basis": "Apple AU observed +A$300 from 48GB to 64GB on M5 Pro config",
                "source_url": "https://www.apple.com/au/macbook-pro/",
            },
        ]
    )

    models = pd.DataFrame(
        [
            {
                "model": "Qwen 2.5 7B",
                "family": "general",
                "params_b": 7,
                "quant": "q4_K_M",
                "artifact_gib": 4.7,
                "context_k": 32,
                "source_url": "https://ollama.com/library/qwen2.5/tags",
            },
            {
                "model": "Qwen 2.5 14B",
                "family": "general",
                "params_b": 14,
                "quant": "q4_K_M",
                "artifact_gib": 9.0,
                "context_k": 32,
                "source_url": "https://ollama.com/library/qwen2.5/tags",
            },
            {
                "model": "Gemma 3 12B",
                "family": "multimodal",
                "params_b": 12,
                "quant": "q4_K_M",
                "artifact_gib": 8.1,
                "context_k": 128,
                "source_url": "https://ollama.com/library/gemma3/tags",
            },
            {
                "model": "Gemma 3 27B",
                "family": "multimodal",
                "params_b": 27,
                "quant": "q4_K_M",
                "artifact_gib": 17.0,
                "context_k": 128,
                "source_url": "https://ollama.com/library/gemma3/tags",
            },
            {
                "model": "Qwen 2.5 32B",
                "family": "general",
                "params_b": 32,
                "quant": "q4_K_M",
                "artifact_gib": 20.0,
                "context_k": 32,
                "source_url": "https://ollama.com/library/qwen2.5/tags",
            },
            {
                "model": "Qwen 2.5 Coder 14B",
                "family": "code",
                "params_b": 14,
                "quant": "q4_K_M",
                "artifact_gib": 8.6,
                "context_k": 32,
                "source_url": "https://ollama.com/library/qwen2.5-coder/tags",
            },
            {
                "model": "Qwen 2.5 Coder 32B",
                "family": "code",
                "params_b": 32,
                "quant": "q4_K_M",
                "artifact_gib": 20.0,
                "context_k": 32,
                "source_url": "https://ollama.com/library/qwen2.5-coder/tags",
            },
            {
                "model": "Llama 3.1 70B",
                "family": "general",
                "params_b": 70,
                "quant": "q4_K_M",
                "artifact_gib": 43.0,
                "context_k": 128,
                "source_url": "https://ollama.com/library/llama3.1/tags",
            },
        ]
    )

    APPLE_LLM_TEST_NOTE = (
        "Apple says MacBook Air M5 was tested with an 8K-token prompt using a 14B "
        "parameter model with 4-bit quantisation in LM Studio."
    )

    AUD_TO_USD = 0.63
    hardware["price_usd"] = (hardware["price_aud"] * AUD_TO_USD).round(-1).astype(int)
    _mask = (hardware["machine"] == "MacBook Pro 14 M5") & (hardware["memory_gib"] == 24)
    hardware.loc[_mask, "price_usd"] = 2049

    print(APPLE_LLM_TEST_NOTE, file=sys.stderr)

    scenario_total_reserves = {
        "idle_only": OS_RESERVE_GIB,
        "light_dev": OS_RESERVE_GIB + LIGHT_DEV_EXTRA_GIB,
        "heavy_dev": OS_RESERVE_GIB + HEAVY_DEV_EXTRA_GIB,
    }

    def usable_memory(memory_gib: float, reserve_gib: float) -> float:
        return max(memory_gib - reserve_gib, 0)

    def required_memory(
        model_artifact_gib: float, runtime_margin_gib: float = RUNTIME_MARGIN_GIB
    ) -> float:
        return model_artifact_gib + runtime_margin_gib

    def fit_table(hardware_df: pd.DataFrame, models_df: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for _, hw in hardware_df.iterrows():
            for scenario_name, reserve in scenario_total_reserves.items():
                usable = usable_memory(hw["memory_gib"], reserve)
                for _, model in models_df.iterrows():
                    req = required_memory(model["artifact_gib"])
                    rows.append(
                        {
                            "machine": hw["machine"],
                            "memory_gib": hw["memory_gib"],
                            "bandwidth_gbps": hw["bandwidth_gbps"],
                            "price_usd": hw["price_usd"],
                            "scenario": scenario_name,
                            "usable_memory_gib": usable,
                            "model": model["model"],
                            "params_b": model["params_b"],
                            "quant": model["quant"],
                            "artifact_gib": model["artifact_gib"],
                            "required_gib": req,
                            "fits": usable >= req,
                        }
                    )
        return pd.DataFrame(rows)

    fit_df = fit_table(hardware, models)

    frontier = (
        fit_df[fit_df["fits"]]
        .sort_values(["price_usd", "memory_gib", "params_b"])
        .groupby(["machine", "memory_gib", "price_usd", "bandwidth_gbps", "scenario"], as_index=False)
        .tail(1)
        .sort_values(["price_usd", "memory_gib", "scenario"])
    )

    scenario_order = ["idle_only", "light_dev", "heavy_dev"]
    scenario_labels = {
        "idle_only": "Idle only",
        "light_dev": "Light dev",
        "heavy_dev": "Heavy dev",
    }

    # Plot 1: Priced MacBook tiers vs total unified memory
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=hardware,
        x="price_usd",
        y="memory_gib",
        size="bandwidth_gbps",
        hue="tier",
        palette=palettes["air_pro"],
        hue_order=["Air", "Pro"],
        sizes=(120, 600),
        alpha=0.85,
        edgecolor="white",
        linewidth=1.2,
        ax=ax,
    )
    for _, row in hardware.iterrows():
        label = f'{row["machine"]}\n{row["memory_gib"]} GB · {row["bandwidth_gbps"]} GB/s'
        ax.annotate(
            label,
            (row["price_usd"], row["memory_gib"]),
            xytext=(10, 8),
            textcoords="offset points",
            fontsize=9,
            fontstyle="italic",
        )
    ax.set_title(
        "Current MacBook tiers: price vs unified memory\n"
        "(marker size scales with memory bandwidth)"
    )
    ax.set_xlabel("Price (US$)")
    ax.set_ylabel("Unified memory (GiB)")
    ax.legend(title="Tier / bandwidth", loc="upper left", framealpha=0.95)
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "price_scatter")

    # Plot 2: Usable memory after workflow reserves
    usable_rows = []
    for _, hw in hardware.iterrows():
        label = f'{hw["machine"]}\n{hw["memory_gib"]} GB'
        for sc in scenario_order:
            usable_rows.append(
                {
                    "machine": label,
                    "scenario": scenario_labels[sc],
                    "usable_gib": usable_memory(hw["memory_gib"], scenario_total_reserves[sc]),
                }
            )
    usable_long = pd.DataFrame(usable_rows)

    fig, ax = plt.subplots()
    sns.barplot(
        data=usable_long,
        x="machine",
        y="usable_gib",
        hue="scenario",
        hue_order=["Idle only", "Light dev", "Heavy dev"],
        palette=palettes["scenario_hues"],
        ax=ax,
    )
    ax.set_title("Usable unified memory left for the model\n(after configurable workflow reserves)")
    ax.set_ylabel("Usable memory for model + runtime (GiB)")
    ax.set_xlabel("")
    ax.legend(title="Workflow scenario", framealpha=0.95)
    for label in ax.get_xticklabels():
        label.set_rotation(35)
        label.set_ha("right")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "usable_memory_bar")

    # Plot 3: Heatmaps
    FIT_YES = C["positive"]
    FIT_NO = C["fit_no"]
    fit_cmap = ListedColormap([FIT_NO, FIT_YES])

    def build_heatmap(scenario_name: str) -> pd.DataFrame:
        subset = fit_df[fit_df["scenario"] == scenario_name].copy()
        subset["machine_label"] = subset["machine"] + "\n" + subset["memory_gib"].astype(str) + " GB"
        order_hw = hardware.sort_values(["price_usd", "memory_gib"])
        hw_labels = (order_hw["machine"] + "\n" + order_hw["memory_gib"].astype(str) + " GB").tolist()
        model_order = models.sort_values(["params_b", "artifact_gib"])
        model_labels = model_order["model"].tolist()
        pivot = (
            subset.pivot_table(
                index="model", columns="machine_label", values="fits", aggfunc="max", fill_value=False
            )
            .reindex(index=model_labels, columns=hw_labels)
            .astype(int)
        )
        return pivot

    fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True, sharey=True, layout="constrained")
    fig.get_layout_engine().set(hspace=0.08)
    for idx, sc in enumerate(scenario_order):
        ax = axes[idx]
        heat = build_heatmap(sc)
        sns.heatmap(
            heat,
            annot=False,
            cmap=fit_cmap,
            linewidths=2.5,
            linecolor="white",
            cbar=False,
            vmin=0,
            vmax=1,
            ax=ax,
        )
        ax.set_ylabel(scenario_labels[sc], fontsize=13, fontweight="bold", labelpad=14)
        ax.set_xlabel("")
        ax.tick_params(left=False, bottom=False, labelsize=10)
    axes[-1].tick_params(axis="x", rotation=0, labelsize=9.5)
    legend_patches = [
        mpatches.Patch(facecolor=FIT_YES, edgecolor="white", linewidth=1.5, label="Model fits"),
        mpatches.Patch(facecolor=FIT_NO, edgecolor=NN["edge"], linewidth=1.5, label="Does not fit"),
    ]
    fig.legend(handles=legend_patches, loc="outside lower center", ncol=2, fontsize=11, frameon=False)
    fig.suptitle("Which models fit on which MacBooks?", fontsize=16, fontweight="bold")
    save_fig(fig, "model_fit_heatmap")

    # Plot 4: Frontier
    frontier_plot = frontier.copy()
    frontier_plot["scenario_label"] = frontier_plot["scenario"].map(scenario_labels)

    fig, ax = plt.subplots()
    sns.lineplot(
        data=frontier_plot,
        x="price_usd",
        y="params_b",
        hue="scenario_label",
        style="scenario_label",
        hue_order=["Idle only", "Light dev", "Heavy dev"],
        palette=palettes["scenario_hues"],
        markers=True,
        dashes=False,
        markersize=10,
        linewidth=2.2,
        ax=ax,
    )
    for _, row in frontier_plot.iterrows():
        ax.annotate(
            f'{int(row["params_b"])}B · {int(row["memory_gib"])} GB',
            (row["price_usd"], row["params_b"]),
            xytext=(6, 8),
            textcoords="offset points",
            fontsize=8,
            fontstyle="italic",
        )
    ax.set_title(
        "Price vs largest representative model that fits\n(actual artifact sizes + runtime margin)"
    )
    ax.set_xlabel("Price (US$)")
    ax.set_ylabel("Largest model that fits (B params)")
    ax.legend(title="Workflow scenario", framealpha=0.95)
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "frontier_line")

    # Export CSVs
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    hardware.to_csv(DATA_DIR / "macbook_local_llm_hardware_2026.csv", index=False)
    models.to_csv(DATA_DIR / "macbook_local_llm_models_2026.csv", index=False)
    fit_df.to_csv(DATA_DIR / "macbook_local_llm_fit_matrix_2026.csv", index=False)
    frontier.to_csv(DATA_DIR / "macbook_local_llm_frontier_2026.csv", index=False)
    print("Exported CSVs to data/", file=sys.stderr)

    # Mirror CSVs for static hosting (same files as `data/` in repo root)
    public_data = REPO_ROOT / "public" / "data"
    public_data.mkdir(parents=True, exist_ok=True)
    for name in (
        "macbook_local_llm_hardware_2026.csv",
        "macbook_local_llm_models_2026.csv",
        "macbook_local_llm_fit_matrix_2026.csv",
        "macbook_local_llm_frontier_2026.csv",
    ):
        shutil.copy2(DATA_DIR / name, public_data / name)
    print("Copied CSVs to public/data/", file=sys.stderr)

    # Section 2 — Hardware trajectory
    memory_sourced = pd.DataFrame(
        {
            "generation": [1, 2, 3, 4, 5],
            "base": [16, 24, 24, 32, 32],
            "Pro": [32, 32, 36, 48, 64],
            "Max": [64, 96, 128, 128, 128],
            "Ultra": [128, 192, 192, np.nan, np.nan],
        }
    )
    memory_projected = pd.DataFrame(
        {
            "generation": [6, 7, 8],
            "base": [32, 48, 48],
            "Pro": [80, 96, 96],
            "Max": [128, 192, 256],
            "Ultra": [np.nan, np.nan, np.nan],
        }
    )
    M5_MAX_LOW_BW = 460
    bw_sourced = pd.DataFrame(
        {
            "generation": [1, 2, 3, 4, 5],
            "base": [68, 100, 100, 120, 153],
            "Pro": [200, 200, 150, 273, 307],
            "Max": [400, 400, 400, 546, 614],
            "Ultra": [800, 800, 819, np.nan, np.nan],
        }
    )
    bw_projected = pd.DataFrame(
        {
            "generation": [6, 7, 8],
            "base": [170, 245, 275],
            "Pro": [340, 520, 580],
            "Max": [680, 1040, 1150],
            "Ultra": [np.nan, np.nan, np.nan],
        }
    )

    gens_all = np.arange(1, 9)
    gen_labels = [f"M{i}" for i in gens_all]

    def build_trajectory(sourced_df: pd.DataFrame, projected_df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        combined = pd.concat([sourced_df, projected_df], ignore_index=True)
        rows = []
        for tier in ["base", "Pro", "Max", "Ultra"]:
            for _, row in combined.iterrows():
                g = int(row["generation"])
                v = row[tier]
                if np.isnan(v):
                    continue
                rows.append({"generation": g, "tier": tier, value_col: float(v), "sourced": g <= 5})
        return pd.DataFrame(rows)

    mem_df = build_trajectory(memory_sourced, memory_projected, "max_memory_gb")
    bw_df = build_trajectory(bw_sourced, bw_projected, "bandwidth_gbps")

    tier_order_traj = ["base", "Pro", "Max", "Ultra"]
    tier_colors = dict(zip(tier_order_traj, palettes["tier_traj"]))

    def plot_tier_trajectory(ax, df, value_col, tier_order, tier_colors):
        for tier in tier_order:
            d = df[df["tier"] == tier].sort_values("generation")
            c = tier_colors[tier]
            ds = d[d["sourced"]]
            dp = d[~d["sourced"]]
            style = ":" if tier == "Ultra" else "-"
            lbl = f"{tier} (niche: <1% of Mac sales)" if tier == "Ultra" else tier
            if not ds.empty:
                ax.plot(
                    ds["generation"],
                    ds[value_col],
                    marker="o",
                    linewidth=2.5,
                    color=c,
                    label=lbl,
                    linestyle=style,
                )
            if not dp.empty:
                bridge = pd.concat([ds.tail(1), dp])
                ax.plot(
                    bridge["generation"],
                    bridge[value_col],
                    linestyle="--",
                    marker="s",
                    linewidth=2,
                    alpha=0.7,
                    color=c,
                )

    fig, ax = plt.subplots(figsize=(12, 6))
    plot_tier_trajectory(ax, mem_df, "max_memory_gb", tier_order_traj, tier_colors)
    ax.axvspan(5.5, 8.5, alpha=0.1, color=NN["text_dim"])
    ax.annotate("projected (LPDDR roadmap)", xy=(7, 15), fontsize=9, alpha=0.5, ha="center")
    ax.annotate(
        "128 GiB ceiling: LPDDR5 package density limit;\nLPDDR6 may unlock 192-256 GiB",
        xy=(4.5, 128),
        xytext=(1.5, 210),
        fontsize=8,
        alpha=0.7,
        arrowprops=dict(arrowstyle="->", alpha=0.5),
    )
    ax.set_xticks(gens_all)
    ax.set_xticklabels(gen_labels)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Max unified memory (GiB)")
    ax.set_title(
        "Apple Silicon: max unified memory by tier (sourced M1-M5; dashed = projected M6-M8)"
    )
    ax.legend(title="Tier", framealpha=0.95, loc="upper left")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "memory_trajectory")

    fig, ax = plt.subplots(figsize=(12, 6))
    plot_tier_trajectory(ax, bw_df, "bandwidth_gbps", tier_order_traj, tier_colors)
    ax.annotate(
        f"M5 Max 32-core GPU: {M5_MAX_LOW_BW} GB/s",
        xy=(5, 614),
        xytext=(3.3, 750),
        fontsize=8,
        alpha=0.7,
        arrowprops=dict(arrowstyle="->", alpha=0.5),
    )
    ax.axvspan(5.5, 8.5, alpha=0.1, color=NN["text_dim"])
    ax.annotate("projected (LPDDR5X -> LPDDR6)", xy=(7, 40), fontsize=9, alpha=0.5, ha="center")
    ax.set_xticks(gens_all)
    ax.set_xticklabels(gen_labels)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Memory bandwidth (GB/s)")
    ax.set_title("Memory bandwidth by tier - drives tokens/sec for local inference")
    ax.legend(title="Tier", framealpha=0.95, loc="upper left")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "bandwidth_trajectory")

    # Section 2b — Params + bandwidth proxy
    HEAVY_DEV_GIB = 6.5
    gib_per_b = float((models["artifact_gib"] / models["params_b"]).median())
    mem_configs = np.array([16, 24, 32, 36, 48, 64, 96])

    def max_params_b_from_budget(budget_gib: float) -> float:
        net = budget_gib - RUNTIME_MARGIN_GIB
        if net <= 0:
            return 0.0
        return net / gib_per_b

    budget_os = mem_configs - OS_RESERVE_GIB
    budget_dev = mem_configs - OS_RESERVE_GIB - HEAVY_DEV_GIB
    params_os = np.array([max_params_b_from_budget(b) for b in budget_os])
    params_dev = np.array([max_params_b_from_budget(b) for b in budget_dev])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.4), layout="constrained")

    ax1.plot(
        mem_configs,
        params_os,
        "o-",
        linewidth=2.4,
        markersize=8,
        label=f"OS reserve only ({OS_RESERVE_GIB:.1f} GiB)",
        color=cat[0],
        zorder=3,
    )
    ax1.plot(
        mem_configs,
        params_dev,
        "s-",
        linewidth=2.4,
        markersize=7,
        label=f"OS + heavy dev ({HEAVY_DEV_GIB:.1f} GiB)",
        color=C["secondary_series"],
        zorder=3,
    )

    ref_lines = pd.DataFrame(
        [
            {"params_b": 7, "label": "Qwen 2.5 7B", "mmlu": 74},
            {"params_b": 12, "label": "Gemma 3 12B", "mmlu": 78},
            {"params_b": 14, "label": "Qwen 2.5 14B", "mmlu": 79},
            {"params_b": 27, "label": "Gemma 3 27B", "mmlu": 82},
            {"params_b": 32, "label": "Qwen 2.5 32B", "mmlu": 83},
            {"params_b": 70, "label": "Llama 3.1 70B", "mmlu": 86},
        ]
    )
    for _, r in ref_lines.iterrows():
        pb = float(r["params_b"])
        ax1.axhline(y=pb, color=NN["text_muted"], linestyle=":", linewidth=1.8, alpha=0.9, zorder=1)
    ax1.text(
        0.98,
        0.02,
        "Dotted lines: q4 reference models (MMLU from this notebook's demand analysis).",
        transform=ax1.transAxes,
        fontsize=8,
        color=NN["text_dim"],
        ha="right",
        va="bottom",
    )
    for _, r in ref_lines.iterrows():
        pb = float(r["params_b"])
        ax1.text(
            mem_configs[-1] + 0.35,
            pb,
            f'{r["label"]} ({pb:.0f}B, MMLU ~{r["mmlu"]})',
            fontsize=7,
            color=NN["text_muted"],
            va="center",
            ha="left",
        )

    ax1.set_xlim(12, 100)
    ax1.set_xticks([16, 24, 32, 36, 48, 64, 96])
    ymax = max(params_os.max(), params_dev.max(), ref_lines["params_b"].max()) * 1.08
    ax1.set_ylim(0, ymax)
    ax1.set_xlabel("Unified memory (GiB)")
    ax1.set_ylabel("Max loadable model size (B parameters, q4_K_M)")
    ax1.set_title(
        "How large a model fits?\n"
        f"(median {gib_per_b:.3f} GiB/B from `models`; +{RUNTIME_MARGIN_GIB:.1f} GiB runtime margin)"
    )
    ax1.legend(framealpha=0.95, loc="upper left")
    sns.despine(ax=ax1)

    row_params = [7, 14, 27, 32, 70]
    row_labels = [f"{p}B" for p in row_params]

    def artifact_for_params(pb: int) -> float:
        if pb == 14:
            row = models.loc[models["model"] == "Qwen 2.5 14B"]
        elif pb == 32:
            row = models.loc[models["model"] == "Qwen 2.5 32B"]
        else:
            row = models.loc[models["params_b"] == pb].iloc[[0]]
        return float(row["artifact_gib"].iloc[0])

    artifacts = [artifact_for_params(p) for p in row_params]
    bandwidths = [153, 307, 460, 614]
    col_labels = [
        "M5 base\n153 GB/s",
        "M5 Pro\n307 GB/s",
        "M5 Max 32c\n460 GB/s",
        "M5 Max 40c\n614 GB/s",
    ]

    mat = np.zeros((len(row_params), len(bandwidths)))
    for i, art in enumerate(artifacts):
        for j, bw in enumerate(bandwidths):
            mat[i, j] = bw / art

    cmap_zones = mcolors.ListedColormap([C["zone_slow"], C["zone_mid"], C["zone_fast"]])
    norm_zones = BoundaryNorm([0, 10, 20, 1000], cmap_zones.N)

    sns.heatmap(
        mat,
        ax=ax2,
        cmap=cmap_zones,
        norm=norm_zones,
        annot=True,
        fmt=".1f",
        linewidths=0.6,
        linecolor="white",
        cbar=False,
        xticklabels=col_labels,
        yticklabels=row_labels,
    )
    ax2.set_xlabel("Chip tier (memory bandwidth)")
    ax2.set_ylabel("Model (q4 artifact from `models`)")
    ax2.set_title(
        "Inference-speed proxy: bandwidth / artifact size\n"
        "(higher = faster decode when memory-bound; not a measured tok/s benchmark)"
    )
    legend_patches = [
        Patch(facecolor=C["zone_slow"], edgecolor="white", label="Slow proxy (<10)"),
        Patch(facecolor=C["zone_mid"], edgecolor="white", label="Acceptable (10–20)"),
        Patch(facecolor=C["zone_fast"], edgecolor="white", label="Fast proxy (≥20)"),
    ]
    ax2.legend(handles=legend_patches, loc="lower right", framealpha=0.95, fontsize=8, title="Interactive feel")

    print(f"Median q4 GiB per billion parameters (from `models`): {gib_per_b:.4f}", file=sys.stderr)
    save_fig(fig, "params_and_bandwidth_proxy")

    # Section 3 — MMLU
    models_mmlu = pd.DataFrame(
        [
            {"model": "GPT-3", "year": 2020, "params_b": 175, "mmlu": 43.0, "source": "Original MMLU paper"},
            {"model": "Chinchilla", "year": 2022, "params_b": 70, "mmlu": 67.5, "source": "Hoffmann et al. 2022"},
            {"model": "Llama 2 7B", "year": 2023, "params_b": 7, "mmlu": 46.0, "source": "Meta model card"},
            {"model": "Llama 2 70B", "year": 2023, "params_b": 70, "mmlu": 69.0, "source": "Meta model card"},
            {"model": "Mistral 7B", "year": 2023, "params_b": 7, "mmlu": 61.0, "source": "Mistral announcement"},
            {"model": "Llama 3 8B", "year": 2024, "params_b": 8, "mmlu": 68.0, "source": "Meta model card"},
            {"model": "Phi-3.5 mini", "year": 2024, "params_b": 3.8, "mmlu": 69.0, "source": "Microsoft model card"},
            {"model": "Gemma 2 9B", "year": 2024, "params_b": 9, "mmlu": 71.3, "source": "Google model card"},
            {"model": "Qwen 2.5 7B", "year": 2024, "params_b": 7, "mmlu": 70.5, "source": "Qwen technical report"},
            {"model": "Qwen 2.5 14B", "year": 2024, "params_b": 14, "mmlu": 79.0, "source": "Qwen technical report"},
            {"model": "Qwen 2.5 32B", "year": 2024, "params_b": 32, "mmlu": 83.0, "source": "Qwen technical report"},
            {"model": "Llama 3.1 70B", "year": 2024, "params_b": 70, "mmlu": 86.0, "source": "Meta model card"},
            {"model": "Gemma 3 12B", "year": 2025, "params_b": 12, "mmlu": 78.0, "source": "Google model card"},
            {"model": "Gemma 3 27B", "year": 2025, "params_b": 27, "mmlu": 82.0, "source": "Google model card"},
            {"model": "Phi-4", "year": 2025, "params_b": 14, "mmlu": 84.8, "source": "llm-stats leaderboard"},
        ]
    )

    mmlu_years_sorted = sorted(models_mmlu["year"].unique())
    mmlu_year_palette = {y: C["year_blues"][i] for i, y in enumerate(mmlu_years_sorted)}

    fig, ax = plt.subplots(figsize=(11, 6.5))
    sns.scatterplot(
        data=models_mmlu,
        x="params_b",
        y="mmlu",
        hue="year",
        palette=mmlu_year_palette,
        hue_order=mmlu_years_sorted,
        s=140,
        edgecolor="white",
        linewidth=1.2,
        ax=ax,
    )
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("Parameters (B, log scale — large models left, small models right)")
    ax.set_ylabel("MMLU (5-shot)")
    ax.set_title(
        "Models get stronger at the same or smaller size\n"
        "(log scale: quality ~ power law of params per Chinchilla; sourced MMLU scores)"
    )
    for _, r in models_mmlu.iterrows():
        ax.annotate(
            r["model"],
            (r["params_b"], r["mmlu"]),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
            alpha=0.85,
        )
    ax.legend(title="Release year", framealpha=0.95, bbox_to_anchor=(1.02, 1), loc="upper left")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "mmlu_scatter")

    years_projected = np.array([2027, 2028])
    thresholds = [65, 70, 75, 80]
    thresh_rows = []
    for thr in thresholds:
        for y in np.arange(2020, 2027):
            elig = models_mmlu[(models_mmlu["year"] <= y) & (models_mmlu["mmlu"] >= thr)]
            if elig.empty:
                continue
            thresh_rows.append(
                {"threshold": thr, "year": int(y), "min_params_b": float(elig["params_b"].min())}
            )
    thresh_df = pd.DataFrame(thresh_rows)
    thresh_df["sourced"] = True

    proj_rows = []
    for thr in thresholds:
        sub = thresh_df[thresh_df["threshold"] == thr].sort_values("year")
        if len(sub) < 2:
            continue
        x = sub["year"].values.astype(float)
        y_log = np.log(sub["min_params_b"].values.astype(float))
        coeffs = np.polyfit(x, y_log, 1)
        for yp in years_projected:
            pred = float(np.exp(np.polyval(coeffs, yp)))
            pred = max(pred, 1.0)
            proj_rows.append({"threshold": thr, "year": int(yp), "min_params_b": pred, "sourced": False})

    plot_df = pd.concat([thresh_df, pd.DataFrame(proj_rows)], ignore_index=True)
    thr_colors = dict(zip(thresholds, palettes["threshold_lines"]))

    fig, ax = plt.subplots(figsize=(11, 6))
    for thr in thresholds:
        d = plot_df[plot_df["threshold"] == thr].sort_values("year")
        c = thr_colors[thr]
        ds = d[d["sourced"]]
        dp = d[~d["sourced"]]
        lab = f"MMLU >= {thr}"
        if not ds.empty:
            ax.plot(ds["year"], ds["min_params_b"], marker="o", linewidth=2.2, color=c, label=lab)
        if not dp.empty:
            bridge = pd.concat([ds.tail(1), dp])
            ax.plot(
                bridge["year"],
                bridge["min_params_b"],
                linestyle="--",
                marker="s",
                linewidth=2,
                color=c,
                alpha=0.7,
            )
    ymax = float(np.ceil(plot_df["min_params_b"].max() / 10.0) * 10.0 + 10.0)
    ax.set_ylim(0, ymax)
    tick_step = 5 if ymax <= 50 else 10
    ax.yaxis.set_major_locator(MultipleLocator(tick_step))
    ax.set_xlabel("Year")
    ax.set_ylabel("Smallest model (B parameters)")
    ax.set_title(
        "Smallest model hitting each MMLU bar falls over time\n"
        "(dashed = projected via log-linear fit across all sourced years)"
    )
    ax.legend(title="Quality bar", framealpha=0.95)
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "mmlu_thresholds")

    # Section 4 — Convergence
    TOTAL_OVERHEAD_GIB = OS_RESERVE_GIB + HEAVY_DEV_GIB
    pro_mem_by_gen = {1: 32, 2: 32, 3: 36, 4: 48, 5: 64}
    gen_to_year = {1: 2020, 2: 2022, 3: 2023, 4: 2024, 5: 2026}

    supply_rows = []
    for g, mem in pro_mem_by_gen.items():
        budget = max(mem - TOTAL_OVERHEAD_GIB, 0)
        supply_rows.append(
            {
                "year": gen_to_year[g],
                "generation": g,
                "pro_total_gb": mem,
                "model_budget_gib": budget,
            }
        )
    supply_df = pd.DataFrame(supply_rows)

    demand_by_year = pd.DataFrame(
        [
            {"year": 2024, "demand_gib": 22.5, "model": "Qwen 2.5 32B (q4)", "sourced": True},
            {"year": 2025, "demand_gib": 19.5, "model": "Gemma 3 27B (q4)", "sourced": True},
            {"year": 2026, "demand_gib": 18.0, "model": "projected ~25B", "sourced": False},
            {"year": 2027, "demand_gib": 15.0, "model": "projected ~20B", "sourced": False},
            {"year": 2028, "demand_gib": 12.0, "model": "projected ~16B", "sourced": False},
        ]
    )

    conv = supply_df.merge(demand_by_year, on="year", how="inner").sort_values("year")
    supply_all = supply_df.sort_values("year")

    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.plot(
        supply_all["year"],
        supply_all["model_budget_gib"],
        marker="o",
        linewidth=2.5,
        color=cat[0],
        label=f"Supply: Pro model budget (total - {TOTAL_OVERHEAD_GIB:.0f} GiB OS + dev)",
    )
    ax.plot(
        demand_by_year["year"],
        demand_by_year["demand_gib"],
        marker="s",
        linewidth=2.5,
        color=C["secondary_series"],
        label="Demand: smallest 80+ MMLU model (q4 artifact + margin)",
    )

    ds_demand = demand_by_year[demand_by_year["sourced"]]
    dp_demand = demand_by_year[~demand_by_year["sourced"]]
    if not dp_demand.empty:
        bridge = pd.concat([ds_demand.tail(1), dp_demand])
        ax.plot(
            bridge["year"],
            bridge["demand_gib"],
            linestyle="--",
            linewidth=2,
            color=C["secondary_series"],
            alpha=0.7,
        )
        ax.plot(
            ds_demand["year"],
            ds_demand["demand_gib"],
            marker="s",
            linewidth=2.5,
            color=C["secondary_series"],
        )

    if not conv.empty:
        ax.fill_between(
            conv["year"],
            conv["demand_gib"],
            conv["model_budget_gib"],
            where=(conv["model_budget_gib"] >= conv["demand_gib"]),
            alpha=0.15,
            color=C["positive"],
            interpolate=True,
            label="Surplus headroom",
        )

    for _, r in demand_by_year.iterrows():
        ax.annotate(r["model"], (r["year"], r["demand_gib"]), textcoords="offset points", xytext=(8, -12), fontsize=8, alpha=0.8)
    for _, r in supply_all.iterrows():
        ax.annotate(
            f'M{int(r["generation"])} Pro {int(r["pro_total_gb"])} GiB',
            (r["year"], r["model_budget_gib"]),
            textcoords="offset points",
            xytext=(8, 6),
            fontsize=8,
            alpha=0.8,
        )

    ax.set_xlabel("Year (generation mapped to first ship year)")
    ax.set_ylabel("Unified memory (GiB)")
    ax.set_title(
        "When does a knowledge-worker MacBook Pro comfortably run strong local models?\n"
        f"(model budget = total RAM - {OS_RESERVE_GIB:.1f} GiB OS - {HEAVY_DEV_GIB:.1f} GiB dev workflow)"
    )
    ax.legend(framealpha=0.95, loc="upper left")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "supply_demand")

    ref_total = 48
    ref_price = 3090
    upgrade_total = 64
    upgrade_price = 3280

    models_local = pd.DataFrame(
        [
            {"model": "Qwen 2.5 7B (q4)", "artifact_gib": 4.7, "mmlu": 74},
            {"model": "Gemma 3 12B (q4)", "artifact_gib": 8.1, "mmlu": 78},
            {"model": "Qwen 2.5 14B (q4)", "artifact_gib": 9.0, "mmlu": 79},
            {"model": "Phi-4 14B (q4)", "artifact_gib": 9.0, "mmlu": 84.8},
            {"model": "Gemma 3 27B (q4)", "artifact_gib": 17.0, "mmlu": 82},
            {"model": "Qwen 2.5 32B (q4)", "artifact_gib": 20.0, "mmlu": 83},
            {"model": "Llama 3.1 70B (q4)", "artifact_gib": 43.0, "mmlu": 86},
        ]
    )
    models_local["total_need"] = models_local["artifact_gib"] + RUNTIME_MARGIN_GIB
    models_local["headroom_48"] = ref_total - TOTAL_OVERHEAD_GIB - models_local["total_need"]
    models_local["headroom_64"] = upgrade_total - TOTAL_OVERHEAD_GIB - models_local["total_need"]
    models_local["fits_48"] = models_local["headroom_48"] >= 0
    models_local["fits_64"] = models_local["headroom_64"] >= 0

    fig, ax = plt.subplots(figsize=(12, 6))
    y_pos = np.arange(len(models_local))
    bar_height = 0.35
    bars_48 = ax.barh(
        y_pos + bar_height / 2,
        models_local["headroom_48"],
        bar_height,
        label=f"M5 Pro 48 GiB (${ref_price:,})",
        color=palettes["headroom_pair"][0],
    )
    bars_64 = ax.barh(
        y_pos - bar_height / 2,
        models_local["headroom_64"],
        bar_height,
        label=f"M5 Pro 64 GiB (${upgrade_price:,})",
        color=palettes["headroom_pair"][1],
    )
    ax.axvline(x=0, color=C["zero_line"], linewidth=1.5, linestyle="-", alpha=0.7, label="Zero headroom (trade-offs begin)")
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f'{r["model"]}\nMMLU {r["mmlu"]}' for _, r in models_local.iterrows()], fontsize=9)
    ax.set_xlabel("Memory headroom after OS + dev workflow + model (GiB)")
    ax.set_title(
        "Knowledge-worker utility: how much headroom remains?\n"
        f"(after {OS_RESERVE_GIB:.1f} GiB OS + {HEAVY_DEV_GIB:.1f} GiB heavy dev + model artifact + {RUNTIME_MARGIN_GIB:.1f} GiB runtime margin)"
    )
    ax.legend(framealpha=0.95, loc="lower right")
    sns.despine()
    plt.tight_layout()
    save_fig(fig, "headroom_knowledge_worker")

    def _hw_usd(hw_df: pd.DataFrame, machine: str, memory_gib: int) -> int:
        row = hw_df.loc[(hw_df["machine"] == machine) & (hw_df["memory_gib"] == memory_gib), "price_usd"]
        if row.empty:
            raise KeyError(f"No hardware row for {machine} {memory_gib} GiB")
        return int(row.iloc[0])

    price_pro14_m5_24 = _hw_usd(hardware, "MacBook Pro 14 M5", 24)
    price_pro16_m5pro_48 = _hw_usd(hardware, "MacBook Pro 16 M5 Pro", 48)
    price_pro16_m5pro_64 = _hw_usd(hardware, "MacBook Pro 16 M5 Pro", 64)
    delta_m5_24_to_m5pro_64 = price_pro16_m5pro_64 - price_pro14_m5_24
    delta_m5pro_48_to_64 = price_pro16_m5pro_64 - price_pro16_m5pro_48

    subscriptions = pd.DataFrame(
        [
            {"service": "ChatGPT Plus", "monthly_usd": 20, "months": 30},
            {"service": "Claude Pro", "monthly_usd": 20, "months": 30},
            {"service": "API (moderate use)", "monthly_usd": 100, "months": 30},
            {"service": "API (heavy use)", "monthly_usd": 200, "months": 30},
        ]
    )
    subscriptions["total_2_5yr"] = subscriptions["monthly_usd"] * subscriptions["months"]

    fig, ax = plt.subplots(figsize=(11, 5.2), layout="constrained")
    sub_bar_colors = palettes["subscription_bars"]
    ax.barh(subscriptions["service"], subscriptions["total_2_5yr"], color=sub_bar_colors, edgecolor="white", linewidth=0.8)
    ax.axvline(
        x=delta_m5_24_to_m5pro_64,
        color=C["positive"],
        linewidth=2.6,
        linestyle="--",
        zorder=5,
        label=(
            f"M5 24 GiB → M5 Pro 64 GiB: ${delta_m5_24_to_m5pro_64:,} "
            f"(Pro 14 M5 24 ${price_pro14_m5_24:,} → Pro 16-inch M5 Pro 64 ${price_pro16_m5pro_64:,})"
        ),
    )
    ax.axvline(
        x=delta_m5pro_48_to_64,
        color=C["secondary_series"],
        linewidth=2.6,
        linestyle=":",
        zorder=5,
        label=(
            f"M5 Pro 48 → 64 GiB: ${delta_m5pro_48_to_64:,} "
            f"(same Pro 16-inch ${price_pro16_m5pro_48:,} → ${price_pro16_m5pro_64:,})"
        ),
    )
    for i, (_, r) in enumerate(subscriptions.iterrows()):
        ax.annotate(f'${r["total_2_5yr"]:,.0f}', (r["total_2_5yr"] + 50, i), va="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("One-time upgrade premium or 2.5-year subscription cost (US$)")
    ax.set_title(
        "Hardware upgrade premiums vs 2.5-year cloud API spend\n"
        f"Benchmarks from this notebook's AU list prices (×{AUD_TO_USD} USD); "
        "first line: Pro 14 M5 @ 24 GiB (Apple US USD 2,049) vs Pro 16-inch M5 Pro @ 64 GiB"
    )
    ax.legend(framealpha=0.95, loc="lower right", fontsize=8.5)
    sns.despine()
    save_fig(fig, "upgrade_vs_subscription")

    OS_LIGHT_GIB = OS_RESERVE_GIB
    tier_year_mem = {
        "<=$1,000": {**{y: 8 for y in range(2020, 2025)}, 2025: 16, 2026: 16, 2027: 16, 2028: 24},
        "<=$1,500": {**{y: 8 for y in range(2020, 2023)}, 2023: 16, 2024: 16, 2025: 24, 2026: 24, 2027: 24, 2028: 32},
        "<=$2,000": {**{y: 16 for y in range(2020, 2025)}, 2025: 32, 2026: 32, 2027: 32, 2028: 48},
        "<=$2,500": {**{y: 16 for y in range(2020, 2023)}, 2023: 24, 2024: 24, 2025: 32, 2026: 32, 2027: 32, 2028: 48},
        ">=$3,000": {2020: 16, 2021: 32, 2022: 32, 2023: 36, 2024: 48, 2025: 48, 2026: 64, 2027: 64, 2028: 96},
    }
    tier_rows = []
    for tier_label, ymap in tier_year_mem.items():
        for year, mem_gib in ymap.items():
            tier_rows.append(
                {
                    "year": year,
                    "tier": tier_label,
                    "mem_gib": mem_gib,
                    "budget_gib": max(mem_gib - OS_LIGHT_GIB, 0.0),
                }
            )
    tier_df = pd.DataFrame(tier_rows)
    dem_plot = demand_by_year.sort_values("year")[["year", "demand_gib"]].copy()
    merged_tier = tier_df.merge(dem_plot, on="year", how="left")
    tier_order_plot = ["<=$1,000", "<=$1,500", "<=$2,000", "<=$2,500", ">=$3,000"]
    tier_palette = palettes["price_tier_lines"]

    fig, ax = plt.subplots(figsize=(11, 6.2), layout="constrained")
    ymax = float(max(merged_tier["budget_gib"].max(), dem_plot["demand_gib"].max()) * 1.12)
    ax.fill_between(
        dem_plot["year"].values,
        dem_plot["demand_gib"].values,
        ymax,
        alpha=0.22,
        color=C["positive"],
        zorder=0,
        label="Adequacy: RAM budget above demand",
    )
    for i, t in enumerate(tier_order_plot):
        d = merged_tier[merged_tier["tier"] == t].sort_values("year")
        ax.plot(
            d["year"],
            d["budget_gib"],
            marker="o",
            markersize=7,
            linewidth=2.4,
            label=t,
            color=tier_palette[i],
            zorder=2,
        )
    ax.plot(
        dem_plot["year"],
        dem_plot["demand_gib"],
        color=NN["text"],
        linestyle="--",
        linewidth=2.6,
        marker="s",
        markersize=8,
        markerfacecolor="white",
        markeredgewidth=1.5,
        markeredgecolor=NN["text"],
        label="Demand: smallest 80+ MMLU (q4 + margin)",
        zorder=4,
    )
    ax.set_ylim(0, ymax)
    ax.set_xlim(2019.5, 2028.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("GiB available for model (total RAM − OS reserve)")
    ax.set_title(
        "When can each price tier run an 80+ MMLU model?\n"
        f"Shaded region: RAM headroom above the demand floor (OS reserve {OS_LIGHT_GIB:.1f} GiB only; not heavy dev)"
    )
    ax.legend(framealpha=0.95, loc="upper left", fontsize=9, ncol=2, columnspacing=1.0)
    ax.set_xticks(range(2020, 2029))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    sns.despine()
    save_fig(fig, "price_tier_viability")

    print(
        f"Economics chart SVGs (single location): {OUT_DIR.relative_to(REPO_ROOT)}/ — "
        "if the site still shows old graphics after `npm run analyze`, hard-refresh the browser "
        "or restart `next dev` (static assets are often cached).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
