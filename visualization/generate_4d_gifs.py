#!/usr/bin/env python3
"""4D graphics generator: regular polytopes, the Clifford torus, the
3-sphere, and 4D fields, rendered as animated GIF/WebP and stills.

Every object is displayed with one of two honest techniques, named in
the title of every output:

* projection -- rotate in 4-space, then perspective-project to 3D with
  scale d/(d - w) (and let matplotlib project 3D to the 2D image);
* slicing   -- intersect with the hyperplane w = const and sweep w.

Objects
-------
tesseract     8-cell, {4,3,3}: 16 vertices, 32 edges (projection)
cell16        16-cell, {3,3,4}: 8 vertices, 24 edges (projection)
cell24        24-cell, {3,4,3}: 24 vertices, 96 edges -- the polytope
              with no 3D analogue (projection)
clifford      the Clifford torus on the 3-sphere, stereographically
              projected; an isoclinic rotation turns it inside out
              (projection)
sphere3       the 3-sphere S^3, displayed as its spherical w-slices
              (slicing)
field         a scalar field f(x, y; w), surface per w-slice (slicing)

Usage
-----
    python3 visualization/generate_4d_gifs.py                 # defaults
    python3 visualization/generate_4d_gifs.py --objects all
    python3 visualization/generate_4d_gifs.py --objects clifford,cell24 \
        --frames 90 --formats gif,webp --stills
    python3 visualization/generate_4d_gifs.py --sharp   # + web variants
                                  (tools/graphics-pipeline, needs Node)

Outputs land in gfx/4d/. The names tesseract_rotation.gif and
field_w_sweep.gif are stable -- the organization profile embeds them.
"""

import argparse
import io
import os
import subprocess
import sys
from itertools import combinations, permutations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "gfx", "4d")
DARK_BG = "#0d1117"
W_NORM = plt.Normalize(-1.8, 1.8)

# ---------------------------------------------------------------------------
# 4D geometry
# ---------------------------------------------------------------------------


def tesseract_vertices():
    verts = np.array([[(i >> k) & 1 for k in range(4)]
                      for i in range(16)], dtype=float) * 2 - 1
    edges = [(i, j) for i, j in combinations(range(16), 2)
             if np.abs(verts[i] - verts[j]).sum() == 2.0]
    return verts, edges


def cell16_vertices():
    """16-cell: vertices +-sqrt(2) e_i; every pair adjacent except
    antipodes (24 edges)."""
    verts = []
    for axis in range(4):
        for sign in (1.0, -1.0):
            v = np.zeros(4)
            v[axis] = sign * 1.4142135623730951
            verts.append(v)
    verts = np.array(verts)
    edges = [(i, j) for i, j in combinations(range(8), 2)
             if not np.allclose(verts[i], -verts[j])]
    return verts, edges


def cell24_vertices():
    """24-cell: all permutations of (+-1, +-1, 0, 0); edges join
    vertices at squared distance 2 (96 edges)."""
    seen = set()
    for pos in permutations(range(4), 2):
        for s1 in (1.0, -1.0):
            for s2 in (1.0, -1.0):
                v = [0.0] * 4
                v[pos[0]], v[pos[1]] = s1, s2
                seen.add(tuple(v))
    verts = np.array(sorted(seen))
    edges = [(i, j) for i, j in combinations(range(len(verts)), 2)
             if abs(np.sum((verts[i] - verts[j]) ** 2) - 2.0) < 1e-9]
    return verts, edges


def rotate_4d(points, theta, planes=((0, 3), (1, 3))):
    """Rotate 4D points by theta simultaneously in the given planes."""
    rot = np.eye(4)
    for a, b in planes:
        r = np.eye(4)
        c, s = np.cos(theta), np.sin(theta)
        r[a, a], r[a, b], r[b, a], r[b, b] = c, -s, s, c
        rot = r @ rot
    return points @ rot.T


def project_perspective(points4, d=3.0):
    """4D -> 3D perspective projection; returns 3D points and w."""
    w = points4[..., 3]
    scale = d / (d - w)
    return points4[..., :3] * scale[..., None], w


def project_stereographic(points4, pole=1.08):
    """Near-stereographic projection of S^3 from the w-pole (softened
    so grid lines through the pole stay finite)."""
    w = points4[..., 3]
    scale = 1.0 / (pole - w)
    return points4[..., :3] * scale[..., None], w


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _new_axes(figsize, dpi, title):
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(DARK_BG)
    ax.set_axis_off()
    ax.set_title(title, color="#e6edf3", fontsize=9, pad=0)
    return fig, ax


def polytope_frame(verts, edges, theta, title, lim, figsize, dpi,
                   elev=18, azim=32):
    v4 = rotate_4d(verts, theta)
    v3, w = project_perspective(v4)
    fig, ax = _new_axes(figsize, dpi, title)
    cmap = matplotlib.colormaps["viridis"]
    for i, j in edges:
        wm = float((w[i] + w[j]) / 2)
        color = cmap(W_NORM(wm))
        # glow: a wide faint pass under a thin bright pass
        ax.plot(*zip(v3[i], v3[j]), color=color, lw=3.2, alpha=0.18)
        ax.plot(*zip(v3[i], v3[j]), color=color, lw=1.2, alpha=0.95)
    ax.scatter(v3[:, 0], v3[:, 1], v3[:, 2], c=w, cmap="viridis",
               norm=W_NORM, s=42, depthshade=False, edgecolors=DARK_BG)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.view_init(elev=elev, azim=azim)
    fig.tight_layout(pad=0.1)
    return fig


def clifford_frame(theta, title, figsize, dpi, n_theta=36, n_phi=72):
    """Clifford torus under an isoclinic rotation, stereographically
    projected: it appears to turn inside out through infinity."""
    th = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    ph = np.linspace(0, 2 * np.pi, n_phi, endpoint=True)
    T, P = np.meshgrid(th, ph, indexing="ij")
    pts = np.stack([np.cos(T), np.sin(T), np.cos(P), np.sin(P)],
                   axis=-1) / np.sqrt(2.0)
    pts = rotate_4d(pts.reshape(-1, 4), theta,
                    planes=((0, 2), (1, 3))).reshape(n_theta, n_phi, 4)
    v3, w = project_stereographic(pts)

    fig, ax = _new_axes(figsize, dpi, title)
    cmap = matplotlib.colormaps["plasma"]
    wn = plt.Normalize(-0.75, 0.75)
    for i in range(n_theta):                      # phi-direction lines
        ax.plot(v3[i, :, 0], v3[i, :, 1], v3[i, :, 2],
                color=cmap(wn(float(w[i].mean()))), lw=0.9, alpha=0.85)
    for j in range(0, n_phi, 3):                  # theta-direction lines
        ax.plot(v3[:, j, 0], v3[:, j, 1], v3[:, j, 2],
                color=cmap(wn(float(w[:, j].mean()))), lw=0.9,
                alpha=0.85)
    lim = 2.6
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.view_init(elev=22, azim=35)
    fig.tight_layout(pad=0.1)
    return fig


def sphere3_frame(w, title, figsize, dpi):
    """w-slice of the unit 3-sphere: a 2-sphere of radius
    sqrt(1 - w^2)."""
    fig, ax = _new_axes(figsize, dpi, title)
    r = float(np.sqrt(max(1.0 - w * w, 0.0)))
    if r > 1e-3:
        u = np.linspace(0, 2 * np.pi, 48)
        v = np.linspace(0, np.pi, 24)
        U, V = np.meshgrid(u, v)
        X = r * np.cos(U) * np.sin(V)
        Y = r * np.sin(U) * np.sin(V)
        Z = r * np.cos(V)
        ax.plot_surface(X, Y, Z, color=matplotlib.colormaps["viridis"](
            plt.Normalize(-1, 1)(w)), alpha=0.75, linewidth=0,
            antialiased=True)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.view_init(elev=18, azim=32)
    fig.tight_layout(pad=0.1)
    return fig


def field_frame(w, X, Y, title, figsize, dpi):
    r2 = X**2 + Y**2
    Z = (np.exp(-0.3 * (r2 + w**2))
         * np.cos(2 * np.sqrt(r2 + w**2) - 1.5 * w)
         + 0.25 * np.exp(-0.5 * ((X - w)**2 + Y**2)) * np.cos(3 * Y))
    fig, ax = _new_axes(figsize, dpi, title)
    ax.plot_surface(X, Y, Z, cmap=cm.viridis, vmin=-1.0, vmax=1.0,
                    linewidth=0, antialiased=True)
    ax.set_zlim(-1.05, 1.05)
    ax.view_init(elev=28, azim=-55)
    fig.tight_layout(pad=0.1)
    return fig


# ---------------------------------------------------------------------------
# Object registry
# ---------------------------------------------------------------------------


def _polytope_frames(builder, name, lim, n_frames, figsize, dpi):
    verts, edges = builder()
    title = (f"{name}: double rotation in (x,w) and (y,w),\n"
             "perspective-projected to 3D — color = w")
    for t in np.linspace(0, 2 * np.pi, n_frames, endpoint=False):
        yield polytope_frame(verts, edges, t, title, lim, figsize, dpi)


def frames_tesseract(n, figsize, dpi):
    yield from _polytope_frames(
        tesseract_vertices, "Tesseract (8-cell, 32 edges)", 2.3,
        n, figsize, dpi)


def frames_cell16(n, figsize, dpi):
    yield from _polytope_frames(
        cell16_vertices, "16-cell (hyperoctahedron, 24 edges)", 2.6,
        n, figsize, dpi)


def frames_cell24(n, figsize, dpi):
    yield from _polytope_frames(
        cell24_vertices, "24-cell (96 edges, no 3D analogue)", 2.4,
        n, figsize, dpi)


def frames_clifford(n, figsize, dpi):
    title = ("Clifford torus on S³, stereographic projection —\n"
             "an isoclinic rotation turns it inside out")
    for t in np.linspace(0, np.pi, n, endpoint=False):
        yield clifford_frame(t, title, figsize, dpi)


def frames_sphere3(n, figsize, dpi):
    ws = np.concatenate([np.linspace(-1, 1, n // 2),
                         np.linspace(1, -1, n // 2)[1:-1]])
    for w in ws:
        yield sphere3_frame(
            w, f"3-sphere S³, slice w = {w:+.2f}:\n"
               f"a 2-sphere of radius √(1−w²) = "
               f"{np.sqrt(max(1 - w * w, 0)):.2f}", figsize, dpi)


def frames_field(n, figsize, dpi):
    grid = np.linspace(-3, 3, 70)
    X, Y = np.meshgrid(grid, grid)
    ws = np.concatenate([np.linspace(-2, 2, n // 2),
                         np.linspace(2, -2, n // 2)[1:-1]])
    for w in ws:
        yield field_frame(w, X, Y,
                          f"4D scalar field f(x, y; w) — slice "
                          f"w = {w:+.2f}", figsize, dpi)


OBJECTS = {
    # name: (frame generator, stable gif filename, frame duration ms)
    "tesseract": (frames_tesseract, "tesseract_rotation.gif", 60),
    "cell16": (frames_cell16, "cell16_rotation.gif", 60),
    "cell24": (frames_cell24, "cell24_rotation.gif", 60),
    "clifford": (frames_clifford, "clifford_torus.gif", 70),
    "sphere3": (frames_sphere3, "sphere3_slices.gif", 70),
    "field": (frames_field, "field_w_sweep.gif", 80),
}


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def render_object(name, n_frames, figsize, dpi, formats, stills):
    gen, gif_name, duration = OBJECTS[name]
    images = [_fig_to_image(f) for f in gen(n_frames, figsize, dpi)]
    written = []

    if "gif" in formats:
        path = os.path.join(OUT_DIR, gif_name)
        pal = [im.convert("P", palette=Image.ADAPTIVE) for im in images]
        pal[0].save(path, save_all=True, append_images=pal[1:],
                    duration=duration, loop=0, optimize=True)
        written.append(path)

    if "webp" in formats:
        path = os.path.join(OUT_DIR, gif_name.replace(".gif", ".webp"))
        images[0].save(path, save_all=True, append_images=images[1:],
                       duration=duration, loop=0, quality=80,
                       method=4)
        written.append(path)

    if stills:
        still = gen(max(8, n_frames // 8), (7, 7), 160)
        fig = None
        for k, fig_k in enumerate(still):
            if fig is not None:
                plt.close(fig)
            fig = fig_k
            if k >= 2:           # a few steps in looks better than t=0
                break
        path = os.path.join(OUT_DIR,
                            gif_name.replace(".gif", "_still.png"))
        fig.savefig(path, facecolor=fig.get_facecolor(), dpi=160)
        plt.close(fig)
        written.append(path)

    for p in written:
        print(f"wrote {p} ({os.path.getsize(p) / 1e6:.1f} MB)")
    return written


def run_sharp_pipeline():
    """Post-process gfx/4d/ with the Node/sharp web pipeline, if set up."""
    tool = os.path.join(REPO_ROOT, "tools", "graphics-pipeline")
    if not os.path.exists(os.path.join(tool, "node_modules")):
        print("sharp pipeline not installed; run "
              "`npm install` in tools/graphics-pipeline first.",
              file=sys.stderr)
        return
    subprocess.run(["node", "optimize.js", "--in", OUT_DIR,
                    "--out", os.path.join(OUT_DIR, "web")],
                   cwd=tool, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--objects", default="tesseract,field",
                        help="comma list of "
                             f"{','.join(OBJECTS)} or 'all'")
    parser.add_argument("--frames", type=int, default=60)
    parser.add_argument("--dpi", type=int, default=80)
    parser.add_argument("--size", type=float, default=5.2,
                        help="figure size in inches (square)")
    parser.add_argument("--formats", default="gif",
                        help="comma list of gif,webp")
    parser.add_argument("--stills", action="store_true",
                        help="also write a high-res PNG still")
    parser.add_argument("--sharp", action="store_true",
                        help="post-process with the Node/sharp web "
                             "pipeline (tools/graphics-pipeline)")
    args = parser.parse_args(argv)

    names = (list(OBJECTS) if args.objects == "all"
             else [n.strip() for n in args.objects.split(",")])
    unknown = [n for n in names if n not in OBJECTS]
    if unknown:
        parser.error(f"unknown objects: {unknown}; "
                     f"choose from {list(OBJECTS)}")

    os.makedirs(OUT_DIR, exist_ok=True)
    formats = [f.strip() for f in args.formats.split(",")]
    for name in names:
        render_object(name, args.frames, (args.size, args.size),
                      args.dpi, formats, args.stills)
    if args.sharp:
        run_sharp_pipeline()


if __name__ == "__main__":
    main()
