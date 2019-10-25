# BMJV

*Note:* This a Python wrapper around the data feeds from the Federal Ministry of Justice and Consumer Protection (BMJV) in Germany. It's content is exclusivly in German. Please see [Translations](https://www.gesetze-im-internet.de/Teilliste_translations.html) on the website of the BMJV for further information.

**BMJV** stands for **B**undes**m**inisterium der **J**ustiz und für **V**erbraucherschutz (Federal Ministry of Justice and Consumer Protection).

# Installation

Install it with ```pip install bmjv```

# Usage

## Rechtsprechung im Internet

The latest rulings from the seven federal german courts.

### Examples
#### As module
```
from BMJV import RechtsprechungImInternet
rim = RechtsprechungImInternet('bverfg')
rim.fetch(10)
for item in rim.items:
    print(item.formatted)
```
#### Standalone
```
$ > python -m BMJV --mode rim --court bverfg --limit 2
INFO:BMJV:Found a total of 2 results for bverfg
INFO:__main__:2019-10-01 23:37:25 - BVerfG 2. Senat 3. Kammer, Ablehnung einstweilige Anordnung vom 22.08.2019, 2 BvQ 70/19 - Ablehnung des Erlasses einer eA bei ausstehender fachgerichtlicher Rechtsmittelentscheidung, mithin mangelnder Rechtswegerschöpfung
INFO:__main__:2019-10-02 23:38:07 - BVerfG 1. Senat 2. Kammer, Ablehnung einstweilige Anordnung vom 17.08.2019, 1 BvQ 67/19 - Ablehnung des Erlasses einer eA bzgl der räumlichen Verlegung einer auf dem Gelände der Gedenkstätte Buchenwald geplanten Versammlung gem § 15 Abs 2 VersammlG - Folgenabwägung

```

```RechtsprechungImInternet(id: str)``` allows the follwoing values for *id*:

* *bverfg*: Bundesverfassungsgericht
* *bgh*: Bundesgerichtshof
* *bverwg*: Bundesverwaltungsgericht
* *bfh*: Bundesfinanzhof
* *bag*: Bundesarbeitsgericht
* *bsg*: Bundessoszialgericht
* *bpatg*: Bundespatengericht

```RechtsprechungImInternet.items``` holds a list of *Judicature()* objects. They have the following attributes:
* ```.title``` : The title as string.
* ```.description``` : The description string.
* ```.pubdate``` : The publication as datetime object.
* ```.formatted```: A formatted string like ```{.pubDate} - {.title} - {.description}```

## Gesetze im Internet

The latest laws published by the german government in the Bundesgesetzblatt (BGBl).

### Examples
#### As module

```
from BMJV import BGBl
gim = BGBl()
gim.fetch(10)
for item in rim.items:
    print(item.formatted)
```
#### Standalone
```
$ > python -m BMJV --mode bgbl --limit 4
INFO:__main__:2017-06-09 05:30:02 - BGBl I  2017, 1396 - Gesetz zur Neuordnung der Aufbewahrung von Notariatsunterlagen und zur Einrichtung des Elektronischen Urkundenarchivs bei der Bundesnotarkammer sowie zur Änderung weiterer Gesetze vom 01. Juni 2017
INFO:__main__:2017-07-25 05:30:01 - BGBl I  2017, 2581 - Gesetz zur Reform der Pflegeberufe vom 17. Juli 2017
INFO:__main__:2017-07-25 05:30:01 - BGBl I  2017, 2581 - Gesetz über die Pflegeberufe  vom 17. Juli 2017
INFO:__main__:2018-10-11 05:30:02 - BGBl I  2018, 1572 - Ausbildungs- und Prüfungsverordnung für die Pflegeberufe  vom 02. Oktober 2018
```

```BGBl.items``` holds a list of *Law()* objects. They have the following attributes:
* ```.title``` : The title as string.
* ```.description``` : The description string.
* ```.guid```: A unique ID
* ```.link```: A link to a more detailed description.
* ```.pubdate``` : The publication as datetime object.
* ```.formatted```: A formatted string like ```{.pubDate} - {.title} - {.description}```

# Data sources

* [Gesetze im Internet](https://www.gesetze-im-internet.de/)
* [Rechtsprechung im Internet](https://www.rechtsprechung-im-internet.de/)

# Background

This Python module was initially written for the ZKM-exhibition *Open Codes. Living in Digital Worlds* at the BMJV. Further information can be found on [zkm.de](https://zkm.de/en/exhibition/2019/03/open-codes-living-in-digital-worlds).
