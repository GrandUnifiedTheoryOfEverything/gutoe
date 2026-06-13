#!/usr/bin/env python3
"""Generate the 4D graphics used by the organization profile page.

Outputs (committed to the repository so the org README can embed them):
    gfx/4d/tesseract_rotation.gif   - double rotation of the tesseract,
                                      perspective-projected 4D -> 3D,
                                      vertex color = 4th coordinate w
    gfx/4d/field_w_sweep.gif        - scalar field f(x, y; w), the slice
                                      swept through the 4th coordinate
    gfx/4d/tesseract_still.png      - high-resolution still frame

Reproduce with:  python3 visualization/generate_4d_gifs.py
"""

import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "gfx", "4d")

DARK_BG = "#0d1117"


def _tesseract():
    verts = np.array([[(i >> k) & 1 for k in range(4)]
                      for i in range(16)], dtype=float) * 2 - 1
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16)
             if np.abs(verts[i] - verts[j]).sum() == 2.0]
    return verts, edges


def _rotate_4d(verts, theta):
    c, s = np.cos(theta), np.sin(theta)
    rot_xw = np.eye(4)
    rot_xw[0, 0], rot_xw[0, 3], rot_xw[3, 0], rot_xw[3, 3] = c, -s, s, c
    rot_yw = np.eye(4)
    rot_yw[1, 1], rot_yw[1, 3], rot_yw[3, 1], rot_yw[3, 3] = c, -s, s, c
    return verts @ rot_xw.T @ rot_yw.T


def _project(verts4, d=3.0):
    w = verts4[:, 3]
    scale = d / (d - w)
    return verts4[:, :3] * scale[:, None], w


def _tesseract_frame(theta, figsize=(5.2, 5.2), dpi=80):
    verts, edges = _tesseract()
    v4 = _rotate_4d(verts, theta)
    v3, w = _project(v4)

    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(DARK_BG)
    norm = plt.Normalize(-1.8, 1.8)
    for i, j in edges:
        ax.plot(*zip(v3[i], v3[j]), color="#4c78a8", lw=1.4, alpha=0.85)
    ax.scatter(v3[:, 0], v3[:, 1], v3[:, 2], c=w, cmap="viridis",
               norm=norm, s=46, depthshade=False, edgecolors=DARK_BG)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    ax.set_zlim(-2.3, 2.3)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=32)
    ax.set_title("Tesseract: double rotation in (x,w) and (y,w),\n"
                 "perspective-projected to 3D — color = w",
                 color="#e6edf3", fontsize=9, pad=0)
    fig.tight_layout(pad=0.1)
    return fig


def _field_frame(w, X, Y, figsize=(5.2, 4.4), dpi=80):
    r2 = X**2 + Y**2
    Z = (np.exp(-0.3 * (r2 + w**2))
         * np.cos(2 * np.sqrt(r2 + w**2) - 1.5 * w)
         + 0.25 * np.exp(-0.5 * ((X - w)**2 + Y**2)) * np.cos(3 * Y))
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor=DARK_BG)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(DARK_BG)
    ax.plot_surface(X, Y, Z, cmap=cm.viridis, vmin=-1.0, vmax=1.0,
                    linewidth=0, antialiased=True)
    ax.set_zlim(-1.05, 1.05)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=-55)
    ax.set_title(f"4D scalar field f(x, y; w) — slice w = {w:+.2f}",
                 color="#e6edf3", fontsize=9, pad=0)
    fig.tight_layout(pad=0.1)
    return fig


def _fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("P", palette=Image.ADAPTIVE)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Tesseract rotation GIF
    frames = [_fig_to_image(_tesseract_frame(t))
              for t in np.linspace(0, 2 * np.pi, 60, endpoint=False)]
    path = os.path.join(OUT_DIR, "tesseract_rotation.gif")
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=60, loop=0, optimize=True)
    print(f"wrote {path} ({os.path.getsize(path) / 1e6:.1f} MB)")

    # Field w-sweep GIF (sweep out and back for a seamless loop)
    grid = np.linspace(-3, 3, 70)
    X, Y = np.meshgrid(grid, grid)
    ws = np.concatenate([np.linspace(-2, 2, 28),
                         np.linspace(2, -2, 28)[1:-1]])
    frames = [_fig_to_image(_field_frame(w, X, Y)) for w in ws]
    path = os.path.join(OUT_DIR, "field_w_sweep.gif")
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=80, loop=0, optimize=True)
    print(f"wrote {path} ({os.path.getsize(path) / 1e6:.1f} MB)")

    # High-resolution still
    fig = _tesseract_frame(0.65, figsize=(7, 7), dpi=160)
    path = os.path.join(OUT_DIR, "tesseract_still.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), dpi=160)
    plt.close(fig)
    print(f"wrote {path} ({os.path.getsize(path) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
