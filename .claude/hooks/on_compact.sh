#!/bin/bash
# Hook: PreCompact - Claude is compacting context
curl -s -X POST http://127.0.0.1:3002/status \
  -H "Content-Type: application/json" \
  -d '{"state": "compacting"}' > /dev/null 2>&1 &
