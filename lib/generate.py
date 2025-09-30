"""
generate.py - Generate a LaTeX resume from a YAML file and a Jinja2 template
"""

import argparse # For parsing command-line options
import re
import logging # For logging error and info
import os
import sys
import yaml
from pathlib import Path # For file path operations
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from colorama import init, Fore # For colored terminal output

# Initialize colorama and enable reset styles after each point
init(autoreset=True)

print(f"{Fore.BLUE}➡️  Starting: Generating LaTeX resume from Jinja template and YAML data")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def load_resume(yaml_path: Path) -> dict:
    """
    Load the resume data from a YAML file.
    Args:
        yaml_path (Path): The path to the YAML file.
    Returns:
        dict: The loaded YAML resume data.
    """
    try:
        with yaml_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load YAML file {yaml_path}: {e}")
        raise

def latex_escape(text: str) -> str:
    """
    Escapes characters for LaTeX.
    Args:
        text (str): The input text to be escaped.
    Returns:
        str: The escaped text.
    """
    latex_special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
        '|': r'\textbar{}',
        '\'': r'\textquotesingle{}',
    }
    return ''.join(latex_special_chars.get(char, char) for char in text)

def markdown_to_latex(text):
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    return link_pattern.sub(r'\\href{\2}{\1}', text).replace('%', '\\%')

def format_date(date_str: str) -> str:
    """
    Formats a date string to 'Month Year'. If the format is unknown, returns the original string.
    Args:
        date_str (str): The input date string.
    Returns:
        str: The formatted date string.
    """
    formats = ['%d-%m-%Y', '%m-%Y', '%Y-%m-%d', '%Y-%m']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime('%b %Y')
        except ValueError:
            continue
    return date_str


def render_template(template_path: Path, resume_data: dict) -> str:
    """
    Render the LaTeX resume template with the provided resume data.

    Args:
        template_path (Path): Path to the Jinja2 template file.
        resume_data (dict): Resume data loaded from YAML.

    Returns:
        str: Rendered LaTeX resume.
    """
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=False,  # Disable HTML escaping for LaTeX
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='<<',
        variable_end_string='>>',
        # Change comment delimiters so LaTeX sequences like '{#1}' are not
        # interpreted as Jinja comments. Use C-style comments for Jinja.
        comment_start_string='/*',
        comment_end_string='*/',
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Register custom filters
    env.filters['latex_escape'] = latex_escape
    env.filters['format_date'] = format_date
    env.filters['markdown_to_latex'] = markdown_to_latex

    template = env.get_template(template_path.name)

    # PDF compilation timestamp in LaTeX-friendly format
    pdf_timestamp = datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")

    # Dynamically unpack all top-level keys from resume_data
    # Pass the whole resume data as `resume` so the template can access
    # keys that are not valid Python identifiers (e.g. 'personal-statement')
    return template.render(resume=resume_data, compilation_timestamp=pdf_timestamp, **{k:v for k,v in resume_data.items() if k.isidentifier()})

def main():
    parser = argparse.ArgumentParser(
        description="Generate a LaTeX resume from a YAML file and a Jinja2 template."
    )
    parser.add_argument(
        "--resume",
        type=Path,
        help="Path to the YAML resume file (default: resume.yml)"
    )
    parser.add_argument(
        "--template",
        type=Path,
        help="Path to the Jinja2 template file (default: template.jinja)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to the output LaTeX file (default: resume.tex)"
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.resume.is_file():
        print(f"{Fore.RED}❌ Error: Resume file not found: {args.resume}")
        sys.exit(1)
    
    if not args.template.is_file():
        print(f"{Fore.RED}❌ Error: Template Jinja file not found: {args.template}")
        sys.exit(1)

    try:
        resume_data = load_resume(args.resume)
    except Exception as e:
        print(f"{Fore.RED}❌ Error loading resume YAML: {e}")
        sys.exit(1)

    try:
        rendered = render_template(args.template, resume_data)
    except Exception as e:
        import traceback
        print(f"{Fore.RED}❌ Error rendering template: {e}")
        traceback.print_exc()
        sys.exit(1)
        sys.exit(1)

    try:
        with args.output.open("w", encoding="utf-8") as file:
            file.write(rendered)
        print(f"{Fore.GREEN}✅ Success: Resume generated at {args.output}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error writing to output file {args.output}: {e}")

if __name__ == "__main__":
    main()
