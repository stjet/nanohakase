import time

from nanohakase import *




rpc = RPC("https://mynano.ninja/api/node", legacy=True)

start_time = time.time()
print("RPC and utils test")

print(f"test: {rpc.ping()}")
print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

# start_time = time.time()
# print(rpc.get_account_history("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps", count=10)["history"][0])
# print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

# start_time = time.time()
# print(raw_to_whole(int(rpc.get_account_balance("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps")["balance"])))
# print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

# print("Wallets test")
# my_account = Wallet(rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=0, try_work=True)


