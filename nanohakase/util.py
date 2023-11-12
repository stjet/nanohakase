import os, math
from hashlib import blake2b
import ed25519_blake2b
from decimal import Decimal, getcontext

NANO_DECIMALS = 30
#nano supply is 100.000.000+, so add 9 decimals
getcontext().prec = NANO_DECIMALS+9
PREAMBLE = "0000000000000000000000000000000000000000000000000000000000000006"

#this function translated to python from https://nanoo.tools/js/termhn_nano-base32_2018-03-06.js
def encode_base32(bytes):
  alphabet = '13456789abcdefghijkmnopqrstuwxyz'
  length = len(bytes)
  leftover = (length * 8) % 5
  offset = 0
  if leftover == 0:
    offset = 0
  else:
    offset = 5 - leftover
  value = 0
  output = ''
  bits = 0
  for i in range(length):
    value = (value << 8) | bytes[i]
    bits += 8
    while (bits >= 5):
      output += alphabet[(value >> (bits + offset - 5)) & 31]
      bits -= 5
  if bits > 0:
    output += alphabet[(value << (5 - (bits + offset))) & 31]
  return output

def decode_base32(base32):
  alphabet = '13456789abcdefghijkmnopqrstuwxyz'
  length = len(base32)
  leftover = (length * 5) % 8
  offset = 0
  if leftover == 0:
    offset = 0
  else:
    offset = 8 - leftover
  bits = 0
  value = 0
  index = 0
  output = bytearray(math.ceil(length * 5 / 8))
  for i in range(length):
    value = (value << 5) | alphabet.index(base32[i])
    bits += 5
    if bits >= 8:
      output[index] = (value >> (bits + offset - 8)) & 255
      index += 1
      bits -= 8
  if bits > 0:
    output[index] = (value << (bits + offset - 8)) & 255
    index += 1
  if leftover != 0:
    output = output[1::]
  return bytes(output)

def bytes_to_hex(bytes: bytes):
  return bytes.hex().upper()

def hex_to_bytes(hex: str):
  return bytes.fromhex(hex)

#bytes_num should be 32, usually
def random_bytes(bytes_num: int):
  return os.urandom(bytes_num)

def get_private_key_from_seed(seed, seed_index):
  #https://docs.nano.org/glossary/#wallet
  #seed_index is 32 bit (4 bytes)
  #use hashlib blake2b
  seed_index = seed_index.to_bytes(4, 'big')
  seed = hex_to_bytes(seed)
  blake_obj = blake2b(digest_size=32)
  blake_obj.update(seed)
  blake_obj.update(seed_index)
  return blake_obj.hexdigest()

def get_public_key_from_private_key(private_key):
  return bytes_to_hex(ed25519_blake2b.SigningKey(hex_to_bytes(private_key)).get_verifying_key().to_bytes())

def get_address_from_public_key(public_key):
  #nanoo.tools
  public_key = hex_to_bytes(public_key)
  first = encode_base32(public_key)
  blake_obj = blake2b(digest_size=5)
  blake_obj.update(public_key)
  #reverse
  checksum = encode_base32(blake_obj.digest()[::-1])
  #base 32 public key, add checksum
  return "nano_"+first+checksum

def get_public_key_from_address(address):
  #ignore checksum for now. todo: don't ignore
  address = address.replace("nano_", "")
  return bytes_to_hex(decode_base32(address[0:52]))

def hash_block(block):
  blake_obj = blake2b(digest_size=32)
  blake_obj.update(hex_to_bytes(PREAMBLE))
  blake_obj.update(hex_to_bytes(get_public_key_from_address(block["account"])))
  blake_obj.update(hex_to_bytes(block["previous"]))
  blake_obj.update(hex_to_bytes(get_public_key_from_address(block["representative"])))
  padded_balance = hex(int(block["balance"])).replace("0x","")
  while len(padded_balance) < 32:
    padded_balance = '0' + padded_balance
  blake_obj.update(hex_to_bytes(padded_balance))
  blake_obj.update(hex_to_bytes(block["link"]))
  return bytes_to_hex(blake_obj.digest())

def sign(private_key, hash):
  #ed25519_blake2b verify
  signing_key = ed25519_blake2b.SigningKey(hex_to_bytes(private_key))
  sign = bytes_to_hex(signing_key.sign(hex_to_bytes(hash)))
  return sign

def whole_to_raw(whole: str):
  return int(Decimal(whole)*(10**NANO_DECIMALS))

def raw_to_whole(raw: int, precision: int = 2):
  return math.floor((raw*10**precision)/(10**NANO_DECIMALS))/10**precision
