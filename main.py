import os
import sys
from dotenv import load_dotenv
from harness.runner import load_prompts, run_attack, save_results
from harness.parser import parse_results
from harness.report_gen import generate_report

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
PROMPTS_DIR = "prompts"
RESULTS_DIR = "results"
REPORTS_DIR = "reports"

ATTACK_CONFIGS = [
    {
        "file": f"{PROMPTS_DIR}/basic_injection.txt",
        "attack_type": "Prompt Injection — Direct Instruction Override"
    },
]
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  LLM RED TEAM HARNESS v0.1")
    print("  by @ShaheerSec | github.com/Shaheer-Cybersec")
    print("=" * 60)
    print(f"\n[*] Target model : {MODEL}")
    print(f"[*] Attack configs: {len(ATTACK_CONFIGS)}")

    all_results_files = []

    for config in ATTACK_CONFIGS:
        prompts_file = config["file"]
        attack_type = config["attack_type"]

        if not os.path.exists(prompts_file):
            print(f"\n[!] Prompts file not found: {prompts_file} — skipping.")
            continue

        # Step 1 — Load prompts
        prompts = load_prompts(prompts_file)
        print(f"\n[*] Loaded {len(prompts)} prompts from {prompts_file}")

        # Step 2 — Run attack
        results = run_attack(MODEL, prompts, attack_type)

        # Step 3 — Save raw results
        results_file = save_results(results, RESULTS_DIR, attack_type.replace(" ", "_").replace("—", "-"))
        all_results_files.append(results_file)

    if not all_results_files:
        print("\n[!] No results generated. Check your prompts files.")
        sys.exit(1)

    # Step 4 — Parse most recent results file
    latest_results = all_results_files[-1]
    parsed_data = parse_results(latest_results)

    # Step 5 — Generate HTML report
    report_path = generate_report(parsed_data, MODEL, REPORTS_DIR)

    print("\n" + "=" * 60)
    print("  RUN COMPLETE")
    print(f"  Results : {latest_results}")
    print(f"  Report  : {report_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()