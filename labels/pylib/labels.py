from pathlib import Path

from flora.pylib.rules import terms as f_terms
from spell_well.pylib.spell_well import SpellWell
from tqdm import tqdm
from traiter.pylib import term_util

from labels.pylib import pipeline
from labels.pylib.label import Label


class Labels:
    def __init__(self, args):
        self.labels: list[Label] = self.get_labels(args)
        self.nlp = pipeline.build()
        self.image_paths = self.get_image_paths(args)
        self.vocabulary: set = self.get_vocabulary()
        self.encoding = args.encoding

    @staticmethod
    def get_labels(args):
        labels = [Label(p) for p in sorted(args.text_dir.glob("*.txt"))]

        if args.limit:
            labels = labels[args.offset : args.limit + args.offset]

        return labels

    @staticmethod
    def get_image_paths(args):
        images = {}
        if args.image_dir:
            images = {p.stem: p for p in args.image_dir.glob("*")}
        return images

    @staticmethod
    def get_vocabulary():
        """Get words for scoring label content."""
        spell_well = SpellWell()
        vocabulary = {w.lower() for w in spell_well.vocab_to_set()}

        path = Path(f_terms.__file__).parent / "binomial_terms.zip"
        for term in term_util.read_terms(path):
            vocabulary |= set(term["pattern"].lower().split())

        path = Path(f_terms.__file__).parent / "monomial_terms.zip"
        vocabulary |= {t["pattern"] for t in term_util.read_terms(path)}

        return vocabulary

    def parse(self):
        for lb in tqdm(self.labels, desc="parse"):
            lb.parse(
                self.nlp, self.image_paths, self.vocabulary, encoding=self.encoding
            )
