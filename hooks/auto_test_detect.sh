#!/usr/bin/env bash
# Detect missing test files for changed source files.
# PostToolUse hook, matcher: Write|Edit
# Does NOT run tests — just warns if no test file exists.

set -uo pipefail

PAYLOAD=$(cat)
FILE=$(echo "$PAYLOAD" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

[ -z "$FILE" ] && exit 0

# Only check source files
case "$FILE" in
    *.ts|*.tsx|*.js|*.jsx|*.py|*.php|*.rb|*.go|*.rs|*.java|*.kt|*.swift|*.cpp|*.c)
        ;;
    *)
        exit 0
        ;;
esac

# Skip if the file itself is a test
case "$FILE" in
    *test*|*spec*|*Test*|*_test*|*tests/*)
        exit 0
        ;;
esac

DIR=$(dirname "$FILE")
BASE=$(basename "$FILE" | sed 's/\.[^.]*$//')

# Look for test files
FOUND=0
for PATTERN in "${DIR}/${BASE}.test."* "${DIR}/${BASE}.spec."* "${DIR}/__tests__/${BASE}."* "${DIR}/test_${BASE}."* "${DIR}/${BASE}_test."*; do
    if compgen -G "$PATTERN" > /dev/null 2>&1; then
        FOUND=1
        break
    fi
done

if [ "$FOUND" -eq 0 ]; then
    # Use Python for safe JSON serialization
    python3 -c "
import json
msg = 'No test file found for $FILE. Consider adding tests.'
print(json.dumps({'systemMessage': msg}))
" 2>/dev/null || echo "{\"systemMessage\": \"No test file found. Consider adding tests.\"}"
fi
