# Submission information for the dApp Introduction HW
# https://aaronbloomfield.github.io/ccc/hws/dappintro/

# The filename of this file must be 'dappintro.py', else the submission
# verification routines will not work properly.

# You are welcome to have additional variables or fields in this file; you
# just can't remove variables or fields.


# Who are you?  Name and UVA userid.  The name can be in any human-readable format.
userid = "yz5zys"
name = "Yufei Zhou"


# eth.coinbase: this is the account that you deployed the smart contracts
# (and performed any necessary transactions) for this assignment.  Be sure to
# include the leading '0x' in the address.
eth_coinbase = "0xf150af2ee45c825c6a96f4a0b47ce286a85b2317"


# This dictionary contains the contract addresses of the various contracts
# that need to be deployed for this assignment.  The addresses do not need to
# be in checksummed form.  The contracts do, however, need to be deployed by
# the eth_coinbase address, above.  Be sure to include the leading '0x' in
# the address.
contracts = {

	# Your deployed Polls contract.  All of the action below on your Polls
	# contract is assumed to be with this one. The address does not need to
	# be in checksummed form.  It must have been deployed by the eth_coinbase
	# address, above.
	'poll': "0xcc4d449FFE0406311A289063ceFcDD6fD3f396Ce",

}


# This dictionary contains various information that will vary depending on the
# assignment.
other = {
	
	# This is the transaction hash where you voted on your own deployed
	# Polls contract in part 3 (deployment) of the assignment.
	'txn_hash_vote_yours': "0x89a2325ba57e4c101cc50268de5e9af91cf2cdf9df7aa636f57d5249dfbc2573",

	# This is the transaction hash where you voted on the course Polls
	# contract in part 5 (vote) of the assignment.
	'txn_hash_vote_course': "0x4ce38c3c20bf76b68aca6be557598ddccfeaf28a48c6e1e8115e8a0cbe409237",

	# Are you using the Desktop version of Remix?  If so, then True.  If you
	# are using the web version at https://remix.ethereum.org, then False.
	# This is just so we can see how many students are using each one.  If
	# you used both, choose this optoin based on which one you expect to use
	# more often in the future.
	'using_desktop_remix': True,

}


# These are various sanity checks, and are meant to help you ensure that you
# submitted everything that you are supposed to submit.  Other than
# submitting the necessary files to Gradescope, all other submission
# requirements are listed herein.  These values need to be changed to True
# (instead of None).
sanity_checks = {
	
	# Did you change the various choices in the `addChoice()` calls in the
	# constructor?  This is from the 'code base' section of the assignment.
	'make_changes_to_addchoice': True,

	# Did you change the value of the `purpose` variable in the code?  This
	# is from the 'code base' section of the assignment.
	'make_changes_to_purpose': True,

	# Did you try out the unit testing section of the homework?  This is from
	# part 2 (testing) of the assignment.
	'tried_out_unit_testing': True,

	# Did you deploy your Polls contract?  This is from part 3
	# (deployment) of the assignment.
	'deployed_choices_contract': True,

	# Did you vote on your own Polls contract?  This is from part 3
	# (deployment) of the assignment.
	'voted_on_your_poll': True,

	# Did you view the web page that reads from a Polls contract?  This is
	# from part 4 (web interface) of the assignment.
	'explored_web_interface': True,

	# Did you vote on the course-wide Polls contract?  This is from part 5
	# (vote) of the assignment.
	'voted_on_course_poll': True,

}


# While some of these are optional, you still have to replace those optional
# ones with the empty string (rather than None).
comments = {

	# How long did this assignment take, in hours?  Please format as an
	# integer or float.
	'time_taken': 1,

	# Any suggestions for how to improve this assignment?  This part is
	# completely optional.  If none, then you can have the value here be the
	# empty string (but not None).
	'suggestions': "",

	# Any other comments or feedback?  This part is completely optional. If
	# none, then you can have the value here be the empty string (but not
	# None).
	'comments': "",
}