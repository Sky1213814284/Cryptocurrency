// SPDX-License-Identifier: GPL-3.0-or-later

// This file is part of the http://github.com/aaronbloomfield/ccc repoistory,
// and is released under the GPL 3.0 license.

pragma solidity ^0.8.16;
import "./ITokenCC.sol";
import "./ERC20.sol"; 
import "./IERC20Receiver.sol";

contract TokenCC is ITokenCC, ERC20 {
    constructor() ERC20("SkyDollar(TM)", "SKYD") {
        _mint(msg.sender, 1000000 * 10**10);
    }

    function decimals() public override(ERC20, IERC20Metadata) pure returns (uint8){
        return 10;
    }

    function supportsInterface(bytes4 interfaceId) external pure returns (bool){
        return 
        interfaceId == type(IERC165).interfaceId || 
        interfaceId == type(IERC20).interfaceId || 
        interfaceId == type(IERC20Metadata).interfaceId || 
        interfaceId == type(ITokenCC).interfaceId;
    }

    function requestFunds() public pure override{
        revert();
    }

    function _afterTokenTransfer(address from, address to, uint256 amount) internal override {
        if ( to.code.length > 0  && from != address(0) && to != address(0) ) {
            IERC20Receiver(to).onERC20Received(from, amount, address(this));
        }
    }
}