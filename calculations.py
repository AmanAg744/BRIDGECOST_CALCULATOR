class CostCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def calculate_costs(self, span_length, width, traffic_volume, design_life):
        """Calculate costs for both steel and concrete bridges."""
        cost_data = self.db_manager.fetch_all_cost_data()
        results = []
        
        for material_data in cost_data:
            (material, base_rate, maintenance_rate, repair_rate, demolition_rate, 
             env_factor, social_factor, delay_factor) = material_data
            
            # Calculate area-based costs
            area = span_length * width
            construction_cost = area * base_rate
            maintenance_cost = area * maintenance_rate * design_life
            repair_cost = area * repair_rate
            demolition_cost = area * demolition_rate
            environmental_cost = area * env_factor
            
            # Calculate traffic-based costs
            social_cost = traffic_volume * social_factor * design_life
            user_cost = traffic_volume * delay_factor * design_life
            
            # Calculate total cost
            total_cost = (construction_cost + maintenance_cost + repair_cost +
                         demolition_cost + environmental_cost + social_cost + user_cost)
            
            # Compile results
            results.append([
                material,
                construction_cost,
                maintenance_cost,
                repair_cost,
                demolition_cost,
                environmental_cost,
                social_cost,
                user_cost,
                total_cost
            ])
        
        return results
    
    @staticmethod
    def get_cost_components():
        """Return list of cost component names."""
        return [
            "Construction Cost",
            "Maintenance Cost",
            "Repair Cost",
            "Demolition Cost",
            "Environmental Cost",
            "Social Cost",
            "User Cost",
            "Total Cost"
        ]