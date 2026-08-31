# Testni podaci i scenariji — Procjena kolaterala

## Pokretanje

- API: `src/Web/pnpm dev:api`, port 5002.
- Web: `src/Web/pnpm dev`, port 8082.
- Bez Keycloaka/SQL Servera koriste se lokalni identitet i InMemory baza sa seed podacima.
- Za test uloga izabrati aktivnu ulogu u headeru; backend ponovo provjerava svaku dozvolu.

## Seed podaci

- Vještaci: Mirza Hodžić, Amra Softić, Procjene d.o.o., Kenan Čović, Lejla Mušanović i Nekretnine Ekspert d.o.o.; pokrivaju različite gradove, FL/PL scope, vrste nekretnina i firme/pojedince.
- Narudžbe: FL i PL nacrti te primjeri kroz ključne statuse; postoje protokol, zadaci, notifikacija i demo dokumenti.
- Šifrarnici, poslovnice/gradovi, role/dozvole i predlošci dokumenata se pune idempotentno.

## Validna FL narudžba

- Klijent: `Hana Mahmutović`; tip FL; JMBG `0605002175028`.
- Kontakt: `Hana Mahmutović`, `+387 61 555 555`, `hana.mahmutovic@raiffeisengroup.ba`.
- Grad Sarajevo; odgovarajuća sarajevska poslovnica i njena adresa.
- Nekretnina: `Zmaja od Bosne 1, Sarajevo`; aktivan tip kolaterala STAN.
- Datum prijema sada; datum slanja isti ili kasniji; nenegativna kvadratura.

## Validna PL narudžba

- `Test Nekretnine d.o.o.`; tip PL; porezni broj `4227890450007`.
- Kontakt `Muamer Hadžić`, `+387 36 555 100`; Mostar i mostarska poslovnica.
- Adresa nekretnine `Bulevar 12, Mostar`; aktivan poslovni kolateral.

## Negativni scenariji

- FL bez/sa neispravnim JMBG-om; PL bez/sa neispravnim poreznim brojem.
- Ime kontakta kraće od 2, broj telefona/e-mail u pogrešnom formatu.
- Poslovnica koja ne pripada gradu; prazna adresa poslovnice ili nekretnine.
- Datum prijema poslije slanja, negativna kvadratura, napomena >500 znakova.
- Neaktivan/nepostojeći kolateral, vještak, šifrarnik ili korisnik.
- Duplikat sistemske role/koda; brisanje korištene vrijednosti; upload pogrešnog tipa/veličine.
- Nedozvoljena tranzicija statusa, akcija pogrešne role, ponovljeno prihvatanje/plaćanje.

## Poslovni tokovi

1. Kreirati FL i PL nacrt, izmijeniti ga, učitati dokumente i submitovati.
2. CA prihvata ili traži korekciju; prodaja dostavlja korekciju; završava pregled.
3. Automatski i ručni izbor vještaka; ponude, prihvatanje ponude i slanje paketa.
4. Vještak prihvata/odbija, traži dodatnu uplatu, šalje procjenu i potpisane dokumente.
5. Mišljenja pravne službe i drugih učesnika; final approval ili povrat na doradu.
6. Faktura: upload, send-for-payment, confirm-paid; svaki korak mijenja status.
7. Dokumenti: upload, download, verzija, deaktivacija/reaktivacija i brisanje gdje je dozvoljeno.
8. Notifikacije: mine, unread-count, mark-read; broj se odmah ažurira.
9. Šifrarnici: definicija + vrijednosti, aktivacija/deaktivacija, usage, preview/confirm import i export.
10. Vještaci: CRUD, odsustvo, blacklist, filteri i kandidati za konkretnu narudžbu.
11. Role/dozvole, korisnici, protokol, audit, izvještaji i health endpointi.

## UI očekivanja

- Sve mutation akcije invalidiraju povezane queryje; nema ručnog Refresh dugmeta.
- Akcija koja više nije dozvoljena nestaje/disabled je nakon promjene statusa.
- API problem se mapira u razumljivu poruku i field errors, bez stack tracea.
- Header, forme, dialog, dropdown i tabele su neprozirni u oba režima.
- Light koristi crni `bankMono`; dark žuti `bankYellowInverse`.

## Automatizovani testovi

- Application: 1.712 prolaznih; Infrastructure: 79; API: 181 — ukupno 1.972 prolazna testa.
- E2E paket sadrži 72 UI scenarija, ali zahtijeva instaliran Playwright Chromium i pokrenute servise; bez browser executablea testovi ne mogu početi.
- Pokretanje bez UI E2E: `dotnet test PropertyValuation/Tests/Application.Tests; dotnet test PropertyValuation/Tests/Infrastructure.Tests; dotnet test PropertyValuation/Tests/Api.Tests`.
- Frontend: `cd src/Web; pnpm test; pnpm build`.
