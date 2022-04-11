# **Kriptografija i mrežna sigurnost - Lab 5** <!-- omit in toc -->

- [CTR encryption mode and repeated counters](#ctr-encryption-mode-and-repeated-counters)
- [Zadatak](#zadatak)
  - [Korisne smjernice za automatizaciju u Pythonu](#korisne-smjernice-za-automatizaciju-u-pythonu)
    - [XOR-ing two large binary strings](#xor-ing-two-large-binary-strings)
    - [Converting `int` to `bytes`](#converting-int-to-bytes)
    - [Converting `bytes` to a string (`str`)](#converting-bytes-to-a-string-str)

## CTR encryption mode and repeated counters

Slično CBC modu, _Counter (CTR) encryption mode_ **probabilistički** je način enkripcije poruka, gdje se _plaintext_ enkriptira jednostavnom _xor_ operacijom s generiranim _pseudo-slučajnim_ nizom ključeva (_pseudorandom key stream_). Pseudo-slučajan niz ključeva generira se na način da se danom blok šiftom (npr. AES) enkriptiraju sukcesivne vrijednosti brojača (_counter_) kako je prikazano na priloženoj slici.

<p align="center">
<img src="../img/ctr.png" alt="CTR encryption" width="450px" height="auto"/>
<br><br>
<em>Enkripcija u CTR modu</em>
</p>

CTR mod enkripcije siguran je način enkripcije (osigurava povjerljivost podataka) ali uz važan preduvjet: **isti brojač (_counter_) ne smije se ponoviti (enkriptirati više puta) pod istim enkripcijskim ključem _K_**. U slučaju ponavljanja istog brojača (pod istim ključem K), moguće je dekriptirati _ciphertext_ bez poznavanja enkripcijskog ključa _K_.

## Zadatak

Zadatak studenta u okviru vježbe je dekriptirati odgovarajući izazov (_challenge_). Za razliku od prethodnih vježbi, u ovoj vježbi izazov je 
enkriptiran u CTR enkripcijskom modu, pri čemu je enkripcijski ključ generiran nasumično (nije izveden iz predefinirane tajne vrijednosti _cookie_). Ranjivost _crypto oracle_ u ovoj vježbi proizlazi iz činjenice da se **brojač bira (nasumično) iz ograničenog/malog skupa brojeva**. Posljedica opisanog načina generiranja brojača za CTR mod je ta da će se nakon određenog broja enkripcija brojač ponaviti što napadaču omogućuje dekripciju _ciphertext_-a bez poznavanja enkripcijskog ključa.

Student će iskoristiti gore opisani propust u _crypto oracle_-u i dekriptirati činjenicu o Chuck Norris-u koja je ovaj put enkriptirana u CTR modu. **U osnovi, nakon što student pošalje dovoljan broj poruka serveru na enkripciju u CTR modu, jedna od poruka biti će enkriptirana pod istim _counter_-om (i ključem) kao i činjenica o Chuck Norris-u.** U tom slučaju vrijedi:

ciphertext<sub>Chuck_Norris_fact</sub> ⊕ plaintext<sub>Chuck_Norris_fact</sub> = ciphertext<sub>chosen_plaintext</sub> ⊕ chosen_plaintext 

> Zadatak u koracima: _password_ &rarr; token &rarr; Chuck Norris fact. Prisjetite se, _password_ ste otkrili u prethodnoj vježbi.

### Korisne smjernice za automatizaciju u Pythonu

Možete iskoristiti popriličnu količinu koda sa prethodnih vježbi.

> VAŽNO: Za razliku od prethodne vježbe (CBC), _plaintext_ poruke koje šaljete _crypto oracle_ će se procesirati kao `utf-8` stringovi (ne trebate ih konvertirati u `hex`).

#### XOR-ing two large binary strings

U Python-u ne možemo izravno raditi _xor_ operaciju između podataka tipa `byte` već ih trebamo prethodno convertirati u `int`.

```python
A_as_int = int.from_bytes(A_as_bytes, byteorder="big")
B_as_int = int.from_bytes(B_as_bytes, byteorder="big")

C_as_int = A_as_int ^ B_as_int
```

#### Converting `int` to `bytes`

```python
# Convert C back to 16 bytes long string
C_as_bytes = C_as_int.to_bytes(16, "big").hex()
```

#### Converting `bytes` to a string (`str`)

```python
# Default encoding is 'utf-8'
C_as_string = C_as_bytes.decode(errors="ignore")
```

By setting `errors="ignore"` we instruct the interpreter to ignore bytes (do not rise exceptions) that cannot be properly decoded.
