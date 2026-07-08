# IA generated shit just to zip the files for manual deploy

import shutil
import os
import argparse
import tempfile

# Default list of files and directories to exclude
DEFAULT_EXCLUDE = [
    "trash",
    "venv",
    ".git",
    ".gitignore",
    "node_modules",
    "__pycache__",
    "*.pyc",
    ".env",
    "env",
    "dist",
    "build",
    ".vscode",
    ".idea",
    ".DS_Store",
]


def create_zip_with_exclusions(output_name, source_dir, exclude_list):
    """Create a zip file with exclusions"""
    try:
        # Get list of files to include
        files_to_zip = []

        for root, dirs, files in os.walk(source_dir):
            # Skip excluded directories
            dir_name = os.path.basename(root)
            if dir_name in exclude_list:
                dirs.clear()
                continue

            for file in files:
                file_path = os.path.join(root, file)
                # Skip the script itself
                if root == source_dir and file == os.path.basename(__file__):
                    continue

                # Skip files with excluded extensions
                should_exclude = False
                for pattern in exclude_list:
                    if pattern.startswith("*."):
                        if file.endswith(pattern[1:]):
                            should_exclude = True
                            break
                if not should_exclude:
                    files_to_zip.append(file_path)

        if not files_to_zip:
            print("No files to zip!")
            return False

        # Create zip using shutil.make_archive with temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            for file_path in files_to_zip:
                rel_path = os.path.relpath(file_path, source_dir)
                dest_path = os.path.join(temp_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)

            shutil.make_archive(output_name, "zip", temp_dir)

        print(f"✅ Created: {output_name}.zip")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Zip directory with exclusions")
    parser.add_argument("-o", "--output", help="Output filename (without .zip)")
    parser.add_argument("-d", "--directory", default=".", help="Directory to zip")
    parser.add_argument(
        "-e", "--exclude", nargs="+", help="Additional items to exclude"
    )
    args = parser.parse_args()

    # Build exclude list
    exclude_list = DEFAULT_EXCLUDE.copy()
    if args.exclude:
        exclude_list.extend(args.exclude)

    # Determine output name
    output_name = args.output or os.path.basename(os.path.abspath(args.directory))

    print(f"Zipping: {args.directory}")
    print(f"Excluding: {', '.join(exclude_list)}")

    create_zip_with_exclusions(output_name, args.directory, exclude_list)


if __name__ == "__main__":
    main()
