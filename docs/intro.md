# **Kriptografija i mrežna sigurnost - Lab 1** <!-- omit in toc -->

- [Setting up the stage](#setting-up-the-stage)
  - [Uvod](#uvod)
  - [Pristup osobnom serveru](#pristup-osobnom-serveru)
  - [Pohrana rješenja (GitLab)](#pohrana-rješenja-gitlab)
- [Važni linkovi](#važni-linkovi)

## Setting up the stage

### Uvod

Student rješava izazove u interackciji sa REST API serverom kojeg kolokvijalno nazivamo _crypto oracle_. _Crypto oracle_ server generira izazove u obliku enkriptiranog teksta ([Chuck Norris facts](https://api.chucknorris.io/)) kojeg student treba dekriptirati. Dekripcijski ključ student treba otkriti u interakciji sa serverom.

> Uspješnom dekripcijom izazova, student uz novu činjenicu o Chuck Norrisu, otkriva i **zaporku** potrebnu za pristup sljedećoj vježbi.

Server je pisan u Python web okviru [FastAPI](https://fastapi.tiangolo.com/). Izvorni kod servera dostupan je u GitHub repozitoriju [CNS-2021-22](https://github.com/mcagalj/CNS-2021-22). Za kriptografske potrebe korištena je Python biblioteka (_package_) [`cryptography`](https://cryptography.io).

### Pristup osobnom serveru

Za svakog studenta pokreće se personalizirana instanca _crypto oracle_ servera u vidu [Docker](https://www.docker.com/) _container_-a. Za pristup osobnom server, student treba koristiti računalo koje ima pristup lokalnoj mreži u laboratoriju. Ovo je trenutno moguće isključivo ako ste na lokalnu mrežu povezani putem Ethernet kabela.

> Spajanjem na WiFi mrežu, ne možete ostvariti pristup personaliziranom serveru.

Osobnom serveru pristupate putem odgovarajuće IP adrese. S obzirom da se adrese dodjeljuju dinamički, podložne su promjenama. Trenutnu adresu svog servera možete doznati na adresi http://containersinfo.local.

> Sve adrese koje završavaju sa sufiksom `.local` dostupne su isključivo sa lokalne mreže (nisu javne adrese).

### Pohrana rješenja (GitLab)

Nakon uspješnog rješavanja pojedine laboratorijske vježbe, student pohranjuje rješenje u odgovarajući repozitorij na loklanoj instanci GitLab servera na adresi http://gitlab.local. Rješenje uključuje dešifrirani izazov (činjenicu o Chuck Norrisu), dešifriranu zaporku (za otključavanje sljdeće vježbe), te izvorni kod kao izvorno autorsko djelo studenta.

> Student se prijavljuje na lokalni GitLab server (http://gitlab.local) s korisničkim imenom i lozinkom izvedenim iz osobnog imena (npr., studentici Ivani Ivić, dodjeljena su identični _username_ i _password_: `ivic_ivana`). Student nakon inicijalne prijave može promjeniti svoju zaporku.

## Važni linkovi

- [Python `cryptography` package](https://cryptography.io)
- [Crypto Oracle source code](/crypto-oracle)
  
Interni linkovi (dostupni isključivo sa lokalne mreže):

- [What is my _crypto oracle_ container's IP?](http://containersinfo.local)
- [Local GitLab server](http://gitlab.local)