# Nanohakase

Nanohakase is a python library for the Nano cryptocurrency. It aims to be the simplest Nano library out there, and is a self fork of Bananopie (Nanopie was taken already).

## Installation

`pip install nanohakase`

Nanohakase is on [pypi](https://pypi.org/project/nanohakase/).

# Quick Start

First, start with a `RPC` class, for read only 
```py
from nanohakase import *
rpc = RPC("https://proxy.nanos.cc/proxy")

#check current blockcount
print(rpc.get_block_count().count)

#get last 10 transactions
print(rpc.get_account_history("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps", count=10)["history"])

#check balance
print(raw_to_whole(int(rpc.get_account_balance("nano_3346kkobb11qqpo17imgiybmwrgibr7yi34mwn5j6uywyke8f7fnfp94uyps")["balance"])))
```

For sending/receiving transactions, use a `Wallet`.
```py
from nanohakase import RPC, Wallet
rpc = RPC("https://app.natrium.io/api")

my_account = Wallet(rpc, seed="seed here", index=0)

#or generate a new one
my_new_account = Wallet(rpc, index=0)

print(my_new_account.seed)

#get address of self
print(my_account.get_address())

#get balance of self
print(my_account.get_balance())

#send 1 nano to the faucet development fund
print(my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1"))

#receive funds
my_account.receive_all()

#change rep
my_account.change_rep("nano_1kd4h9nqaxengni43xy9775gcag8ptw8ddjifnm77qes1efuoqikoqy5sjq3")

#change seed index
my_account.index = 2
```

Utility functions are also provided.
```py
import nanohakase

#whole to raw nano
print(nanohakase.whole_to_raw("492.2"))

#raw to whole nano
print(nanohakase.raw_to_whole(1900000000000000000000000000))
```

# Documentation

Also see the [Nano RPC docs](https://docs.nano.org/commands/rpc-protocol) for information on what rpc call wrapper functions return.

## RPC (Class)
**Parameters:**
- `rpc_url` (*str*): IP or URL of node
- `auth` (*str* or *bool*, Default: False): Optional HTTP Authorization header

Sample:
```py
rpc = RPC("https://proxy.nanos.cc/proxy")
```

**Properties:**
- `rpc_url` (*str*): IP or URL of node
- `auth` (*str* or *bool*): Optional HTTP Authorization header

**Methods:**

### call (Function)
RPC call. Intended for internal use, but useful for RPC calls that aren't directly implemented.

**Parameters:**
- `payload` (*dictionary*): Payload to send to node

Sample:
```py
rpc.call({"action": "block_count"})
```

**Returns:**
Response of RPC call (JSON dictionary)

### get_block_count (Function)
Get network block count.

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#block_count)


### get_block_info (Function)
Get block info for hash.

**Parameters**
- `block` (*st*): Block hash

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#block_info)

### get_blocks (Function)
Get blocks.

**Parameters**
- `blocks` (*str list*): List of block hashes to get information on

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#blocks)

### get_blocks_info (Function)
Get blocks, with more detailed information.

**Parameters**
- `blocks` (*str list*): List of block hashes to get information on

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#blocks_info)

### get_representatives (Function)
Get list of network representatives and their weight

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#representatives)

### get_representatives_online (Function)
Get list of network representatives that have recently voted

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#representatives_online)

### get_account_history (Function)
Get account history (confirmed and received transaction list)

**Parameters**
- `account` (*str*): Address of account
- `count` (*int*, Default: -1): Optional parameter to specify amount of transactions to return. `-1` means all, or at least as much as the node will allow

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_history)

### get_account_info (Function)
Get account information, like height, frontier, balance, etc

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_info)

### get_account_balance (Function)
Get account balance

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_balance)

### get_account_representative (Function)
Get account representative

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_representative)

### get_accounts_representatives (Function)
Get representatives of accounts

**Parameters**
- `account` (*str list*): List of addresses

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_representatives)

### get_account_weight (Function)
Get delegated weight of representative

**Parameters**
- `account` (*str*): Address of representative

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_weight)

### get_receivable (Function)
Get receivable transactions for account

**Parameters**
- `account` (*str*): Address of representative
- `count` (*int*, Default: 20): Optional parameter to specify max amount of receivable transactions to return
- `thereshold` (*int or bool*, Default: False): Optional parameter to filter out any receivable transactions with value less than the thereshold

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#receivable)

## Wallet (class)

**Parameters:**
- `rpc` (*RPC*): A RPC class
- `seed` (*str* or *bool*, Default: False): 64 character hex seed, if `False`, will generate a seed by itself. Private keys are derived from the seed.
- `index` (*int*, Default: 0): Optional parameter that is the index of the seed. Any number from 0 to 4294967295. Each index of the seed is a different private key, and so different address.

Sample:
```py
my_wallet = Wallet(RPC("https://proxy.nanos.cc/proxy"), "seed here", 0)
```

**Properties:**
- `rpc_url` (*str*): IP or URL of node
- `seed` (*str*): Nano seed (64 character hex string)
- `index` (*int*): Seed index. Change this property to change the wallet seed index.

**Methods**

### send_process (Function)
Internal use function to send a `process` RPC call

**Parameters**
- `block` (*dictionary*): block content
- `subtype` (*str*): Send, receive, or change

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### send (Function)
High level function to send Nano

**Parameters**
- `to` (*str*): Address to send to
- `amount` (*str*): Amount of Nano to send (in whole, not raw)
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

Sample:
```py
my_wallet = Wallet(RPC("https://app.natrium.io/api"), "seed here", 0)
my_account.send("nano_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_specific (Function)
Receive a specific block

**Parameters**
- `hash` (*str*): Block hash to receive
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_all (Function)
Receive all (technically, 20) receivable transactions

**Parameters**
None

Sample:
```py
my_wallet = Wallet(RPC("https://proxy.nanos.cc/proxy"), "seed here", 0)
my_account.receive_all()
```

**Returns**
Nothing

### change_rep (Function)
Change account representative

**Parameters**
- `new_representative` (*str*): Representative Nano address to change to
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

Sample:
```py
my_wallet = Wallet(RPC("https://proxy.nanos.cc/proxy"), "seed here", 0)
my_account.change_rep("nano_1kd4h9nqaxengni43xy9775gcag8ptw8ddjifnm77qes1efuoqikoqy5sjq3")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### get_address (Function)
Get address at current index of current seed

**Parameters**
None

**Returns**
*str*, Nano address

### get_balance (Function)
Double wrapped function to get balance of self (see `RPC`'s `get_account_balance`)

### get_receivable (Function)
Double wrapped function to get receivable blocks (see `RPC`'s `get_receivable`)

### get_representative (Function)
Double wrapped function to get representative of self (see `RPC`'s `get_account_representative`)

### get_account_info (Function)
Double wrapped function to get account info of self (see `RPC`'s `get_account_info`)

### generate_seed (static Function)
Generate a random seed using `os.urandom`

**Parameters**
None

Sample:
```py
print(Wallet.generate_seed())
```

**Returns**
64 character hex seed

## Util

**Properties**
- `NANO_DECIMALS` (*int*): Amount of decimals that Nano has (30)
- `PREAMBLE` (*str*): Hex string to prepend when signing

**Methods**

`encode_base32`, `decode_base32`, `bytes_to_hex`, `hex_to_bytes`, `random_bytes`, `get_private_key_from_seed`, `get_public_key_from_private_key`, `get_address_from_public_key`, `get_public_key_from_address`, `hash_block`, `sign` are internal use Functions that are currently undocumented. Look at `/nanohakase/util.py` to see what they do.

### whole_to_raw (Function)
Converts whole Nano to raw Nano

**Parameters**
- `whole` (*str*): Whole amount of Nano

**Returns**
*int*, that is raw amount of Nano

### raw_to_whole (Function)
Converts raw Nano to whole Nano (Cuts off at 2 decimal places)

**Parameters**
- `raw` (*int*): Raw amount of Nano

**Returns**
*int*, that is whole amount of Nano
