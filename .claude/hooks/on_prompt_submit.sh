#!/bin/bash
# Hook: UserPromptSubmit - User sent a message
curl -s -X POST http://127.0.0.1:3002/status \
  -H "Content-Type: application/json" \
  -d '{"state": "working"}' > /dev/null 2>&1 &
