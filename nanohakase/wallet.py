from .rpc import RPC
from .util import *

#todo: request work with work_generate
class Wallet:
  def __init__(self, rpc: RPC, seed = False, index: int = 0, try_work = False):
    self.rpc = rpc
    #if seed is False, automatically generate new seed
    if not seed:
      seed = self.generate_seed()
    self.seed = seed
    self.index = index
    self.try_work = try_work
  @staticmethod
  def generate_seed():
    return bytes_to_hex(random_bytes(32))
  def get_address(self):
    return get_address_from_public_key(get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index)))
  def send_process(self, block, subtype: str):
      payload = {
          "action": "process",
          "subtype": subtype,
          "json_block": "true",
          "block": block
      }
      if "work" not in block:
          if self.try_work:
              # if opening block, there is no previous, so use public key as hash instead
              if block["previous"] == "0000000000000000000000000000000000000000000000000000000000000000":
                  block["work"] = gen_work(get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index)), subtype)
              else:
                  block["work"] = gen_work(block["previous"], subtype)
              # Check if the RPC server is reachable after the work generation.
              if not self.rpc.ping():
                  raise Exception("RPC server is not reachable after work generation. Transaction aborted. Nano")
          else:
              payload["do_work"] = True
      return self.rpc.call(payload)

  #actions
  def send(self, to: str, amount: str, work = False):
    amount = whole_to_raw(amount)
    address_sender = self.get_address()
    private_key_sender = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    public_key_receiver = get_public_key_from_address(to)
    info = self.get_account_info()
    previous = info["frontier"]
    representative = info["representative"]
    before_balance = info["balance"]
    #height not actually needed
    block = {
      "type": "state",
      "account": address_sender,
      "previous": previous,
      "representative": representative,
      "balance": str(int(int(before_balance)-amount)),
      #link in this case is public key of account to send to
      "link": public_key_receiver,
      "link_as_account": to
    }
    block_hash = hash_block(block)
    signature = sign(private_key_sender, block_hash)
    block["signature"] = signature
    if work:
      block["work"] = work
    return self.send_process(block, "send")
  def receive_specific(self, hash: str, work=False):
    #no need to check as opened, I think?
    #get block info of receiving
    block_info = self.rpc.get_block_info(hash)
    amount = int(block_info["amount"])
    address_sender = self.get_address()
    private_key_receiver = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    public_key_sender = get_public_key_from_address(block_info["block_account"])
    #these are the defaults, if the account is unopened
    before_balance = 0
    representative = address_sender
    previous = "0000000000000000000000000000000000000000000000000000000000000000"
    try:
      #if account is opened
      info = self.get_account_info()
      previous = info["frontier"]
      representative = info["representative"]
      before_balance = info["balance"]
    except Exception as e:
      #probably, unopened account
      pass
    #height not actually needed
    block = {
      "type": "state",
      "account": address_sender,
      "previous": previous,
      "representative": representative,
      "balance": str(int(before_balance)+amount),
      #link in this case is hash of send
      "link": hash
    }
    block_hash = hash_block(block)
    signature = sign(private_key_receiver, block_hash)
    block["signature"] = signature
    if work:
      block["work"] = work
    return self.send_process(block, "receive")
  def receive_all(self):
    receivable_blocks = self.get_receivable()["blocks"]
    for block_hash in receivable_blocks:
      #receive them
      self.receive_specific(block_hash)
  def change_rep(self, new_representative, work=False):
    address_self = self.get_address()
    private_key_self = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    #these are the defaults, if the account is unopened
    before_balance = 0
    previous = "0000000000000000000000000000000000000000000000000000000000000000"
    try:
      #if account is opened
      info = self.get_account_info()
      previous = info["frontier"]
      before_balance = info["balance"]
    except Exception as e:
      #probably, unopened account
      pass
    block = {
      "type": "state",
      "account": address_self,
      "previous": previous,
      "representative": new_representative,
      "balance": before_balance,
      #link in this case is 0
      "link": "0000000000000000000000000000000000000000000000000000000000000000"
    }
    block_hash = hash_block(block)
    signature = sign(private_key_self, block_hash)
    block["signature"] = signature
    if work:
      block["work"] = work
    return self.send_process(block, "change")
  #double wrapped
  def get_balance(self):
    return self.rpc.get_account_balance(self.get_address())
  def get_receivable(self):
    return self.rpc.get_receivable(self.get_address())
  def get_representative(self):
    return self.rpc.get_account_representative(self.get_address())
  def get_account_info(self):
