import numpy as np
import pandas as pd
from computation_graph import GraphRunner

class MonteCarlo:

    def __init__(self, model: GraphRunner, mc_inputs: list, iterations=100):
        self.mc_inputs = mc_inputs
        self.model = model
        self.iterations = iterations

    def make_mc_inputs(self):
        
        # mc_df = pd.DataFrame({"i": np.arange(1,self.iterations+1)})
        mc_df = pd.DataFrame()

        for input in self.mc_inputs:
            value = self.model.G.nodes[input.node]["value"]
            print(value)

            array = np.random.normal(value, value*input.uncertainty, self.iterations)
            mc_df[input.node] = array
            
        return mc_df
    
    def run_mc(self, mc_df):

        flux_nodes = mc_df.columns.values
        static_nodes = [node for node in self.model.G.nodes if node not in flux_nodes]
        # print(flux_nodes, static_nodes)

        mc_results = []
        for i, row in mc_df.iterrows():
            # print(row.index)
            
            inputs = self.model.inputs
            # print(inputs)
            for node in flux_nodes:
                inputs[node] = row[node]
            
            self.model.inputs = inputs
            self.model.run()

            #@TODO make this agnostic to input data.
            mc_results.append(self.model.query_results("closing_costs")["closing_costs"])
        
        mc_df['results'] = np.array(mc_results)

        return mc_df
