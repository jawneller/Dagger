import networkx as nx
import matplotlib.pyplot as plt
import inspect
import warnings

class ComputationGraph:

    def __init__(self, formula_source):
        # calculation_params = 1
        self.G = nx.DiGraph()
        self.formula_source = formula_source
        self.formulas = formula_source()
        self._method_map = self._create_method_map()

    def _create_method_map(self) -> dict:

        # Collect all methods in the formaulas class that don't start with an underscore
        # By convention, these will be our 'formulas'
        all_members = dir(self.formulas)
        public_methods = [
            member for member in all_members
            if callable(getattr(self.formulas, member)) and not member.startswith('_')
        ]

        # --- Crate mapping dictionary with keys as method name and values as a list of parameters --- #
        method_parameter_mapping = {}
        for method_name in public_methods:

            # --- get method object and parameters --- #
            method_obj = getattr(self.formula_source, method_name)
            params = inspect.signature(method_obj).parameters.items()

            # --- method_obj, params = self._get_method_obj_w_parameters(method_name) --- #
            method_parameter_mapping[method_name] = dict()
            method_parameter_mapping[method_name]["method_obj"] = method_obj
            method_parameter_mapping[method_name]["params"] = [param[0] for param in params]

        return method_parameter_mapping

    def create_graph(self) -> None:

        # Add nodes - one per method and parameter
        for method_name in self._method_map.keys():

            # print(f"adding node for {method_name}")
            self.G.add_node(
                method_name,
                func=self._method_map[method_name]['method_obj'],
                args=self._method_map[method_name]['params'],
                value=None
            )

        # Add edge from the parameter nodes to respective target methods
        for method_name in self._method_map.keys():
            for param in self._method_map[method_name]['params']:
                self.G.add_edge(param, method_name)

        return None

    def get_required_inputs(self) -> list:
        """Output a list of nodes that are roots of the tree and thus require inputs"""

        return [node for node, degree in self.G.in_degree() if degree == 0]

    def run_graph(self, inputs) -> None:

        # --- Create dictionary of dictionaries to set node attributes --- #
        dod = {}
        for k, v in inputs.items():
            dod[k] = dict()
            dod[k]["value"] = v
            if k not in self.G.nodes:
                warnings.warn(
                    f"'{k}' was provided as an input but is not a node in the graph"
                )

        nx.set_node_attributes(self.G, dod)

        # --- Run the graph --- #
        for node in nx.topological_sort(self.G):
            # print("node: ", node)
            func = self.G.nodes[node].get("func")
            if func:
                argmap = self.G.nodes[node]["args"]
                inputs = {arg: self.G.nodes[arg]["value"] for arg in argmap}
                # print("inputs: ", inputs)
                self.G.nodes[node]["value"] = func(**inputs)

        return None

    def query_results(self, nodes=None) -> dict:

        if nodes:
            G = self.G.subgraph(nodes).nodes
        else:
            G = self.G.nodes
        
        return dict(G.data("value"))

def visualize_graph(G):
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()