import numpy as np

def gen_primes(n):
    primes = np.zeros(n, dtype=np.int64)
    primes[0] = 2
    i = 1
    c = 5
    while i < n:
        if np.all(c % primes[:i]):
            primes[i] = c
            i += 1
        c += 2
    return primes

def rsa(p, q, sel_candidate=np.random.choice, verbose=True):
    n = p * q
    phi = np.lcm(p - 1, q - 1)
    
    ks = np.arange(1, phi, 1)
    ks = np.where(np.gcd(ks, phi) == 1, ks, 0)
    ks = ks[ks != 0]
    k = sel_candidate(ks)
    
    ds = np.arange(1, 100000, 1)
    ds = np.where(ds * k % phi == 1, ds, 0)
    ds = ds[ds != 0]
    d = sel_candidate(ds)

    if verbose: 
        print(f'''
p={p}, q={q}
n={n}
phi={phi}
k={k}
d={d}
        ''')
    return (int(n), int(k)), (int(n), int(d))

def double_expo(base, exponent, modulo):
    result = 1
    while exponent > 0:
        if not exponent & 1:
            base = base**2 % modulo
            exponent >>= 1
        else:
            result = result * base % modulo
            exponent -= 1
    return result

def get_primes_for_string(s):
    ords = [ord(c) for c in s]
    primes = gen_primes(1000)
    candidates = primes[np.append(primes[:-1] * primes[1:] > max(ords), [True])]
    return candidates[:2]

def _crypt(string, modulo, exponent):
    return ''.join(chr(double_expo(ord(c), exponent, modulo)) for c in  string)

decrypt = encrypt = _crypt


to_encrypt = "Very cool string here bruh. Уникод 先輩に気づいて"
p, q = get_primes_for_string(to_encrypt)
public, private = rsa(p, q)

encrypted = encrypt(to_encrypt, *public)
decrypted = decrypt(encrypted, *private)
print(encrypted, decrypted, sep='\n')
