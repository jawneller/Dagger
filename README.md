# Dagger
A small toolkit to turn calculations into a directed acyclic graph (DAG), run the computations, and inspect intermediate results, using the "entry points" of Python code or Excel.

## What it does
- Build a computation graph from a class of calculation functions (`GraphFactory` / `GraphFactoryPython`).
- Run the graph with inputs and capture intermediate and final values (`GraphRunner`).
- Visualize the graph to audit the calculation flow and graph the dependencies (`visualize_graph_nx`, `visualize_graph_dot`).
- (In Progress) Build a graph from an Excel workbook (`GraphFactoryExcel`).

## Project layout
- `dagger/` — core code (`computation_graph.py`, `monte_carlo.py`, `visualization.py`, `__init__.py`).
- `examples/demo.ipynb` — walkthrough notebook for the Python entry point.
- `examples/Formula Test.xlsx` — demo workbook referenced in the notebook.
- `dev_notebooks/` — scratch/dev notebooks.

## Quickstart
```bash
# clone
git clone <this repo URL>
cd dagger

# (optional) create conda env
conda create -n dagger-env python=3.11 -y
conda activate dagger-env


# install
pip install --upgrade pip
pip install -e .                   # editable install for local dev
# or: pip install -r requirements.txt
```

## Usage (from the demo notebook)
Define your calculations as static methods on a class (no `__init__`, and parameter names must match upstream method names):
```python
class RealEstateCalcs:
    @staticmethod
    def purchase_price():
        return 300_000

    @staticmethod
    def rehab_costs():
        return 25_000

    @staticmethod
    def closing_costs(purchase_price, rehab_costs):
        return purchase_price * 0.02 + rehab_costs * 0.01
```

Build and run the graph:
```python
from dagger import GraphFactoryPython, GraphRunner

gf = GraphFactoryPython()
gf.build_graph_from_code(RealEstateCalcs)

runner = GraphRunner(gf, inputs={})
runner.run()
print(runner.query_results())      # intermediate + output values
```

To visualize dependencies during development/audits:
```python
from dagger import visualize_graph_dot
visualize_graph_dot(gf.G)
```

For a full walkthrough (including notes on inputs/outputs and color-coding of nodes), open `examples/demo.ipynb`.
