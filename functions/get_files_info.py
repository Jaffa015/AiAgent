import os
from pathlib import Path
from google.genai import types


def get_files_info(working_directory, directory=None):
    path_working_directory = Path(working_directory).resolve()
    path_directory = Path(directory)
    if not path_directory.is_absolute():
        path_directory = (path_working_directory / path_directory).resolve()

    if not path_directory.is_relative_to(path_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not path_directory.is_dir():
        return f'Error: "{directory}" is not a directory'

    dir_objects = os.listdir(path_directory)
    print(f"Listing files of - {working_directory}/{directory}")
    object_strings = []
    try:
        for dir_object in dir_objects:
            object_path = os.path.join(path_directory, dir_object)
            object_size = os.path.getsize(object_path)
            is_dir = os.path.isdir(object_path)
            object_strings.append(
                f"- {dir_object}: file_size={object_size}, is_dir={is_dir}"
            )
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(object_strings)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
