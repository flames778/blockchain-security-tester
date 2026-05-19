#!/usr/bin/env python3
"""
Blockchain Security Scanner
Checks Solidity contracts for:
- Reentrancy (SWC-107)
- Arithmetic overflow/underflow (SWC-101)
- Access control issues (missing modifiers, tx.origin abuse)
"""

import subprocess
import json
import re
import sys
from pathlib import Path

class SolidityScanner:
    def __init__(self, contract_path):
        self.contract_path = Path(contract_path)
        self.results = {"reentrancy": [], "overflow": [], "access_control": []}
    
    def run_slither(self):
        try:
            result = subprocess.run(
                ["slither", str(self.contract_path), "--json", "-"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            for detector in data.get("detectors", []):
                if "reentrancy" in detector["check"].lower():
                    for elem in detector["elements"]:
                        self.results["reentrancy"].append({
                            "contract": elem["type_specific_fields"]["parent"]["name"],
                            "function": elem["name"],
                            "line": elem["line"],
                            "description": detector["description"]
                        })
                if "access control" in detector["check"].lower() or "tx.origin" in detector["description"].lower():
                    for elem in detector["elements"]:
                        self.results["access_control"].append({
                            "contract": elem["type_specific_fields"]["parent"]["name"],
                            "function": elem["name"],
                            "line": elem["line"],
                            "description": detector["description"]
                        })
        except Exception as e:
            print(f"Slither failed: {e}")
    
    def detect_overflow_manual(self):
        with open(self.contract_path, 'r') as f:
            code = f.read()
        if "pragma solidity" in code:
            pragma_line = re.search(r"pragma solidity\s*([^;]+);", code)
            if pragma_line:
                version = pragma_line.group(1)
                if any(op in version for op in ["^0.4", "^0.5", "^0.6", "^0.7"]):
                    arithmetic = re.finditer(r"\b(\w+)\s*(\+=|-=|\*=|\/=|\+\+|--)\b", code)
                    for match in arithmetic:
                        line_no = code[:match.start()].count('\n') + 1
                        self.results["overflow"].append({
                            "line": line_no,
                            "code": match.group(),
                            "description": "Potential arithmetic overflow/underflow (SafeMath recommended)"
                        })
    
    def scan(self):
        print(f"🔍 Scanning {self.contract_path}...")
        self.run_slither()
        self.detect_overflow_manual()
        return self.results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <contract.sol>")
        sys.exit(1)
    scanner = SolidityScanner(sys.argv[1])
    vulns = scanner.scan()
    print("\n📋 VULNERABILITY REPORT:")
    for category, issues in vulns.items():
        print(f"\n[{category.upper()}] – {len(issues)} issue(s)")
        for issue in issues:
            print(f"  ⚠️ {issue}")
