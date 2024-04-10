# LabelTraiter ![Python application](https://github.com/rafelafrance/FloraTraiter/workflows/CI/badge.svg)

Extract traits about plants from labels on herbarium sheets.

I should also mention that this repository builds upon other repositories:
- `common_utils`: This is just a grab bag of simple utilities I used in several other project. I got tired of having to change every repository that used them each time there was an edit, so I just put them here.
  - `https://github.com/rafelafrance/common_utils`
- `spell-well`: Is a super simple "delete-only" spell checker I wrote. There may be better options now, but it survives until I can find one that handles our particular needs.
  - `https://github.com/rafelafrance/spell-well`
- `traiter`: This is the base code for all the rule-based parsers (aka traiters) that I write. The details change but the underlying process is the same for all.
  - `https://github.com/rafelafrance/traiter`
- `FloraTraiter`: This repository branched off from FloraTraiter and uses many of the same traits/fields as it does.
  - `https://github.com/rafelafrance/FloraTraiter`

## All righty, what's this all about then?

The task is take text like this:

```
Herbarium of
San Diego State College
Erysimum capitatum (Dougl.) Greene.
Growing on bank beside Calif. Riding and
Hiking Trail north of Descanso.
13 May 1967 San Diego Co., Calif.
Coll: R.M. Beauchamp No. 484
```

And convert it into a machine-readable Darwin Core format like:

```json
{
    "dwc:country": "United States",
    "dwc:county": "San Diego",
    "dwc:eventDate": "1967-05-13",
    "dwc:recordNumber": "484",
    "dwc:recordedBy": "R.M. Beauchamp",
    "dwc:scientificName": "Erysimum capitatum (Dougl.) Greene",
    "dwc:scientificNameAuthorship": "Dougl Greene",
    "dwc:stateProvince": "California",
    "dwc:taxonRank": "species",
    "dwc:verbatimEventDate": "13 May 1967",
    "dwc:verbatimLocality": "Bank beside California, Riding and Hiking Trail north of Descanso"
}
```

Of course, the OCRed input text and the resulting JSON are not always this clean.

### Strategy

LabelTraiter uses a multistep approach to parse text into traits. The rules themselves are written using spaCy, with enhancements we developed to streamline the rule building process. The general outline of the rule building process follows:

1. Have experts identify relevant terms and target traits.
2. We use expert identified terms to label terms using spaCy's phrase matchers. These are sometimes traits themselves, but are more often used as anchors for more complex patterns of traits.
3. We then build up more complex terms from simpler terms using spaCy's rule-based matchers repeatedly until there is a recognizable trait. See the image below.
4. Depending on the trait we may then link traits to each other (entity relationships) using also spaCy rules.
   1. Typically, a trait gets linked to a higher level entity like SPECIES <--- FLOWER <--- {COLOR, SIZE, etc.}.

As an example of parsing a locality is shown below:

![<img src="assets/locality_parsing.jpg" width="700" />](assets/locality_parsing.jpg)

The rules can become complex and the vocabularies for things like taxa, or a gazetteer can be huge, but the image above should get the idea of what is involved in label parsing.

LabelTraiter was originally developed to parse plant treatments and was later adapted to parse label text. As such, it does have some issues with parsing label text. When dealing with treatments the identification of traits/terms is fairly easy and the linking of traits to their proper plant part is only slightly more difficult.

With labels, both the recognition of terms and linking them is difficult. There is often an elision of terms, museums or collectors may have their own abbreviations, and there is an inconsistent formatting of labels. Rule based-parsers are best at terms like dates, elevations, and latitudes/longitudes where the terms have recognizable structures, like numbers followed by units with a possible leading label. They are weakest is with vague terms like habitat, locality, or even names that require some sort of analysis of the context and meaning of the words.

## Install

You will need to have Python3.11+ installed, as well as pip, a package manager for Python.
If you have `make` you can install the requirements into your python environment like so:

```bash
git clone https://github.com/rafelafrance/LabelTraiter.git
cd LabelTraiter
make install
```

Every time you run any script in this repository, you'll have to activate the virtual environment once at the start of your session.

```bash
cd LabelTraiter
source .venv/bin/activate
```

```bash
parse-labels <arguments to parse your labels>
```

## Tests

There are tests which you can run like so:

```bash
make test
```
