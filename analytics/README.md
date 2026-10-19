# ARMOR Phase 2: Autonomous Detection Engines

This directory contains the stateful pattern matching (CEP) and graph-based behavior analysis engines. These services consume raw telemetry streams from the NATS message bus, correlate actions across micro-windows, and emit high-severity threat alerts.