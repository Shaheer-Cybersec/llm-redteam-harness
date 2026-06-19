import os
from datetime import datetime
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Red Team Report — {{ model }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', monospace; background: #0a0a0f; color: #e0e0e0; padding: 40px; }
        .header { border-bottom: 2px solid #00ff9d; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { font-size: 28px; color: #00ff9d; letter-spacing: 2px; }
        .header p { color: #888; margin-top: 8px; font-size: 14px; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-left: 10px; }
        .badge-critical { background: #ff003c22; color: #ff003c; border: 1px solid #ff003c; }
        .badge-high { background: #ff6b0022; color: #ff6b00; border: 1px solid #ff6b00; }
        .badge-unknown { background: #ffffff22; color: #aaa; border: 1px solid #aaa; }
        .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
        .summary-card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 8px; padding: 20px; text-align: center; }
        .summary-card .number { font-size: 36px; font-weight: bold; color: #00ff9d; }
        .summary-card .number.danger { color: #ff003c; }
        .summary-card .number.warning { color: #ff6b00; }
        .summary-card .label { font-size: 12px; color: #888; margin-top: 6px; letter-spacing: 1px; text-transform: uppercase; }
        .section-title { font-size: 16px; color: #00ff9d; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; border-left: 3px solid #00ff9d; padding-left: 12px; }
        .finding { background: #12121a; border: 1px solid #1e1e2e; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
        .finding.vulnerable { border-left: 3px solid #ff003c; }
        .finding.resisted { border-left: 3px solid #00ff9d; }
        .finding-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .finding-id { font-size: 12px; color: #888; }
        .finding-status { font-size: 12px; font-weight: bold; padding: 3px 10px; border-radius: 4px; }
        .status-vulnerable { background: #ff003c22; color: #ff003c; border: 1px solid #ff003c; }
        .status-resisted { background: #00ff9d22; color: #00ff9d; border: 1px solid #00ff9d; }
        .owasp-tag { font-size: 11px; color: #888; margin-bottom: 10px; }
        .owasp-tag span { color: #7c7cff; font-weight: bold; }
        .prompt-box { background: #0d0d14; border: 1px solid #1e1e2e; border-radius: 4px; padding: 12px; margin-bottom: 10px; font-size: 13px; color: #ff6b00; font-family: monospace; }
        .response-box { background: #0d0d14; border: 1px solid #1e1e2e; border-radius: 4px; padding: 12px; font-size: 13px; color: #c0c0c0; font-family: monospace; max-height: 150px; overflow-y: auto; }
        .flag-reason { font-size: 12px; color: #888; margin-top: 10px; font-style: italic; }
        .label-small { font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #1e1e2e; text-align: center; color: #444; font-size: 12px; }
        .footer span { color: #00ff9d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚡ LLM RED TEAM REPORT</h1>
        <p>Target Model: <strong style="color:#fff">{{ model }}</strong> &nbsp;|&nbsp; Generated: {{ timestamp }} &nbsp;|&nbsp; Tool: llm-redteam-harness v0.1</p>
    </div>

    <div class="summary-grid">
        <div class="summary-card">
            <div class="number">{{ summary.total_prompts }}</div>
            <div class="label">Total Attacks</div>
        </div>
        <div class="summary-card">
            <div class="number danger">{{ summary.flagged }}</div>
            <div class="label">Vulnerabilities Found</div>
        </div>
        <div class="summary-card">
            <div class="number">{{ summary.resisted }}</div>
            <div class="label">Attacks Resisted</div>
        </div>
        <div class="summary-card">
            <div class="number warning">{{ summary.risk_score }}%</div>
            <div class="label">Risk Score</div>
        </div>
    </div>

    <div class="section-title">Detailed Findings</div>

    {% for finding in results %}
    <div class="finding {{ 'vulnerable' if finding.flagged else 'resisted' }}">
        <div class="finding-header">
            <span class="finding-id">#{{ finding.id }} — {{ finding.attack_type }}</span>
            <span class="finding-status {{ 'status-vulnerable' if finding.flagged else 'status-resisted' }}">
                {{ '⚠ VULNERABLE' if finding.flagged else '✓ RESISTED' }}
            </span>
        </div>
        <div class="owasp-tag">
            OWASP LLM Top 10: <span>{{ finding.owasp.id }} — {{ finding.owasp.title }}</span>
            <span class="badge badge-{{ finding.owasp.severity.lower() }}">{{ finding.owasp.severity }}</span>
        </div>
        <div class="label-small">Attack Prompt</div>
        <div class="prompt-box">{{ finding.prompt }}</div>
        <div class="label-small">Model Response</div>
        <div class="response-box">{{ finding.response }}</div>
        <div class="flag-reason">{{ finding.flag_reason }}</div>
    </div>
    {% endfor %}

    <div class="footer">
        Generated by <span>llm-redteam-harness</span> — Built by <span>@ShaheerSec</span> | github.com/Shaheer-Cybersec/llm-redteam-harness
    </div>
</body>
</html>
"""

def generate_report(parsed_data: dict, model: str, output_dir: str) -> str:
    """Render HTML report from parsed results."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_dir}/report_{timestamp}.html"
    
    template = Template(HTML_TEMPLATE)
    html = template.render(
        model=model,
        timestamp=datetime.now().strftime("%B %d, %Y %H:%M:%S"),
        summary=parsed_data["summary"],
        results=parsed_data["results"]
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n[+] HTML Report generated: {output_path}")
    return output_path