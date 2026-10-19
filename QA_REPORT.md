[Back to README](README.md) | [Assessment responses](ASSESSMENT_RESPONSES.md) | [Prompt diffs](prompts/prompt_patch_diffs.md)

# QA Report – Retell AI Voice Agent (Topic 13)

**Agents under test:** AI Receptionist (router, V2), Sales Specialist (V2), Tech Support Specialist (V2)
**Model:** GPT 5.6 Terra | **Voice:** Cimo | **Language:** English (US) | **Date:** 2026-10-19
**Tester:** Sheikh Mohammed Shahid

> Results below come from 2 real web calls (credits are limited). Scenarios not exercised are marked NOT TESTED, not PASS. Full Call IDs: copy from Retell Call History and replace the truncated ones.

## 1. Scope
Dimensions: Happy Path, Interruptions, Edge Cases, Unsupported Requests, Failures. Pass bar: all tested scenarios pass, average latency < 1200 ms.

Live calls:
- **Call A** – AI Receptionist, 07:40 IST, 1m 24s, ID `call_cfb5066a728c84d2f0b...aea`
- **Call B** – AI Receptionist -> Sales -> back to Receptionist, 07:42 IST, 1m 28s, ID `call_9460ec3a7b4f651e6fa...641`

## 2. 15-Scenario QA Log

| ID | Category | Scenario | Test input | Actual (from transcript) | Status | Latency | Call |
|---|---|---|---|---|---|---|---|
| SC-001 | Normal | FAQ | "What are your business hours?" | KB retrieval, answered "Mon-Fri, 9 AM to 6 PM" | PASS | 1103 ms (call e2e) | A |
| SC-002 | Normal | Specialist transfer w/ consent | "I need pricing for the enterprise plan." | Agent asked "Is that okay?", caller said yes, then `transfer_agent_sales` fired | PASS | 1003 ms (call e2e) | B |
| SC-003 | Normal | Account verification | Name + account "1235" | Name collected and spelled back; account number collected; `extract_caller_context` called | PASS | – | B |
| SC-004 | Difficult | Interruption | "Wait. I have a different question." | Agent was not speaking at that moment, so barge-in was not proven. Agent also stayed silent ~11 s, then asked "Are you still there?" | NOT PROVEN (see Bug 3) | not measured | A |
| SC-005 | Difficult | Silence prompt | ~10 s quiet | "Are you still there?" delivered, no premature disconnect | PASS (timing approximate) | – | A |
| SC-006 | Difficult | Out-of-scope / competitor | "What is competitive pricing?" | "I can only discuss our own services. The main desk can help further." | PASS | – | A |
| SC-007 | Difficult | Background noise | – | – | NOT TESTED | – | – |
| SC-008 | Difficult | Slang | – | – | NOT TESTED | – | – |
| SC-009 | Difficult | Wrong language | "Hola. Hola." | "I'm sorry, I can only assist in English." No invented words | PASS | – | A |
| SC-010 | Failure | Database offline | – | – | NOT TESTED | – | – |
| SC-011 | Failure | SIP busy on transfer | – | – | NOT TESTED | – | – |
| SC-012 | Failure | Silent call -> 3 warnings -> disconnect | ~20 s silence at end | Reminders "Are you still there?", "I'm still here whenever you're ready.", then goodbye + `end_call` | PASS | – | A |
| SC-013 | Normal | DNC opt-out | – | Existing outbound agent rule and `register_dnc_optout` tool configured, no live call (no outbound number) | NOT TESTED | – | – |
| SC-014 | Difficult | Spelling confirmation | Name "Sheikh Mohammed Shahid" | Agent spelled name letter by letter and asked to confirm | PASS | – | B |
| SC-015 | Failure | API timeout (10 s) | – | – | NOT TESTED | – | – |

Extra checks from the calls:
- **Billing bounce (Bug 1 retest):** "How do I check my account balance?" was NOT transferred to Sales/Tech Support. Bounce loop fixed. But see Bug 2.
- **Transfer back (R8):** Sales asked consent ("Is that okay?"), caller said yes, `transfer_agent_receptionist` fired, Receptionist resumed. PASS.

**Summary:** 8 PASS, 1 NOT PROVEN, 6 NOT TESTED, 0 hard FAIL on tested scenarios, but 2 real defects found (Bug 2, Bug 3).

## 3. Bug / Fix Log (before vs after)

### Bug 1 – Billing request bounced between agents (FIXED, verified in Call A)
- Before: Receptionist sent "account balance" to Sales, Sales bounced to Tech Support (no billing specialist exists).
```diff
- 5. Immediately call the matching transfer tool. No consent is needed for internal transfers.
+ 4. Explain the transfer and ask: "I can transfer you to our [Sales/Support] specialist for that. Is that okay?"
+ 5. Only after the caller agrees, call the matching transfer tool. If they decline, offer a callback instead.
+ - Billing, invoices, account balance, payments: do not transfer. (new Routing Rules line)
```
- Evidence: Call A (no transfer), Call B (consent before transfer).

### Bug 2 – Hallucinated billing instructions (FOUND, fix proposed, NOT yet applied or retested)
- Call A 0:17: agent said "You can check your account balance by signing in to your account portal and opening the Billing or Account section." The FAQ has nothing about billing and no knowledge-base retrieval ran on that turn. Expected: "We don't have a billing specialist available. I can arrange a callback..." This is a hallucination (unverified detail).
- Proposed fix:
```diff
- - Billing, invoices, account balance, payments: do not transfer. Check the FAQ; if it has no answer, say "We don't have a billing specialist available..."
+ - Billing, invoices, account balance, payments: do not transfer. The FAQ has NO billing information. Never explain how to check a balance or mention any portal. Always say "We don't have a billing specialist available. I can arrange a callback within one business day." and offer the callback.
```
- Retest: ____ (to run after publishing)

### Bug 3 – "Wait. I have a different question." treated like a hold request (FOUND, suspected cause, fix proposed)
- Call A 0:27: agent did not answer for ~11 s, then asked "Are you still there?". The Receptionist prompt has a hold rule that outputs `NO_RESPONSE_NEEDED` when the caller says to wait. Likely the word "Wait" triggered it. (Hypothesis from transcript, not confirmed in logs.)
- Proposed fix (adapt to the exact existing hold line):
```diff
+ Only output NO_RESPONSE_NEEDED when the caller asks you to hold or wait without asking anything new. If the caller says "wait" and then asks a question, answer the question.
```
- Retest: ____

### Minor observations
- Sales language rule fired on garbled speech ("I only speak English" when the caller's server sentence was mis-transcribed); caller rephrased and it recovered.
- Post-call `call_outcome` was `abandoned` for Call B although two transfers happened (expected `transferred`). Preset "Call Successful" showed Unsuccessful for both calls.

## 4. Latency Audit

Retell call-level end-to-end latency from the Conversation Analysis panel:

| Call | e2e latency |
|---|---|
| A | 1103 ms |
| B | 1003 ms |
| Average | 1053 ms (< 1200 ms) |

Script run (fill after export): `python scripts/audit_ftl.py calls/*.json` -> avg ____ ms, max ____ ms.
Limitations: only 2 calls (the requirement file suggests ~100 turns); e2e latency is Retell's metric, not a `first_token_latency_ms` field. Retell's header estimate shows 1445-1985 ms for the Receptionist, which is only an estimate. Factors affecting latency: model, prompt length, tool count, knowledge-base retrieval, response wait time (550 ms).

## 5. Traceability

| Source | BRD | PRD | FR/NFR | User Story | Test Case |
|---|---|---|---|---|---|
| BRD-001 | BRD-001 | PRD-001 | FR-001 | US-001 | TC-001, TC-004 |
| BRD-002 | BRD-002 | PRD-003 | FR-002 | n/a | TC-002 |
| BRD-003 | BRD-003 | PRD-002 | FR-003, NFR-001 | US-002 | TC-005 |
| BRD-004 | BRD-004 | PRD-004 | FR-004, FR-005 | US-001 | TC-003 |

## 6. Post-Call Analysis Check
- Summary: complete and accurate in both calls.
- Sentiment (`caller_sentiment`): Neutral, reasonable.
- Outcome (`call_outcome`): `abandoned` for both; Call B should be `transferred` (not accurate).
- Platform `user_sentiment` preset has no "Frustrated" value; custom `caller_sentiment` was added instead.

## 7. Configuration Evidence
Speech: response wait time 550 ms (target was 600 ms; the slider steps in 50 ms and stopped at 550), interruption sensitivity 0.5 (Medium), reminders every 5 s x 3, end call on silence 30 s, on all 3 agents. V2 "QA fixes - billing, consent, silence" published on all 3. Tools: `end_call`, `transfer_agent_receptionist` (Sales, Tech Support), existing transfer tools kept. `register_dnc_optout` (phone_number, optout_reason) exists on the outbound agent.

## 8. Final Verification
Verdict: **Not yet production-ready**. Two open defects (Bug 2 hallucinated billing answer, Bug 3 "Wait" handling) need the proposed prompt fixes, a publish, and a retest.

## 9. Comments (limitations and assumptions)
- Credits were limited, so only 2 live calls were run; SC-007, 008, 010, 011, 013, 015 were not tested.
- `agent_swap` cannot carry `target_agent_id` / `transfer_reason`, so a parameterised `transfer_agent` tool was not created; existing transfer tools perform real transfers.
- Platform DNC toggle left unchanged on purpose to avoid the caller hearing two DNC scripts; DNC covered by prompt rule + `register_dnc_optout`.
- No voicemail tool exists, so busy-line fallback is a callback offer.
- Identity check accepts any account number (known weakness, not changed).
- `register_dnc_optout` timeout is 20 s (assessment mentions 10 s); header secret not shown in evidence.
