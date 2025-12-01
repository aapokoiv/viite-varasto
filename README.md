## Viite Varasto

[![CI](https://github.com/aapokoiv/viite-varasto/actions/workflows/ci.yaml/badge.svg)](https://github.com/aapokoiv/viite-varasto/actions/workflows/ci.yaml)

[![codecov](https://codecov.io/gh/aapokoiv/viite-varasto/graph/badge.svg?token=SWCL3S26WF)](https://codecov.io/gh/aapokoiv/viite-varasto)

Backlogi: [täällä](https://helsinkifi-my.sharepoint.com/:x:/g/personal/aapokoiv_ad_helsinki_fi/IQDEuVCXAv8rSYSaMAgaQt6zAbibmJOpDFhpTtWDTGlsCXM?e=8AC0gf)

**Definition of done** 
- Ominaisuus on valmis, kun se on suunniteltu, toteutettu, testattu, dokumentoitu ja puskettu main haaralle siten, että se toteuttaa user storyn hyväksymiskriteerit

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

**Testaaminen**

- Aja testit läpi seuraavilla komennoilla:

  ```bash
  pytest
  robot --variable HEADLESS:true src/story_tests
  pylint --rcfile=src/.pylintrc src
  ```

**Tietokannan alustaminen**

- Aja `db_helper.py` projektin juuressa `setup` argumentilla:

```bash
python3 src/db_helper.py setup
```

**Käyttö**

- Mene virtuaaliympäristöön:

```bash
eval $(poetry env activate)
```

- Käynnistä sovellus:

```bash
python3 src/index.py
```

- Avaa `http://localhost:5001` selaimella.

