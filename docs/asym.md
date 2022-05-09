# **Kriptografija i mrežna sigurnost - Lab 6**

## Asymmetric cryptography: RSA signatures and DH key exchange

Student će realizirati protokol prikazan u nastavku. Protokol u osnovi implementira potpisani _Diffie-Hellman key exchange protocol_ i omogućava uspostavu dijeljenog simetričnog ključa sa serverom. Uspostavljeni ključ se u konačnici koristi za zaštitu povjerljivosti _challenge_-a.

>**DISCLAIMER: _Prikazani protokol služi isključivo za edukativnu svrhu. U ovoj formi protokol nije siguran._**

### Opis protokola

Popis oznaka u protokolu:

| Oznaka                                 | Opis                                                              |
| -------------------------------------- | :---------------------------------------------------------------- |
| C                                      | klijent (student/ovo računalo)                                    |
| S                                      | server (_crypto oracle_)                                          |
| RSA<sub>priv</sub>                     | privatni RSA key                                                  |
| RSA<sub>priv,C</sub>                   | klijentov privatni RSA ključ                                      |
| RSA<sub>pub</sub>                      | javni RSA ključ                                                   |
| DH<sub>priv</sub>                      | privatni DH ključ                                                 |
| DH<sub>priv,C</sub>                    | klijentov privatni DH ključ                                       |
| DH<sub>pub</sub>                       | javni DH ključ                                                    |
| DH<sub>parameters</sub>                | javni DH parametri: _prime modulus_ (p) i _group generator_ (g)   |
| **Sig**(RSA<sub>priv</sub></sub>, _m_) | RSA digitalno potpisana poruka _m_                                |
| `shared_secret`                        | dijeljena DH tajna (i.e., g<sup>xy</sup> mod p)                   |
| K                                      | AES simetrični ključ izveden iz djeljene tajne `shared_secret`    |
| **AES-256-CBC**(K, _m_)                | enkripcija poruke _m_ u CBC modu s AES šifrom i 256-bit ključem K |
| _a_ \|\| _b_                           | konkatenacija (spajanje) poruka _a_ i _b_                         |

#### Protokol:

| Tko šalje  | Poruka koja se šalje                                                                                                                  |
| :--------: | :------------------------------------------------------------------------------------------------------------------------------------ |
| C &rarr; S | RSA<sub>pub,C</sub>                                                                                                                   |
| S &rarr; C | RSA<sub>pub,S</sub>, DH<sub>parameters</sub>                                                                                          |
| C &rarr; S | DH<sub>pub,C</sub> \|\| **Sig**(RSA<sub>priv,C</sub></sub> , DH<sub>pub,C</sub>)                                                      |
| S &rarr; C | DH<sub>pub,S</sub> \|\| **Sig**(RSA<sub>priv,S</sub></sub> , DH<sub>parameters</sub> \|\| DH<sub>pub,S</sub> \|\| DH<sub>pub,C</sub>) |
| S &rarr; C | **AES-256-CBC**(K, "...Chuck Norris...")                                                                                              |

> Primjetite da šala u posljednjoj poruci nije autenticirana; ne štitimo njen integritet. U praksi, uz povjerljivost želite zaštititi i integritet poruke.

Klijent C i server S, po uspješnom prijemu odgovarajućih poruka, provjeravaju digitalne potpise, zatim izvode zajedničku Diffie-Hellman tajnu `shared_secret`, te iz te tajne 256-bitni AES ključ K kojim se enkriptira studentova šala (u CBC modu). Ključ K izvodi se iz `shared_secret` kako je prikazano u nastavku (`HKDF` je tzv. [_hash-based key derivation function_](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/?highlight=hkdf)):

```python
const K = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"ServerClient",
        info=None
    ).derive(shared_secret)
```
