"""Package the ShipPDF Claude plugin for upload, using only distributable files."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    repository = Path(__file__).resolve().parent.parent
    plugin = repository
    manifest = plugin / ".claude-plugin" / "plugin.json"
    version = json.loads(manifest.read_text())["version"]
    if not version or any(
        character not in "0123456789abcdefghijklmnopqrstuvwxyz.-" for character in version
    ):
        raise ValueError("Plugin version must be a safe filename component")

    files = [manifest, plugin / "README.md", *sorted((plugin / "skills").rglob("SKILL.md"))]
    if len(files) < 3:
        raise ValueError("Plugin must contain at least one skill")
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(plugin.resolve()):
            raise ValueError(f"Plugin file must be contained in the plugin directory: {path}")

    output = repository / "dist" / f"shippdf-claude-plugin-{version}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(plugin).as_posix())
    print(output)


if __name__ == "__main__":
    main()
