from bech32m import encode, decode
import hashlib

Prime = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
xB = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
yB = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
GPoint = (xB,yB)
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def modinv(a,n):
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high//low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def ECadd(a,b): # EC Addition
    λ = ((b[1]-a[1]) * modinv(b[0]-a[0],Prime)) % Prime
    x = (λ**2-a[0]-b[0]) % Prime
    y = (λ*(a[0]-x)-a[1]) % Prime
    return (x,y)

def ECdouble(a): # EC Doubling
    λ = ((3*a[0]*a[0]) * modinv((2*a[1]),Prime)) % Prime
    x = (λ**2-2*a[0]) % Prime
    y = (λ*(a[0]-x)-a[1]) % Prime
    return (x,y)

def EccMultiply(GenPoint,ScalarHex): # Doubling & Addition
    if ScalarHex == 0 or ScalarHex >= N: raise Exception("Invalid Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    Q=GenPoint
    for i in range (1, len(ScalarBin)):
        Q=ECdouble(Q)
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint)
    return (Q)

priv = int('72777925c653a50f0bd132ebbbc3693c8668263578ba79e56e13a65820097ecc',16)
xpub, ypub = EccMultiply(GPoint, priv)


def compr(x, y): # compress public key 
    if y % 2 == 0:
        compress = '02' + '{:064x}'.format(x)
    if y % 2 == 1:
        compress = '03' + '{:064x}'.format(x)
    return compress

# Create address

bytes_compress = bytes.fromhex('0021' + compr(xpub,ypub))
address = encode('bc', 1, bytes_compress[2:])
print('Address:', address)

#--------------------------------scriptPubkey(Output lock)-----------------------
addr = 'bc1pq0qendqa9a0taq3a5y80hsll9h7jjryd7ptqwychunwnynsf5klkww463ne'
decoded = bytes(decode('bc', addr)).hex()
scriptPubkey = '21' + decoded
print('scriptPubkey:', scriptPubkey)
#--------------------------------Witness(Output unlock)--------------------------
message = 34963332507398480427682254676401311569483304378095876365101580641046399456536 # unsigned raw transaction
txid_input = '4e70baf76571193c34cf6dd12ac0fa677a6250386ade9c59ac6819dbe3ea28bf' + '00000000'
dsha256 = int(hashlib.sha256(hashlib.sha256(bytes.fromhex(txid_input)).digest()).hexdigest(),16)
s = (dsha256 * xpub + message)* modinv(priv,N)%N
s = '{0:x}'.format(s)
if len(s)% 2 == 1:
    s = '0' + s
print('Witness:', s) # Witness is just "s"
#--------------------------------verify(nodes)-----------------------------
x = bytes.fromhex(scriptPubkey)[1:].hex()
def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

y_parity = int(x[:2],16) - 2
x = int(x[2:], 16)
dx = (pow_mod(x, 3, Prime) + 7) % Prime
dy = pow_mod(dx, (Prime+1)//4, Prime)

if dy % 2 != y_parity:
    dy = -dy % Prime
    
y = dy

p1 = EccMultiply(GPoint,(message * modinv(int(s,16),N))%N) # message: unsigned raw transaction
x1, y1 = EccMultiply(GPoint, dsha256)
p2 = EccMultiply((x1, y1),(x * modinv(int(s,16),N))%N)
x2,y2 = ECadd(p1, p2)
print('Verify:',x2 == x) # True

