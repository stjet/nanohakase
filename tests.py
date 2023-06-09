import time

from nanohakase import *

rpc = RPC("https://mynano.ninja/api/node", legacy=True)

start_time = time.time()
print("RPC and utils test")

print(rpc.get_block_count()["count"])
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

start_time = time.time()
print(rpc.get_account_history("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps", count=10)["history"][0])
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

start_time = time.time()
print(raw_to_whole(int(rpc.get_account_balance("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps")["balance"])))
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

print("Wallets test")
my_account = Wallet(rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=0, try_work=True)

start_time = time.time()
assert my_account.get_address() == "nano_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9"
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

start_time = time.time()
print(my_account.get_balance())
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

print("Receive test")
start_time = time.time()
print(my_account.receive_all())
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

print("Send test")
start_time = time.time()
print(my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.001"))
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

print("Change test")
start_time = time.time()
print(my_account.change_rep("nano_1kd4h9nqaxengni43xy9775gcag8ptw8ddjifnm77qes1efuoqikoqy5sjq3"))
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

my_account.index = 1

start_time = time.time()
assert my_account.get_address() == "nano_1rgkz7ipqntii8ic9j411agmtf6do3nxseey3x4jhrqsjcoitj3g9zgi9f53"
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

start_time = time.time()
print(my_account.receive_all())
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

start_time = time.time()
print(my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.001"))
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")