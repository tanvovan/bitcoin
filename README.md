# Generate and verify ECDSA signature without "r"
- 1. Address: private key -> ECC -> public key compression -> Bech32m encode
- 2. scriptPubkey: Address -> Bech32m decode -> public key compression
- 3. Segwit: (dsha256(txid_input & index) * x public key + dsha256(unsigned raw transaction) mod (private key)) mod (N) => Will give a number of 32 bytes
- 4. Verify:
- x1, y1 = ECC(G * dsha256(txid_input & index))
- p1 = ECC(G * dsha256(unsigned raw transaction) mod (Segwit))
- p2 = ECC((x1,y1) * x public key mod (Segwit)
- x2, y2 = ECAddpoint(p1, p2)
- If x2 = x public key => OK
