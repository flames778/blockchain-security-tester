Here's an **updated, comprehensive `README.md`** that explains the entire system, its architecture, usage, and educational value. Replace your current `README.md` with this.

---

```markdown
# 🔒 Blockchain Security Tester

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.25-blue)](https://soliditylang.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)

**A complete, hands‑on security lab for Solidity smart contracts.**  
Scan for vulnerabilities → deploy vulnerable contracts → exploit them → apply fixes.  
Perfect for security researchers, developers, and students learning blockchain security.

---

## 📖 Table of Contents

- [What It Does](#what-it-does)
- [System Architecture](#system-architecture)
- [Vulnerabilities Covered](#vulnerabilities-covered)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [1. Run the Scanner](#1-run-the-scanner)
  - [2. Start Local Testnet](#2-start-local-testnet)
  - [3. Deploy & Exploit](#3-deploy--exploit)
  - [4. Deploy the Fixed Contract](#4-deploy-the-fixed-contract)
- [Project Structure](#project-structure)
- [Educational Value](#educational-value)
- [Extending the Tester](#extending-the-tester)
- [License](#license)

---

## 🎯 What It Does

| Capability | Description |
|------------|-------------|
| **🔍 Smart Contract Scanner** | Detects reentrancy, arithmetic overflow/underflow, and missing access control using static analysis + custom regex. |
| **💣 Exploit Scripts** | Ready‑to‑run Python scripts that attack the vulnerabilities on a local Anvil testnet. |
| **🛡️ Fixed Contracts** | Industry‑standard mitigations (`ReentrancyGuard`, `Ownable`, Solidity 0.8+). |
| **🧪 Safe Test Environment** | Everything runs locally – no real funds, no mainnet risk. |

---

## 🧩 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER TERMINAL                           │
├─────────────────────────────────────────────────────────────────┤
│  scanner.py ──► static analysis (Slither + regex)               │
│  deploy.py ───► deploys VulnerableBank.sol to Anvil             │
│  exploit_*.py ─► interacts with the deployed contract           │
│  fix/ ─────────► SecureBank.sol + deployment script             │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL TESTNET (Anvil)                         │
│  • 10 funded accounts                                           │
│  • Chain ID 31337                                               │
│  • Listens on 127.0.0.1:8545                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Vulnerabilities Covered

| Vulnerability | SWC | Attack Vector | Mitigation |
|---------------|-----|---------------|-------------|
| **Reentrancy** | SWC‑107 | External call before state update → recursive withdrawal | `ReentrancyGuard` + checks‑effects‑interactions |
| **Arithmetic Overflow** | SWC‑101 | Unsafe addition/subtraction in Solidity <0.8.0 | Use Solidity 0.8+ or SafeMath |
| **Access Control** | SWC‑105 | Public function transfers value without owner check | `onlyOwner` modifier (OpenZeppelin Ownable) |

---

## 🚀 Quick Start

### Prerequisites

- Linux (Ubuntu/Kali) or WSL2
- Python 3.8+
- Foundry (for `anvil` – local testnet)
- `solc` (Solidity compiler)

### One‑line setup (Ubuntu/Kali)

```bash
git clone https://github.com/yourusername/blockchain-security-tester.git
cd blockchain-security-tester
chmod +x scripts/setup.sh
./scripts/setup.sh
source venv/bin/activate
```

The setup script installs:
- Python virtual environment with `web3` and `slither-analyzer`
- Foundry (`anvil`, `cast`, `forge`)
- `solc` 0.8.25 static binary

---

## 📖 Usage Guide

### 1. Run the Scanner

```bash
# Simple scanner (no Slither required, works immediately)
python scanner/scanner_simple.py contracts/VulnerableBank.sol

# Full scanner (requires Slither)
python scanner/scanner.py contracts/VulnerableBank.sol
```

**Example output:**
```
🔍 Scanning contracts/VulnerableBank.sol...

📋 VULNERABILITY REPORT:

[REENTRANCY] – 1 issue(s)
  ⚠️ Line 15: (bool success, ) = msg.sender.call{value: _amount}("");
     → External call before state update (potential reentrancy)

[OVERFLOW] – 1 issue(s)
  ⚠️ Line 22: balances[msg.sender] += msg.value;
     → Arithmetic without SafeMath (overflow risk)

[ACCESS_CONTROL] – 1 issue(s)
  ⚠️ Line 26: function withdrawAll() public {
     → Function with no access control performs value transfer
```

### 2. Start Local Testnet (separate terminal)

```bash
anvil --port 8545
```

Keep it running – you will see account addresses and private keys.

### 3. Deploy & Exploit

**Compile the vulnerable contract:**
```bash
solc --bin --abi contracts/VulnerableBank.sol -o contracts/build/
```

**Deploy:**
```bash
python scripts/deploy.py
```
Output: `✅ VulnerableBank deployed at: 0x5FbDB2315678afecb367f032d93F642f64180aa3`

**Exploit access control (replace address with yours):**
```bash
python exploits/access_control_exploit.py 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

Output:
```
💰 Bank balance before: 1.0 ETH
💀 Bank balance after: 0.0 ETH (should be 0)
```

**Exploit reentrancy (advanced):**
```bash
python exploits/reentrancy_exploit.py <bank_address>
```

The reentrancy attack recursively withdraws funds until the bank is empty.

### 4. Deploy the Fixed Contract

```bash
# Compile SecureBank.sol (requires OpenZeppelin – see note)
solc --bin --abi contracts/SecureBank.sol -o contracts/build/
python scripts/deploy_secure.py
```

Now run the same exploit scripts – they will fail because:
- `nonReentrant` blocks recursive calls
- `onlyOwner` prevents unauthorized `withdrawAll()`
- Solidity 0.8+ reverts on overflow

---

## 📂 Project Structure

blockchain-security-tester/
├── README.md                     # You are here
├── scanner/
│   ├── scanner.py                # Full Slither integration
│   └── scanner_simple.py         # Lightweight regex scanner
├── contracts/
│   ├── VulnerableBank.sol        # All three vulnerabilities
│   ├── SecureBank.sol            # Fixed version (needs OpenZeppelin)
│   └── ReentrancyAttacker.sol    # Attacker contract for reentrancy
├── exploits/
│   ├── access_control_exploit.py
│   ├── reentrancy_exploit.py
│   └── overflow_demo.py          # (placeholder)
├── scripts/
│   ├── deploy.py                 # Deploy VulnerableBank
│   ├── deploy_secure.py          # Deploy SecureBank
│   └── setup.sh                  # One‑time environment setup
├── screenshots/                  # Your demo images
│   ├── scanner_output.png
│   ├── deployment.png
│   └── exploit_access.png
└── requirements.txt              # Python dependencies

---

## 🧠 Educational Value

This project is ideal for:

- Blockchain security courses– students see real attacks and fixes.
- CTF challenges – use `VulnerableBank.sol` as a target.
- Portfolio / Job applications – demonstrate hands‑on security skills.
- Internal developer training – show why access control and reentrancy guards matter.

After using this tester, you will be able to:

- Explain how reentrancy works and why the DAO hack happened.
- Identify unsafe arithmetic in legacy Solidity.
- Spot missing `onlyOwner` modifiers.
- Write secure contracts using battle‑tested patterns.

---

## 🔧 Extending the Tester

You can easily add new vulnerability detectors:

1. Add a new check in `scanner_simple.py` – e.g., front‑running via `tx.origin`:
   ```python
   if 'tx.origin' in line:
       self.results["access_control"].append(...)
   ```

2. Create a new exploit script – following the pattern of `access_control_exploit.py`.

3. Integrate Mythril for symbolic execution – see `scanner.py` for the placeholder.

---

## 📄 License

MIT – free for educational and security research use.  
No warranty; use only on networks you own or have permission to test.

---

## 🙏 Acknowledgments

- [Foundry](https://github.com/foundry-rs/foundry) for Anvil
- [Slither](https://github.com/crytic/slither) for static analysis
- [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts) for security contracts

---

Happy (ethical) hacking! 🛡️
