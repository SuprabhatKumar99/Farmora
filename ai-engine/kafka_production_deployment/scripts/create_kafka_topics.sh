#!/usr/bin/env bash
set -euo pipefail

BOOTSTRAP="${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}"

topics=(
  ai.inference.request
  ai.inference.completed
  ai.inference.failed
  ai.inference.dlq
  followup.feedback.received
)

for topic in "${topics[@]}"; do
  kafka-topics.sh     --bootstrap-server "$BOOTSTRAP"     --create     --if-not-exists     --topic "$topic"     --partitions 3     --replication-factor 1
done
