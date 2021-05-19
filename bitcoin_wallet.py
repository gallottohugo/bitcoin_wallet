from bit import PrivateKey, PrivateKeyTestnet, wif_to_key
from bit.format import bytes_to_wif
from bit.network import satoshi_to_currency, currency_to_satoshi
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


	def send_bitcoins(self, from_user, to_address, amount, currency, testnet=False):
		try:
			private_key = self.convert_wif_to_privatekey(from_user, testnet)
			if currency in self.supported_currencies().keys():
				tx_hash = private_key.send([(to_address, amount, currency)])
				return tx_hash
			else: return None
		except: return None


	def send_bitcoins_with_fee(self, from_user, to_address, amount, testnet=False):
		try:
			total_fee = 0.00015000
			currency = 'satoshi'
			
			satoshi_amount = int(amount * 100000000)
			satoshi_fee = int(total_fee * 100000000)

			private_key = self.convert_wif_to_privatekey(from_user, testnet)
			if currency in self.supported_currencies().keys():
				tx_hash = private_key.send([(to_address, satoshi_amount, currency)], fee=satoshi_fee, absolute_fee=True, leftover=private_key.address)
				return tx_hash
			else: return None
		except: return None


	@staticmethod
	def satoshi_to_currency(self, satoshi, currency):
		if currency in self.supported_currencies().keys():
			return satoshi_to_currency(satoshi, currency)
		else:
			return None


	@staticmethod
	def currency_to_satoshi(self, amount, currency):
		if currency in self.supported_currencies().keys():
			return currency_to_satoshi(amount, currency)
		else:
			return None



	@staticmethod
	def convert_wif_to_privatekey(user, testnet=False):
		if testnet == True:
			private_key_wif = user.wallet_crypto.btc_private_key_testnet
		else:
			private_key_wif = user.wallet_crypto.btc_private_key

		private_key = wif_to_key(private_key_wif)
		return private_key