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
