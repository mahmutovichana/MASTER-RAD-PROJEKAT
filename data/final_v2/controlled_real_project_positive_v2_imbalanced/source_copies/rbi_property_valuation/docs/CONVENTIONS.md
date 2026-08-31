# Konvencije

- Svi .NET projekti i namespaceovi počinju sa `RBBH.CollateralAppraisal`.
- Zavisnosti idu prema unutra: Api/Infrastructure → Application → Domain.
- React ne pristupa bazi; koristi OpenAPI tipove i zajednički HTTP klijent.
- SQL Server je jedini trajni provider; InMemory je samo Development/Testing fallback.
- Tajne su u deployment ili lokalnom secret storeu.
- Produkcija uvijek zahtijeva validan Keycloak i bazu.
