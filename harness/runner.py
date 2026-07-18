import ollama
import json
import os
from datetime import datetime


def load_prompts(filepath: str) -> list:
    """Parse prompts with their categories from '# CATEGORY:' headers.
    Returns a list of (attack_type, prompt) tuples."""
    entries = []
    current_category = "Uncategorized"
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("# CATEGORY:"):
                current_category = line.replace("# CATEGORY:", "").strip()
            elif line.startswith("#"):
                continue
            else:
                entries.append((current_category, line))
    return entries


def run_attack(model: str, entries: list) -> list:
    """Send each (attack_type, prompt) pair to the model and collect responses."""
    results = []
    total = len(entries)
    print(f"\n[*] Starting run — {total} prompts")
    print(f"[*] Model: {model}\n")

    for i, (attack_type, prompt) in enumerate(entries, 1):
        print(f"[{i}/{total}] {attack_type[:50]}")
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response["message"]["content"]
        except Exception as e:
            content = f"ERROR: {str(e)}"

        result = {
            "id": i,
            "model": model,
            "attack_type": attack_type,
            "prompt": prompt,
            "response": content,
            "timestamp": datetime.now().isoformat(),
            "flagged": False,
            "flag_reason": ""
        }
        results.append(result)
        print(f"    Response captured ({len(content)} chars)")

    return results


def save_results(results: list, output_dir: str, run_label: str = "run") -> str:
    """Save results to JSONL file."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{run_label}_{timestamp}.jsonl"
    with open(filename, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    print(f"\n[+] Results saved to: {filename}")
    return filename
