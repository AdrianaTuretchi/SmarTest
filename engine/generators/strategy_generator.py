import random
from typing import Dict, Any

class StrategyGenerator:
    """
    Generates specific instances for Strategy Selection questions by processing
    generation rules and replacing placeholders in the template text.
    """
    
    def generate(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        # Deep copy to avoid modifying the original template
        result = {
            "id": template_data.get("id"),
            "template": template_data.get("template"),
            "tags": template_data.get("tags", []),
            "raw_data": template_data.get("raw_data", {}).copy(),
            "template_id": template_data.get("template_id")
        }
        
        raw_data = result['raw_data']
        rules = raw_data.get('generation_rules', {})
        problem_type = raw_data.get('problem_type')
        
        generated_params = {}

        # Logic for N-Queens
        if problem_type == 'n-queens':
            n_val = random.choice(rules.get('values', [8]))
            generated_params = {'n_value': n_val}
            result['template'] = result['template'].replace('{{n_value}}', str(n_val))

        # Logic for Graph Coloring with multiple scenario types
        elif problem_type == 'graph-coloring':
            scenario_type = raw_data.get('scenario_type', 'standard')
            num_nodes_range = rules.get('num_nodes_range', [10, 30])
            is_tree = rules.get('is_tree', False)
            density = rules.get('density', 'medium')
            
            # Generate random number of nodes within range
            num_nodes = random.randint(num_nodes_range[0], num_nodes_range[1])
            
            generated_params = {
                'num_nodes': num_nodes,
                'scenario_type': scenario_type,
                'is_tree': is_tree,
                'density': density
            }
            
            result['template'] = result['template'].replace('{{num_nodes}}', str(num_nodes))

        # Logic for Scenarios (Hanoi, Knights Tour)
        elif problem_type in ['hanoi', 'knights-tour']:
            scenarios = rules.get('scenarios', [])
            if scenarios:
                scenario = random.choice(scenarios)
                generated_params = scenario
                
                # Replace all keys in the scenario dictionary
                for key, val in scenario.items():
                    placeholder = f"{{{{{key}}}}}"
                    result['template'] = result['template'].replace(placeholder, str(val))

        # Update raw_data with the specific generated parameters
        # Remove generation_rules to clean up the output
        if 'generation_rules' in result['raw_data']:
            del result['raw_data']['generation_rules']
            
        result['raw_data'].update(generated_params)

        # Populate the question_text field using the template
        result['question_text'] = result['template']

        return result