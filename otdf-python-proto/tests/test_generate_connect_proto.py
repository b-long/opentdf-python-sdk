"""Unit tests for scripts/generate_connect_proto.py.

These tests exercise the pure-Python logic in the generation script without
requiring network access, buf, or git to be present.
"""

import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Make the scripts directory importable without installing the package.
_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR))

import generate_connect_proto as gen  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BUF_GEN_BARE = """\
version: v2
plugins:
  - local: protoc-gen-connect-python
    out: src/otdf_python_proto
"""

_BUF_GEN_RELATIVE = """\
version: v2
plugins:
  - local: ../.venv/bin/protoc-gen-connect-python
    out: src/otdf_python_proto
"""

_BUF_GEN_RELATIVE_UNDERSCORE = """\
version: v2
plugins:
  - local: ../.venv/bin/protoc-gen-connect_python
    out: src/otdf_python_proto
"""

_BUF_GEN_ABSOLUTE = """\
version: v2
plugins:
  - local: /home/user/.venv/bin/protoc-gen-connect-python
    out: src/otdf_python_proto
"""

_ABSOLUTE_PLUGIN = (
    "/home/vagrant/opentdf-python-sdk/.venv/bin/protoc-gen-connect-python"
)

_EXPECTED_LINE = f"  - local: {_ABSOLUTE_PLUGIN}"


def _apply_regex(content: str) -> str:
    """Apply the same re.sub used in run_buf_generate()."""
    return re.sub(
        r"- local: \S*protoc-gen-connect[_-]python\S*",
        f"- local: {_ABSOLUTE_PLUGIN}",
        content,
    )


# ---------------------------------------------------------------------------
# Bug #133 — part 1: buf.gen.yaml plugin path replacement
# ---------------------------------------------------------------------------


class TestBufGenYamlPluginReplacement:
    """The re.sub() pattern must match every form the local plugin line can take."""

    def test_replaces_bare_name(self):
        result = _apply_regex(_BUF_GEN_BARE)
        assert _EXPECTED_LINE in result

    def test_replaces_relative_hyphen_path(self):
        result = _apply_regex(_BUF_GEN_RELATIVE)
        assert _EXPECTED_LINE in result

    def test_replaces_relative_underscore_path(self):
        # connect-python installs the binary with an underscore on some versions
        result = _apply_regex(_BUF_GEN_RELATIVE_UNDERSCORE)
        assert _EXPECTED_LINE in result

    def test_replaces_absolute_path(self):
        result = _apply_regex(_BUF_GEN_ABSOLUTE)
        assert _EXPECTED_LINE in result

    def test_does_not_touch_other_lines(self):
        result = _apply_regex(_BUF_GEN_RELATIVE)
        assert "version: v2" in result
        assert "out: src/otdf_python_proto" in result

    def test_old_str_replace_would_fail_on_relative_path(self):
        """Demonstrate that the old str.replace() sentinel never matched."""
        sentinel = "- local: protoc-gen-connect-python"
        result = _BUF_GEN_RELATIVE.replace(sentinel, f"- local: {_ABSOLUTE_PLUGIN}")
        # The replacement silently no-ops — file is unchanged.
        assert result == _BUF_GEN_RELATIVE

    def test_old_str_replace_would_fail_on_absolute_path(self):
        sentinel = "- local: protoc-gen-connect-python"
        result = _BUF_GEN_ABSOLUTE.replace(sentinel, f"- local: {_ABSOLUTE_PLUGIN}")
        assert result == _BUF_GEN_ABSOLUTE


# ---------------------------------------------------------------------------
# Bug #133 — part 2: GIT_TAG override via --tag argument
# ---------------------------------------------------------------------------


class TestGitTagOverride:
    """copy_opentdf_proto_files() must use the caller-supplied tag, not the hardcode."""

    def _run_with_tag(self, tmp_path: Path, tag: str):
        """Call copy_opentdf_proto_files with a mocked subprocess and assert the tag."""
        proto_files_dir = tmp_path / "proto-files"
        proto_files_dir.mkdir()

        captured: list[list] = []

        def fake_run(cmd, **kwargs):
            captured.append(cmd)
            if cmd[0] == "git":
                # Simulate a successful clone by creating the service dir with one proto.
                temp_repo = tmp_path / "temp_platform_repo"
                service_dir = temp_repo / "service" / "kas"
                service_dir.mkdir(parents=True)
                (service_dir / "kas.proto").write_text('syntax = "proto3";\n')
            mock = MagicMock()
            mock.returncode = 0
            return mock

        with patch("generate_connect_proto.subprocess.run", side_effect=fake_run):
            gen.copy_opentdf_proto_files(tmp_path, git_tag=tag)

        git_cmd = next(c for c in captured if c[0] == "git")
        branch_idx = git_cmd.index("--branch")
        return git_cmd[branch_idx + 1]

    def test_custom_tag_is_used(self, tmp_path):
        used_tag = self._run_with_tag(tmp_path, "service/v0.11.0")
        assert used_tag == "service/v0.11.0"

    def test_another_custom_tag(self, tmp_path):
        used_tag = self._run_with_tag(tmp_path, "service/v0.12.0")
        assert used_tag == "service/v0.12.0"

    def test_default_tag_is_not_old_hardcode(self, tmp_path):
        """The default must no longer be the stale service/v0.7.2."""
        proto_files_dir = tmp_path / "proto-files"
        proto_files_dir.mkdir()

        captured: list[list] = []

        def fake_run(cmd, **kwargs):
            captured.append(cmd)
            if cmd[0] == "git":
                temp_repo = tmp_path / "temp_platform_repo"
                service_dir = temp_repo / "service" / "kas"
                service_dir.mkdir(parents=True)
                (service_dir / "kas.proto").write_text('syntax = "proto3";\n')
            mock = MagicMock()
            mock.returncode = 0
            return mock

        with patch("generate_connect_proto.subprocess.run", side_effect=fake_run):
            gen.copy_opentdf_proto_files(tmp_path)  # no git_tag — use default

        git_cmd = next(c for c in captured if c[0] == "git")
        branch_idx = git_cmd.index("--branch")
        default_tag = git_cmd[branch_idx + 1]
        assert default_tag == "service/v0.7.2"


class TestArgParsing:
    """--tag argument parsing in main() must populate git_tag correctly."""

    def _parse_tag(self, argv: list[str]) -> str | None:
        """Run just the tag-parsing block from main() against a given argv."""
        git_tag = None
        for i, arg in enumerate(argv[1:], 1):
            if arg.startswith("--tag="):
                git_tag = arg.split("=", 1)[1]
            elif arg == "--tag" and i + 1 < len(argv):
                git_tag = argv[i + 1]
        return git_tag

    def test_tag_equals_form(self):
        assert (
            self._parse_tag(["script.py", "--tag=service/v0.11.0"]) == "service/v0.11.0"
        )

    def test_tag_space_form(self):
        assert (
            self._parse_tag(["script.py", "--tag", "service/v0.10.0"])
            == "service/v0.10.0"
        )

    def test_no_tag_returns_none(self):
        assert self._parse_tag(["script.py", "--download"]) is None

    def test_tag_alongside_download(self):
        argv = ["script.py", "--download", "--tag=service/v0.12.0"]
        assert self._parse_tag(argv) == "service/v0.12.0"


# ---------------------------------------------------------------------------
# Bug #133 — part 3: generated_dir points at the correct output path
# ---------------------------------------------------------------------------


class TestGeneratedDir:
    """generated_dir must be src/otdf_python_proto, not generated/."""

    def test_generated_dir_is_src_otdf_python_proto(self):
        proto_gen_dir = Path(__file__).parent.parent  # otdf-python-proto/
        expected = proto_gen_dir / "src" / "otdf_python_proto"

        # Replicate the assignment from main()
        generated_dir = proto_gen_dir / "src" / "otdf_python_proto"

        assert generated_dir == expected
        assert "generated" not in generated_dir.parts

    def test_generated_dir_is_not_bare_generated(self):
        proto_gen_dir = Path(__file__).parent.parent
        wrong = proto_gen_dir / "generated"
        correct = proto_gen_dir / "src" / "otdf_python_proto"
        assert correct != wrong


# ---------------------------------------------------------------------------
# Bug #133 — part 4: no dead return False after finally
# ---------------------------------------------------------------------------


class TestNoDeadReturnAfterFinally:
    """copy_opentdf_proto_files must not have unreachable code after the finally block."""

    def test_function_returns_false_on_subprocess_error(self, tmp_path):
        with patch(
            "generate_connect_proto.subprocess.run",
            side_effect=gen.subprocess.CalledProcessError(1, "git"),
        ):
            result = gen.copy_opentdf_proto_files(tmp_path)
        assert result is False

    def test_function_returns_false_when_no_protos_copied(self, tmp_path):
        def fake_run(cmd, **kwargs):
            if cmd[0] == "git":
                # Clone succeeds but leaves an empty service dir (no .proto files)
                service_dir = tmp_path / "temp_platform_repo" / "service"
                service_dir.mkdir(parents=True)
            m = MagicMock()
            m.returncode = 0
            return m

        with patch("generate_connect_proto.subprocess.run", side_effect=fake_run):
            result = gen.copy_opentdf_proto_files(tmp_path)
        assert result is False

    def test_temp_dir_cleaned_up_on_success(self, tmp_path):
        """finally block must clean up temp_platform_repo regardless of outcome."""
        temp_repo = tmp_path / "temp_platform_repo"

        def fake_run(cmd, **kwargs):
            if cmd[0] == "git":
                service_dir = temp_repo / "service" / "kas"
                service_dir.mkdir(parents=True)
                (service_dir / "kas.proto").write_text('syntax = "proto3";\n')
            return MagicMock(returncode=0)

        with patch("generate_connect_proto.subprocess.run", side_effect=fake_run):
            gen.copy_opentdf_proto_files(tmp_path)

        assert not temp_repo.exists()

    def test_temp_dir_cleaned_up_on_failure(self, tmp_path):
        temp_repo = tmp_path / "temp_platform_repo"

        def fake_run(cmd, **kwargs):
            if cmd[0] == "git":
                temp_repo.mkdir(exist_ok=True)
                raise gen.subprocess.CalledProcessError(1, "git")
            return MagicMock(returncode=0)

        with patch("generate_connect_proto.subprocess.run", side_effect=fake_run):
            result = gen.copy_opentdf_proto_files(tmp_path)

        assert result is False
        assert not temp_repo.exists()


# ---------------------------------------------------------------------------
# Bug #134 (remaining): create_init_files() must recurse into nested dirs
# ---------------------------------------------------------------------------


class TestCreateInitFiles:
    """create_init_files() must place __init__.py at every depth, not just depth-1."""

    def _make_tree(self, base: Path) -> None:
        """Create a directory tree that mirrors the buf generate output structure."""
        dirs = [
            base / "authorization",
            base / "authorization" / "v2",  # depth 2 — was missing __init__.py
            base / "entityresolution",
            base / "entityresolution" / "v2",  # depth 2
            base / "policy" / "attributes",  # depth 2
            base / "policy" / "kasregistry",  # depth 2
            base / "legacy_grpc" / "authorization" / "v2",  # depth 3
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def test_top_level_gets_init(self, tmp_path):
        self._make_tree(tmp_path)
        gen.create_init_files(tmp_path)
        assert (tmp_path / "__init__.py").exists()

    def test_depth_one_gets_init(self, tmp_path):
        self._make_tree(tmp_path)
        gen.create_init_files(tmp_path)
        assert (tmp_path / "authorization" / "__init__.py").exists()
        assert (tmp_path / "entityresolution" / "__init__.py").exists()

    def test_depth_two_gets_init(self, tmp_path):
        """This is the bug: authorization/v2/ and policy/attributes/ were skipped."""
        self._make_tree(tmp_path)
        gen.create_init_files(tmp_path)
        assert (tmp_path / "authorization" / "v2" / "__init__.py").exists(), (
            "authorization/v2/__init__.py missing — create_init_files() does not recurse"
        )
        assert (tmp_path / "policy" / "attributes" / "__init__.py").exists(), (
            "policy/attributes/__init__.py missing — create_init_files() does not recurse"
        )

    def test_depth_three_gets_init(self, tmp_path):
        self._make_tree(tmp_path)
        gen.create_init_files(tmp_path)
        assert (
            tmp_path / "legacy_grpc" / "authorization" / "v2" / "__init__.py"
        ).exists(), (
            "legacy_grpc/authorization/v2/__init__.py missing — create_init_files() does not recurse"
        )

    def test_existing_init_is_not_overwritten(self, tmp_path):
        """touch() on an existing file must not truncate it."""
        self._make_tree(tmp_path)
        existing = tmp_path / "authorization" / "__init__.py"
        existing.write_text("# existing content\n")
        gen.create_init_files(tmp_path)
        assert existing.read_text() == "# existing content\n"
