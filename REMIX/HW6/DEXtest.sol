// SPDX-License-Identifier: GPL-3.0-or-later

// This file is part of the http://github.com/aaronbloomfield/ccc repository,
// and is released under the GPL 3.0 license.

pragma solidity ^0.8.16;

import "./DEX.sol";
import "./TokenCC.sol";
import "./EtherPriceOracleConstant.sol";

// See the homework description for how to use this program

contract DEXtest {

    TokenCC public tc;
    DEX public dex;

    constructor() {
        tc = new TokenCC();
        dex = new DEX();
    }

    function test() public payable {
        require (msg.value == 13 ether, "Must call test() with 13 ether");

        // Step 1: deploy the ether price oracle
        IEtherPriceOracle pricer = new EtherPriceOracleConstant();

        // Step 1 tests: DEX is deployed
        require(dex.k() == 0, "k value not 0 after DEX creation()");
        require(dex.x() == 0, "x value not 0 after DEX creation()");
        require(dex.y() == 0, "y value not 0 after DEX creation()");

        // Step 2: createPool() is called with 10 (fake) ETH and 100 TC
        bool success = tc.approve(address(dex),100*10**tc.decimals());
        require (success,"Failed to approve TC before createPool()");
        try dex.createPool{value: 10 ether}(100*10**tc.decimals(), 5, 1000, address(tc), address(pricer)) {
            // do nothing
        } catch Error(string memory reason) {
            require (false, string.concat("createPool() call reverted: ",reason));
        }
        
        // Step 2 tests
        require(dex.k() == 1e21 * 10**tc.decimals(), "k value not correct after createPool()");
        require(dex.x() == 10 * 1e18, "x value not correct after createPool()");
        require(dex.y() == 100 * 10**tc.decimals(), "y value not correct after createPool()");

        // Step 3: transaction 1, where 2.5 ETH is provided to the DEX for exchange
        payable(dex).call{value: 2.5 ether}("");
        

        // Step 3 tests
        require(dex.x() == 12.5 * 1e18, "x value not correct after giving 2.5 ether.");
        require(dex.y() == 80 * 10**tc.decimals(), "y value not correct after receiving 2.5 ether");
        require(dex.getPoolLiquidityInUSDCents() == 2500 * 10**2, "the price does not match");
        require(dex.feesToken() == 10**tc.decimals()/10, "the feesToken does not match");

        // Step 4: transaction 2, where 120 TC is provided to the DEX for exchange
        tc.transfer(address(dex), 120 * 10**tc.decimals());
  
        // Step 4 tests
        require(dex.x() == 5 * 1e18, "x value not correct after receiving 120 TC");
        require(dex.y() == 200 * 10**tc.decimals(), "y value not correct after receiving 120 TC");
        require(dex.getPoolLiquidityInUSDCents() == 1000 * 10**2, "the value does not match");
        require(dex.feesEther() == 375 * 1e14, "the feesEther does not match");
        // Step 5: addLiquidity() is called with 1 (fake) ETH and 40 TC
        bool successAL = tc.approve(address(dex),40*10**tc.decimals());
        require (successAL,"Failed to approve TC before addLiquidity");
        dex.addLiquidity{value : 1 ether}();

        // Step 5 tests
        require(dex.x() == 6 * 1e18, "x value not correct after addLiquidity");
        require(dex.y() == 240 * 10**tc.decimals(), "y value not correct after addLiquidity");
        require(dex.k() == 6 * 240 * 1e18 * 10**tc.decimals(), "k value not correct after AddLiquidity");
        require(dex.getPoolLiquidityInUSDCents() == 1200 * 10**2, "the value does not match");

        // finish up
        require(false,"end fail"); // huh?  see why in the homework description!
    }
 
    receive() external payable { } // see note in the HW description

}