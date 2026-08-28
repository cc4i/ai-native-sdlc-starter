# Intent: Incident Anomaly Remediation [INC-NNN]

**Trigger Source**: [Automated Control Band Breach / Metric Alert / Sentry / Datadog / Cron]  
**Severity**: [SEV-1 | SEV-2 | SEV-3]  
**Detected At**: [YYYY-MM-DD HH:MM:SS UTC]  
**Diagnosing Agent**: [Sidecar Diagnostics Agent / Antigravity]  
**Status**: [Draft / Triaged / In Progress / Resolved]  

---

## 1. Anomaly & Breached Metric

- **Metric**: [e.g., `ci_test_failure_rate`, `api_5xx_rate`, `latency_p99`]
- **Observed Value**: [e.g., 8.4% error rate]
- **Control Threshold**: [e.g., > 1.0% error rate (3σ breach)]
- **Time Window**: [e.g., 2026-08-27 10:15 UTC - 10:45 UTC]

---

## 2. Automated Root-Cause Diagnosis

- **Affected Endpoints / Subsystems**: [e.g., `POST /api/v1/checkout`]
- **Observed Error Signatures**: [e.g., `TimeoutError: Connection pool exhausted`]
- **Suspected Cause**: [e.g., Downstream payment gateway latency spike causing connection starvation]
- **Diagnostic Evidence / Trace Links**: [Logs, spans, stack traces]

---

## 3. Proposed Remediation Outcome

- **Immediate Fix**: [e.g., Add connection timeout & circuit breaker to gateway adapter]
- **Long-term Guardrail**: [e.g., Add integration stress test and continuous eval case]

---

## 4. Constraints & Safety Checks

- [ ] Must not break active checkout transactions.
- [ ] Must fallback gracefully with user-friendly retry message.
- [ ] Add permanent regression test in `tests/integration/`.

---

## 5. Triage & Lifecycle Handover

- **On-Call Engineer Action**: [ ] Fix Now (Escalate to Stage 2 `specs/`) | [ ] Schedule | [ ] Dismiss False Positive
- **Assigned To**: @[engineer or team]
- **Next Artifact**: `specs/incident-INC-NNN-fix.md`
