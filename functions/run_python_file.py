import os
import subprocess
from pathlib import Path
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_directory = Path(working_directory).resolve()
    abs_file_path = Path(file_path)
    if not abs_file_path.is_absolute():
        abs_file_path = (working_directory / abs_file_path).resolve()

    if not abs_file_path.is_relative_to(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.suffix == ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python3", abs_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            cwd=working_directory,
            timeout=30,
        )
        strings = []
        if result.stdout:
            strings.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            strings.append(f"STDERR: {result.stderr}")
        if result.returncode > 0:
            strings.append(f"Process exited with code {result.returncode}")
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if len(strings) == 0:
        return "No output produced."
    return "\n".join(strings)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to execute, relative to the working directory. Has to be provided",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
