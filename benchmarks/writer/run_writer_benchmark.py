import os
import time
import json
from datetime import datetime

from app.services.note_writer_service import generate_note_draft
from benchmarks.writer.model_pricing import calculate_cost


MODELS = [
    "gpt-4.1-mini",
    "gpt-5-mini",
    "gpt-5.4-nano",
    "gpt-5.6-luna",
]

CASES_DIR = os.path.join("benchmarks", "writer", "cases")
RESULTS_DIR = os.path.join("benchmarks", "writer", "results")


def load_test_cases():
    cases = []

    for filename in sorted(os.listdir(CASES_DIR)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(CASES_DIR, filename)

        with open(path, "r", encoding="utf-8") as file:
            user_input = file.read().strip()

        cases.append({
            "name": filename.replace(".txt", ""),
            "filename": filename.replace("_test.txt", ""),
            "input": user_input,
        })

    return cases

def load_expectations(case_name):
    expectations_path = os.path.join(
        CASES_DIR,
        f"{case_name}.json",
    )

    if not os.path.exists(expectations_path):
        return {
            "must_contain": [],
            "must_not_contain": [],
        }

    with open(expectations_path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_output(content, expectations):
    checks = []

    for expected in expectations.get("must_contain", []):
        passed = expected in content

        checks.append({
            "type": "must_contain",
            "value": expected,
            "passed": passed,
        })

    for forbidden in expectations.get("must_not_contain", []):
        passed = forbidden not in content

        checks.append({
            "type": "must_not_contain",
            "value": forbidden,
            "passed": passed,
        })

    passed_checks = sum(check["passed"] for check in checks)
    total_checks = len(checks)

    return {
        "passed": all(check["passed"] for check in checks),
        "passed_checks": passed_checks,
        "total_checks": total_checks,
        "checks": checks,
    }


def create_run_directory():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = os.path.join(RESULTS_DIR, timestamp)

    os.makedirs(run_dir, exist_ok=True)

    return run_dir


def save_result(run_dir, case_name, model, content):
    case_dir = os.path.join(run_dir, case_name)
    os.makedirs(case_dir, exist_ok=True)

    file_path = os.path.join(case_dir, f"{model}.md")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def run_benchmark():
    cases = load_test_cases()
    run_dir = create_run_directory()
    results = []

    print("\n=== WRITER MODEL BENCHMARK ===\n")

    for case in cases:
        print(case["name"])
        expectations = load_expectations(case["name"])

        for model in MODELS:
            start_time = time.perf_counter()

            try:
                draft = generate_note_draft(
                    filename=case["filename"],
                    user_input=case["input"],
                    model=model,
                )

                elapsed = time.perf_counter() - start_time
                usage = draft["usage"]

                evaluation = evaluate_output(
                    content=draft["content"],
                    expectations=expectations,
                )

                cost = calculate_cost(
                    model=model,
                    input_tokens=usage["input_tokens"],
                    output_tokens=usage["output_tokens"],
                )

                output_path = save_result(
                    run_dir=run_dir,
                    case_name=case["name"],
                    model=model,
                    content=draft["content"],
                )

                results.append({
                    "case": case["name"],
                    "model": model,
                    "status": "success",
                    "quality_passed": evaluation["passed"],
                    "passed_checks": evaluation["passed_checks"],
                    "total_checks": evaluation["total_checks"],
                    "checks": evaluation["checks"],
                    "time_seconds": round(elapsed, 2),
                    "input_tokens": usage["input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "total_tokens": usage["total_tokens"],
                    "cost_usd": round(cost, 6) if cost is not None else None,
                    "output_file": output_path,
                })

                cost_text = f"${cost:.5f}" if cost is not None else "n/a"
                quality_status = "PASS" if evaluation["passed"] else "FAIL"

                print(
                    f"  ✓ {model:<20} "
                    f"{quality_status:<4} "
                    f"{evaluation['passed_checks']}/{evaluation['total_checks']}  "
                    f"{elapsed:>6.2f}s  "
                    f"in: {usage['input_tokens']:>5}  "
                    f"out: {usage['output_tokens']:>5}  "
                    f"cost: {cost_text}"
                )

            except Exception as error:
                elapsed = time.perf_counter() - start_time

                results.append({
                    "case": case["name"],
                    "model": model,
                    "status": "failed",
                    "time_seconds": round(elapsed, 2),
                    "error": str(error),
                })

                print(f"  ✗ {model:<20} {elapsed:.2f}s")
                print(f"    {error}")

        print()

    results_path = os.path.join(run_dir, "results.json")

    with open(results_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Benchmark complete.")
    print(f"Results saved to: {run_dir}")


if __name__ == "__main__":
    run_benchmark()