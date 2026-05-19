// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureBank is ReentrancyGuard, Ownable {
    mapping(address => uint256) public balances;
    
    constructor() Ownable(msg.sender) {}
    
    // ✅ FIXED: checks‑effects‑interactions + reentrancy guard
    function withdraw(uint256 _amount) external nonReentrant {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        balances[msg.sender] -= _amount;
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");
    }
    
    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }
    
    // ✅ FIXED: only owner can withdraw all
    function withdrawAll() external onlyOwner {
        (bool success, ) = owner().call{value: address(this).balance}("");
        require(success, "Transfer failed");
    }
    
    receive() external payable {}
}