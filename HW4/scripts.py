#!/usr/bin/python3

# This is the homework submission file for the BTC Scripting homework, which
# can be found at http://aaronbloomfield.github.io/ccc/hws/btcscript.  That
# page describes how to fill in this program.


from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret
from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction
from bitcoin.core.script import *
from bitcoin.core import x



#------------------------------------------------------------
# Do not touch: change nothing in this section!

# ensure we are using the bitcoin testnet and not the real bitcoin network
SelectParams('testnet')

# The address that we will pay our tBTC to -- do not change this!
tbtc_return_address = CBitcoinAddress('mwL32bFWqjymzgcQmQ9rdH34VPi8fAfsWh')

# The address that we will pay our BCY to -- do not change this!
bcy_dest_address = CBitcoinAddress('mgBT4ViPjTTcbnLn9SFKBRfGtBGsmaqsZz')

# Yes, we want to broadcast transactions
broadcast_transactions = True

# Ensure we don't call this directly
if __name__ == '__main__':
    print("This script is not meant to be called directly -- call bitcoinctl.py instead")
    exit()


#------------------------------------------------------------
# Setup: your information

# Your UVA userid
userid = 'yz5zys'

# Enter the BTC private key and invoice address from the setup 'Testnet Setup'
# section of the assignment.  
my_private_key_str = "cVsmoKvSisMCDa2FW8sVgtVkez55hzrHLx7GVgNCaCuptN5LTZEN"
my_invoice_address_str = "mfosjNxd3taieCELeFKwReaHRaEgoq5qJn"

# Enter the transaction ids (TXID) from the funding part of the 'Testnet
# Setup' section of the assignment.  Each of these was provided from a faucet
# call.  And obviously replace the empty string in the list with the first
# one you botain..
txid_funding_list = ["2d4f07bbf6406dd12edfb8c7cf5b4857d43fd2a685d71d18339778e58cb1b9c8"]

# Don't change this -- it is so we can easily access the first such funding
# transaction.
txid_initial = txid_funding_list[0]

# These conversions are so that you can use them more easily in the functions
# below -- don't change these two lines.
if my_private_key_str != "":
    my_private_key = CBitcoinSecret(my_private_key_str)
    my_public_key = my_private_key.pub


#------------------------------------------------------------
# Utility function(s)

# This function will create a signature of a given transaction.  The
# transaction itself is passed in via the first three parameters, and the key
# to sign it with is the last parameter.  The parameters are:
# - txin: the transaction input of the transaction being signed; type: CMutableTxIn
# - txout: the transaction output of the transaction being signed; type: CMutableTxOut
# - txin_scriptPubKey: the pubKey script of the transaction being signed; type: list
# - private_key: the private key to sign the transaction; type: CBitcoinSecret
def create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key):
    tx = CMutableTransaction([txin], [txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx, 0, SIGHASH_ALL)
    return private_key.sign(sighash) + bytes([SIGHASH_ALL])


#------------------------------------------------------------
# Testnet Setup: splitting coins

# The transaction ID that is to be split -- the assumption is that it is the
# transaction hash, above, that funded your account with tBTC.  If you are
# splitting a different faucet transaction, then change this appropriately.
# It must have been paid to the address that corresponds to the private key
# above
split_txid = txid_initial

# How much BTC is in that UTXO; look this up on https://live.blockcypher.com
# to get the correct amount.
split_amount_to_split = 0.001

# How many UTXO indices to split it into.  Note that it will actually split
# into one less, and use the last one as the transaction fee.
split_into_n = int(split_amount_to_split/0.0001)

# The transaction IDs obtained after successfully splitting the tBTC.
txid_split_list = ["9861ca89bbc1d6d2085da84a878a48b15819262dd09a44e51c0fb0c8525a8631"]

# Don't change this -- it's so some of our legacy grading code still works.
txid_split = txid_split_list[0]


#------------------------------------------------------------
# Global settings: some of these will need to be changed for EACH RUN

# The transaction ID that is being redeemed for the various parts herein --
# this should be the result of the split transaction, above; thus, the
# default is probably sufficient.
txid_utxo = txid_split

# The index of the UTXO that is being spent -- note that these indices are
# indexed from 0.  Note that you will have to change this for EACH run, as
# once a UTXO index is spent, it can't be spent again.  If there is only one
# index, then this should be set to 0.
utxo_index = 8

# How much tBTC to send -- this should be LESS THAN the amount in that
# particular UTXO index -- if it's not less than the amount in the UTXO, then
# there is no miner fee, and it will not be mined into a block.  Setting it
# to 90% of the value of the UTXO index is reasonable.  Note that the amount
# in a UTXO index is split_amount_to_split / split_into_n.
send_amount = 0.00009


#------------------------------------------------------------
# Part 1: P2PKH transaction

# This defines the pubkey script (aka output script) for the transaction you
# are creating.  This should be a standard P2PKH script.  The parameter is:
# - address: the address this transaction is being paid to; type:
#   P2PKHBitcoinAddress
def P2PKH_scriptPubKey(address):
    return [ 
             OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG
           ]

# This function provides the sigscript (aka input script) for the transaction
# that is being redeemed.  This is for a standard P2PKH script.  The
# parameters are:
# - txin: the transaction input of the UTXO being redeemed; type:
#   CMutableTxIn
# - txout: the transaction output of the UTXO being redeemed; type:
#   CMutableTxOut
# - txin_scriptPubKey: the pubKey script (aka output script) of the UTXO being
#   redeemed; type: list
# - private_key: the private key of the redeemer of the UTXO; type:
#   CBitcoinSecret
def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key):
    sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, private_key)
    pubkey = private_key.pub
    return [ 
             sig, pubkey
           ]

# The transaction hash received after the successful execution of this part
txid_p2pkh = "64a0aa5ec7163405292e30011747c7380a3953e73354a9b12fdc1db2f853b091"


#------------------------------------------------------------
# Part 2: puzzle transaction

# These two values are constants that you should choose -- they should be four
# digits long.  They need to allow for only integer solutions to the linear
# equations specified in the assignment.
puzzle_txn_p = 9199
puzzle_txn_q = 8933

# These are the solutions to the linear equations specified in the homework
# assignment.  You can use an online linear equation solver to find the
# solutions.
puzzle_txn_x = 2333
puzzle_txn_y = 2200

# This function provides the pubKey script (aka output script) that requres a
# solution to the above equations to redeem this UTXO.
def puzzle_scriptPubKey():
    return [ 
             OP_2DUP, OP_3DUP, OP_ADD, OP_ADD, OP_ADD, 8933, OP_EQUAL, OP_VERIFY, OP_DUP, OP_ADD, OP_ADD, OP_ADD, 9199, OP_EQUAL
           ]

# This function provides the sigscript (aka input script) for the transaction
# that you are redeeming.  It should only provide the two values x and y, but
# in the order of your choice.
def puzzle_scriptSig():
    return [ 
             puzzle_txn_x, puzzle_txn_y
           ]

# The transaction hash received after successfully submitting the first
# transaction above (part 2a)
txid_puzzle_txn1 = "7fcc633bd1f98ead019a281759bbfee8c2504755d1284ffae60b60b769359d57"

# The transaction hash received after successfully submitting the second
# transaction above (part 2b)
#710661a703c6adadc627fcd5362f2b89da4259262a6b5b39b3929c32ec20b962
#The above transaction never confirms
txid_puzzle_txn2 = "d2c28cd3327b171e96da0d807babc051cb8efc827f196a0c10c4163f9c109614"


#------------------------------------------------------------
# Part 3: Multi-signature transaction

# These are the public and private keys that need to be created for alice,
# bob, and charlie
alice_private_key_str = "cSUjdocqoeJGMUAw7ARn3TKe564XMDFZ4wz43jRbokNBmkNJMniQ"
alice_invoice_address_str = "mhT9ki9YgWSg7Q8i3cqcQVoJEQDL9Evtzc"
bob_private_key_str = "cVNE6RRoppUBbMrbNuAhtcEbTwiqRNog7BNZ6EcGQLAUQcwDaYUb"
bob_invoice_address_str = "muzqNV1SaCWq9vD1dStRt6PXU7pexTdMFV"
charlie_private_key_str = "cT42CE8LecaC6BVRxGNP46Hen6Rpz5281z2HFNmMP4LKZz9NxGPW"
charlie_invoice_address_str = "mxWmadhkSQgSgLRLAhu8GoPZiy7XvpAN5b"

# These three lines convert the above strings into the type that is usable in
# a script -- you should NOT modify these lines.
if alice_private_key_str != "":
    alice_private_key = CBitcoinSecret(alice_private_key_str)
if bob_private_key_str != "":
    bob_private_key = CBitcoinSecret(bob_private_key_str)
if charlie_private_key_str != "":
    charlie_private_key = CBitcoinSecret(charlie_private_key_str)

# This function provides the pubKey script (aka output script) that will
# require multiple different keys to allow redeeming this UTXO.  It MUST use
# the OP_CHECKMULTISIGVERIFY opcode.  While there are no parameters to the
# function, you should use the keys above for alice, bob, and charlie, as
# well as your own key.
def multisig_scriptPubKey():
    alice_pubkey = alice_private_key.pub
    bob_pubkey = bob_private_key.pub
    charlie_pubkey = charlie_private_key.pub
    return [ 
            my_public_key, OP_CHECKSIGVERIFY, OP_2, alice_pubkey, bob_pubkey, charlie_pubkey, OP_3, OP_CHECKMULTISIG
           ]

# This function provides the sigScript (aka input script) that can redeem the
# above transaction.  The parameters are the same as for P2PKH_scriptSig
# (), above.  You also will need to use the keys for alice, bob, and charlie,
# as well as your own key.  The private key parameter used is the global
# my_private_key.
def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    alice_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, alice_private_key)
    bob_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, bob_private_key)
    charlie_sig = create_CHECKSIG_signature(txin, txout, txin_scriptPubKey, charlie_private_key)
    return [ 
             OP_0, alice_sig, bob_sig, bank_sig
           ]

# The transaction hash received after successfully submitting the first
# transaction above (part 3a)
txid_multisig_txn1 = "80c65eaa9c96469d34de7a6430f34c72e457fa7ff0398ffb309cd05397028b50"#"c26c4aa3b3067ab60b8599e4af3606b3986398dc5245ac9ee16e582b491338bf"

# The transaction hash received after successfully submitting the second
# transaction above (part 3b)
txid_multisig_txn2 = "8757dd7600dfd30cf16d36c37657bb81d302a9e6fd1213a21af53aa4939c6872"


#------------------------------------------------------------
# Part 4: cross-chain transaction

# This is the API token obtained after creating an account on
# https://accounts.blockcypher.com/.  This is optional!  But you may want to
# keep it here so that everything is all in once place.
blockcypher_api_token = "3ffbb36f313b487c89f26e99f8ae1231"

# These are the private keys and invoice addresses obtained on the BCY test
# network.
my_private_key_bcy_str = "8426e40694ce1cf8e334658350000abd99912f55497e5b2a95bf59667f46068d"
my_invoice_address_bcy_str = "BtAfmYE9NviEP7y2GnYa4CC6hux19X9rEh"
bob_private_key_bcy_str = "8bdb532d8069677496aadc24ba7627110136bb47ccf09c3fc230389792f04afb"
bob_invoice_address_bcy_str = "C5qjBQH9hxUd6329bajhTomBpSvhYxhHhv"

# This is the transaction hash for the funding transaction for Bob's BCY
# network wallet.
txid_bob_bcy_funding = "40346eecc3d4a64ed0cc125988c43646a884ce8cb5b99183477f04f45813d5f9"

# This is the transaction hash for the split transaction for the trasnaction
# above.
txid_bob_bcy_split = "a3166f552ac8c504e01bea881c8d187319e0132f31d21ce844bafee803b3e398"

# This is the secret used in this atomic swap.  It needs to be between 1 million
# and 2 billion.
atomic_swap_secret = 200000000

# This function provides the pubKey script (aka output script) that will set
# up the atomic swap.  This function is run by both Alice (aka you) and Bob,
# but on different networks (tBTC for you/Alice, and BCY for Bob).  This is
# used to create TXNs 1 and 3, which are described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.
def atomicswap_scriptPubKey(public_key_sender, public_key_recipient, hash_of_secret):
    return [ 
             OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, 
             OP_CHECKSIG, OP_ELSE, OP_0, OP_ROT, OP_ROT, OP_2, public_key_recipient, 
             public_key_sender, OP_2, OP_CHECKMULTISIG, OP_ENDIF
           ]

# This is the ScriptSig that the receiver will use to redeem coins.  It's
# provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This creates the "normal" redeeming script, shown in steps 5 and 6 at 
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/atomicsteps.
def atomcswap_scriptSig_redeem(sig_recipient, secret):
    return [
        sig_recipient, secret, OP_TRUE,
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed; it
# is provided in full so that you can write the atomicswap_scriptPubKey()
# function, above.  This is used to create TXNs 2 and 4, which are
# described at
# http://aaronbloomfield.github.io/ccc/slides/bitcoin.html#/xchainpt1.  In
# practice, this would be time-locked in the future -- it would include a
# timestamp and call OP_CHECKLOCKTIMEVERIFY.  Because the time can not be
# known when the assignment is written, and as it will vary for each student,
# that part is omitted.
def atomcswap_scriptSig_refund(sig_sender, sig_recipient):
    return [
        sig_recipient, sig_sender, OP_FALSE,
    ]

# The transaction hash received after successfully submitting part 4a
txid_atomicswap_alice_send_tbtc = "f37a53c24b42740a250c7772f2bf55af9e65c9f9a728d404ac7350203744c862"

# The transaction hash received after successfully submitting part 4b
txid_atomicswap_bob_send_bcy = "4a0746610a36a2272f4d7cb9f94ae55c62e7ec4d63ec5838c4194934d38b1693"

# The transaction hash received after successfully submitting part 4c
txid_atomicswap_alice_redeem_bcy = "14a6537160d0b09d019225baaec9a4446357f57ca821efa757b6579b4d9c3c4e"

# The transaction hash received after successfully submitting part 4d
txid_atomicswap_bob_redeem_tbtc = "59aa7b97f1f1ac929791a76cb5bcfada885ffc24141abdd3f66136cbf4c8c789"


#------------------------------------------------------------
# part 5: return everything to the faucet

# nothing to fill in here, as we are going to look at the balance of
# `my_invoice_address_str` to verify that you've completed this part.