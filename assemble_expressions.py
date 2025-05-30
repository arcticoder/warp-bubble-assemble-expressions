#!/usr/bin/env python3
import requests, re

def fetch_between(url, start, end):
    txt = requests.get(url).text
    parts = txt.split(start, 1)
    if len(parts) < 2:
        raise ValueError(f"Couldn't find start '{{start}}' in {{url}}")
    parts = parts[1].split(end, 1)
    if len(parts) < 2:
        raise ValueError(f"Couldn't find end '{{end}}' in {{url}}")
    return parts[0].strip()

metric_url = "https://raw.githubusercontent.com/arcticoder/warp-bubble-metric-ansatz/refs/heads/main/metric_ansatz.tex"
conn_url   = "https://raw.githubusercontent.com/arcticoder/warp-bubble-connection-curvature/refs/heads/main/connection_curvature.tex"
stress_url = "https://raw.githubusercontent.com/arcticoder/warp-bubble-einstein-equations/refs/heads/main/stress_energy.tex"

line_elem = fetch_between(metric_url, "\[", "\]")
R_scalar  = fetch_between(conn_url, "Ricci scalar", "$")
Ricci_sq  = fetch_between(conn_url, "R_{\\mu\\nu}R^{\\mu\\nu} =", "$")
T_matrix  = fetch_between(stress_url, "\\begin{pmatrix}", "\\end{pmatrix}")

with open("final_expressions.tex", "w") as f:
    f.write(r"\documentclass{article}\usepackage{amsmath}\begin{document}\n")
    f.write(r"\section*{Metric}\n")
    f.write(f"\\[ {line_elem} \\]\n")
    f.write(r"\section*{Curvature Invariants}\n")
    f.write(f"\\[ R = {R_scalar} \\]\n")
    f.write(f"\\[ R_{{\\mu\\nu}}R^{{\\mu\\nu}} = {Ricci_sq} \\]\n")
    f.write(r"\section*{Stress–Energy Tensor}\n")
    f.write(f"\\[ T_{{\\mu\\nu}} = \\begin{{pmatrix}}{T_matrix}\\end{{pmatrix}} \\]\n")
    f.write(r"\end{document}\n")

print("Generated final_expressions.tex")
