#!/usr/bin/env python3
import requests, re

def fetch_block(url, open_delim, close_delim):
    txt = requests.get(url).text
    # non-greedy match across newlines
    m = re.search(re.escape(open_delim) + r"(.*?)" + re.escape(close_delim),
                  txt, re.S)
    if not m:
        raise ValueError(f"Couldn't find {open_delim}…{close_delim} in {url}")
    return m.group(1).strip()

def fetch_nth_block(url, open_delim, close_delim, n=0):
    txt = requests.get(url).text
    # Find all matches
    matches = re.findall(re.escape(open_delim) + r"(.*?)" + re.escape(close_delim),
                        txt, re.S)
    if len(matches) <= n:
        raise ValueError(f"Couldn't find block {n+1} with {open_delim}…{close_delim} in {url}")
    return matches[n].strip()

metric_url = "https://raw.githubusercontent.com/arcticoder/warp-bubble-metric-ansatz/refs/heads/main/metric_ansatz.tex"
conn_url   = "https://raw.githubusercontent.com/arcticoder/warp-bubble-connection-curvature/refs/heads/main/connection_curvature.tex"
stress_url = "https://raw.githubusercontent.com/arcticoder/warp-bubble-einstein-equations/refs/heads/main/stress_energy.tex"

# Extract complete mathematical expressions
line_elem = fetch_nth_block(metric_url, r"\[", r"\]", 0)  # First math block
R_scalar  = fetch_nth_block(conn_url, r"\[", r"\]", 4)    # Fifth math block (Ricci scalar)
# Note: R_{μν}R^{μν} not available in current source files
T_matrix  = fetch_block(stress_url, r"\begin{pmatrix}", r"\end{pmatrix}")

with open("final_expressions.tex", "w") as f:
    f.write(r"\documentclass{article}")
    f.write(r"\usepackage{amsmath}")
    f.write(r"\usepackage[margin=0.5in]{geometry}")  # Smaller margins for wide expressions
    f.write(r"\begin{document}" + "\n\n")
    f.write(r"\section*{Metric}" + "\n")
    f.write(f"\\[ {line_elem} \\]\n\n")
    f.write(r"\section*{Curvature Invariants}" + "\n")
    f.write(f"\\[ R = {R_scalar} \\]\n")
    f.write(r"\[ R_{\mu\nu}R^{\mu\nu} = \text{(not available in source files)} \]" + "\n\n")
    f.write(r"\section*{Stress--Energy Tensor}" + "\n")
    f.write(f"\\[ T_{{\\mu\\nu}} = \\begin{{pmatrix}}{T_matrix}\\end{{pmatrix}} \\]\n")
    f.write(r"\end{document}" + "\n")

print("Generated final_expressions.tex")
