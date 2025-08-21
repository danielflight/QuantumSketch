import os
from pathlib import Path

from quantumsketch.tex_to_pdf import run_latex_commands


def sketch_circuit(circuit_history: list[map], num_qubits: int, rundir = None, just_pdf = True):
    """
    Draws the circuit based on its history, assuming it starts from vacuum states.
    
    Args:
        circuit_history (list): List of various gates (in reverse order of application) in the format
                        [..., {"gate": "S", "targets": [0, 1]}, ...]
        num_qubits (int); total number of qubits in the circuit
        rundir (str): the working directory to save the output files to
        just_pdf (bool): if True, will only output the original .pdf file

    """

    # location to save the output directory
    rundir = rundir if rundir else os.getcwd()

    # Create a directory
    Path(f"{rundir}/quantumsketch").mkdir(parents=True, exist_ok=True)
    savepath = f"{rundir}/quantumsketch"

    # Each line starts with a qubit wire
    lines = ["\\lstick{\ket{0}} & " for i in range(num_qubits)]

    for gate in circuit_history:
        g = gate["gate"]

        # ----- single qubit gates -----
        if "controls" not in gate and len(gate["targets"]) == 1:
            t = gate["targets"][0]
            if g == "M":
                lines[t] += "\\meter & "
            else:
                lines[t] += f"\\gate{{{g}}} & "
            for i in range(num_qubits):
                if i != t: lines[i] += "\\qw & "

        # ----- controlled gates -----
        elif "controls" in gate:
            ctrls = gate["controls"]
            tgts = gate["targets"]
            for i in range(num_qubits):
                if i in ctrls:
                    lines[i] += "\\ctrl{" + str(tgts[0]-i) + "} & "
                elif i in tgts:
                    lines[i] += "\\targ & " if g in ["CX","CNOT"] else f"\\gate{{{g}}} & "
                else:
                    lines[i] += "\\qw & "

        # ----- multi-qubit block gates -----                       
        elif len(gate["targets"]) > 1:
            tgts = sorted(gate["targets"])
            span = tgts[-1] - tgts[0]
            top = tgts[0]

            # Top wire
            lines[top] += f"\\multigate{{{span}}}{{{g}}} & "

            # All wires inside the span (not just explicit targets)
            for k in range(top+1, top+span+1):
                lines[k] += f"\\ghost{{{g}}} & "

            # All other wires outside the span
            for i in range(num_qubits):
                if not (top <= i <= top+span):
                    lines[i] += "\\qw & "

    for i in range(num_qubits):
        lines[i] += "\\qw & "

    # full qcircuit code
    circuit_code = "\\Qcircuit @C=1em @R=0.7em {\n" + "\n".join(
        line[:-2] + " \\\\" for line in lines
    ) + "\n}"

    # now compile the rest of the LaTeX document
    with open(f"{savepath}/circuit.tex", "w") as f:
            f.write(
            """
            \\documentclass{amsart}
            \\usepackage[matrix,frame,arrow]{xypic}
            \\usepackage[braket]{qcircuit}

            \\vfuzz2pt
            """
    )
            f.write("\n\n\\begin{document}\n\n\[\n")
            f.write(circuit_code)
            f.write(
            f"""
            \]

            \end{{document}}
            """
    )

    # this compiles the .tex into a .pdf
    run_latex_commands(target_file=f"{savepath}/circuit", output_dir=savepath, just_pdf=just_pdf)

