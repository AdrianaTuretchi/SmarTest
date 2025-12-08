"""
Test script to verify API endpoints return feedback_text.
"""
import requests
import json


BASE_URL = "http://127.0.0.1:8000"


def test_nash_endpoint():
    """Test Nash generation and evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing Nash API Endpoints")
    print("="*60)
    
    # Generate question
    print("\n1. Generating Nash question...")
    response = requests.get(f"{BASE_URL}/generate/nash")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Question generated (template_id: {data.get('template_id')})")
        raw_data = data['raw_data']
        
        # Submit evaluation (wrong answer to test feedback)
        print("\n2. Submitting evaluation (intentionally wrong)...")
        eval_payload = {
            "user_answer": "0,0",
            "raw_data": raw_data
        }
        eval_response = requests.post(f"{BASE_URL}/evaluate/nash", json=eval_payload)
        print(f"Status: {eval_response.status_code}")
        
        if eval_response.status_code == 200:
            eval_data = eval_response.json()
            print(f"\nScore: {eval_data['score']}")
            print(f"Correct coords: {eval_data['correct_coords']}")
            print(f"\n{'='*60}")
            print("FEEDBACK TEXT:")
            print('='*60)
            print(eval_data.get('feedback_text', 'NO FEEDBACK'))
            print('='*60)
        else:
            print(f"❌ Evaluation failed: {eval_response.text}")
    else:
        print(f"❌ Generation failed: {response.text}")


def test_csp_endpoint():
    """Test CSP generation and evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing CSP API Endpoints")
    print("="*60)
    
    # Generate question
    print("\n1. Generating CSP question...")
    response = requests.get(f"{BASE_URL}/generate/csp")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Question generated (template_id: {data.get('template_id')})")
        raw_data = data['raw_data']
        
        # Submit evaluation (correct answer)
        print("\n2. Submitting evaluation...")
        eval_payload = {
            "user_answer": {"A": 1, "B": 2, "C": 1},
            "raw_data": raw_data
        }
        eval_response = requests.post(f"{BASE_URL}/evaluate/csp", json=eval_payload)
        print(f"Status: {eval_response.status_code}")
        
        if eval_response.status_code == 200:
            eval_data = eval_response.json()
            print(f"\nScore: {eval_data['score']}")
            print(f"Correct assignment: {eval_data['correct_assignment']}")
            print(f"\n{'='*60}")
            print("FEEDBACK TEXT:")
            print('='*60)
            print(eval_data.get('feedback_text', 'NO FEEDBACK'))
            print('='*60)
        else:
            print(f"❌ Evaluation failed: {eval_response.text}")
    else:
        print(f"❌ Generation failed: {response.text}")


def test_minmax_endpoint():
    """Test MinMax generation and evaluation with feedback."""
    print("\n" + "="*60)
    print("Testing MinMax API Endpoints")
    print("="*60)
    
    # Generate question
    print("\n1. Generating MinMax question...")
    response = requests.get(f"{BASE_URL}/generate/minmax")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Question generated (template_id: {data.get('template_id')})")
        raw_data = data['raw_data']
        
        # Submit evaluation (partially correct)
        print("\n2. Submitting evaluation...")
        eval_payload = {
            "root_value": 5,
            "visited_count": 2,
            "raw_data": raw_data
        }
        eval_response = requests.post(f"{BASE_URL}/evaluate/minmax", json=eval_payload)
        print(f"Status: {eval_response.status_code}")
        
        if eval_response.status_code == 200:
            eval_data = eval_response.json()
            print(f"\nScore: {eval_data['score']}")
            print(f"Correct root value: {eval_data['correct_root_value']}")
            print(f"Correct visited count: {eval_data['correct_visited_count']}")
            print(f"\n{'='*60}")
            print("FEEDBACK TEXT:")
            print('='*60)
            print(eval_data.get('feedback_text', 'NO FEEDBACK'))
            print('='*60)
        else:
            print(f"❌ Evaluation failed: {eval_response.text}")
    else:
        print(f"❌ Generation failed: {response.text}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("API INTEGRATION TEST - FEEDBACK TEXT")
    print("="*60)
    
    try:
        test_nash_endpoint()
        test_csp_endpoint()
        test_minmax_endpoint()
        
        print("\n" + "="*60)
        print("✅ ALL API TESTS COMPLETED")
        print("="*60)
        print("\nThe Swagger UI is available at:")
        print("http://127.0.0.1:8000/docs")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
