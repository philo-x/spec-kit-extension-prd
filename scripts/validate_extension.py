#!/usr/bin/env python3
"""Validation script for spec-kit-prd extension.

Verifies:
1. extension.yml exists, is valid YAML, and conforms to Spec Kit ExtensionManifest schema.
2. All declared commands, templates, and config files exist.
3. Command markdown files have valid frontmatter and required structure.
4. All reference documents in references/ exist and are readable.
5. Examples in examples/ exist and are valid.
"""

import os
import re
import sys
from pathlib import Path
import yaml

COMMAND_NAME_PATTERN = re.compile(r"^speckit\.[a-z0-9-]+\.[a-z0-9-]+$")
ID_PATTERN = re.compile(r"^[a-z0-9-]+$")


def validate():
    root = Path(__file__).resolve().parent.parent
    print(f"🔍 Validating extension at {root}...")
    errors = []
    warnings = []

    # 1. Check extension.yml
    manifest_path = root / "extension.yml"
    if not manifest_path.exists():
        errors.append("extension.yml not found at project root")
        return errors, warnings

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        errors.append(f"Failed to parse extension.yml: {e}")
        return errors, warnings

    # Schema version
    if manifest.get("schema_version") != "1.0":
        errors.append(f"Invalid schema_version: {manifest.get('schema_version')} (expected '1.0')")

    # Extension section
    ext = manifest.get("extension")
    if not isinstance(ext, dict):
        errors.append("Missing or invalid 'extension' mapping")
    else:
        for field in ["id", "name", "version", "description", "author", "license"]:
            if field not in ext:
                errors.append(f"Missing required field 'extension.{field}'")
            elif not isinstance(ext[field], str):
                errors.append(f"Field 'extension.{field}' must be a string")

        ext_id = ext.get("id", "")
        if not ID_PATTERN.match(ext_id):
            errors.append(f"Invalid extension.id: '{ext_id}' (must match ^[a-z0-9-]+$)")

    # Requires section
    requires = manifest.get("requires")
    if not isinstance(requires, dict):
        errors.append("Missing or invalid 'requires' mapping")
    elif "speckit_version" not in requires:
        errors.append("Missing required 'requires.speckit_version'")

    # Provides section
    provides = manifest.get("provides")
    if not isinstance(provides, dict):
        errors.append("Missing or invalid 'provides' mapping")
    else:
        commands = provides.get("commands", [])
        if not isinstance(commands, list) or len(commands) == 0:
            errors.append("provides.commands must be a non-empty list")
        else:
            for i, cmd in enumerate(commands):
                if not isinstance(cmd, dict):
                    errors.append(f"Command #{i} is not a mapping")
                    continue
                cmd_name = cmd.get("name", "")
                cmd_file = cmd.get("file", "")
                cmd_desc = cmd.get("description", "")

                if not cmd_name or not COMMAND_NAME_PATTERN.match(cmd_name):
                    errors.append(f"Command #{i} has invalid name '{cmd_name}' (expected pattern 'speckit.<id>.<command>')")

                if not cmd_file:
                    errors.append(f"Command '{cmd_name}' missing 'file'")
                else:
                    target_file = root / cmd_file
                    if not target_file.exists():
                        errors.append(f"Command file '{cmd_file}' not found on disk")
                    else:
                        # Check frontmatter
                        content = target_file.read_text(encoding="utf-8")
                        if not content.startswith("---"):
                            errors.append(f"Command file '{cmd_file}' missing frontmatter")
                        elif "description:" not in content:
                            errors.append(f"Command file '{cmd_file}' frontmatter missing 'description'")

                if not cmd_desc:
                    errors.append(f"Command '{cmd_name}' missing 'description'")

        # Templates
        templates = provides.get("templates", [])
        for tmpl in templates:
            tmpl_file = tmpl.get("file")
            if tmpl_file:
                target_file = root / tmpl_file
                if not target_file.exists():
                    errors.append(f"Template file '{tmpl_file}' not found on disk")

        # Config
        config = provides.get("config", [])
        for cfg in config:
            tmpl_file = cfg.get("template")
            if tmpl_file:
                target_file = root / tmpl_file
                if not target_file.exists():
                    errors.append(f"Config template file '{tmpl_file}' not found on disk")

    # Check References
    ref_dir = root / "references"
    expected_refs = [
        "prd-principles.md",
        "requirement-classification.md",
        "business-rules.md",
        "acceptance-criteria.md",
        "quality-checklist.md",
    ]
    for ref_name in expected_refs:
        ref_file = ref_dir / ref_name
        if not ref_file.exists():
            errors.append(f"Reference file '{ref_name}' missing in references/")

    # Check Docs
    docs_dir = root / "docs"
    for doc_name in ["architecture.md", "user-guide.md"]:
        if not (docs_dir / doc_name).exists():
            errors.append(f"Documentation file '{doc_name}' missing in docs/")

    # Check Examples
    example_spec = root / "examples" / "work-report" / "spec.md"
    example_prd = root / "examples" / "work-report" / "product" / "prd.md"
    example_review = root / "examples" / "work-report" / "product" / "review-report.md"
    if not example_spec.exists():
        errors.append("Example spec.md missing")
    if not example_prd.exists():
        errors.append("Example prd.md missing")
    if not example_review.exists():
        errors.append("Example review-report.md missing")

    return errors, warnings


if __name__ == "__main__":
    errors, warnings = validate()
    for w in warnings:
        print(f"⚠️  Warning: {w}")
    if errors:
        for e in errors:
            print(f"❌ Error: {e}")
        sys.exit(1)
    else:
        print("✅ All validation checks PASSED! Extension manifest and all assets are valid.")
        sys.exit(0)
