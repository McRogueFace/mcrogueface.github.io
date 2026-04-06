#!/bin/bash
# Hook: Stop - Claude finished processing
curl -s -X POST http://127.0.0.1:3002/status \
  -H "Content-Type: application/json" \
  -d '{"state": "idle"}' > /dev/null 2>&1 &
