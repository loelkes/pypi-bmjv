# BMJV

*Note:* This a pathon wrapper around the data feeds from the Federal Ministry of Justice and Consumer Protection in Germany. It's content is exclusivly in German. Please see [Translations](https://www.gesetze-im-internet.de/Teilliste_translations.html) on the website of the ministry for further information.

**BMJV** stands for **B**undes**m**inisterium der **J**ustiz und für **V**erbraucherschutz (Federal Ministry of Justice and Consumer Protection).

# Installation

1. Install it with ```pip install bmjv```

## Usage

1. ```from BMJV import BGBl, RechtsprechungImInternet```

### Rechtsprechung im Internet

The latest rulings from the seven major german courts.

```foobar = RechtsprechungImInternet( id )```

```id``` can be used to select a special court. It is optional and set to *bverfg* by default.

* *bverfg*: Bundesverfassungsgericht
* *bgh*: Bundesgerichtshof
* *bverwg*: Bundesverwaltungsgericht
* *bfh*: Bundesfinanzhof
* *bag*: Bundesarbeitsgericht
* *bsg*: Bundessoszialgericht
* *bpatg*: Bundespatengericht

All results are stored in a list at ```foobar.items```. Each item is a *Judicature* with the following attributes:
* ```.title``` : The title as string.
* ```.description``` : The description string.
* ```.pubdate``` : The publication as datetime object.

### Gesetze im Internet

The latest laws published by the german government in the Bundesgesetzblatt (BGBl).

```foobar = BGBl()```

All results are stored in a list at ```foobar.items```. Each item is a *Law* with the following attributes:
* ```.title``` : The title as string.
* ```.description``` : The description string.
* ```.pubdate``` : The publication as datetime object.

## Data sources

* [Gesetze im Internet](https://www.gesetze-im-internet.de/)
* [Rechtsprechung im Internet](https://www.rechtsprechung-im-internet.de/)
