from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39WordsNum, Bip39SeedGenerator
import json

num = int(input("How many addresses do you need: "))

# Seed bytes
mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
print(mnemonic)
seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
# Create from seed
bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)

# Derive account 0 for Bitcoin: m/44'/0'/0'
bip44_acc = bip44_mst.Purpose() \
                     .Coin()    \
                     .Account(0)
# Derive the external chain: m/44'/0'/0'/0
bip44_change = bip44_acc.Change(Bip44Changes.CHAIN_EXT)
f = open("newgen.txt", 'w')
fw = open("addresses_only.txt", 'w')
f.write("[")
for i in range(num):
    newaddr = {}
    bip44_addr = bip44_change.AddressIndex(i)
    newaddr["addr"] = bip44_addr.PublicKey().ToAddress()
    newaddr["publ_key"] = bip44_addr.PublicKey().ToExtended()
    newaddr["priv_key_ext"] = bip44_addr.PrivateKey().ToExtended()
    newaddr["priv_key_wif"] = bip44_addr.PrivateKey().ToWif()
    if i != num-1:
        f.write(json.dumps(newaddr, indent=1)+",\n")
    else:
        f.write(json.dumps(newaddr, indent=1)+"]")
    fw.write(newaddr["addr"]+"\n")
    if i%10000 == 0:
        print(f"{i} addresses ready.")
        
f.close()
fw.close()
