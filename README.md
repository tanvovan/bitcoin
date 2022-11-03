# bitcoin
* P2PC (Pay to Prototype Compressed)
- Address = Compressed public key -> encode Bech32, Bech32m
- Create transaction data: version,....,txid input, vout, ...........,scriptPubkey.............,nLocktime.
| With scriptPubkey = Decode Address
- Output unlock: version,..............................................Witness, nLocktime.
| With Witness = dhash256(txid input + vout) * x + dhash256(unsigned raw transaction) mod (private key)
| Witness mod (N) = Number 32 bytes
- Verify: 
- p1 = ECC(G, (dhash256(unsigned raw transaction) mod (Witness))) 
- p2 = ECC(ECC(G, dhash256(txid input + vout)), (x mod (Witness))) 
- x1, y1 = ECAdd(1, 2) 
- If x1 = x
- OK
