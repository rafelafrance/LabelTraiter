from dataclasses import dataclass
from pathlib import Path

from flora.pylib.writers.html_writer import HtmlWriter as BaseWriter
from flora.pylib.writers.html_writer import HtmlWriterRow as BaseWriterRow
from tqdm import tqdm

from labels.pylib.labels import Labels


@dataclass(kw_only=True)
class HtmlWriterRow(BaseWriterRow):
    label_id: str = ""
    label_image: str = ""
    word_count: int = 0
    valid_words: int = 0
    score: float = 0.0


class HtmlWriter(BaseWriter):
    def __init__(self, html_file, spotlight=""):
        super().__init__(
            template_dir=f"{Path.cwd()}/labels/pylib/writers/templates",
            template="label_html_writer.html",
            html_file=html_file,
            spotlight=spotlight,
        )

    def write(self, labels: Labels, args=None):
        length_cutoff, score_cutoff = 0, 0

        for lb in tqdm(labels.labels, desc="write"):
            if lb.too_short(args.length_cutoff):
                length_cutoff += 1
                continue

            if lb.bad_score(args.score_cutoff):
                score_cutoff += 1
                continue

            self.formatted.append(
                HtmlWriterRow(
                    label_id=lb.path.stem,
                    formatted_text=self.format_text(lb, exclude=["trs"]),
                    formatted_traits=self.format_traits(lb),
                    label_image=lb.encoded_image,
                    word_count=lb.word_count,
                    valid_words=lb.valid_words,
                    score=lb.score,
                ),
            )

        total = len(labels.labels)
        total_removed = length_cutoff + score_cutoff
        summary = {
            "Total labels:": total,
            "Kept:": total - total_removed,
            "Total removed:": total_removed,
            "Too short:": length_cutoff,
            "Score too low:": score_cutoff,
            "Length cutoff:": args.length_cutoff,
            "Score cutoff:": args.score_cutoff,
        }

        self.write_template(args.text_dir, args.image_dir, summary=summary)
