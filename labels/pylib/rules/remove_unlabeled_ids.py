"""Remove unlabeled ID number traits if there is one that is labeled."""
from collections import defaultdict

from flora.pylib import trait_util as tu
from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

LABEL = "id_number"


def pipe(nlp: Language):
    add.custom_pipe(nlp, "remove_unlabeled_ids")


@Language.factory("remove_unlabeled_ids")
class RemoveUnlabeledIds:
    def __init__(
        self,
        nlp: Language,
        name: str,
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        one_is_labeled = defaultdict(bool)

        for ent in doc.ents:
            if ent.label_ == LABEL:
                one_is_labeled[ent.label_] |= bool(ent._.trait.has_label)

        for ent in doc.ents:
            if (
                ent.label_ == LABEL
                and one_is_labeled[ent.label_]
                and not ent._.trait.has_label
            ):
                tu.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
