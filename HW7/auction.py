# Submission information for the NFT Auction HW
# https://aaronbloomfield.github.io/ccc/hws/auction/

# The filename of this file must be 'auction.py', else the submission
# verification routines will not work properly.

# You are welcome to have additional variables or fields in this file; you
# just cant remove variables or fields.


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

	# Your auctioneer contract.  All of the auction bids that are not on the
	# class-wide auctioneer are assumed to come from this contract.  The
	# address does not need to be in checksummed form.  It must have been
	# deployed by the eth_coinbase address, above.
	'auctioneer': '0xF67684897caA5A158f4443F3af5427b97785365e',

	# We are not asking for the NFT Manager's contract address, as we can find
	# that out via a call to the nftmanager() function in your Auctioneer
	# contract.
}


# This dictionary contains various information that will vary depending on the
# assignment.
other = {
	
	# This is the auction ID for the auction in your auctioneer contract whose
	# time should be expired and should be closed at the time of the
	# assignment due date.
	'your_auction_id_1': 0,

	# This is the NFT token ID, in your deployed NFT manager, for the above
	# auction.
	'your_nft_token_id_1': 0,

	# This is the auction ID for the auction in your auctioneer contract that
	# stays open for two weeks after the assignment due date.
	'your_auction_id_2': 1,

	# This is the NFT token ID, in your deployed NFT manager, for the above
	# auction.
	'your_nft_token_id_2': 1,

	# This is the auction ID, in the class-wide auctioneer, that needs to stay
	# open for one week past the assignment due date.
	'course_auction_id': 33,

	# This is the NFT token ID, in the class-wide NFT manager, for the above
	# auction.
	'course_nft_token_id': 54945779114938317797448592518154778008574284477162144708282165204058550304768,

}


# These are various sanity checks, and are meant to help you ensure that you
# submitted everything that you are supposed to submit.  Other than
# submitting the necessary files to Gradescope (which checks for those
# files), all other submission requirements are listed herein.  These values
# need to be changed to True (instead of None).
sanity_checks = {
	
	# Did you deploy both the Auctioneer and NFT manager contracts to the
	# blockchain?
	'deployed_both_contracts': True,

	# Will your first auction ('your_auction_id_1', above) have expired by the
	# assignment due date/time?
	'auction_1_expiration': True,

	# Are there multiple bids, from at least 2 accounts, on action #1?
	'auction_1_has_multiple_bids': True,

	# Did you call closeAuction() on auction #1?
	'auction_1_called_closeAuction': True,

	# Will your second auction ('your_auction_id_2', above) stay open for TWO
	# WEEKS after the assignment due date/time?
	'auction_2_expiration': True,

	# Are there multiple bids, from at least 2 accounts, on action #2?
	'auction_2_has_multiple_bids': True,

	# Will the course auction that you submitted ('course_auction_id', above)
	# stay open for ONE WEEK after the assignment due date/time?
	'course_auction_expiration': True,

	# Did you, or will you, bid on three (or more) auctions viewable on the
	# course auction web site?
	'will_have_bid_on_course_auctions': True,

}


# While some of these are optional, you still have to replace those optional
# ones with the empty string (rather than None).
comments = {

	# How long did this assignment take, in hours?  Please format as an
	# integer or float.
	'time_taken': 6,

	# Any suggestions for how to improve this assignment?  This part is
	# completely optional.  If none, then you can have the value here be the
	# empty string (but not None).
	'suggestions': "I think the description of the payable function is not that clear. I spent some time to figure out that when the payable function is called, the amount of eth is set to be sent to current contract address by default.",

	# Any other comments or feedback?  This part is completely optional. If
	# none, then you can have the value here be the empty string (but not
	# None).
	'comments': "interesting",
}