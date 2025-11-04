from engine.question_generator import QuestionGenerator
from engine.evaluation_engine import EvaluationEngine
from core_logic.nash_equilibrium import find_pure_nash

def main():
    # Inițializare module
    generator = QuestionGenerator("assets/json_output/templates.json")
    evaluator = EvaluationEngine()

    # Generăm 5 întrebări
    questions = [generator.generate_question_by_type("nash") for _ in range(5)]

    print("\n=== ÎNTREBĂRILE ===\n")
    for idx, q in enumerate(questions, 1):
        print(f"Întrebarea {idx}:\n{q['question_text']}\n")

    print("\n=== TESTUL ===\n")
    for idx, q in enumerate(questions, 1):
        print(f"Întrebarea {idx}:\n{q['question_text']}")
        user_answer = input("Răspunsul tău (format: (r, c)): ")

        correct_solution = find_pure_nash(q['raw_data'])
        score = evaluator.evaluate_nash_answer(user_answer, correct_solution)

        print(f" Scorul tău: {score * 100:.2f}%")
        print(f" Răspunsul corect era: {correct_solution}\n")

if __name__ == "__main__":
    main()
