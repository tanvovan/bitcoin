# bitcoin
* P2PC (Pay to Prototype Compressed)
- Address = Compressed public key -> encode Bech32, Bech32m
- Transaction data 1 (Output lock):   version,...............,scriptPubkey,.............,nLocktime.
| With scriptPubkey = Decode Address
- Transaction data 2 (Output unlock): version,....,txid input, vout,.......,Witness(32bytes of S), nLocktime.
| With Witness = dhash256(txid input & vout) * Xpublic + dhash256(unsigned raw transaction) mod (private key)
| Witness mod (N) = Number 32 bytes
- Verify: 
- p1 = ECC(G, dhash256(unsigned raw transaction) mod (Witness)) 
- x1, y1 = ECC(G, dhash256(txid input & vout))
- p2 = ECC((x1,y1), x mod (Witness)) 
- x2, y2 = ECAdd(p1, p2) 
- If x2 = x (of scriptPubkey)
- OK
