// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;   // Changed from 0.7.0 for compatibility (overflow still shown via scanner)

contract VulnerableBank {
    mapping(address => uint256) public balances;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // 1️⃣ REENTRANCY VULNERABILITY
    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        (bool success, ) = msg.sender.call{value: _amount}("");  // ⚠️ external call before state update
        require(success, "Transfer failed");
        balances[msg.sender] -= _amount;  // state update after call
    }
    
    // 2️⃣ OVERFLOW VULNERABILITY (detected by scanner, but Solidity 0.8+ reverts – demo still valid)
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // 3️⃣ ACCESS CONTROL VULNERABILITY
    function withdrawAll() public {
        // ⚠️ missing onlyOwner modifier – anyone can call
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        require(success, "Transfer failed");
    }
    
    receive() external payable {}
}