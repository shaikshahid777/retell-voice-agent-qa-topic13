[Back to README](README.md) | [QA report](QA_REPORT.md)

# Topic 13 – Production Testing, Debugging & Conversation QA
## Assessment Responses

---

## Part A – FAQ Answers

### Section 1: QA Testing Fundamentals

**Q1. Purpose of the 15-scenario QA pack and its three categories**
It is a repeatable checklist used to validate a Retell voice agent *before client rollout*, so failures are caught internally. It covers three categories:
- **Normal** – standard conditions (FAQ, billing transfer, account verification, DNC opt-out).
- **Difficult** – interruptions, long silence, out-of-scope asks, noise, slang, wrong language, spelling checks.
- **Failure** – system breakdowns (database offline, SIP line busy, silent call, API timeout).

**Q2. Five dialogue dimensions**
1. **Happy Paths** – typical error-free conversations; validates basic correctness.
2. **User Interruptions** – agent stops talking when the caller talks over it (VAD / backchanneling).
3. **Edge Cases** – accents, noise, slurred words, long pauses; agent must not hang up or crash.
4. **Unsupported Requests** – agent stays in prompt scope and does not hallucinate.
5. **Telephony & Function Failures** – API timeouts / DB drops; agent runs fallback (e.g. voicemail).

**Q3. Infrastructure tools**
(1) Retell AI developer account (call logs + recordings), (2) Postman or curl CLI to query Retell call endpoints, (3) a QA testing sheet to log runs.

**Q4. First-Token Latency (FTL)**
Time between the caller finishing speaking and the agent producing the first syllable of audio. Target is **< 1200 ms** average; above that a flag is raised.

### Section 2: Scenario Execution & Interruption Handling

**Q5. SC-004**
User interrupts the agent mid-speech. Agent must halt instantly, listen, and reply to the new input. **Pass if speech aborts within 500 ms.**

**Q6. Long silence (SC-005)**
Agent says "Are you still there?" or keeps waiting. **Pass if no premature disconnect.** (SC-012 covers fully silent calls: goodbye + hang up after 3 warnings.)

**Q7. Unsupported language (SC-009)**
Agent explains its limit ("I only speak English"). **Pass if the agent doesn't hallucinate words.** Hallucinating would mean inventing meaning or replying in a language it cannot reliably handle, giving the caller wrong or confusing information.

**Q8. VAD interruption config**
Retell console → Agent Settings → Interruption Settings:
- Enable Interruption = **True**
- Sensitivity Threshold = **Medium** (raise if background noise causes false interruptions)
- VAD silence timeout = **600 ms**

### Section 3: Prompt Debugging & Bug Fixing

**Q9. Hallucination**
The agent states details/promises not in its prompt or knowledge base. Example from docs: the Sales agent quoted a **custom 50% discount** that management never approved.

**Q10. Documenting a prompt patch**
Record: Bug identified → Before prompt → After prompt, using **diff format** (`-` removed line, `+` added line), then retest and log the pass. Example:
```diff
- - Answer any user queries regarding account upgrades.
+ - Only answer upgrades using the upgrades_faq_tool. Do not quote custom pricing discounts; refer them to Sales.
```

**Q11. Regression risk**
Fixing Scenario A can break Scenario B. Mitigation: **re-run the complete 15-scenario pack after every prompt change**, and keep prompt versions in Git.

### Section 4: Latency Auditing & Call Log Analysis

**Q12. Retrieving call logs**
```bash
curl -X GET "https://api.retellai.com/get-call/call_102983_abc" \
  -H "Authorization: Bearer YOUR_RETELL_API_KEY"
```
Response includes `call_id`, `agent_id`, `first_token_latency_ms`, `user_response_latency_ms`, `call_status`, and the `transcript` array (role, content, words).

**Q13. Full latency metrics**
| Metric | Measures |
|---|---|
| `first_token_latency_ms` | Caller stops → first audio syllable from agent |
| `user_response_latency_ms` | Delay in the user's own response time |
| `telephony_rtt_ms` | Round-trip transport latency over WebRTC/SIP |
| `total_turn_around_time_ms` | Full turn duration end to end |

### Section 5: Tools, Compliance & Annotations

**Q14. Custom tools**
- **TOOL-001 `transfer_agent`** – params `target_agent_id`, `transfer_reason`; transfers the call to another agent.
- **TOOL-002 `register_dnc_optout`** – params `phone_number`, `optout_reason`; registers the caller on the Do-Not-Call list.

**Q15. State node annotation colors**
- **Green** – Inbound state (greet)
- **Purple** – Telephony tool call (transfer execution)
- **Yellow** – VAD interruption event (sensitivity config)
- **Orange** – Fallback redirect (busy-line voicemail)
- **Red** – Halt/disconnect (silent call cleanup)

---

## Part B – Exercise Responses (based on the real results in `QA_REPORT.md`)

**Exercise 1 – QA Fundamentals:** Voice QA differs from text QA because voice runs in real-time audio (noise, lag, overlapping speech). Framework = 5 dialogue dimensions, a 15-scenario pack, FTL target < 1200 ms, version-controlled prompt fixes, post-call analytics audit. See FAQ Q1–Q4.

**Exercise 2 – Dialogue Dimension Testing:** Mapping and live coverage:
- Happy Path: SC-001, 002, 003 tested live (PASS). SC-013 not live-tested.
- Interruptions: SC-004 attempted, **not proven** (agent was not mid-speech; "Wait" was treated like a hold request, Bug 3).
- Edge Cases: SC-005, 009, 012 PASS. SC-007 (noise) and SC-008 (slang) not tested. SC-014 (spelling) PASS.
- Unsupported Requests: SC-006 PASS.
- Failures: SC-010, 011, 015 not tested (need failure simulation, credits limited).

**Exercise 3 – 15-Scenario Checklist:** All 15 are logged in `QA_REPORT.md` Section 2. Result of 2 real web calls: **8 PASS, 1 NOT PROVEN, 6 NOT TESTED**. Untested scenarios are marked as such, not as PASS.

**Exercise 4 – Interruption Settings:** Configured in the Retell UI on all 3 inbound agents: Interruption Sensitivity 0.5 (Medium), Response Wait time 550 ms (target was 600 ms; slider moves in 50 ms steps and stopped at 550), reminders every 5 s x 3, End Call on Silence 30 s. Retell's UI exposes "Response Wait time", which I treated as the closest equivalent to the VAD timeout; the mapping is not officially confirmed. Screenshots: `evidence/speech-settings-*.png`, `evidence/call-settings-*.png`. Barge-in timing (< 500 ms) was **not measured**.

**Exercise 5 – Prompt Patch Debugging:** See `prompts/prompt_patch_diffs.md` and `QA_REPORT.md` Section 3.
- Bug 1 (billing bounce between agents, and "no consent" transfers): fixed and verified in Calls A and B.
- Bug 2 (agent invented portal steps for account balance): found, fix proposed, **not applied or retested**.
- Bug 3 ("Wait. I have a different question." treated like a hold request): found, fix proposed, **not applied or retested**.
- A full 15-scenario regression rerun was **not done** (credits). Regression risk (RSK-001) is therefore still open.

**Exercise 6 – Retrieve & Analyze Call Logs:** Both calls were reviewed in Retell Call History (transcript, summary, sentiment, outcome, e2e latency). Findings: summaries accurate; `call_outcome` was `abandoned` for Call B although two transfers happened. The curl export and `scripts/audit_ftl.py` are provided; add the exported JSON to `calls/` and the script output to `QA_REPORT.md` Section 4 once run.

**Exercise 7 – Audit First-Token Latency:** Retell call-level End-to-End latency: Call A 1103 ms, Call B 1003 ms, average 1053 ms (< 1200 ms). Limits: only 2 calls, and this is Retell's e2e metric, not a per-turn `first_token_latency_ms`. Retell's header estimate for the Receptionist (1445-1985 ms) is an estimate only.

**Exercise 8 – Configure Custom Tools:** `register_dnc_optout` (phone_number, optout_reason) exists on the Cloud Solutions Outbound agent and was left unchanged. Transfers use the existing `transfer_agent_sales` / `transfer_agent_tech_support` / `transfer_agent` tools plus the new `transfer_agent_receptionist` (agent_swap) and `end_call`. A tool named `transfer_agent` with `target_agent_id` and `transfer_reason` parameters was **not created**, because Retell's `agent_swap` type cannot carry custom parameters.

**Exercise 9 – Documentation & Annotation Standards:** The colour and sticky-note standard is documented in `docs/ANNOTATIONS.md`. It was **not applied inside the Retell UI** (limitation).

**Exercise 10 – BRD/PRD/FR/NFR Mapping:** See the traceability table in `QA_REPORT.md` Section 5: BRD-001→PRD-001→FR-001→US-001→TC-001/004; BRD-002→PRD-003→FR-002→TC-002; BRD-003→PRD-002→FR-003/NFR-001→US-002→TC-005; BRD-004→PRD-004→FR-004/005→US-001→TC-003.

**Exercise 11 – User Stories, Risks & Acceptance Criteria:**
- US-001: partially met. 9 of 15 scenarios were run; failures were documented; retest after patches is still pending.
- US-002: partially met. Latency checked on 2 calls; average below 1200 ms; no 100-turn sample.
- RSK-001 (regression): not fully mitigated, because the full 15-scenario pack was not rerun after patching.
- NFR-002 (encrypted recording storage): not verified.

**Exercise 12 – End-to-End Production QA Verification:** Verdict: **not yet production-ready.** Two open defects (Bug 2, Bug 3) need the proposed prompt fixes, a publish, and a retest with the full pack. See `QA_REPORT.md` Section 8.
