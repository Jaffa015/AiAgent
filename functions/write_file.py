import os
from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    working_directory = Path(working_directory).resolve()
    file_path = Path(file_path)
    if not file_path.is_absolute():
        file_path = (working_directory / file_path).resolve()

    if not file_path.is_relative_to(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file, will create files if not exists and overwrite the current content of the file. constrained to the working directory and a .py python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
