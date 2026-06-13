/* GUToE Scientific Dashboard - D3.js panels and button interactions.
 *
 * 1. Ripple effect on every .btn (material-style, pure JS + CSS).
 * 2. Pure-D3 tesseract: double rotation in the (x,w) and (y,w) planes,
 *    4D -> 3D perspective projection, drag-steerable 3D viewpoint,
 *    button-controlled speed/pause.
 * 3. Force-directed structure map of the composite action.
 *
 * D3 v7 is loaded from CDN via Dash external_scripts; Dash renders the
 * React DOM after this file loads, so both panels initialize via a short
 * poll for their containers.
 */

/* ---------- 1. Button ripples (event delegation survives re-renders) -- */
document.addEventListener("click", function (ev) {
  const btn = ev.target.closest(".btn");
  if (!btn) return;
  const rect = btn.getBoundingClientRect();
  const d = Math.max(rect.width, rect.height);
  const ripple = document.createElement("span");
  ripple.className = "ripple";
  ripple.style.width = ripple.style.height = d + "px";
  ripple.style.left = (ev.clientX - rect.left - d / 2) + "px";
  ripple.style.top = (ev.clientY - rect.top - d / 2) + "px";
  btn.appendChild(ripple);
  setTimeout(() => ripple.remove(), 600);
});

/* ---------- 2. Tesseract ---------------------------------------------- */
function initTesseract(container) {
  const W = container.clientWidth || 640;
  const H = container.clientHeight || 420;
  const svg = d3.select(container).append("svg")
    .attr("width", W).attr("height", H)
    .style("cursor", "grab");

  // 16 vertices of {-1,1}^4
  const verts = [];
  for (let i = 0; i < 16; i++) {
    verts.push([1 - 2 * (i & 1), 1 - 2 * ((i >> 1) & 1),
                1 - 2 * ((i >> 2) & 1), 1 - 2 * ((i >> 3) & 1)]);
  }
  // 32 edges at Hamming distance 1
  const edges = [];
  for (let i = 0; i < 16; i++)
    for (let j = i + 1; j < 16; j++) {
      let diff = 0;
      for (let k = 0; k < 4; k++) if (verts[i][k] !== verts[j][k]) diff++;
      if (diff === 1) edges.push([i, j]);
    }

  const state = { theta: 0, speed: 0.012, paused: false,
                  yaw: 0.6, pitch: 0.35 };
  const D4 = 3.0, scale = Math.min(W, H) / 6.2;
  const color = w => d3.interpolateViridis((w + 1.8) / 3.6);

  const edgeSel = svg.append("g").selectAll("line").data(edges).join("line")
    .attr("stroke", "#4c78a8").attr("stroke-width", 1.6)
    .attr("stroke-opacity", 0.85);
  const vertSel = svg.append("g").selectAll("circle").data(verts).join("circle")
    .attr("r", 5).attr("stroke", "#0d1117").attr("stroke-width", 1);

  function project() {
    const c = Math.cos(state.theta), s = Math.sin(state.theta);
    const cy = Math.cos(state.yaw), sy = Math.sin(state.yaw);
    const cp = Math.cos(state.pitch), sp = Math.sin(state.pitch);
    return verts.map(v => {
      // double rotation in (x,w) then (y,w)
      let [x, y, z, w] = v;
      let x1 = c * x - s * w, w1 = s * x + c * w;
      let y1 = c * y - s * w1; w1 = s * y + c * w1;
      // 4D -> 3D perspective
      const k = D4 / (D4 - w1);
      let X = x1 * k, Y = y1 * k, Z = z * k;
      // 3D viewpoint (yaw around y-axis, pitch around x-axis)
      let X2 = cy * X + sy * Z, Z2 = -sy * X + cy * Z;
      let Y2 = cp * Y - sp * Z2;
      return { x: W / 2 + scale * X2, y: H / 2 - scale * Y2, w: w1 };
    });
  }

  function draw() {
    const p = project();
    edgeSel
      .attr("x1", e => p[e[0]].x).attr("y1", e => p[e[0]].y)
      .attr("x2", e => p[e[1]].x).attr("y2", e => p[e[1]].y);
    vertSel
      .attr("cx", (d, i) => p[i].x).attr("cy", (d, i) => p[i].y)
      .attr("fill", (d, i) => color(p[i].w));
  }

  d3.timer(() => {
    if (!state.paused) { state.theta += state.speed; draw(); }
  });
  draw();

  // Drag steers the 3D viewpoint
  svg.call(d3.drag()
    .on("start", () => svg.style("cursor", "grabbing"))
    .on("drag", ev => {
      state.yaw += ev.dx * 0.008;
      state.pitch = Math.max(-1.4, Math.min(1.4, state.pitch + ev.dy * 0.008));
      draw();
    })
    .on("end", () => svg.style("cursor", "grab")));

  // Button wiring via delegation (Dash owns the buttons)
  document.addEventListener("click", function (ev) {
    const t = ev.target.closest("button");
    if (!t) return;
    if (t.id === "d3-tess-toggle") {
      state.paused = !state.paused;
      t.textContent = state.paused ? "Play" : "Pause";
    } else if (t.id === "d3-tess-slower") {
      state.speed = Math.max(0.002, state.speed / 1.6);
    } else if (t.id === "d3-tess-faster") {
      state.speed = Math.min(0.12, state.speed * 1.6);
    } else if (t.id === "d3-tess-reset") {
      state.yaw = 0.6; state.pitch = 0.35; draw();
    }
  });
}

/* ---------- 3. Force-directed structure map ---------------------------- */
function initGraph(container) {
  const dataEl = document.getElementById("d3-graph-data");
  if (!dataEl) return;
  const data = JSON.parse(dataEl.textContent);
  const W = container.clientWidth || 640;
  const H = container.clientHeight || 520;

  const GROUP_COLORS = {
    core: "#58a6ff", sector: "#79c0ff", action: "#3fb950",
    program: "#d29922", result: "#a371f7", experiment: "#f85149",
    obstacle: "#8b949e",
  };

  const svg = d3.select(container).append("svg")
    .attr("width", W).attr("height", H);

  const link = svg.append("g").selectAll("line")
    .data(data.links).join("line")
    .attr("stroke", "#30363d").attr("stroke-width", 1.4)
    .attr("stroke-dasharray", d => d.dashed ? "4 3" : null);

  const node = svg.append("g").selectAll("circle")
    .data(data.nodes).join("circle")
    .attr("r", d => d.r)
    .attr("fill", d => GROUP_COLORS[d.group] || "#8b949e")
    .attr("stroke", "#0d1117").attr("stroke-width", 1.5)
    .style("cursor", "grab");
  node.append("title").text(d => d.id);

  const label = svg.append("g").selectAll("text")
    .data(data.nodes).join("text")
    .text(d => d.id)
    .attr("font-size", 10.5).attr("fill", "#8b949e")
    .attr("pointer-events", "none");

  const sim = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(78))
    .force("charge", d3.forceManyBody().strength(-260))
    .force("center", d3.forceCenter(W / 2, H / 2))
    .force("collide", d3.forceCollide().radius(d => d.r + 14))
    .on("tick", () => {
      link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
      node.attr("cx", d => d.x = Math.max(20, Math.min(W - 20, d.x)))
          .attr("cy", d => d.y = Math.max(20, Math.min(H - 20, d.y)));
      label.attr("x", d => d.x + d.r + 4).attr("y", d => d.y + 3.5);
    });

  node.call(d3.drag()
    .on("start", (ev, d) => {
      if (!ev.active) sim.alphaTarget(0.25).restart();
      d.fx = d.x; d.fy = d.y;
    })
    .on("drag", (ev, d) => { d.fx = ev.x; d.fy = ev.y; })
    .on("end", (ev, d) => {
      if (!ev.active) sim.alphaTarget(0);
      d.fx = null; d.fy = null;
    }));

  // Hover: emphasize the node's neighborhood
  const neighbors = new Map(data.nodes.map(n => [n.id, new Set([n.id])]));
  data.links.forEach(l => {
    const s = typeof l.source === "object" ? l.source.id : l.source;
    const t = typeof l.target === "object" ? l.target.id : l.target;
    neighbors.get(s).add(t); neighbors.get(t).add(s);
  });
  node.on("mouseenter", (ev, d) => {
    const keep = neighbors.get(d.id);
    node.attr("opacity", n => keep.has(n.id) ? 1 : 0.18);
    label.attr("opacity", n => keep.has(n.id) ? 1 : 0.12)
         .attr("fill", n => keep.has(n.id) ? "#e6edf3" : "#8b949e");
    link.attr("stroke-opacity", l =>
      l.source.id === d.id || l.target.id === d.id ? 1 : 0.15)
        .attr("stroke", l =>
      l.source.id === d.id || l.target.id === d.id ? "#58a6ff" : "#30363d");
  }).on("mouseleave", () => {
    node.attr("opacity", 1);
    label.attr("opacity", 1).attr("fill", "#8b949e");
    link.attr("stroke-opacity", 1).attr("stroke", "#30363d");
  });

  // Legend
  const legend = svg.append("g").attr("transform", "translate(12,16)");
  Object.entries(GROUP_COLORS).forEach(([g, c], i) => {
    legend.append("circle").attr("cx", 0).attr("cy", i * 17).attr("r", 5)
      .attr("fill", c);
    legend.append("text").attr("x", 10).attr("y", i * 17 + 3.5).text(g)
      .attr("font-size", 10.5).attr("fill", "#8b949e");
  });
}

/* ---------- bootstrap --------------------------------------------------- */
(function waitForPanels() {
  let tessDone = false, graphDone = false;
  const poll = setInterval(() => {
    if (typeof d3 === "undefined") return;
    const tess = document.getElementById("d3-tesseract");
    const graph = document.getElementById("d3-graph");
    if (tess && !tessDone && tess.clientWidth > 0) {
      tessDone = true; initTesseract(tess);
    }
    if (graph && !graphDone && graph.clientWidth > 0) {
      graphDone = true; initGraph(graph);
    }
    if (tessDone && graphDone) clearInterval(poll);
  }, 300);
  setTimeout(() => clearInterval(poll), 30000);
})();
