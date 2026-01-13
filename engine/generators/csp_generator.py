import json
import random
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional


class CSPGenerator:
    # Tags that trigger data generation
    DATA_TRIGGER_TAGS = {'requires_calculation', 'hybrid'}
    
    # Default fallback template if JSON file is empty or not found
    DEFAULT_TEMPLATE = "Se dă următoarea problemă CSP:"
    
    def __init__(self, templates_path: Optional[str] = None):
        self.csp_templates = []
        
        if templates_path:
            try:
                with open(templates_path, 'r', encoding='utf-8') as f:
                    all_templates = json.load(f)
                # Filter templates that have 'csp' in tags
                self.csp_templates = [
                    t for t in all_templates 
                    if 'csp' in t.get('tags', [])
                ]
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # Log warning but continue with empty list
                print(f"Warning: Could not load CSP templates from {templates_path}: {e}")
                self.csp_templates = []

    def _generate_csp_data(self):
        """
        Generate a random CSP instance with random variables, domains, constraints,
        and a partial assignment.
        """
        # 1. Random number of variables (3 to 5)
        available_vars = ['A', 'B', 'C', 'D', 'E']
        num_variables = random.randint(3, 5)
        variables = available_vars[:num_variables]
        
        # 2. Random domains for each variable
        # Domain sizes can be 2 or 3 elements
        domains = {}
        for var in variables:
            domain_size = random.randint(2, 3)
            domains[var] = list(range(1, domain_size + 1))
        
        # 3. Random constraints (create a connected graph)
        constraints = []
        # Ensure connectivity: create a chain first
        for i in range(len(variables) - 1):
            constraints.append((variables[i], variables[i + 1]))
        
        # Add additional random edges (0 to 2 extra constraints)
        num_extra_constraints = random.randint(0, min(2, len(variables) - 2))
        for _ in range(num_extra_constraints):
            # Pick two random non-adjacent variables
            var1, var2 = random.sample(variables, 2)
            # Avoid duplicate constraints
            if (var1, var2) not in constraints and (var2, var1) not in constraints:
                constraints.append((var1, var2))
        
        # 4. Random partial assignment (assign one variable)
        assigned_var = random.choice(variables)
        assigned_value = random.choice(domains[assigned_var])
        partial_assignment = {assigned_var: assigned_value}
        
        return variables, domains, constraints, partial_assignment

    def _format_csp_data_string(self, data) -> str:
        """Format the CSP data as a structured string."""
        variables, domains, constraints, partial_assignment = data
        
        # Format constraints in human-readable form
        constraint_strings = [f"{c[0]} ≠ {c[1]}" for c in constraints]
        constraints_text = ", ".join(constraint_strings)
        
        data_text = (
            f"Variabile: {variables}\n"
            f"Domenii: {domains}\n"
            f"Constrângeri: {constraints_text}\n"
            f"Asignare parțială: {partial_assignment}"
        )
        return data_text

    def generate(self, template_id: Optional[str] = None) -> Dict[str, Any]:
        # Select template
        selected_template = None
        
        if template_id and self.csp_templates:
            # Try to find specific template by ID
            selected_template = next(
                (t for t in self.csp_templates if t['id'] == template_id),
                None
            )
        
        if not selected_template and self.csp_templates:
            # Random selection from available templates
            selected_template = random.choice(self.csp_templates)
        
        # Use template text or fallback
        if selected_template:
            template_text = selected_template['template']
            final_template_id = selected_template['id']
            template_tags = set(selected_template.get('tags', []))
        else:
            template_text = self.DEFAULT_TEMPLATE
            final_template_id = 'csp-default'
            template_tags = set()
        
        # CSP questions always need raw_data for evaluation
        # Generate CSP data for all questions
        data = self._generate_csp_data()
        variables, domains, constraints, partial_assignment = data
        question_text = template_text + "\n\n" + self._format_csp_data_string(data)
        
        # Include template tags in raw_data for evaluation logic
        raw_data = {
            'variables': variables,
            'domains': domains,
            'constraints': constraints,
            'partial_assignment': partial_assignment,
            'tags': list(template_tags),
        }
        
        return {
            'question_text': question_text,
            'raw_data': raw_data,
            'template_id': final_template_id,
        }
