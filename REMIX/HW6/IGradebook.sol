// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.16;

// See the actual IGradebook.sol file, linked to above, for much more detailed comments

interface IGradebook {

    event assignmentCreationEvent (uint indexed _id);

    event gradeEntryEvent (uint indexed _id);

    // The following six methods are done for you automatically -- as long as
    // you make the appropriate variable public, then Solidity will create
    // the getter function for you
    
    function tas(address ta) external returns (bool);

    function max_scores(uint id) external returns (uint);

    function assignment_names(uint id) external returns (string memory);

    function scores(uint id, string memory userid) external returns (uint);

    function num_assignments() external returns (uint);

    function instructor() external returns (address);

    // The following five functions are ones you must implement

    function designateTA(address ta) external;

    function addAssignment(string memory name, uint max_score) external returns (uint);

    function addGrade(string memory student, uint assignment, uint score) external;

    function getAverage(string memory student) external view returns (uint);

    function requestTAAccess() external;

    // The implementation for the following is provided in the HW description

    function supportsInterface(bytes4 interfaceId) external view returns (bool);

}
