from bit import PrivateKey, PrivateKeyTestnet
from bit.format import bytes_to_wif

from wallets_crypto.models import WalletCrypto

class BitcoinWallet():
	def create_wallet(self, user):
		try:
			user.wallet_crypto
			return None
		except:
			""" Wallet Crypto """
			prikey = PrivateKey()
			prikey_wif = prikey.to_wif()
			pubkey = prikey.public_key
			pubkey_wif = bytes_to_wif(pubkey, compressed=False)
			address = prikey.address


			""" Wallet Crypto TestNet """
			prikey_testnet = PrivateKeyTestnet()
			prikey_wif_testnet = prikey_testnet.to_wif()
			pubkey_testnet = prikey_testnet.public_key
			pubkey_testnet_wif = bytes_to_wif(pubkey_testnet, compressed=False)
			address_testnet = prikey_testnet.address


			wallet_crypto = WalletCrypto()
			wallet_crypto.owner_id = user.id
			wallet_crypto.btc_private_key = prikey_wif
			wallet_crypto.btc_public_key = pubkey_wif
			wallet_crypto.btc_address = address
			wallet_crypto.btc_private_key_testnet = prikey_wif_testnet
			wallet_crypto.btc_public_key_testnet = pubkey_testnet_wif
			wallet_crypto.btc_address_testnet = address_testnet
			wallet_crypto.save()
			return wallet_crypto


	def get_balance(self, user, currency, testnet=False):
		try:
			if currency in self.supported_currencies().keys():
				private_key = self.convert_wif_to_privatekey(user, testnet)
				balance = private_key.get_balance(currency)
				return balance
			else:
				return None
		except:
			return None

	def get_transactions(self, user, testnet=False):
		try:
			private_key = self.convert_wif_to_privatekey(user, testnet)
			txs = private_key.get_transactions()
			return txs
		except: return []


	