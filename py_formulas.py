class RealEstateFormulas:
    """Real Estate Property Investment Calcs"""

    # def property_taxes(tax_rate, purchase_price):
    #     return tax_rate * purchase_price
    
    def closing_costs(purchase_price, closing_costs_multiplier):
        return purchase_price * closing_costs_multiplier
    
    def total_equity_investment(down_payment, purchase_price, closing_costs, renovations_at_purchase):
        return (
            down_payment * (
                purchase_price + closing_costs + renovations_at_purchase
            )
        )


# @TODO move to dedicated units module
MGD_TO_GPM = 694.44
METERS_TO_FT = 3.28

class EngineeringFormulas:

    def pipe_diameter(flow_rate, path_to_pipe_sizer, envelope_agg: str) -> float:

        # df_pipe_sizing 

        # pipe_diameter = df_pipe_sizing[df_pipe_sizing["Flow Rate (MGD)"] == flow_rate]["Diameter (inch)"].agg(envelope_agg)

        return 3 #float(pipe_diameter)

    def head_loss_per_100ft(flow_rate, pipe_diameter, c) -> float:

        flow_rate_gpm = flow_rate * MGD_TO_GPM

        h100ft = (
            (0.2083 * (100 / c) ** 1.852) *
            (flow_rate_gpm ** 1.852) /
            (pipe_diameter ** 4.8655)
        )

        return h100ft

    def head_loss(head_loss_per_100ft, pipe_length) -> float:
        """Convert head loss per 100 ft to actual head loss based on pipe distance"""

        return head_loss_per_100ft * pipe_length * METERS_TO_FT / 100

    def total_head(head_loss, elevation_change) -> float:
        """Total head (aka differential head) combines head losses for elevation and frictional head loss"""

        return head_loss + elevation_change

    def pump_power(flow_rate, total_head, specific_gravity, pump_efficiency) -> float:

        return flow_rate * MGD_TO_GPM * total_head * specific_gravity / (3960 * pump_efficiency)
   
    def pipe_unit_construction_costs(path_to_pipe_costs) -> int:

        return 3

    def pipe_cost_multipliers(path_to_cost_multipliers) -> int:

        return 3

    def pipe_capex(
            location_multiplier, pipe_unit_construction_costs, flow_rate,
            pipe_diameter, pipe_cost_multipliers, pipe_length
        ) -> float:

        """Estimate the CAPEX cost of the pipe itself"""

        # Import unit costs
        construction_cost_per_in_per_lf = (
            pipe_unit_construction_costs[
                pipe_unit_construction_costs["Flow Rate (MGD)"] == flow_rate
            ]["Construction Cost (Materials+Labor)[$/in/LF]"].iloc[0]
        )
        print(construction_cost_per_in_per_lf)

        # Calc consolidated unit price per LF
        construction_cost_per_lf = construction_cost_per_in_per_lf * pipe_diameter
        print(construction_cost_per_lf)

        # Import cost multiplier
        cost_multiplier = pipe_cost_multipliers["Cost Multiplier (TX)"].sum()
        print(cost_multiplier)

        # Cost per LF
        total_cost_per_lf = construction_cost_per_lf * (1 + cost_multiplier) * location_multiplier
        print(total_cost_per_lf)

        pipe_capex = total_cost_per_lf * pipe_length

        return pipe_capex