from nanohakase import *

#todo: change tests so they use assert
#todo: fix bug with trailing raw, slight precision errors

rpc = RPC("https://app.natrium.io/api")

print("RPC and utils test")
#check current blockcount
print(rpc.get_block_count()["count"])

#get last 10 transactions
print(rpc.get_account_history("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps", count=10)["history"][0])

#check balance
print(raw_to_whole(int(rpc.get_account_balance("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps")["balance"])))

assert whole_to_raw("492.2") == 492200000000000000000000000000000
assert raw_to_whole(15*(10**NANO_DECIMALS)) == 15.0

#if someone drains the funds in this test seed I will be very upset >:(
print("Wallets test")
my_account = Wallet(rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=0)

#or generate a new one
my_new_account = Wallet(rpc, index=0)

print(my_new_account.seed)

#get address of self
assert my_account.get_address() == "nano_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9"

#get balance of self
print(my_account.get_balance())

#receive all transactions
print("Receive test")
print(my_account.receive_all())

#send 1 banano to the faucet development fund
print("Send test")
print(my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.001"))

#receive funds
print("Change test")
print(my_account.change_rep("nano_1kd4h9nqaxengni43xy9775gcag8ptw8ddjifnm77qes1efuoqikoqy5sjq3"))

#change rep

#change seed index
my_account.index = 1

assert my_account.get_address() == "nano_1rgkz7ipqntii8ic9j411agmtf6do3nxseey3x4jhrqsjcoitj3g9zgi9f53"

print(my_account.receive_all())

print(my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.001"))
