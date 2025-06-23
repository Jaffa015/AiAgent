import os
from pathlib import Path
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    working_directory = Path(working_directory).resolve()
    file_path = Path(file_path)
    if not file_path.is_absolute():
        file_path = (working_directory / file_path).resolve()

    if not file_path.is_relative_to(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string += (
                f'[...File "{file_path}" truncated at 10000 characters]'
            )
    except Exception as e:
        return f"Error: {e}"

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Lists the contents of a file truncated after {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory. Has to be provided",
            ),
        },
        required=["file_path"],
    ),
)
