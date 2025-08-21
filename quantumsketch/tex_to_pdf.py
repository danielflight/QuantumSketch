import subprocess
from pathlib import Path

def run_latex_commands(target_file: str, output_dir: str = ".", just_pdf=True):
    """
    Runs the bash commands to compile a .tex into a .pdf

    Args:
        target_file (str): the .tex file to compile
        output_dir (str): the directory to save the output to
        just_pdf (bool): if True, will only output the original .pdf file
    """
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Set filenames
    file_tex = f"{target_file}.tex"
    file_pdf = output_path / f"{target_file}.pdf"
    file_crop = output_path / f"{target_file}-crop.pdf"
    name_svg = output_path / f"{target_file}.svg"

    # Run pdflatex to generate PDF in the output folder
    print(f"Running pdflatex on {file_tex}")
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(output_path), file_tex],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if not just_pdf:
        # Crop the PDF
        print(f"Cropping {file_pdf} -> {file_crop}")
        subprocess.run(
            ["pdfcrop", str(file_pdf), str(file_crop)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Convert to SVG
        print(f"Converting {file_crop} to SVG")
        subprocess.run(["pdf2svg", str(file_crop), str(name_svg)])

        print(f"Conversion complete. SVG saved as {name_svg}")
