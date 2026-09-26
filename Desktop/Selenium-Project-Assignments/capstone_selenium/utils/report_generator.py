"""
report_generator.py
--------------------
Satisfies capstone requirement #10: "Generate execution report".

pytest-html already produces a full run report (see pytest.ini), but this
module builds an additional lightweight, self-contained HTML summary per
test case -- listing each automation step, its status, timestamp, and a
link to the matching screenshot. Useful for demo purposes since it doesn't
require opening the pytest-html file.
"""

import os
import time

REPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Execution Report - {case_id}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 30px; background: #f7f7f9; }}
  h1 {{ color: #222; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; }}
  th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }}
  th {{ background: #333; color: #fff; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  .PASS {{ color: green; font-weight: bold; }}
  .FAIL {{ color: red; font-weight: bold; }}
  .meta {{ margin-bottom: 15px; color: #555; }}
  img.thumb {{ max-width: 160px; border: 1px solid #ccc; border-radius: 4px; }}
</style>
</head>
<body>
  <h1>Selenium Execution Report</h1>
  <div class="meta">
    <p><b>Test case:</b> {case_id}</p>
    <p><b>Generated:</b> {generated_at}</p>
    <p><b>Overall result:</b> <span class="{overall_class}">{overall_status}</span></p>
  </div>
  <table>
    <tr><th>#</th><th>Step</th><th>Status</th><th>Timestamp</th><th>Screenshot</th></tr>
    {rows}
  </table>
</body>
</html>
"""

_ROW_TEMPLATE = """<tr>
  <td>{idx}</td>
  <td>{step}</td>
  <td class="{status_class}">{status}</td>
  <td>{timestamp}</td>
  <td>{screenshot_cell}</td>
</tr>"""


class ExecutionReport:
    """Collects steps for one test case, then renders an HTML report."""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.steps = []  # list of dicts: step, status, timestamp, screenshot

    def log_step(self, step: str, status: str = "PASS", screenshot_path: str = None):
        self.steps.append(
            {
                "step": step,
                "status": status,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "screenshot": screenshot_path,
            }
        )

    def render(self) -> str:
        os.makedirs(REPORT_DIR, exist_ok=True)
        overall_status = "FAIL" if any(s["status"] == "FAIL" for s in self.steps) else "PASS"

        rows_html = []
        for i, s in enumerate(self.steps, start=1):
            if s["screenshot"] and os.path.exists(s["screenshot"]):
                rel = os.path.relpath(s["screenshot"], REPORT_DIR)
                screenshot_cell = f'<a href="{rel}" target="_blank"><img class="thumb" src="{rel}"></a>'
            else:
                screenshot_cell = "-"

            rows_html.append(
                _ROW_TEMPLATE.format(
                    idx=i,
                    step=s["step"],
                    status=s["status"],
                    status_class=s["status"],
                    timestamp=s["timestamp"],
                    screenshot_cell=screenshot_cell,
                )
            )

        html = _HTML_TEMPLATE.format(
            case_id=self.case_id,
            generated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            overall_status=overall_status,
            overall_class=overall_status,
            rows="\n".join(rows_html),
        )

        out_path = os.path.join(REPORT_DIR, f"report_{self.case_id}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        return out_path
