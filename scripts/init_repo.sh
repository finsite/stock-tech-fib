#!/bin/bash
set -euo pipefail

REPO_NAME=$(basename "$PWD")
TODAY=$(date +%F)
VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.1.0")

echo "🔧 Initializing repository: $REPO_NAME"
echo "📅 Date: $TODAY"
echo "📌 Version: $VERSION"

# Update pyproject.toml — [project] only
echo "📝 Updating pyproject.toml..."
sed -i.bak -E "/^\[project\]/,/^\[.*\]/ s|^name = \".*\"$|name = \"$REPO_NAME\"|" pyproject.toml
sed -i.bak -E "/^\[project\]/,/^\[.*\]/ s|^version = \".*\"$|version = \"$VERSION\"|" pyproject.toml
sed -i.bak -E "/^\[project\]/,/^\[.*\]/ s|^description = \".*\"$|description = \"A template for the $REPO_NAME python project\"|" pyproject.toml
rm pyproject.toml.bak

# Precisely update [tool.commitizen] version using awk
awk -v v="$VERSION" '
  /^\[tool.commitizen\]/ { in_block=1; print; next }
  /^\[.*\]/              { in_block=0 }
  in_block && /^version = / { print "version = \"" v "\""; next }
  { print }
' pyproject.toml > pyproject.tmp && mv pyproject.tmp pyproject.toml

# Update mkdocs.yml
echo "📝 Updating mkdocs.yml..."
sed -i.bak -E "s/site_name: .*/site_name: $(echo "$REPO_NAME" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')/" mkdocs.yml
sed -i.bak -E "s/site_description: .*/site_description: Documentation for the $(echo "$REPO_NAME" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g') Project/" mkdocs.yml
sed -i.bak -E "s|repo_url: .*|repo_url: https://github.com/finsite/$REPO_NAME|" mkdocs.yml
rm mkdocs.yml.bak

# Reset and write changelog
echo "📝 Creating CHANGELOG.md..."
cat > CHANGELOG.md <<EOF
# Changelog

## [$VERSION] - $TODAY

### Added

- Initial project structure cloned from \`template_python\`
- Custom configuration and module setup for \`$REPO_NAME\`
EOF

# Run K8s Helm/Argo scaffolding generator
if [[ -f scripts/generate_k8_manifests.py ]]; then
    echo "🚀 Running generate_k8_manifests.py to create Helm/Argo structure..."
    python scripts/generate_k8_manifests.py --skip-validate
else
    echo "⚠️  generate_k8_manifests.py not found. Skipping K8/Argo structure generation."
fi

# Global replace template_python → REPO_NAME
echo "🔁 Replacing 'template_python' → '$REPO_NAME' where applicable..."
for file in README.md mkdocs.yml requirements.in requirements-dev.in .github/workflows/*; do
    if [[ -f "$file" ]]; then
        grep -q 'template_python' "$file" && sed -i.bak "s/template_python/$REPO_NAME/g" "$file"
    fi
done
find . -name '*.bak' -delete

# Optional: Recompile requirements if pip-compile is available
if command -v pip-compile &> /dev/null; then
    echo "🔁 Recompiling requirements files..."
    pip-compile requirements.in
    pip-compile requirements-dev.in
else
    echo "⚠️  pip-compile not found, skipping requirements recompile."
fi

# Final instructions
echo "✅ Initialization complete."
echo "👉 Next steps:"
echo "- [ ] Review README.md and mkdocs.yml manually"
echo "- [ ] Run: pre-commit install"
echo "- [ ] Run: mkdocs gh-deploy --clean --force (if docs ready)"
echo "- [ ] Run: pre-commit run --all-files"
