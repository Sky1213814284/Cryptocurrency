// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.16;

import "./IGradebook.sol";

contract Gradebook is IGradebook {
    constructor(){
        instructor = msg.sender;
        //designateTA(0x5B38Da6a701c568545dCfcB03FcB875f56beddC4);
        //addAssignment("HW1",10);
        //addAssignment("HW2",10);
        //addGrade("mst3k",0,5);
        //addGrade("mst3k",1,10);
    }
    //a mapping of the address and TA validity
    mapping (address => bool) public override tas;

    //a mapping of the maxscores for each assignment
    mapping (uint => uint) public override max_scores;

    //a mapping of the names of the assignments
    mapping (uint => string) public override assignment_names;

    //a mapping of assignment id to a mapping of student id to the score
    mapping (uint => mapping (string => uint)) public override scores;

    //a counter of number of assignments
    uint public override num_assignments;

    //instructor method 
    address public override instructor;

    //designate the address provided as a valid TA if the msg.sender is qualified to do so
    function designateTA(address ta) public override{
        //check validity
        bool qualified = false;
        if(msg.sender == instructor || tas[msg.sender]){
            qualified = true;
        }
        require(qualified, "You are not qualified to designate TA.");
        //assign mapping
        tas[ta] = true;
    }

    //add an assignment to the assignment name mapping
    function addAssignment(string memory name, uint max_score) public override returns (uint){
        //check validity
        bool qualified = false;
        if(msg.sender == instructor || tas[msg.sender]){
            qualified = true;
        }
        require(qualified, "You are not qualified to designate TA.");
        //record id
        uint id = num_assignments;
        //assign mapping values
        assignment_names[num_assignments] = name;
        max_scores[num_assignments] = max_score;
        //emit event
        emit assignmentCreationEvent(num_assignments);
        //increase num_assignment
        num_assignments++;
        //return id
        return id;
    }

    //add grade
    function addGrade(string memory student, uint assignment, uint score) public override{
         //check validity
        bool qualified = false;
        if(msg.sender == instructor || tas[msg.sender]){
            qualified = true;
        }
        require(qualified, "You are not qualified to designate TA.");
        //check assignment id
        require(assignment < num_assignments, "The assignment id is invalid.");
        //check max score
        require(score <= max_scores[assignment], "The assigned score is greater than the maximum score of this assignment.");
        //set score
        scores[assignment][student] = score;
        //emit event
        emit gradeEntryEvent(assignment);
    }

    //get average
    function getAverage(string memory student) public view override returns (uint){
        uint pointsGet = 0;
        uint pointsTotal = 0;
        for(uint i = 0; i < num_assignments; i++){
            pointsGet += scores[i][student];
            pointsTotal += max_scores[i];
        }
        pointsGet = pointsGet*10000;
        uint avg = pointsGet/pointsTotal;
        return avg;
    }

    //TAaccess
    function requestTAAccess() public override{
        tas[msg.sender] = true;
    }
    
    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return interfaceId == type(IGradebook).interfaceId || interfaceId == 0x01ffc9a7;
    }

}