## Ohtu miniprojekti boilerplate

Lue [täältä](https://ohjelmistotuotanto-hy.github.io/flask/) lisää.

Muutamia vihjeitä projektin alkuun [täällä](https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/blob/main/misc/ohjeita.md).


Backlogi: [täällä](https://helsinkifi-my.sharepoint.com/:x:/g/personal/aapokoiv_ad_helsinki_fi/IQDEuVCXAv8rSYSaMAgaQt6zAbibmJOpDFhpTtWDTGlsCXM?e=8AC0gf)

**Definition of done** 
- Ominaisuus on valmis, kun se on suunniteltu, toteutettu, testattu ja dokumentoitu siten, että se toteuttaa kaikki osan vaatimukset

**Asennus**

- **Esivaatimukset:** Python 3.12 ja `poetry`.

```bash
poetry install
```

**Ympäristömuuttujat**

- Luo .env tiedosto ja aseta tietokantayhteys ja `SECRET_KEY`:

```bash
DATABASE_URL=postgresql://xxx
TEST_ENV=true
SECRET_KEY=satunnainen_merkkijono
```

**Tietokannan alustaminen**

- Aja `db_helper.py` projektin juuressa:

```bash
python3 src/db_helper.py
```

**Käyttö**

- Mene virtuaaliympäristöön:

```bash
eval $(poetry env activate)
```

- Käynnistä sovellus:

```bash
flask run
```

- Avaa `http://127.0.0.1:5001` selaimella.

