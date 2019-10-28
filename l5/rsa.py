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

def rsa(p, q, sel_candidate=lambda cs, name: np.random.choice(cs), verbose=True):
    n = p * q
    phi = np.lcm(p - 1, q - 1)
    
    ks = np.arange(2, phi, 1)
    ks = np.where(np.gcd(ks, phi) == 1, ks, 0)
    ks = ks[ks != 0]
    k = sel_candidate(ks, name='k')
    
    ds = np.arange(2, 100000, 1)
    ds = np.where(ds * k % phi == 1, ds, 0)
    ds = ds[ds != 0]
    d = sel_candidate(ds, name='d')

    if verbose: 
        print(f'''
p={p}, q={q}
n={n}
phi={phi}
k={k}
d={d}
        ''')
    return (int(n), int(k)), (int(n), int(d))


def sel_prompt(candidates, name):
    print(f"Choosing {name}")
    print(f"Candidates are:\n")
    print(candidates)
    i = None
    while True:
        i = int(input("Input number from candidates:"))
        if not i in candidates:
            print(f"This number is not in candidates")
        else:
            break
    return i

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


to_encrypt = '''
Более короткая строка здесь
Test test test yes man I like me some cookies
'''
p, q = get_primes_for_string(to_encrypt)
public, private = rsa(p, q, sel_candidate=sel_prompt)

encrypted = encrypt(to_encrypt, *public)
decrypted = decrypt(encrypted, *private)
print(encrypted, decrypted, sep='\n')
