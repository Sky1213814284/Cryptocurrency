// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.16;
import "./IDAO.sol";
import "./NFTManager.sol";

contract DAO is IDAO {
    //variables
    mapping (uint => Proposal) public override proposals;
    uint constant public override minProposalDebatePeriod = 600;
    address public override tokens;
    string constant public override purpose = "To get to a grad school";
    mapping (address => mapping (uint => bool)) public override votedYes;
    mapping (address => mapping (uint => bool)) public override votedNo;
    uint public override numberOfProposals;
    string constant public override howToJoin = "Create a weChat account and add SkYyZzz7 as friend to apply";
    uint public override reservedEther;
    address public override curator;
    Proposal private prop;
    mapping (address => bool) private membership;
    mapping (address => uint) private tokenIDmapping;

    constructor(){
        tokens = address(new NFTManager());
        //set the deployer as curator
        curator = msg.sender;
        //set membership pf the curator to be true;
        membership[msg.sender] = true;
        //mint an nft for the deployer
        //addMember(msg.sender);
        string memory uri = substring(Strings.toHexString(msg.sender),2,34);
        uint nftid = NFTManager(tokens).mintWithURI(msg.sender, uri);
        tokenIDmapping[msg.sender] = nftid;
    }

    receive() external payable override{
    }

    function newProposal(address recipient, uint amount, string memory description, uint debatingPeriod) public payable returns (uint){
        require(membership[msg.sender], "You are not a member of the DAO. Revert");
        require(debatingPeriod >= minProposalDebatePeriod, "Minimum debate period is 600. Please select a longer period. Revert");
        require(msg.value <= address(msg.sender).balance, "You don't have enough ether to pay. Revert.");
        require(msg.value + address(this).balance >= amount + reservedEther, "The money in the contract is not enough to pay when the proposal is due. Revert");
        prop.recipient = recipient;
        prop.amount = amount;
        prop.description = description;
        reservedEther += amount;
        prop.creator = msg.sender;
        prop.yea = 0;
        prop.nay = 0;
        prop.votingDeadline = block.timestamp + debatingPeriod * 1 seconds;
        prop.open = true;
        uint pid = numberOfProposals;
        proposals[pid] = prop;
        emit NewProposal(numberOfProposals, recipient, amount, description);
        numberOfProposals++;
        return pid;
    }

    function vote(uint proposalID, bool supportsProposal) public override{
        require(isMember(msg.sender), "You are not a member of the DAO. Revert");
        require(proposals[proposalID].votingDeadline != 0, "The proposal ID is not created. Revert");
        require(proposals[proposalID].open, "The proposal is closed. Revert");
        require(!votedYes[msg.sender][proposalID] && !votedNo[msg.sender][proposalID], "You already voted. Revert");
        if(supportsProposal){
            proposals[proposalID].yea ++;
            votedYes[msg.sender][proposalID] = true;
        }else{
            proposals[proposalID].nay ++;
            votedNo[msg.sender][proposalID] = true;
        }
        emit Voted(proposalID, supportsProposal, msg.sender);
    }

    function closeProposal(uint proposalID) public override{
        require(isMember(msg.sender), "You are not a member of the DAO. Revert");
        require(proposals[proposalID].votingDeadline != 0, "The proposal ID is not created. Revert");
        require(proposals[proposalID].open, "The proposal is already been closed. Revert");
        require(proposals[proposalID].votingDeadline <= block.timestamp, "The voting deadline is not reached yet. Revert");
        bool pass = false;
        if(proposals[proposalID].yea >= proposals[proposalID].nay){
            pass = true;
        }
        if(pass){
            (bool success, ) = payable(proposals[proposalID].recipient).call{value: proposals[proposalID].amount}("");
            require(success, "Failed to transfer ETH to the proposal recipient");
            proposals[proposalID].proposalPassed = true;
        }
        proposals[proposalID].open = false;
        reservedEther -= proposals[proposalID].amount;
        emit ProposalClosed(proposalID, pass);
    }

    function isMember(address who) public view override returns (bool){
        bool member = true;
        if(!membership[who]){
            member = false;
        }
        if(NFTManager(tokens).balanceOf(who) <= 0){
            member = false;
        }
        return member;  
    }

    function substring(string memory str, uint startIndex, uint endIndex) private pure returns (string memory) {
        bytes memory strBytes = bytes(str);
        bytes memory result = new bytes(endIndex-startIndex);
        for(uint i = startIndex; i < endIndex; i++)
            result[i-startIndex] = strBytes[i];
        return string(result);
}

    function addMember(address who) public override{
        require(isMember(msg.sender), "Only member of DAO can add member. Revert");
        //32-character url to mint a new nft
        string memory uri = substring(Strings.toHexString(who),2,34);
        uint nftid = NFTManager(tokens).mintWithURI(who, uri);
        tokenIDmapping[who] = nftid;
        membership[who] = true;
    }

    function requestMembership() public pure{
        revert();
    }

    function supportsInterface(bytes4 interfaceId) override public pure returns (bool){
        return 
        interfaceId == type(IERC721).interfaceId || 
        interfaceId == type(IERC165).interfaceId || 
        interfaceId == type(IDAO).interfaceId;
    }



}