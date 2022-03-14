
# **Kriptografija i mrežna sigurnost - Lab 1** <!-- omit in toc -->

- [Man-in-the-middle attacks (ARP spoofing)](#man-in-the-middle-attacks-arp-spoofing)
- [ARP spoofing](#arp-spoofing)
- [Zadatak](#zadatak)
- [Zadatak u koracima](#zadatak-u-koracima)
  - [Presretanje autentikacijskog tokena](#presretanje-autentikacijskog-tokena)
  - [Tajni `cookie`](#tajni-cookie)
  - [Dekripcijski ključ](#dekripcijski-ključ)
  - [Dekripcija izazova](#dekripcija-izazova)
  - [Pohrana rješenja u GitLab repo](#pohrana-rješenja-u-gitlab-repo)

## Man-in-the-middle attacks (ARP spoofing)

U okviru vježbe upoznajemo se s osnovnim sigurnosnim prijetnjama i ranjivostima u računalnim mrežama. Analizirat ćemo ranjivost _Address Resolution Protocol_-a (_ARP_) koja napadaču omogućava izvođenje _man in the middle_ napada na računala koja dijele zajedničku lokalnu mrežu (_LAN_).

## ARP spoofing

<p align="center">
<img src="../img/arp_spoofing.png" width="650px" height="auto"/>
</p>

## Zadatak

Dekriptirati _crypto_ izazov (_challenge_) enkriptiran _AES šifrom u CBC enkripcijskom modu rada_ (AES-CBC); korištene kratice i terminologija vam u ovom trenutku možda nisu bliske ni poznate, no s vremenom će sve "sjesti na svoje mjesto". Dekripcijski ključ potreban za dekripciju izazova otkriti ćete u interakciji s _crypto oracle_ serverom .

Ključ za enkripciju/dekripciju, u okviru ove vježbe, izveden je iz tajne vrijednosti koju zovemo _cookie_. Tajni _cookie_ možete dobiti slanjem sljedećeg REST API zahtjeva _crypto oracle_ serveru: `GET /arp/cookie`. Ovaj zahtjev mora biti autoriziran odgovarajućim autentikacijskim tokenom. Token možete dobiti slanjem korisničkog imena (ime vašeg Docker _container_-a) i odgovarajuće lozinke _crypto oracle_ serveru kako slijedi:

```txt
POST username=my_name&password=my_pass /arp/token`
```

> Zadatak u koracima: (password &rarr;) token &rarr;  cookie &rarr; key &rarr; Chuck Norris fact.

## Zadatak u koracima

### Presretanje autentikacijskog tokena

> Zadatak u koracima: **token** &rarr;  cookie &rarr; key &rarr; Chuck Norris fact.

Iskoristiti ranjivost ARP protokola i izvršiti MitM napad na način da presretnete komunikaciju između _crypto oracle_ servera i računala `arp_client`. Računalo `arp_client` periodično se logira na _crypto oracle_ server slanjem zahtjeva:

```txt
POST username=my_name&password=my_pass /arp/token
```

Na ovaj zahtjev, _crypto oracle_ odgovara slanjem autentikacijskog tokena u sljedećem formatu:

```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

Za izvođenje ovog napada, za student će koristiti specijalizirano napadačko računalo koje u nazivu ima sufiks `_arpspoof`.

1. Otvorite dva (2) _remote_ terminala na svom napadačkom računalu (prethodno trebate saznati njegovu IP adresu, e.g., `10.0.15.x`):

    ```cmd
    ssh prezime_ime@10.0.15.x
    ```

2. Prije izvršavanja napada, otkrijte MAC i IP adrese za _crypto oracle_, `_arpspoof` i `arp_client` računala. Za ove potrebe možete (u prethodno otvorenom terminalu) koristiti naredbe `ifconfig`, `ping` i `arp`.

3. Jedan terminal koristite za osluškivanje prometa na lokalnoj mrežnoj kartici. Za ovo korisite `tcpdump` program, kojeg trebate pokretati sa administratorskim ovlastima (`sudo tcpdump`).

    ```cmd
    sudo tcpdump
    ```

    Koji tip mrežnog prometa vidite?

4. Drugi terminal koristite za izvršavanje **ARP spoofing** napada. Za napad koristite program `arpspoof`, kojeg također trebate pokretati sa administratorskim ovlastima (`sudo arpspoof`).

    ```bash
    # Usage: arpspoof [-i interface] [-c own|host|both] [-t target] [-r] host
    sudo arpspoof
    ```

    Izvršite MitM napad na način da presretnete komunikaciju u smjeru od _crypto_oracle_ servera prema `arp_client` računalu; drugim rječima lažno se predstavite _crypto_oracle_ računalu kao `arp_client`.

5. Nakon što ste pokrenuli napad, u prvom terminalu filtrirajte ARP pakete kako slijedi:

    ```cmd
    sudo tcpdump arp and host arp_client.macvlan
    ```

    Komentirajte rezultat.

6. Popunite sljedeća polja zaglavlja mrežnih paketa koje šalje žrtva (_crypto_oracle_) `arp_client` računalu:

    |               | MAC<sub>src</sub> | MAC<sub>dst</sub> | IP<sub>src</sub> | IP<sub>dst</sub> |
    | ------------- | ----------------- | ----------------- | ---------------- | ---------------- |
    | Before attack |                   |                   |                  |                  |
    | After attack  |                   |                   |                  |                  |

7. Autentikacijski token koji _crypto_oracle_ šalje `arp_client` računalu možete doznati primjenom odgovarajućeg `tcpdump` filtra.

    ```cmd
    sudo tcpdump -vvAls0 | grep "access_token"
    ```

    Kopirajte token i prekinite napad (`Ctrl + C`).

### Tajni `cookie`

> Zadatak u koracima: token &rarr;  **cookie** &rarr; key &rarr; Chuck Norris fact.

### Dekripcijski ključ

> Zadatak u koracima: token &rarr;  cookie &rarr; **key** &rarr; Chuck Norris fact.

**HINT:** Pogledati _output_ sa prošlih labova i/ili pogledati izvorni kod _crypto_oracle_-a (kako se izvodi enkripcijski ključ za enkripciju izazova za ARP lab).

### Dekripcija izazova

> Zadatak u koracima: token &rarr;  cookie &rarr; key &rarr; **Chuck Norris fact**.

**HINT:** Pogledati _output_ sa prošlih labova i/ili pogledati izvorni kod _crypto_oracle_-a (kako se enkriptira izazov za ARP lab).

> Testirajte okrivenu lozinku.

### Pohrana rješenja u GitLab repo

Potrebno pohraniti:

1. Popunjenu tablicu sa MAC i IP adresama (koristitie `markdown` format).
2. Dekriptirani izazov i zaporku za otključavanje sljedećih labova (možete staviti u istu `markdown` datoteku kao i prethodnu tablicu).
3. Python skriptu za dekripciju izazova.
