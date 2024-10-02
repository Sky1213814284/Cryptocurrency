// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.16;
import "./IAuctioneer.sol";
import "./NFTManager.sol";
import "./ERC721.sol";
contract Auctioneer is IAuctioneer {
    mapping (uint => Auction) public auctions;
    uint public num_auctions;
    address public nftmanager;
    uint public totalFees;
    uint public unpaidFees;
    address public deployer;
    Auction private auction;
    mapping (uint => bool) private nft_auctioning;

    constructor() {
        nftmanager = address(new NFTManager());
        deployer = msg.sender;
    }

    function collectFees() public override{
        require(msg.sender == deployer, "Only deployer of the auction can collect fee. Revert");
        (bool success, ) = payable(deployer).call{value: unpaidFees}("");
        require(success, "Failed to transfer ETH");
        unpaidFees = 0;
    }

    function startAuction(uint m, uint h, uint d, string memory data, uint reserve, uint nftid) public override returns (uint){
        bool timeValidity = true;
        if (m == 0 && h == 0 && d == 0){
            timeValidity = false;
        }
        require(timeValidity, "Invalid auction lasting time. Revert");
        bool dataValidity = true;
        if (bytes(data).length == 0){
            dataValidity = false;
        }
        require(dataValidity, "Invalid description of the auction, Revert");
        bool reserveValidity = true;
        if (reserve < 0){
            reserveValidity = false;
        }
        require(reserveValidity, "Reserve cannot be lower than 0. Revert");
        bool onGoingAuction = true;
        if (nft_auctioning[nftid] == true){
            onGoingAuction = false;
        }
        require(onGoingAuction, "The auction regarding the provided nftid already exists. Revert");
        //get the address of current contract
        address owner = IERC721(nftmanager).ownerOf(nftid);
        require(owner == msg.sender, "Only the owner of the nft can initiate the auction. Revert");
        IERC721(nftmanager).transferFrom(owner, address(this), nftid);
        uint endTime = block.timestamp + m * 1 minutes + h * 1 hours + d * 1 days;
        uint auctionId = num_auctions;
        auction.id = auctionId;
        auction.num_bids = 0;
        auction.data = data;
        auction.highestBid = reserve;
        auction.winner = msg.sender;
        auction.initiator = msg.sender;
        auction.nftid = nftid;
        auction.endTime = endTime;
        auction.active = true;
        auctions[auctionId] = auction;
        emit auctionStartEvent(auctionId);
        num_auctions++;
        auctions[auctionId] = auction;
        nft_auctioning[nftid] = true;
        return auctionId;
    }

    function auctionTimeLeft(uint id) public view override returns (uint){
        uint endTime = auctions[id].endTime;
        if(endTime > block.timestamp){
            return endTime - block.timestamp;
        }
        return 0;
    }

    function closeAuction(uint id) public override{
        require(block.timestamp >= auctions[id].endTime, "The end time of this auction is not reached. Revert");
        if (auctions[id].num_bids == 0){
            IERC721(nftmanager).safeTransferFrom(address(this), auctions[id].initiator, auctions[id].nftid);
            auctions[id].active = false;
        } else{
            IERC721(nftmanager).safeTransferFrom(address(this), auctions[id].winner, auctions[id].nftid);
            totalFees += auctions[id].highestBid/100;
            unpaidFees += auctions[id].highestBid/100;
            uint transToInitiator = auctions[id].highestBid - auctions[id].highestBid/100;
            (bool success, ) = payable(auctions[id].initiator).call{value: transToInitiator}("");
            require(success, "Failed to transfer ETH back to the auction deployer");
            auctions[id].active = false;
        }
        emit auctionCloseEvent(id);
    }

    function placeBid(uint id) public payable override{
        require(auctions[id].active, "The auction is not longer active. Revert");
        require(block.timestamp < auctions[id].endTime, "Already passed the end time of the auction. Revert.");
        require(msg.value > auctions[id].highestBid, "You must place a bid that is higher than the current bid. Revert");
        (bool success, ) = payable(auctions[id].winner).call{value: auctions[id].highestBid}("");
        require(success, "Failed to transfer ETH back to the current winner");
        auctions[id].highestBid = msg.value;
        auctions[id].winner = msg.sender;
        auctions[id].num_bids++;
        emit higherBidEvent(id);
    }

    function supportsInterface(bytes4 interfaceId) override public pure returns (bool){
        return 
        interfaceId == type(IERC165).interfaceId || 
        interfaceId == type(IAuctioneer).interfaceId;
    }

}