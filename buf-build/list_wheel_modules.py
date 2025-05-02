import zipfile
import sys
import argparse  # For better command-line argument handling


def list_modules_in_wheel(wheel_path):
    """
    Lists all Python modules (.py files) contained within a wheel file.

    Args:
      wheel_path (str): The path to the .whl file.

    Returns:
      list: A list of strings, where each string is the path to a .py file
            within the wheel archive. Returns None if an error occurs.
    """
    modules = []
    try:
        # Check if the file exists and is a file
        # (zipfile might raise different errors depending on the OS for directories)
        import os

        if not os.path.isfile(wheel_path):
            print(
                f"Error: Path '{wheel_path}' does not exist or is not a file.",
                file=sys.stderr,
            )
            return None

        # Open the wheel file (which is essentially a zip archive) in read mode ('r')
        with zipfile.ZipFile(wheel_path, "r") as zf:
            # Get a list of all archive members (files and directories)
            all_files = zf.namelist()

            # Filter the list to include only files ending with '.py'
            modules = [name for name in all_files if name.endswith(".py")]

        return modules

    except zipfile.BadZipFile:
        print(
            f"Error: '{wheel_path}' is not a valid zip file or wheel file.",
            file=sys.stderr,
        )
        return None
    except FileNotFoundError:
        # This might be redundant due to the os.path.isfile check, but good practice
        print(f"Error: File not found at '{wheel_path}'", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None


# --- Example Usage (when running the script directly) ---
if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="List Python modules (.py files) found inside a wheel (.whl) file."
    )
    parser.add_argument("wheel_file", help="The path to the .whl file to inspect.")
    args = parser.parse_args()

    # Get the list of modules
    module_list = list_modules_in_wheel(args.wheel_file)

    # Print the results
    if module_list is not None:  # Check if the function execution was successful
        if module_list:
            print(f"Found {len(module_list)} module(s) in '{args.wheel_file}':")
            for module_path in module_list:
                print(f"- {module_path}")
        else:
            print(f"No .py modules found in '{args.wheel_file}'.")
        sys.exit(0)  # Exit with success code
    else:
        sys.exit(1)  # Exit with error code
