#!/usr/bin/env python3
"""Enhanced script to generate Python Connect RPC clients from .proto definitions.

This script:
1. Downloads the latest proto files from OpenTDF platform
2. Generates standard Python protobuf files
3. Generates Connect RPC Python clients (preferred)
4. Optionally generates legacy gRPC clients for backward compatibility
"""

import subprocess
import sys
from pathlib import Path


def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    dependencies = [
        ("buf", "buf --version"),
        ("connect-python", "uv run python -c 'import connectrpc'"),
    ]

    missing = []
    for name, check_cmd in dependencies:
        try:
            subprocess.run(check_cmd, shell=True, capture_output=True, check=True)
            print(f"✓ {name} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):  # noqa: PERF203
            missing.append(name)
            print(f"✗ {name} is missing")

    if missing:
        print("\nMissing dependencies. Install them with:")
        for dep in missing:
            if dep == "buf":
                print("  # Install buf: https://buf.build/docs/installation")
                print("  # macOS: brew install bufbuild/buf/buf")
                print("  # Or: go install github.com/bufbuild/buf/cmd/buf@latest")
            elif dep == "connect-python":
                print("  uv add connect-python[compiler]")
        return False

    return True


def copy_opentdf_proto_files(proto_gen_dir: Path) -> bool:
    """Clone OpenTDF platform repository and copy all proto files."""
    GIT_TAG = "service/v0.7.2"
    REPO_URL = "https://github.com/opentdf/platform.git"

    temp_repo_dir = proto_gen_dir / "temp_platform_repo"
    proto_files_dir = proto_gen_dir / "proto-files"
    proto_files_dir.mkdir(exist_ok=True)

    copied_files = 0

    try:
        # Remove existing temp directory if it exists
        if temp_repo_dir.exists():
            subprocess.run(["rm", "-rf", str(temp_repo_dir)], check=True)

        print(f"Cloning OpenTDF platform repository (tag: {GIT_TAG})...")

        # Shallow clone the specific tag
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                GIT_TAG,
                REPO_URL,
                str(temp_repo_dir),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Find all .proto files in the service directory and copy them immediately
        service_dir = temp_repo_dir / "service"
        if service_dir.exists():
            for proto_file in service_dir.glob("**/*.proto"):
                try:
                    # Get the relative path from the service directory
                    relative_path = proto_file.relative_to(service_dir)

                    # Create the destination path
                    dest_path = proto_files_dir / relative_path

                    # Create any necessary parent directories
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    print(f"  Copying {relative_path}...")

                    # Copy the file content
                    with proto_file.open() as src:
                        content = src.read()

                    with dest_path.open("w") as dst:
                        dst.write(content)

                    copied_files += 1

                except Exception as e:  # noqa: PERF203
                    print(f"  Warning: Failed to copy {relative_path}: {e}")

        print(f"Found and copied {copied_files} proto files from repository")
        return copied_files > 0

    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error copying proto files: {e}")
        return False
    finally:
        # Clean up temp directory
        if temp_repo_dir.exists():
            subprocess.run(["rm", "-rf", str(temp_repo_dir)], check=False)

    return False


def download_proto_files(proto_gen_dir: Path) -> bool:
    """Download proto files from OpenTDF platform."""
    print("Copying proto files from OpenTDF platform...")

    try:
        return copy_opentdf_proto_files(proto_gen_dir)
    except Exception as e:
        print(f"Error getting proto files: {e}")
        return False


def run_buf_generate(proto_gen_dir: Path) -> bool:
    """Run buf generate to create protobuf and Connect RPC files."""
    print("Generating protobuf and Connect RPC files...")

    try:
        # First, get the path to protoc-gen-connect_python
        result = subprocess.run(
            ["uv", "run", "which", "protoc-gen-connect_python"],
            cwd=proto_gen_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        connect_plugin_path = result.stdout.strip()
        print(f"Using Connect plugin at: {connect_plugin_path}")

        # Update buf.gen.yaml with the correct path
        buf_gen_path = proto_gen_dir / "buf.gen.yaml"
        with buf_gen_path.open() as f:
            content = f.read()

        # Replace the local plugin path
        updated_content = content.replace(
            "- local: protoc-gen-connect_python", f"- local: {connect_plugin_path}"
        )

        with buf_gen_path.open("w") as f:
            f.write(updated_content)

        # Run buf generate
        subprocess.run(
            ["buf", "generate"],
            cwd=proto_gen_dir,
            capture_output=True,
            text=True,
            check=True,
        )

        print("✓ Successfully generated protobuf and Connect RPC files")
        return True

    except subprocess.CalledProcessError as e:
        print("✗ buf generate failed:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ buf command not found. Please install buf.")
        return False


def create_init_files(generated_dir: Path) -> None:
    """Create __init__.py files in generated directories."""
    # Create __init__.py in main generated directory
    (generated_dir / "__init__.py").touch()

    # Create __init__.py files in any subdirectories
    for subdir in generated_dir.iterdir():
        if subdir.is_dir():
            (subdir / "__init__.py").touch()


def _fix_ignore_if_default_value(proto_files_dir):
    """TODO: Fix buf validation: Updated the proto files to use the correct enum value:

    Changed IGNORE_IF_DEFAULT_VALUE → IGNORE_IF_ZERO_VALUE in:
        attributes.proto
        key_access_server_registry.proto
        namespaces.proto

    See release notes:
        * https://github.com/bufbuild/protovalidate/releases/tag/v0.14.2

    > IGNORE_IF_DEFAULT_VALUE is removed.
    > In most cases, you can replace it with IGNORE_IF_ZERO_VALUE. See #396 for details.
    > https://github.com/bufbuild/protovalidate/pull/396

    """
    # raise NotImplementedError

    # Iterate all .proto files in the directory
    for proto_file in proto_files_dir.glob("**/*.proto"):
        try:
            with proto_file.open("r") as file:
                content = file.read()

            # Replace the old enum value with the new one
            updated_content = content.replace(
                "IGNORE_IF_DEFAULT_VALUE", "IGNORE_IF_ZERO_VALUE"
            )

            # Write the updated content back to the file
            with proto_file.open("w") as file:
                file.write(updated_content)

            print(f"Updated {proto_file.name} to use IGNORE_IF_ZERO_VALUE")

        except Exception as e:  # noqa: PERF203
            print(f"Error updating {proto_file.name}: {e}")


def main():
    """Main function to coordinate the generation process."""
    print("OpenTDF Connect RPC Client Generator")
    print("===================================")

    # Get the proto-gen directory (parent of scripts)
    proto_gen_dir = Path(__file__).parent.parent
    proto_files_dir = proto_gen_dir / "proto-files"
    generated_dir = proto_gen_dir / "generated"

    # Check dependencies
    if not check_dependencies():
        return 1

    # Ensure directories exist
    proto_files_dir.mkdir(exist_ok=True)
    generated_dir.mkdir(exist_ok=True)

    # Download proto files (optional - can use existing files)
    if (
        "--download" in sys.argv or not any(proto_files_dir.glob("**/*.proto"))
    ) and not download_proto_files(proto_gen_dir):
        return 1

    # Check if we have any proto files
    proto_files = list(proto_files_dir.glob("**/*.proto"))
    if not proto_files:
        print("No .proto files found. Use --download to fetch from OpenTDF platform.")
        return 1

    print(f"Found {len(proto_files)} proto files:")
    for proto_file in proto_files:
        print(f"  - {proto_file.name}")

    # Fix IGNORE_IF_DEFAULT_VALUE in proto files
    _fix_ignore_if_default_value(proto_files_dir)

    # Generate protobuf and Connect RPC files using buf
    if not run_buf_generate(proto_gen_dir):
        return 1

    # Create __init__.py files
    create_init_files(generated_dir)

    print("\n✓ Connect RPC client generation complete!")
    print(f"  Generated files are in: {generated_dir}")
    print(f"  Connect RPC clients: {generated_dir}/*_connect.py")
    print(f"  Protobuf files: {generated_dir}/*_pb2.py")
    print(f"  Type stubs: {generated_dir}/*_pb2.pyi")

    if (generated_dir / "legacy_grpc").exists():
        print(f"  Legacy gRPC files: {generated_dir}/legacy_grpc/*_pb2_grpc.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
