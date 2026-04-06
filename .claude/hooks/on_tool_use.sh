#!/bin/bash
# Hook: PostToolUse - Claude used a tool
# $1 = tool name
TOOL_NAME="${1:-unknown}"
curl -s -X POST http://127.0.0.1:3002/status \
  -H "Content-Type: application/json" \
  -d "{\"state\": \"working\", \"tool\": \"$TOOL_NAME\"}" > /dev/null 2>&1 &
