# bitcoin
* P2PC (Pay to Prototype Compressed)
- Address = Compressed public key -> encode Bech32, Bech32m
- Create transaction data: version,....,txid input, vout, ...........,scriptPubkey.............,nLocktime.
| With scriptPubkey = Decode Address
- Output unlock: version,..............................................Witness(32bytes of S), nLocktime.
| With Witness = dhash256(txid input & vout) * Xpublic + dhash256(unsigned raw transaction) mod (private key)
| Witness mod (N) = Number 32 bytes
- Verify: 
- p1 = ECC(G, dhash256(unsigned raw transaction) mod (Witness)) 
- x1, y1 = ECC(G, dhash256(txid input & vout))
- p2 = ECC((x1,y1), x mod (Witness)) 
- x2, y2 = ECAdd(p1, p2) 
- If x2 = x (of scriptPubkey)
- OK
