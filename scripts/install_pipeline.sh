#!/bin/bash
# Idempotent installer for the DIY clipping pipeline.
# Safe to run on every session start; finishes fast when already installed.

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  apt-get update -qq && apt-get install -y -qq ffmpeg || true
fi

pip install --quiet --upgrade yt-dlp faster-whisper || true

exit 0
