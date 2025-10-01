"""
compile.py - Compiling LaTeX files into a PDF
"""

import subprocess
import argparse # For parsing command-line options
from pathlib import Path # For file path operations
from colorama import init, Fore # For colored terminal output

# Initialize colorama and enable reset styles after each point
init(autoreset=True)

print(f"{Fore.BLUE}➡️  Starting: Compiling LaTeX files into a PDF")

def compile_latex(input_tex: Path, output_pdf: Path, timeout: int = 60) -> None:
    """
    Compiles a LaTeX file into a PDF using pdflatex.

    Args:
        input_tex (Path): The path to the input LaTeX (.tex) file.
        output_pdf (Path): The path to the output PDF file.
        timeout (int): The timeout in seconds for the LaTeX compilation process.
    """
    try:
        input_tex = Path(input_tex)
        output_pdf = Path(output_pdf)
        output_dir = output_pdf.parent
        output_without_suffix = output_pdf.stem # Output filename without .pdf suffix

        print(f"Compiling '{input_tex}' to '{output_pdf}'...")

        # Ensure the output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Run the pdflatex command in the directory of the input .tex file
        compile_cmd = [
            "pdflatex",
            "-interaction=nonstopmode", # do not stop for user input on errors
            "-halt-on-error", # exit with an error code when an error is encountered
            "-file-line-error", # print error messages in the form file:line:error
            "-output-directory",
            str(output_dir),
            f"-jobname={output_without_suffix}",  # force output filename
            str(input_tex),
        ]
        result = subprocess.run(
            compile_cmd,
            check=True, # will raise CalledProcessError if return code is non-zero
            capture_output=True, # log it if needed
            text=True, # get string output instead of bytes
            timeout=timeout, # prevent hanging
        )

        # Let's log the output for debugging purposes
        if result.returncode == 0:
            # Run pdflatex a second time to resolve references (e.g., LastPage)
            subprocess.run(compile_cmd, check=False, capture_output=True, text=True, timeout=timeout)
            print(f"{Fore.GREEN}✅ Compilation successful: PDF generated at {output_pdf}")
        else:
            # Shouldn't reach here because check=True raises on non-zero, but keep for completeness
            print(f"{Fore.RED}❌ Error: Compilation failed.")
            print(result.stdout)
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        # Print captured output from the failed run for debugging
        if hasattr(e, 'stdout'):
            print(e.stdout)
        if hasattr(e, 'stderr'):
            print(e.stderr)
        print(f"{Fore.RED}❌ Error: Compilation failed: {e}")
    except subprocess.TimeoutExpired as e:
        print(f"{Fore.RED}❌ Error: Compilation process timed out.")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX file into a PDF.")
    parser.add_argument("--input", required=True, type=Path, help="Path to the input LaTeX (.tex) file")
    parser.add_argument("--output", required=True, type=Path, help="Path to the output PDF file")

    args = parser.parse_args()

    input_tex = args.input
    output_pdf = args.output

    if input_tex is None or not input_tex.exists():
        print(f"{Fore.RED}❌ Error: Input file not found: '{input_tex}'")
        return

    if output_pdf is None or output_pdf.suffix.lower() != '.pdf':
        print(f"{Fore.RED}❌ Error: Output file '{output_pdf}' must have a .pdf extension")
        return

    compile_latex(input_tex, output_pdf)

if __name__ == "__main__":
    main()
