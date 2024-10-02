// SPDX-License-Identifier: GPL-3.0-or-later
//"Yufei Zhou yz5zys"
pragma solidity ^0.8.16;

import "./INFTManager.sol";
import "./ERC721.sol";
contract NFTManager is INFTManager, ERC721 {

    constructor() ERC721("SkyNFT", "SNFT"){
    }

    function supportsInterface(bytes4 interfaceId) override(IERC165,ERC721) public pure returns (bool){
        return 
        interfaceId == type(IERC721).interfaceId || 
        interfaceId == type(IERC721Metadata).interfaceId || 
        interfaceId == type(IERC165).interfaceId || 
        interfaceId == type(INFTManager).interfaceId;
    }

    uint public override count;

    mapping (uint => string) private tokenName;
    mapping (string => bool) private nameValidity;

    function tokenURI(uint256 tokenID) public override(ERC721, IERC721Metadata) view returns(string memory){
        string memory base = "https://collab.its.virginia.edu/access/content/group/e9ad2fbb-faca-414b-9df1-6f9019e765e9/ipfs/";
        require(tokenID <= count, "Provided invalid token ID, revert.");
        return string.concat(base, tokenName[tokenID]);
    }

    function mintWithURI(address _to, string memory _uri) public override returns (uint){
        require(nameValidity[_uri] == false, "The name is already taken, revert.");
        uint256 tokenID = count;
        _mint(_to, tokenID);
        count++;
        nameValidity[_uri] = true;
        tokenName[tokenID] = _uri;
        return tokenID;
    }

    function mintWithURI(string memory _uri) public override returns(uint){
        return mintWithURI(msg.sender, _uri);
    }



}