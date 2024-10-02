// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.16;
import "./IDEX.sol";
import "./ERC20.sol";
contract DEX is IDEX{
    uint public override decimals;
    function symbol() public view override returns(string memory){
        return ERC20(erc20Address).symbol();
    }
    uint public override k;
    uint public override x;
    uint public override y;
    uint public override feeNumerator;
    uint public override feeDenominator;
    uint public override feesEther;
    uint public override feesToken;
    mapping (address => uint) override public etherLiquidityForAddress;
    mapping (address => uint) override public tokenLiquidityForAddress;
    address override public etherPricer;
    address override public erc20Address;
    bool private created = false;
    address private owner;
    bool adjustLiquidity = false;

    constructor(){
        adjustLiquidity = true;
        owner = msg.sender;
        adjustLiquidity = false;
    }

    function getEtherPrice() public view override returns(uint){
        return IEtherPriceOracle(etherPricer).price();
    }

    function getTokenPrice() public view override returns(uint){
        //adding 1 token to the pool will equal to how many eth
        return x*getEtherPrice()*(10**decimals)/((10**18)*y);
    }

    function getPoolLiquidityInUSDCents() public view override returns(uint){
        return 2*x*getEtherPrice()/(10**18);
    }

    function setEtherPricer(address p) public override{
        etherPricer = p;
    }

    function getDEXinfo() public view override returns(address, string memory, string memory, address, uint, uint, uint, uint, uint, uint, uint, uint){
        return (address(this), ERC20(erc20Address).symbol(), ERC20(erc20Address).name(), erc20Address, k, x, y, feeNumerator, feeDenominator, decimals, feesEther, feesToken);
    }

    function createPool(uint _tokenAmount, uint _feeNumerator, uint _feeDenominator, address _erc20token, address _etherPricer) external payable override{
        adjustLiquidity = true;
        require(msg.sender == owner, "This function can only be called by deployer. Revert");
        require(created == false, "Pool already created, cannot create again. Revert");
        require(ERC20(_erc20token).balanceOf(msg.sender) >= _tokenAmount, "You do not have enough token approved. Revert");
        require(_feeDenominator != 0, "Cannot set fee Denominator to 0. Revert");
        ERC20(_erc20token).transferFrom(msg.sender, address(this), _tokenAmount);
        decimals = ERC20(_erc20token).decimals();
        y = _tokenAmount;
        feeNumerator = _feeNumerator;
        feeDenominator = _feeDenominator;
        erc20Address = _erc20token;
        etherPricer = _etherPricer;
        etherLiquidityForAddress[msg.sender] += msg.value;
        tokenLiquidityForAddress[msg.sender] += _tokenAmount;
        x = msg.value;
        k = x*y;
        created = true;
        adjustLiquidity = false;
        emit liquidityChangeEvent();
    }

    function addLiquidity() external payable override{
        adjustLiquidity = true;
        uint numToken = msg.value*y/x;
        require(ERC20(erc20Address).balanceOf(msg.sender) >= numToken, "The approved number of token is less than the token to be put in. Revert");
        x += msg.value;
        y += numToken;
        k = x*y;
        tokenLiquidityForAddress[msg.sender] += numToken;
        etherLiquidityForAddress[msg.sender] += msg.value;
        adjustLiquidity = false;
        emit liquidityChangeEvent();
    }

    function removeLiquidity(uint amountEther) external override{
        adjustLiquidity = true;
        require(etherLiquidityForAddress[msg.sender] >= amountEther, "Not enough ether stored in the pool. Revert");
        uint numToken = amountEther*y/x;
        require(tokenLiquidityForAddress[msg.sender] >= numToken, "Not enough token stored in the pool. Revert");
        (bool success, ) = payable(msg.sender).call{value: amountEther}("");
        require (success, "Payment didn't work. Revert");
        bool successToken = ERC20(erc20Address).transfer(msg.sender, numToken);
        require(successToken, "Failed to transfer token back to caller. Revert");
        etherLiquidityForAddress[msg.sender] -= amountEther;
        tokenLiquidityForAddress[msg.sender] -= numToken;
        x -= amountEther;
        y -= numToken;
        k = x*y;
        adjustLiquidity = false;
        emit liquidityChangeEvent();
    }

    receive() external payable override{
        uint tokenRemaining = k/(x+msg.value);
        uint tokenToGive = y - tokenRemaining;
        uint tokenFee = tokenToGive*feeNumerator/feeDenominator;
        uint tokenGiveActual = tokenToGive - tokenFee;
        require(tokenToGive <= y, "Not enough token in the contract. Revert");
        ERC20(erc20Address).transfer(msg.sender, tokenGiveActual);
        feesToken += tokenFee;
        x += msg.value;
        y -= tokenToGive;
        emit liquidityChangeEvent();
    }

    function onERC20Received(address from, uint amount, address erc20) public override returns (bool) {
        if (!adjustLiquidity){
            require(erc20 == erc20Address, "Wrong token cryptocurrency for this DEX");
            uint etherRemaining = k/(y+amount);
            uint etherToGive = x - etherRemaining;
            uint etherFee = etherToGive*feeNumerator/feeDenominator;
            uint etherGivenActual = etherToGive - etherFee;
            (bool success, ) = payable(from).call{value: etherGivenActual}("");
            require (success, "Payment didn't work. Revert");
            feesEther += etherFee;
            x -= etherToGive;
            y += amount;
            emit liquidityChangeEvent();
            return true;
        }
        return true;
    }

    function supportsInterface(bytes4 interfaceId) override public pure returns (bool){
        return 
        interfaceId == type(IERC165).interfaceId || 
        interfaceId == type(IDEX).interfaceId ||
        interfaceId == type(IERC20Receiver).interfaceId;
    }









}