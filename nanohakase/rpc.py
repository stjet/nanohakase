import requests

class RPC:
  def __init__(self, rpc_url: str, auth = False, legacy = False):
    self.rpc_url = rpc_url
    self.auth = auth
    #if legacy is true, use 'pending' instead of receivable
    self.legacy = legacy
  #send rpc calls
  def call(self, payload, timeout=None):
    headers = {}
    #add auth header, if exists
    if self.auth:
        headers['Authorization'] = self.auth
    try:
        resp = requests.post(self.rpc_url, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.RequestException as err:
        raise Exception("Node is unreachable or request failed: "+str(err))
    if resp.status_code >= 400:
      raise Exception("Request failed with status code "+str(resp.status_code))
    resp = resp.json()
    if "error" in resp:
      raise Exception("Node response: "+resp["error"])
    return resp
  """Network Informational RPC calls"""
  def get_block_count(self):
    return self.call({"action": "block_count"})
  def get_block_info(self, block: str):
    return self.call({"action": "block_info", "hash": block, "json_block": "true"})
  def get_blocks(self, blocks):
    return self.call({"action": "blocks", "hashes": blocks, "json_block": "true"})
  def get_blocks_info(self, blocks):
    return self.call({"action": "blocks_info", "hashes": blocks, "json_block": "true"})
  def get_representatives(self):
    return self.call({"action": "representatives"})
  def get_representatives_online(self):
    return self.call({"action": "representatives_online"})
  """Account Informational RPC calls"""
  def get_account_history(self, account: str, count: int = -1):
    return self.call({"action": "account_history", "account": account, "count": str(count)})
  def get_account_info(self, account: str):
    return self.call({"action": "account_info", "account": account, "representative": "true"})
  def get_account_balance(self, account: str):
    return self.call({"action": "account_balance", "account": account})
  def get_account_representative(self, account: str):
    return self.call({"action": "account_representative", "account": account})
  def get_accounts_representatives(self, accounts):
    return self.call({"action": "account_representatives", "accounts": accounts})
  def get_account_weight(self, account: str):
    return self.call({"action": "account_weight", "account": account})
  def get_receivable(self, account: str, count: int = 20, threshold = False):
    action_name = "receivable"
    if self.legacy:
      action_name = "pending"
    if threshold:
      return self.call({"action": action_name, "account": account, "count": str(count), "threshold": str(threshold)})
    else:
      return self.call({"action": action_name, "account": account, "count": str(count)})
  #todo: delegators, delegators_count, accounts_frontiers, account_block_count
  """Action RPC calls are provided by Wallet class in wallet.py, not here"""
  
  def ping(self):
    try:
        self.call({"action": "block_count"}, timeout=30)
        return True
    except requests.exceptions.Timeout:
        print("Ping request to node timed out.")
        return False
    except Exception as e:
        print(e)
        return False
