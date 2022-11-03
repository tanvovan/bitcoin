# bitcoin
P2PC
Address = Compressed public key -> encode Bech32, Bech32m
- Create transaction data: version,....,txid input, vout, ...........,scriptPubkey.............,nLocktime.
With scriptPubkey = Decode Address
- Output unlock: version,..............................................Witness, nLocktime.
With Witness = dhash256(txid input + vout) * x + dhash256(unsigned raw transaction) mod (private key)
| Witness mod (N) = 32 bytes
- Verify: 
