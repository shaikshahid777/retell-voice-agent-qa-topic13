# Documentation and annotation standard (Implementation Doc section 5)

Status: documented here. NOT applied inside the Retell UI (no node-colour or sticky-note step was performed). Limitation, see QA_REPORT section 8.

## State node colours (intended standard)
| Colour | Meaning | Where in this project |
|---|---|---|
| Green | Inbound greet state | Receptionist begin message |
| Purple | Telephony / transfer tool call | transfer_agent_sales, transfer_agent_tech_support, transfer_agent_receptionist |
| Yellow | VAD / interruption setting | Speech settings (sensitivity 0.5, response wait 550 ms) |
| Orange | Fallback redirect | Busy-line / tool-failure callback offer |
| Red | Halt / disconnect | Silence handling, end_call after reminders |

## Designer notes (intended text)
- Interruption note: "Interruption Threshold: Calibrated to Medium sensitivity. VAD timeout set to 600ms to allow callers to interrupt prompts naturally." (Actual values used: sensitivity 0.5, response wait 550 ms.)
- DNC safety override note: "Opt-Out Interceptor: Scans for DNC requests, reads legal warnings, and triggers register_dnc_optout tool." (Lives on the outbound agent.)
- Latency note: "FTL Audit Check: Tracks first-token latencies. Average FTL must remain under 1200ms across test executions."
