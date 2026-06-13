#!/usr/bin/env python3
"""Triangle -> circle -> square -> circle: rotation as a generator of form.

A narrative animation in six phases, rendered frame by frame:

  A  a right-isosceles triangle pivots about a single fixed point (its
     right-angle vertex), advancing 1 degree per frame for 360 frames;
     the path traced by its far vertices closes into a complete circle;
  B  the rotation accelerates -- motion-blur ghosts pile up;
  C  at full speed the swept region is indistinguishable from a solid
     circle: a circle has appeared out of a spinning triangle;
  D  the spin stops and the triangle is put back where it began;
  E  the triangle is doubled: a copy rotates 180 degrees about the
     midpoint of the hypotenuse, and the two halves form a square
     (this is why the triangle is right-isosceles -- an equilateral
     triangle cannot tile a square);
  F  the square spins about the same pivot until its own, larger
     circle appears (radius sqrt(2): the corner diagonal).

The same fact drives both circles: under rotation about a fixed point,
every shape becomes the disc of its farthest vertex.

Usage:
    python3 visualization/spin_polygon.py                # full ~13s GIF
    python3 visualization/spin_polygon.py --quick        # fast test render
    python3 visualization/spin_polygon.py --webp         # also animated WebP

Output: gfx/2d/triangle_to_circle.gif (and .webp with --webp).
"""

import argparse
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "gfx", "2d")

DARK_BG = "#0d1117"
TRI_COLOR = "#58a6ff"
TWIN_COLOR = "#a371f7"
TRACE_COLOR = "#3fb950"
CIRCLE_COLOR = "#e6edf3"

# The triangle: right-isosceles, pivot at the right-angle vertex (origin).
# Far vertices (1,0) and (0,1) lie at distance 1: the emergent circle is
# the unit circle. Two of these triangles make the unit square.
TRIANGLE = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
SQUARE = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
PIVOT = np.array([0.0, 0.0])
LIM = 1.75


def rotate(points, theta_deg, center=PIVOT):
    """Rotate points (N,2) about `center` by theta in degrees."""
    t = np.radians(theta_deg)
    rot = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return (points - center) @ rot.T + center


# ---------------------------------------------------------------------------
# Frame description: a small dict per frame keeps the narrative logic
# separate from the matplotlib rendering.
# ---------------------------------------------------------------------------


def build_script(quick=False):
    """Yield one frame-description dict per frame."""
    frames = []

    def add(**kw):
        desc = dict(shape="triangle", theta=0.0, ghosts=(),
                    trace_until=None, disc=0.0, radius=1.0,
                    twin_theta=None, caption="")
        desc.update(kw)
        frames.append(desc)

    # Phase A -- 360 incremental frames, 1 degree each, tracing the path
    n_a = 60 if quick else 360
    step_a = 360.0 / n_a
    for i in range(n_a):
        theta = step_a * (i + 1)
        add(theta=theta, trace_until=theta,
            caption=f"one fixed point, {theta:.0f}° of 360° — "
                    "the path closes into a circle")

    # Phase B -- accelerate: step ramps 1 -> 40 deg/frame (ease-in)
    n_b = 30 if quick else 100
    theta = 360.0
    steps = 1.0 + 39.0 * (np.linspace(0, 1, n_b) ** 2)
    for k, d in enumerate(steps):
        theta += d
        # ghosts: subsample the recent sweep so blur grows with speed
        sweep = min(8 + 14 * k * d / 40.0, 360.0)
        ghosts = tuple(theta - g for g in np.linspace(0, sweep, 14)[1:])
        add(theta=theta % 360, ghosts=tuple(g % 360 for g in ghosts),
            trace_until=360.0, disc=min(d / 40.0, 1.0) * 0.5,
            caption="faster…")

    # Phase C -- full speed: the circle has appeared
    n_c = 20 if quick else 60
    for k in range(n_c):
        theta = (theta + 40.0) % 360
        ghosts = tuple((theta - g) % 360
                       for g in np.linspace(0, 320, 16)[1:])
        add(theta=theta, ghosts=ghosts, trace_until=360.0, disc=0.85,
            caption="a circle appears — the disc of the farthest vertex")

    # Phase D -- decelerate to rest at 0 deg, put the triangle back
    n_d1 = 8 if quick else 18
    remaining = (360.0 - theta) % 360 + 360.0
    decel = np.cos(np.linspace(0, np.pi / 2, n_d1))
    decel = decel / decel.sum() * remaining
    for k, d in enumerate(decel):
        theta = (theta + d) % 360
        fade = 1.0 - (k + 1) / n_d1
        ghosts = tuple((theta - g) % 360
                       for g in np.linspace(0, 200 * fade + 8, 10)[1:])
        add(theta=theta, ghosts=ghosts, trace_until=360.0,
            disc=0.85 * fade, caption="…stopping")
    n_d2 = 8 if quick else 25
    for _ in range(n_d2):
        add(theta=0.0, trace_until=360.0,
            caption="the triangle, back where it began")

    # Phase E -- double it: a copy rotates 180 deg about the hypotenuse
    # midpoint, completing the square
    n_e = 15 if quick else 45
    for k in range(n_e):
        add(theta=0.0, twin_theta=180.0 * (k + 1) / n_e,
            trace_until=360.0,
            caption="double the triangle: rotate a copy 180° about the "
                    "hypotenuse midpoint")
    n_e2 = 8 if quick else 20
    for _ in range(n_e2):
        add(theta=0.0, twin_theta=180.0, trace_until=360.0,
            caption="two right triangles — a square")

    # Phase F -- spin the square: slow, then accelerate to its own circle
    n_f1 = 12 if quick else 36
    theta = 0.0
    for i in range(n_f1):
        theta += 2.5
        add(shape="square", theta=theta, radius=np.sqrt(2),
            caption="now spin the square about the same point")
    n_f2 = 25 if quick else 80
    steps = 2.5 + 37.5 * (np.linspace(0, 1, n_f2) ** 2)
    for k, d in enumerate(steps):
        theta = (theta + d) % 360
        sweep = min(8 + 14 * k * d / 40.0, 360.0)
        ghosts = tuple((theta - g) % 360
                       for g in np.linspace(0, sweep, 14)[1:])
        add(shape="square", theta=theta, ghosts=ghosts,
            disc=min(d / 40.0, 1.0) * 0.85, radius=np.sqrt(2),
            caption="…and a larger circle appears: radius √2, "
                    "the corner diagonal")
    n_f3 = 15 if quick else 45
    for _ in range(n_f3):
        theta = (theta + 40.0) % 360
        ghosts = tuple((theta - g) % 360
                       for g in np.linspace(0, 320, 16)[1:])
        add(shape="square", theta=theta, ghosts=ghosts, disc=0.85,
            radius=np.sqrt(2),
            caption="…and a larger circle appears: radius √2, "
                    "the corner diagonal")

    return frames


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_frame(desc, figsize, dpi):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, facecolor=DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_aspect("equal")
    ax.set_axis_off()

    base = TRIANGLE if desc["shape"] == "triangle" else SQUARE
    color = TRI_COLOR

    # The swept disc (the emergent circle), under everything else
    if desc["disc"] > 0:
        ax.add_patch(Circle(PIVOT, desc["radius"], facecolor=color,
                            alpha=0.30 * desc["disc"], edgecolor="none"))
        ax.add_patch(Circle(PIVOT, desc["radius"], facecolor="none",
                            edgecolor=CIRCLE_COLOR, lw=1.6,
                            alpha=desc["disc"]))

    # The traced path of the far vertex (phase A's growing arc)
    if desc["trace_until"]:
        t = np.radians(np.linspace(0, desc["trace_until"], 240))
        ax.plot(np.cos(t), np.sin(t), color=TRACE_COLOR, lw=1.1,
                alpha=0.65)

    # Motion-blur ghosts
    n_g = len(desc["ghosts"])
    for k, g in enumerate(desc["ghosts"]):
        alpha = 0.26 * (1.0 - k / max(n_g, 1))
        ax.add_patch(Polygon(rotate(base, g), closed=True,
                             facecolor=color, edgecolor="none",
                             alpha=alpha))

    # The twin triangle completing the square (phase E)
    if desc["twin_theta"] is not None:
        hyp_mid = np.array([0.5, 0.5])
        twin = rotate(TRIANGLE, desc["twin_theta"], center=hyp_mid)
        ax.add_patch(Polygon(twin, closed=True, facecolor=TWIN_COLOR,
                             edgecolor=TWIN_COLOR, lw=1.4, alpha=0.75))

    # The shape itself
    ax.add_patch(Polygon(rotate(base, desc["theta"]), closed=True,
                         facecolor=color, edgecolor="#9ecbff", lw=1.6,
                         alpha=0.92))

    # The fixed point
    ax.plot(*PIVOT, marker="o", markersize=6, color="#f85149", zorder=5)

    ax.set_title(desc["caption"], color="#e6edf3", fontsize=9, pad=8)
    fig.tight_layout(pad=0.15)
    return fig


def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=os.path.join(
        OUT_DIR, "triangle_to_circle.gif"))
    parser.add_argument("--size", type=float, default=4.2,
                        help="figure size in inches (square)")
    parser.add_argument("--dpi", type=int, default=85)
    parser.add_argument("--duration", type=int, default=20,
                        help="ms per frame in the GIF")
    parser.add_argument("--quick", action="store_true",
                        help="short test render (~200 frames)")
    parser.add_argument("--webp", action="store_true",
                        help="also write an animated WebP")
    args = parser.parse_args(argv)

    script = build_script(quick=args.quick)
    print(f"rendering {len(script)} frames…")
    images = []
    for i, desc in enumerate(script):
        images.append(fig_to_image(
            render_frame(desc, (args.size, args.size), args.dpi)))
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(script)}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    pal = [im.convert("P", palette=Image.ADAPTIVE, colors=128)
           for im in images]
    pal[0].save(args.out, save_all=True, append_images=pal[1:],
                duration=args.duration, loop=0, optimize=True)
    print(f"wrote {args.out} "
          f"({os.path.getsize(args.out) / 1e6:.1f} MB)")

    if args.webp:
        webp = args.out.rsplit(".", 1)[0] + ".webp"
        images[0].save(webp, save_all=True, append_images=images[1:],
                       duration=args.duration, loop=0, quality=75,
                       method=4)
        print(f"wrote {webp} ({os.path.getsize(webp) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
