import subprocess
from pathlib import Path


def run_latex_commands(target_file: str, output_dir: str = "."):
    """
    Runs the bash commands to compile a .tex into a .pdf

    Args:
        target_file (str): the .tex file to compile
        output_dir (str): the directory to save the output to
    """

    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Set filenames
    file_tex = f"{target_file}.tex"
    file_pdf = output_path / f"{target_file}.pdf"

    # Run pdflatex to generate PDF in the output folder
    print(f"Running pdflatex on {file_tex}")
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(output_path), file_tex],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"\nSaved PDF: {file_pdf}")
