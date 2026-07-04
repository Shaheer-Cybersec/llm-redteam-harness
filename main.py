import os
import sys
from dotenv import load_dotenv
from harness.runner import load_prompts, run_attack, save_results
from harness.parser import parse_results
from harness.report_gen import generate_report

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
PROMPTS_DIR = "prompts"
RESULTS_DIR = "results"
REPORTS_DIR = "reports"

PROMPT_FILES = [
    f"{PROMPTS_DIR}/basic_injection.txt",
]
# ─────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print("  LLM RED TEAM HARNESS v0.1")
    print("  by @ShaheerSec | github.com/Shaheer-Cybersec")
    print("=" * 60)
    print(f"\n[*] Target model : {MODEL}")
    print(f"[*] Prompt files : {len(PROMPT_FILES)}")

    all_entries = []
    for prompts_file in PROMPT_FILES:
        if not os.path.exists(prompts_file):
            print(f"\n[!] Prompts file not found: {prompts_file} — skipping.")
            continue
        entries = load_prompts(prompts_file)
        print(f"[*] Loaded {len(entries)} prompts from {prompts_file}")
        all_entries.extend(entries)

    if not all_entries:
        print("\n[!] No prompts loaded. Check your prompts files.")
        sys.exit(1)

    # Step 1 — Run attack across all loaded (category, prompt) pairs
    results = run_attack(MODEL, all_entries)

    # Step 2 — Save raw results
    results_file = save_results(results, RESULTS_DIR, run_label="full_run")

    # Step 3 — Parse results
    parsed_data = parse_results(results_file)

    # Step 4 — Generate HTML report
    report_path = generate_report(parsed_data, MODEL, REPORTS_DIR)

    print("\n" + "=" * 60)
    print("  RUN COMPLETE")
    print(f"  Results : {results_file}")
    print(f"  Report  : {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()