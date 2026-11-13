"""Render local paper-figure reconstructions; requires numpy and matplotlib.

Run export_figures.jl first, and run run.jl for the Table 1/2 comparison.
All plots retain the literal quadratures and are labeled reconstructions.
"""
from pathlib import Path
import csv
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullFormatter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
COLORS = ("#007f86", "#da654a", "#6660a8")
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10.5,
    "axes.titlesize": 12, "axes.labelsize": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#919ba5", "axes.labelcolor": "#263746",
    "xtick.color": "#52616e", "ytick.color": "#52616e",
    "text.color": "#233645", "figure.facecolor": "white",
    "savefig.facecolor": "white", "svg.fonttype": "none",
})


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as source:
        return list(csv.DictReader(source))


def numeric_rows(name, case=None):
    rows = read_csv(OUT / f"{name}_solution.csv")
    return [r for r in rows if case is None or r["case"] == case]


def grid(rows, field):
    ts = sorted(set(float(r["t"]) for r in rows))
    xs = sorted(set(float(r["x"]) for r in rows))
    by_index = {(int(r["time_index"]), int(r["point_index"])): float(r[field]) for r in rows}
    z = np.array([[by_index[n, i] for i in range(len(xs))] for n in range(len(ts))])
    return np.asarray(xs), np.asarray(ts), z


def title(fig, name, subtitle):
    fig.suptitle(name, x=0.06, y=0.98, ha="left", fontsize=17, weight="bold")
    fig.text(0.06, 0.918, subtitle, ha="left", fontsize=10.5, color="#52616e")


def save(fig, name, footer):
    fig.text(0.06, 0.027, footer, fontsize=9.5, color="#52616e", va="bottom")
    for extension in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{extension}", dpi=190, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)


def surface(ax, x, y, z, *, title_text, y_label="t", limits=None, cmap="viridis"):
    X, Y = np.meshgrid(x, y)
    limits = limits or (float(np.min(z)), float(np.max(z)))
    result = ax.plot_surface(X, Y, z, cmap=cmap, vmin=limits[0], vmax=limits[1],
                             linewidth=0.15, edgecolor=(1, 1, 1, 0.22),
                             antialiased=True, rcount=max(50, len(y)), ccount=max(50, len(x)))
    ax.set(xlabel="x", ylabel=y_label, zlabel="u", title=title_text)
    ax.view_init(elev=27, azim=-125)
    ax.set_box_aspect((1.1, 1.0, 0.75))
    ax.tick_params(labelsize=9, pad=1)
    ax.xaxis.labelpad = ax.yaxis.labelpad = 5
    ax.zaxis.labelpad = 4
    ax.set_zlim(*limits)
    ax.set_xticks(np.linspace(-1, 1, 5))
    ax.set_yticks(np.linspace(float(np.min(y)), float(np.max(y)), 5))
    ax.set_zticks(np.linspace(-1, 1, 5) if limits[0] < 0 else np.linspace(0, 1, 5))
    return result


def paired_1d(name, heading, subtitle, scheme):
    rows = numeric_rows(name)
    x, t, truth = grid(rows, "exact")
    _, _, computed = grid(rows, "numerical")
    fig = plt.figure(figsize=(12, 5.7))
    title(fig, heading, subtitle)
    axes = [fig.add_axes([0.04 + k * 0.455, 0.13, 0.43, 0.73], projection="3d") for k in range(2)]
    limits = (0, max(np.max(truth), np.max(computed)) * 1.03)
    surface(axes[0], x, t, truth, title_text="Exact solution", limits=limits)
    mappable = surface(axes[1], x, t, computed, title_text=f"{scheme} Galerkin reconstruction", limits=limits)
    cax = fig.add_axes([0.955, 0.23, 0.013, 0.50])
    fig.colorbar(mappable, cax=cax, label="u")
    save(fig, name, f"Reconstruction on the caption's nodal grid.  Maximum nodal error: {np.max(abs(computed-truth)):.3e}.")


def convergence_figure():
    rows = read_csv(OUT / "figure3_convergence.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.19, top=0.77, wspace=0.27)
    title(fig, "Figure 3 · Example 6.1 convergence reconstruction",
          "Caption parameters | α=0.5, ν=2.3, M=9 | N=4, 8, 16 | uniform time mesh")
    for ax, scheme, display in zip(axes, ("L1", "L12"), ("L1", "L1-2")):
        selected = sorted((r for r in rows if r["scheme"] == scheme), key=lambda r: int(r["N"]))
        N = np.array([int(r["N"]) for r in selected])
        errors = np.array([float(r["L2"]) for r in selected])
        # A visibly scaled guide conveys only slope; it is not an error bound.
        guide = 1.35 * errors[0] * (N[0] / N)**1.5
        ax.loglog(N, errors, "o-", color=COLORS[0], lw=2.1, ms=7, label="Local reconstruction")
        ax.loglog(N, guide, "--", color="#52616e", lw=1.8, label="Scaled N⁻¹·⁵ slope guide")
        rate = np.log2(errors[-2] / errors[-1])
        ax.set(title=f"{display} · last measured rate {rate:.3f}", xlabel="Number of time steps N", ylabel="Paper's discrete L² error")
        ax.set_xticks(N, [str(n) for n in N])
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(True, which="both", color="#dce3e7", alpha=0.7)
        ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    save(fig, "figure3", "Original plotting values were not digitized. Dashed lines reproduce the printed slope label and are scaled guides, not bounds.")


def table_comparison():
    comparison_path = ROOT / "results" / "comparison.csv"
    # A separately launched full-table runner may still be finishing its file.
    deadline = time.monotonic() + 120
    while not comparison_path.exists():
        if time.monotonic() >= deadline:
            raise FileNotFoundError("Run run.jl first: results/comparison.csv is needed for Figure 3")
        time.sleep(1)
    published = read_csv(ROOT / "reference_tables.csv")
    local = read_csv(comparison_path)
    table_rows = [r for r in published if int(r["table"]) in (1, 2)]
    local_lookup = {(r["table"], float(r["alpha"]), int(r["N"])): r for r in local}
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8))
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.22, top=0.77, wspace=0.27)
    title(fig, "Example 6.1 · Published table comparison",
          "Tables 1–2 diagnostic | M=9, ν=2.3 | α=0.4, 0.6, 0.8")
    parameter_rows = []
    for ax, table, scheme in zip(axes, (1, 2), ("L1", "L1-2")):
        for alpha, color in zip((0.4, 0.6, 0.8), COLORS):
            chosen = sorted((r for r in table_rows if int(r["table"]) == table and float(r["alpha"]) == alpha), key=lambda r: int(r["N"]))
            Ns = [int(r["N"]) for r in chosen]
            printed = [float(r["L2"]) for r in chosen]
            reconstructed = []
            for row in chosen:
                computed = local_lookup[row["table"], alpha, int(row["N"])]
                if computed["status"] != "computed":
                    raise RuntimeError("A convergence configuration was not computed")
                reconstructed.append(float(computed["L2_computed"]))
                parameter_rows.append({**row, "L2_computed": computed["L2_computed"], "status": "related reconstruction"})
            ax.loglog(Ns, printed, "o--", color=color, ms=6.5, mfc="white", lw=1.6)
            ax.loglog(Ns, reconstructed, "s-", color=color, ms=5.5, lw=1.8)
        ax.set(title=f"{scheme}: published values and local solve", xlabel="Number of time steps N", ylabel="Paper's discrete L² error")
        ax.set_xticks((4, 8, 16), ("4", "8", "16"))
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(True, which="both", color="#dce3e7", alpha=0.7)
    legend_items = [Line2D([], [], color=c, lw=2, label=f"α={a}") for a, c in zip((0.4, 0.6, 0.8), COLORS)]
    legend_items += [Line2D([], [], color="#52616e", ls="--", marker="o", mfc="white", label="Published table"),
                     Line2D([], [], color="#52616e", marker="s", label="Local reconstruction")]
    fig.legend(handles=legend_items, loc="lower center", bbox_to_anchor=(0.53, 0.085), ncol=5, frameon=False)
    save(fig, "table_convergence_diagnostic", "Original Fig. 3 uses α=0.5. This separate diagnostic compares the published table values without fitting.")
    with (OUT / "table_convergence_diagnostic_parameters.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(parameter_rows[0]))
        writer.writeheader()
        writer.writerows(parameter_rows)


def figure4():
    rows = numeric_rows("figure4")
    x, t, z = grid(rows, "numerical")
    _, _, exact = grid(rows, "exact")
    fig = plt.figure(figsize=(12, 5.8))
    title(fig, "Figure 4 · Example 6.2 with nonzero initial data",
          "Reconstruction | L1, α=0.7, β=0.3 | N=16, M=20, uniform time mesh")
    left = fig.add_axes([0.03, 0.13, 0.47, 0.70], projection="3d")
    surface(left, x, t, z, title_text="Numerical solution", limits=(-1.05, 1.05), cmap="coolwarm")
    ax = fig.add_axes([0.61, 0.20, 0.34, 0.57])
    k = int(np.argmin(abs(t - 0.5)))
    dense = np.linspace(-1, 1, 501)
    ax.plot(dense, (1 - t[k]**3.7) * np.sin(np.pi*dense), color="#263746", lw=2, label="Exact solution")
    ax.plot(x, z[k], "o", color=COLORS[0], ms=4.8, mfc="white", mew=1.4, label="L1 nodal values")
    ax.set(title=f"Cross-section at t={t[k]:g}", xlabel="x", ylabel="u(x,t)", xlim=(-1, 1))
    ax.grid(color="#dce3e7", alpha=0.7)
    ax.legend(frameon=False, loc="upper left")
    save(fig, "figure4", f"Caption parameters and t=0.5 section.  Maximum error over all nodes and times: {np.max(abs(z-exact)):.3e}.")


def figure5():
    rows = numeric_rows("figure5", "alpha0.3")
    x, t, z = grid(rows, "numerical")
    fig = plt.figure(figsize=(12, 5.8))
    title(fig, "Figure 5 · Example 6.3 initial layer",
          "Reconstruction | L1, β=0.5 | N=20, M=16 | graded time mesh ρ=(2−α)/α")
    ax3d = fig.add_axes([0.02, 0.12, 0.48, 0.72], projection="3d")
    surface(ax3d, x, t, z, title_text="Numerical surface, α=0.3", limits=(0, 1.05))
    ax = fig.add_axes([0.60, 0.20, 0.35, 0.57])
    dense = np.r_[0, np.geomspace(1e-7, 1, 700)]
    for alpha, color in zip((0.3, 0.6, 0.9), COLORS):
        case = numeric_rows("figure5", f"alpha{alpha}")
        xs, ts, values = grid(case, "numerical")
        i = int(np.argmin(abs(xs)))
        ax.plot(dense, dense**alpha * np.cos(np.pi*xs[i]/2), color=color, lw=1.8, label=f"α={alpha}")
        ax.plot(ts, values[:, i], "o", color=color, ms=3.8, mfc="white", mew=1)
    ax.set(title="Evolution at the node nearest x=0", xlabel="t", ylabel="u(0,t)", xlim=(0, 1), ylim=(0, 1.07))
    ax.grid(color="#dce3e7", alpha=0.7)
    ax.legend(frameon=False, loc="lower right")
    save(fig, "figure5", "Solid curves: exact profiles. Open circles: reconstructed nodal solutions. Each α uses its own stated grading.")


def figure6():
    rows = numeric_rows("figure6")
    last = max(int(r["time_index"]) for r in rows)
    rows = [r for r in rows if int(r["time_index"]) == last]
    x = np.array(sorted(set(float(r["x"]) for r in rows)))
    y = np.array(sorted(set(float(r["y"]) for r in rows)))
    ordered = sorted(rows, key=lambda r: int(r["point_index"]))
    truth = np.array([float(r["exact"]) for r in ordered]).reshape(len(y), len(x))
    computed = np.array([float(r["numerical"]) for r in ordered]).reshape(len(y), len(x))
    fig = plt.figure(figsize=(12, 5.8))
    title(fig, "Figure 6 · Example 6.4 in two spatial dimensions",
          "Reconstruction at T=1 | L1, α=0.6, β=0.7 | N=8, M₁=M₂=9 | ρ=2(2−α)/α")
    axes = [fig.add_axes([0.035 + k * 0.455, 0.13, 0.43, 0.72], projection="3d") for k in range(2)]
    surface(axes[0], x, y, truth, title_text="Exact solution", y_label="y", limits=(-1.05, 1.05), cmap="coolwarm")
    mappable = surface(axes[1], x, y, computed, title_text="L1 Galerkin reconstruction", y_label="y", limits=(-1.05, 1.05), cmap="coolwarm")
    cax = fig.add_axes([0.955, 0.23, 0.013, 0.50])
    fig.colorbar(mappable, cax=cax, label="u")
    save(fig, "figure6", f"Tensor Legendre grid; x index varies fastest. Maximum final-time nodal error: {np.max(abs(computed-truth)):.3e}.")


def memory_diagnostic():
    rows = read_csv(OUT / "memory_diagnostic.csv")
    N = np.array([int(r["N"]) for r in rows])
    errors = np.array([float(r["absolute_error"]) for r in rows])
    fitted_rate = np.log2(errors[-2]/errors[-1])
    fig, ax = plt.subplots(figsize=(9.4, 5.8))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.78, bottom=0.17)
    title(fig, "The printed memory rule misses its claimed order",
          "Constant-input counterexample | u(s)=1, β=0.5, T=1 | literal Eq. (6), exact integral = 2")
    ax.loglog(N, errors, "o-", color=COLORS[0], lw=2.2, ms=6.5, label=f"Measured error; last rate {fitted_rate:.4f}")
    ax.loglog(N, errors[-1]*(N[-1]/N)**0.5, "--", color="#263746", lw=1.7, label="Reference slope 1−β = 0.5")
    ax.loglog(N, errors[0]*(N[0]/N)**1.5, ":", color=COLORS[1], lw=2.2, label="Paper's claimed slope 2−β = 1.5")
    ax.set(xlabel="Number of uniform time steps N", ylabel="Absolute quadrature error")
    ax.set_xticks(N, [str(v) for v in N])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="both", color="#dce3e7", alpha=0.7)
    ax.legend(frameon=False, loc="lower left")
    save(fig, "memory_diagnostic", "Constants are exact on the last cell; old-cell trapezoid errors near the singularity dominate the total error.")


def main():
    OUT.mkdir(exist_ok=True)
    paired_1d("figure1", "Figure 1 · Example 6.1", "Reconstruction | L1, α=0.55, ν=2.5 | N=10, M=32, uniform time mesh", "L1")
    paired_1d("figure2", "Figure 2 · Example 6.1", "Reconstruction | L1-2, α=0.7, ν=2.9 | N=16, M=32, uniform time mesh", "L1-2")
    convergence_figure()
    table_comparison()
    figure4()
    figure5()
    figure6()
    memory_diagnostic()
    print(f"Eight PNG/SVG figure pairs written to {OUT}")


if __name__ == "__main__":
    main()
