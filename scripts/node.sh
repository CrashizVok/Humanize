#!/bin/sh
# The humanize mode switch. One command, three verbs, and it always reports what
# it verified rather than what it attempted.
#
#   sh .claude/skills/humanize/scripts/mode.sh on
#   sh .claude/skills/humanize/scripts/mode.sh off
#   sh .claude/skills/humanize/scripts/mode.sh status
#
# Why this exists: the off path used to be a bare shell line in SKILL.md, and it
# reported "Failed to disable" twice in live testing while the mode was in fact
# off. Any non-zero exit from any part of that line looked like a failed switch.
# This script separates doing from reporting: it tries both ways of turning the
# mode off, then reads the state back and prints what is actually true.

set -u

root="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$root" ]; then
  root=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
fi
state="$root/.claude/.humanize-mode"

# Reads the state file and echoes on or off. A missing file is off. A file whose
# first line does not start with on is off, which is the same rule the hook uses.
read_state() {
  if [ -f "$state" ] && head -n 1 "$state" 2>/dev/null | grep -qi '^on'; then
    echo on
  else
    echo off
  fi
}

case "${1:-status}" in
  on)
    mkdir -p "$root/.claude" 2>/dev/null
    printf 'on\nscope=prose\nlang=auto\n' > "$state" 2>/dev/null
    ;;
  off)
    # Write first, then delete. If the delete is refused the file still says off,
    # and if the write is refused the delete still removes it. Only both failing
    # leaves the mode on, and then the report below says so.
    printf 'off\n' > "$state" 2>/dev/null
    rm -f "$state" 2>/dev/null
    ;;
  status) ;;
  *)
    echo "usage: mode.sh on|off|status" >&2
    exit 2
    ;;
esac

now=$(read_state)
echo "humanize mode: $now"
if [ -f "$state" ]; then
  echo "state file: $state"
else
  echo "state file: none"
fi
exit 0
