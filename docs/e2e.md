# **Kriptografija i mrežna sigurnost - Lab 7** <!-- omit in toc -->

- [Securing end-2-end communication](#securing-end-2-end-communication)
- [Redosljed primjene enkripcijskih i autentikacijskih funkcija](#redosljed-primjene-enkripcijskih-i-autentikacijskih-funkcija)
  - [**_Encrypt-and-Authenticate (EaA)_**](#encrypt-and-authenticate-eaa)
  - [**_Authenticate-than-Encrypt (AtE)_**](#authenticate-than-encrypt-ate)
  - [**_Encrypt-than-Authenticate (EtA)_**](#encrypt-than-authenticate-eta)
- [Zadatak](#zadatak)
  - [Pripremne radnje](#pripremne-radnje)

## Securing end-2-end communication

Cilj ove vježbe je u okviru jednostavnog _chat_ servisa osigurati **povjerljivost** i **autentičnost** razmjenjenih poruka. Preciznije, servis će osigurati neke od sljedećih svojstava:

1. povjerljivost (_**forward secure key updating**_),
2. autentičnost izvorišta poruka (_**source integrity**_),
3. integritet samih poruka (_**data integrity**_),
4. zaštitu od _**replay**_ napada.

Navedena zaštita implementirat će se prema principu _**end-2-end**_; drugim riječima, samo krajnji korisnici/entiteti će moći pristupiti sadržaju poruka, odnosno detektirati pokušaje narušavanja integriteta na posredničkom serveru.

Svojstvo **forward secrecy** ćemo implementirati (samo dijelom) prema specifikacijama [Signal protokola](https://signal.org/docs/specifications/doubleratchet/#symmetric-key-ratchet) na kojem je zasnovan i popularni WhatsApp.

## Redosljed primjene enkripcijskih i autentikacijskih funkcija

Prilikom zaštite poruke _M_ jedan od velikih izazova je odrediti siguran redosljed primjene enkripcijske funkcije **_c = E<sub>Ke</sub>(M)_** i autentikacijske funkcije **_tag=MAC<sub>Ka</sub>(M)_**. Odabir ispravnog redosljeda/kompozicije kriptografskih funkcija krucijalan je za sigurnost podataka. Postoji nekoliko mogućnosti kompozicije enkripcijskih i autentikacijskih funkcija:

### **_Encrypt-and-Authenticate (EaA)_**

U ovom slučaju, poruka _M_ štiti se na način da se enkripcijska funkcija _E<sub>Ke</sub>(.)_ i autentikacijska funkcija _MAC<sub>Ka</sub>(.)_ primjenjuju neovisno jedna o drugoj. _Ciphertext_ i autentikacijski tag za poruku _M_ računaju se kako slijedi:

> _<p align="center">c = E<sub>Ke</sub>(M), &nbsp; tag=MAC<sub>Ka</sub>(M)</p>_

### **_Authenticate-than-Encrypt (AtE)_**

_Ciphertext_ i autentikacijski tag za poruku _M_ računaju se kako slijedi:

> _<p align="center">tag=MAC<sub>Ka</sub>(M), &nbsp; c = E<sub>Ke</sub>(M || tag)</p>_

U ovom slučaju, pošiljatelj najprije izračuna autentikacijski tag za danu poruku (primjeni autentikacijsku funkciju) a zatim enkriptira poruku _M_ zajedno s tagom _tag_.

### **_Encrypt-than-Authenticate (EtA)_**

_Ciphertext_ i autentikacijski tag za poruku _M_ računaju se kako slijedi:

> _<p align="center">c = E<sub>Ke</sub>(M), &nbsp; tag = MAC<sub>Ka</sub>(c)</p>_

Pošiljatelj najprije enkriptira poruku (primjeni enkripcijsku funkciju), zatim generira autentikacijski tag ali ne za originalnu poruku _M_ već za _ciphertext_ iz prethodnog koraka.

**NAPOMENA:** Dobra sigurnosna praksa nalaže korištenje različitih odnosno međusobno neovisnih simetričnih ključeva u enkripcijskim i autentikacijskim funkcijama (_Ke &ne; Ka_).

Iako se u praksi koriste sve tri kompozicije, **_Encrypt-than-Authenticate (EtA)_** preporučena je kompozicija. _EtA_ kompozicija, ispravno primjenjena, osigurava zaštitu od najjače kategorije napada na kriptografske sustave: **_chosen ciphertext attacks_.** Kod ove kategorije napada napadač priprema _ciphertext_, šalje ga žrtvi, te od žrtve očekuje odgovarajući _plaintext_. Budući da je kod _EtA_ kompozicije integritet _ciphertext_-a zaštićen, a žrtva prije dekripcije primljenog _ciphertext_-a provjerava integritet istog, žrtva će odbaciti neispravan/modificiran _ciphertext_ prije njegove dekripcije. Na ovaj način napadač ne može dobiti odgovarajući _plaintext_. U okviru labova korisit ćemo stoga _Encrypt-than-Authenticate (EtA)_ kompoziciju.

Nekoliko referenci na ovu temu:

- [Padding oracles and the decline of CBC-mode cipher suites](https://blog.cloudflare.com/padding-oracles-and-the-decline-of-cbc-mode-ciphersuites/)
- [Should we MAC-then-encrypt or encrypt-then-MAC?](https://crypto.stackexchange.com/questions/202/should-we-mac-then-encrypt-or-encrypt-then-mac)

## Zadatak

Implementirati i testirati _end-2-end_ zaštitu poruka između dva klijenta. Pri tome je potrebno osigurati: _povjerljivost_, _autentičnost/integritet_, kao i zaštitu od _replay_ napada. Zaštitu implementirati primjenom CBC moda (povjerljivost) i HMAC autentikacijske funkcije (integritet) u _Encrypt than Authenticate (EtA)_ komopoziciji (WhatsApp koristi ovaj pristup).

### Pripremne radnje

1. Klonirajte repozitorij sa inicijalnom implementacijom _chat_ aplikacije kako je prikazano u nastavku:

   ```bash
   git clone https://github.com/mcagalj/CNS-2021-22-Lab7-E2E.git
   ```

2. Aktivirajte Python virtualno okruženje.
3. Pozicionirajte se unutar kloniranog direktorija i instalirajte odgovarajuće Python pakete (_package_) izvršavanjem sljedeće naredbe u konzoli:

   ```bash
   pip install -r requirements.txt
   ```

4. Pokrenite aplikaciju (primitivna/rudimentarna _chat_ klijent aplikacija) kako slijedi:

   ```bash
   # Flag -h will show help
   python -m app.main -h
   ```

5. Pokrenite _unit_ testove kako slijedi:

   ```bash
   pytest -v
   ```

   Alat [pytest](https://docs.pytest.org) ćemo koristiti za povremeno testiranje aplikacije.
