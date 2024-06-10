#!/usr/bin/env python3
import argparse
import json
import textwrap
from pathlib import Path

from traiter.pylib.darwin_core import DarwinCore
from util.pylib import log

from labels.pylib.labels import Labels
from labels.pylib.writers.label_html_writer import HtmlWriter


def main():
    log.started()
    args = parse_args()

    labels: Labels = Labels(args)
    labels.parse()

    if args.html_file:
        writer = HtmlWriter(args.html_file, args.spotlight)
        writer.write(labels, args)

    if args.traiter_dir:
        args.traiter_dir.mkdir(parents=True, exist_ok=True)
        write_separate_files(
            labels, args.length_cutoff, args.score_cutoff, args.traiter_dir
        )

    if args.json_output:
        write_single_file(
            labels, args.length_cutoff, args.score_cutoff, args.json_output
        )

    log.finished()


def write_single_file(labels, length_cutoff, score_cutoff, json_output):
    records = []

    for lb in labels.labels:
        if lb.too_short(length_cutoff) or lb.bad_score(score_cutoff):
            continue

        rec = {
            "image": lb.path.stem,
            "word_count": lb.word_count,
            "valid_words": lb.valid_words,
            "score": lb.score,
        }

        dwc = DarwinCore()
        _ = [t.to_dwc(dwc) for t in lb.traits]
        rec |= dwc.to_dict()

        records.append(rec)

    with json_output.open("w") as f:
        json.dump(records, f, indent=2)


def write_separate_files(labels, length_cutoff, score_cutoff, traiter_dir):
    for lb in labels.labels:
        if lb.too_short(length_cutoff) or lb.bad_score(score_cutoff):
            continue

        dwc = DarwinCore()
        _ = [t.to_dwc(dwc) for t in lb.traits]

        path = traiter_dir / f"{lb.path.stem}.json"
        with path.open("w") as f:
            json.dump(dwc.to_dict(), f, indent=4)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from label text extracted
            from herbarium sheets.

            Images of the input label are not required but when you
            use them the text and label image file stems must match.

            A file stem is a file name without the directories and
            without the file suffix. For example:
                /my_dir/sub_dir/my_label_file.txt -> my_label_file
            """,
        ),
    )

    arg_parser.add_argument(
        "--text-dir",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Directory containing the input text files.""",
    )

    arg_parser.add_argument(
        "--json-output",
        metavar="PATH",
        type=Path,
        help="""Output a JSON file holding traits.""",
    )

    arg_parser.add_argument(
        "--traiter-dir",
        metavar="PATH",
        type=Path,
        help="""Output JSON files holding traits, one for each input text file, in this
            directory.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output HTML formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--image-dir",
        metavar="PATH",
        type=Path,
        help="""Directory containing the images of labels or treatments.
            These images are for HTML output.""",
    )

    arg_parser.add_argument(
        "--score-cutoff",
        type=float,
        default=0.7,
        metavar="FRACTION",
        help="""Only keep labels if their score is this or more.
            The score is between 0.0 and 1.0. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--length-cutoff",
        type=int,
        default=10,
        metavar="LENGTH",
        help="""Only keep labels if they have at least this many words.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Read this many labels for input.""",
    )

    arg_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="""Offset for splitting data.""",
    )

    arg_parser.add_argument(
        "--spotlight",
        metavar="TRAIT",
        help="""This trait will get its own color for HTML output.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
