"""
Clean up some odd things that rule parsers do in isolation.

- Take the last record number entity in a label. The record number tends to be at the
  end of a label.
"""

from flora.pylib import trait_util as tu
from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language):
    config = {
        "delete": ["trs", "utm"],
    }
    add.custom_pipe(nlp, "label_post_process", config=config)


@Language.factory("label_post_process")
class PostProcess:
    def __init__(self, nlp: Language, name: str, delete: list[str]):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        rec_num_found = False

        for ent in doc.ents[::-1]:
            if ent.label_ in self.delete:
                tu.clear_tokens(ent)
                continue

            if ent._.trait.trait == "id_number" and ent._.trait.type == "record_number":
                if rec_num_found:
                    tu.clear_tokens(ent)
                    continue
                rec_num_found = True

            entities.append(ent)

        entities.reverse()
        doc.ents = entities
        return doc
