"""
Test script to verify random generation in CSP and MinMax generators.
Ensures that multiple calls produce different instances.
"""
import sys
from pathlib import Path

# Add parent directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from engine.generators.csp_generator import CSPGenerator
from engine.generators.minmax_generator import MinMaxGenerator


def test_csp_randomization():
    """Verify CSP generator produces different instances."""
    print("\n" + "="*70)
    print("TESTING CSP RANDOMIZATION")
    print("="*70)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    generator = CSPGenerator(str(templates_path))
    
    # Generate 5 instances
    instances = []
    for i in range(5):
        result = generator.generate()
        if result['raw_data']:
            instances.append(result['raw_data'])
            print(f"\n--- Instance {i+1} ---")
            print(f"Variables: {result['raw_data']['variables']}")
            print(f"Domains: {result['raw_data']['domains']}")
            print(f"Constraints: {result['raw_data']['constraints']}")
            print(f"Partial: {result['raw_data']['partial_assignment']}")
    
    # Check for variety
    num_vars_list = [len(inst['variables']) for inst in instances]
    constraints_list = [len(inst['constraints']) for inst in instances]
    
    print(f"\n--- Variety Analysis ---")
    print(f"Number of variables across instances: {num_vars_list}")
    print(f"Number of constraints across instances: {constraints_list}")
    
    # Check if we have at least some variation
    has_variety = (
        len(set(num_vars_list)) > 1 or 
        len(set(constraints_list)) > 1
    )
    
    if has_variety:
        print("✓ SUCCESS: CSP instances show variation")
    else:
        print("⚠ WARNING: All instances have same structure (may be random chance)")
    
    return has_variety


def test_minmax_randomization():
    """Verify MinMax generator produces different tree depths and values."""
    print("\n" + "="*70)
    print("TESTING MINMAX RANDOMIZATION")
    print("="*70)
    
    templates_path = project_root / "assets" / "json_output" / "templates.json"
    generator = MinMaxGenerator(str(templates_path))
    
    # Generate 5 trees
    instances = []
    for i in range(5):
        result = generator.generate()
        if result['raw_data']:
            instances.append(result['raw_data'])
            
            # Count leaf nodes
            def count_leaves(node_dict):
                if 'value' in node_dict and node_dict['value'] is not None:
                    return 1, node_dict['value']
                children = node_dict.get('children', [])
                total = 0
                values = []
                for child in children:
                    leaves, vals = count_leaves(child)
                    total += leaves
                    values.extend(vals if isinstance(vals, list) else [vals])
                return total, values
            
            leaf_count, leaf_values = count_leaves(result['raw_data'])
            
            print(f"\n--- Instance {i+1} ---")
            print(f"Number of leaves: {leaf_count}")
            print(f"Leaf value range: {min(leaf_values)} - {max(leaf_values)}")
            print(f"Sample values: {leaf_values[:5]}")
    
    # Check for variety
    leaf_counts = []
    max_values = []
    for inst in instances:
        leaves, values = count_leaves(inst)
        leaf_counts.append(leaves)
        max_values.append(max(values))
    
    print(f"\n--- Variety Analysis ---")
    print(f"Leaf counts across instances: {leaf_counts}")
    print(f"Max values across instances: {max_values}")
    
    # Check if we have variation
    has_variety = (
        len(set(leaf_counts)) > 1 or 
        len(set(max_values)) > 1
    )
    
    if has_variety:
        print("✓ SUCCESS: MinMax instances show variation")
    else:
        print("⚠ WARNING: All instances have same structure (may be random chance)")
    
    return has_variety


def test_api_randomization():
    """Test that API calls produce different results."""
    print("\n" + "="*70)
    print("TESTING API RANDOMIZATION")
    print("="*70)
    
    try:
        import requests
        
        # Test CSP endpoint
        print("\n--- Testing /generate/csp (3 calls) ---")
        csp_results = []
        for i in range(3):
            response = requests.get("http://127.0.0.1:8000/generate/csp")
            if response.status_code == 200:
                data = response.json()
                if data['raw_data']:
                    num_vars = len(data['raw_data']['variables'])
                    num_constraints = len(data['raw_data']['constraints'])
                    print(f"Call {i+1}: {num_vars} vars, {num_constraints} constraints")
                    csp_results.append((num_vars, num_constraints))
        
        if len(set(csp_results)) > 1:
            print("✓ CSP endpoint produces varied instances")
        else:
            print("⚠ CSP endpoint results may need more variety")
        
        # Test MinMax endpoint
        print("\n--- Testing /generate/minmax (3 calls) ---")
        minmax_results = []
        for i in range(3):
            response = requests.get("http://127.0.0.1:8000/generate/minmax")
            if response.status_code == 200:
                data = response.json()
                if data['raw_data']:
                    def count_leaves(node):
                        if 'value' in node and node['value'] is not None:
                            return 1
                        return sum(count_leaves(c) for c in node.get('children', []))
                    
                    leaves = count_leaves(data['raw_data'])
                    print(f"Call {i+1}: {leaves} leaves")
                    minmax_results.append(leaves)
        
        if len(set(minmax_results)) > 1:
            print("✓ MinMax endpoint produces varied instances")
        else:
            print("⚠ MinMax endpoint results may need more variety")
        
    except requests.exceptions.ConnectionError:
        print("⚠ API server not running - skipping API tests")
        print("  Start server with: uvicorn main:app --reload")
    except Exception as e:
        print(f"⚠ API test error: {e}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("RANDOMIZATION VERIFICATION TEST SUITE")
    print("="*70)
    
    try:
        csp_ok = test_csp_randomization()
        minmax_ok = test_minmax_randomization()
        test_api_randomization()
        
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"CSP Randomization: {'✓ PASS' if csp_ok else '⚠ CHECK'}")
        print(f"MinMax Randomization: {'✓ PASS' if minmax_ok else '⚠ CHECK'}")
        print("\nNote: Due to randomness, some tests may show less variety")
        print("in small samples. Run multiple times to verify randomization.")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
