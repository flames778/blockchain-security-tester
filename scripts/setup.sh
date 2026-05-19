#!/bin/bash
# One‑time setup script for Ubuntu/Kali

echo "🔧 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip git curl build-essential

echo "📦 Installing Foundry (anvil)..."
curl -L https://foundry.paradigm.xyz | bash
foundryup

echo "📦 Installing solc..."
# Download static binary
mkdir -p ~/bin
wget -O ~/bin/solc https://github.com/ethereum/solidity/releases/download/v0.8.25/solc-static-linux
chmod +x ~/bin/solc
export PATH="$HOME/bin:$PATH"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc

echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install web3 slither-analyzer

echo "📂 Creating build directory for compiled contracts..."
mkdir -p contracts/build

echo "✅ Setup complete. To activate the environment, run: source venv/bin/activate"