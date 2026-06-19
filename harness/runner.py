import ollama
import json
import os
from datetime import datetime

def load_prompts(filepath: str) -> list:
    """Load attack prompts from a text file, one per line."""
    with open(filepath, "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return prompts

def run_attack(model: str, prompts: list, attack_type: str) -> list:
    """Send each prompt to the model and collect responses."""
    results = []
    
    print(f"\n[*] Starting attack: {attack_type}")
    print(f"[*] Model: {model}")
    print(f"[*] Total prompts: {len(prompts)}\n")
    
    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] Sending prompt...")
        
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = {
                "id": i,
                "attack_type": attack_type,
                "prompt": prompt,
                "response": response["message"]["content"],
                "timestamp": datetime.now().isoformat(),
                "flagged": False,
                "flag_reason": ""
            }
            
        except Exception as e:
            result = {
                "id": i,
                "attack_type": attack_type,
                "prompt": prompt,
                "response": f"ERROR: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "flagged": False,
                "flag_reason": ""
            }
        
        results.append(result)
        print(f"    Response captured ({len(result['response'])} chars)")
    
    return results

def save_results(results: list, output_dir: str, attack_type: str) -> str:
    """Save results to JSONL file."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{attack_type}_{timestamp}.jsonl"
    
    with open(filename, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")
    
    print(f"\n[+] Results saved to: {filename}")
    return filename