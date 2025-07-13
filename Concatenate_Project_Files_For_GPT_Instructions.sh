#!/usr/bin/env bash
# ./Concatenate_Project_Files_For_GPT_Instructions.sh

set -euo pipefail  # Exit immediatly on error, undefined variable, or failed command
# see https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425 for details
cd "$(dirname "$0")" # Change to the script's directory
shopt -s globstar # Enable recursive globbing **/* will match files in subdirectories

echo "🔄 Generating timestamped context files..."

ts=$(date +"%Y%m%d_%H%M")
backup_dir="context_backup"
mkdir -p "$backup_dir"

# ─── Backup old contexts ───────────────────────────────────────────
for old in context_*.txt; do
  [[ -f "$old" ]] && mv "$old" "$backup_dir/"
done

# ─── Helper to append a file with a header ────────────────────────
append_file() {
  local target="$1"
  local src="$2"
  [[ "$src" == *"__pycache__"* ]] && return
  printf "\n\n# ===== %s =====\n" "$src" >> "$target"
  cat "$src" >> "$target"
}

# ─── Define context buckets ──────────────────────────────────
declare -A maps=(
  [app]="app/**/*.py app/Dockerfile app/entrypoint.sh"
  [config]="Makefile docker-compose.yml .env* pyproject.toml pyrightconfig.json alembic.ini app/alembic/env.py app/alembic/versions/*.py"
  [routes]="app/api/routes_*.py"
  [seed]="app/create_tables.py app/seed/**/*.py"
  [tests]="tests/**/*.py app/tests/**/*.py"
  [ci]=".github/workflows/*.yml README.md LICENSE"
)

# ─── Generate timestamped contexts ─────────────────────────────────
for name in "${!maps[@]}"; do
  out="context_${name}_${ts}.txt"
  : > "$out"

  matched=false
  for pattern in ${maps[$name]}; do
    for f in $pattern; do
      if [[ -f "$f" ]]; then
        matched=true
        append_file "$out" "$f"
      fi
    done
  done

  if ! $matched; then
    echo "⚠️  No files matched for ‘$name’; $out is empty"
  fi

  echo "  • $out"
done

# ─── Report sizes & warn if too large ─────────────────────────────
threshold="${CONTEXT_THRESHOLD:-800000}"
total=0

echo -e "\n📊 Character counts:"
for f in context_*_"$ts".txt; do
  count=$(wc -m < "$f")
  printf "  • %s: %d chars\n" "$f" "$count"
  total=$((total + count))
done

printf "Total across all files: %d chars\n" "$total"
if (( total > threshold )); then
  echo "⚠️  Total exceeds ${threshold} chars – consider trimming your context."
fi

echo "✅ Done."

