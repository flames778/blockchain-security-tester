#!/usr/bin/env python3
import re
import sys
from pathlib import Path

class SimpleScanner:
    def __init__(self, contract_path):
        self.contract_path = Path(contract_path)
        self.results = {"reentrancy": [], "overflow": [], "access_control": []}
    
    def scan(self):
        print(f"🔍 Scanning {self.contract_path}...")
        with open(self.contract_path, 'r') as f:
            code = f.read()
            lines = code.split('\n')
        
        # Reentrancy
        for i, line in enumerate(lines, 1):
            if '.call{' in line and 'value:' in line:
                for j in range(i, min(i+10, len(lines))):
                    if 'balances[' in lines[j] and '-=' in lines[j]:
                        self.results["reentrancy"].append({
                            "line": i,
                            "code": line.strip(),
                            "description": "External call before state update (potential reentrancy)"
                        })
                        break
        
        # Overflow (only if pragma <0.8)
        if 'pragma solidity' in code:
            pragma_match = re.search(r'pragma solidity\s*([^;]+);', code)
            if pragma_match and any(v in pragma_match.group(1) for v in ['^0.4', '^0.5', '^0.6', '^0.7']):
                for i, line in enumerate(lines, 1):
                    if any(op in line for op in ['+=', '-=', '*=', '/=', '++', '--']):
                        if 'balances' in line or 'uint' in line:
                            self.results["overflow"].append({
                                "line": i,
                                "code": line.strip(),
                                "description": "Arithmetic without SafeMath (overflow risk)"
                            })
        
        # Access control
        for i, line in enumerate(lines, 1):
            if 'function' in line and 'public' in line:
                if 'withdrawAll' in line or 'owner' not in line:
                    for j in range(i, min(i+15, len(lines))):
                        if 'call.value' in lines[j] or 'transfer(' in lines[j]:
                            self.results["access_control"].append({
                                "line": i,
                                "code": line.strip(),
                                "description": "Function with no access control performs value transfer"
                            })
                            break
        
        return self.results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanner_simple.py <contract.sol>")
        sys.exit(1)
    scanner = SimpleScanner(sys.argv[1])
    vulns = scanner.scan()
    print("\n📋 VULNERABILITY REPORT:")
    for category, issues in vulns.items():
        print(f"\n[{category.upper()}] – {len(issues)} issue(s)")
        for issue in issues:
            print(f"  ⚠️ Line {issue['line']}: {issue['code']}")
            print(f"     → {issue['description']}")