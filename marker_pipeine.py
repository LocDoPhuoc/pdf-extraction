import argparse
import os

from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

configure_logging()


def orc(filename, output, max_pages=100, batch_multiplier=2, langs=None):
    if langs is None:
        langs = ['English']

    model_lst = load_all_models()
    full_text, images, out_meta = convert_single_pdf(filename, model_lst, max_pages=max_pages, langs=langs,
                                                     batch_multiplier=batch_multiplier)

    fname = os.path.basename(filename)
    subfolder_path = save_markdown(output, fname, full_text, images, out_meta)

    print(f"Saved markdown to the {subfolder_path} folder")
