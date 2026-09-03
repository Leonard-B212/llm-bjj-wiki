import os
import time
from datetime import datetime

from app.services.note_writer_service import generate_note_draft


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

    print("\n=== WRITER MODEL BENCHMARK ===\n")

    for case in cases:
        print(case["name"])

        for model in MODELS:
            start_time = time.perf_counter()

            try:
                draft = generate_note_draft(
                    filename=case["filename"],
                    user_input=case["input"],
                    model=model,
                )

                elapsed = time.perf_counter() - start_time

                save_result(
                    run_dir=run_dir,
                    case_name=case["name"],
                    model=model,
                    content=draft["content"],
                )

                print(f"  ✓ {model:<20} {elapsed:.2f}s")

            except Exception as error:
                elapsed = time.perf_counter() - start_time

                print(f"  ✗ {model:<20} {elapsed:.2f}s")
                print(f"    {error}")

        print()

    print("Benchmark complete.")
    print(f"Results saved to: {run_dir}")


if __name__ == "__main__":
    run_benchmark()