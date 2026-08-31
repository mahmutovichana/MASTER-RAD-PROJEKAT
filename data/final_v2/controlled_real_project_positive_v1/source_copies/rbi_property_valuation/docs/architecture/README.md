# Arhitektura

Tok je `Browser → React (Web) → HTTPS/OpenAPI → Api → Application → Domain`, dok `Infrastructure` implementira bazu, dokumente, audit i vanjske integracije. Domain ne zavisi od tehničkih slojeva; Application definira use-caseove; Api je tanak HTTP ulaz. SQL Server je trajna baza, a Keycloak identitetski sistem. Development ima seedovani InMemory i lokalni auth fallback.

Backend OCP artefakt je kontejnerska slika. Frontend IIS artefakt je skup statičkih fajlova.
