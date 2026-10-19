<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:2563eb,100:06b6d4&height=230&section=header&text=Voice%20Agent%20QA&fontSize=64&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Production%20Testing%20%7C%20Debugging%20%7C%20Conversation%20QA&descAlignY=60&descSize=18&descColor=e2e8f0" alt="Voice Agent QA" width="100%">
</p>

<h1 align="center">Retell AI Voice Agent QA</h1>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=800&color=2563EB&center=true&vCenter=true&width=700&lines=15-Scenario+Test+Pack;Prompt+Patch+Debugging+(Before+%2F+After);Latency+Audit+and+Real+Call+Evidence;Honest+Results%3A+PASS+%7C+NOT+PROVEN+%7C+NOT+TESTED" alt="Typing animation">
</p>

<p align="center">
  <a href="LOOM_LINK_HERE"><img src="https://img.shields.io/badge/WATCH%20DEMO-Loom-625DF5?style=for-the-badge&logo=loom&logoColor=white" alt="Watch Demo"></a>
  <a href="QA_REPORT.md"><img src="https://img.shields.io/badge/QA%20REPORT-Open-16a34a?style=for-the-badge" alt="QA Report"></a>
  <a href="ASSESSMENT_RESPONSES.md"><img src="https://img.shields.io/badge/RESPONSES-Open-2563eb?style=for-the-badge" alt="Assessment Responses"></a>
</p>
<p align="center">
  <a href="prompts/prompt_patch_diffs.md"><img src="https://img.shields.io/badge/PROMPT%20DIFFS-Open-f97316?style=for-the-badge" alt="Prompt Diffs"></a>
  <a href="evidence/"><img src="https://img.shields.io/badge/EVIDENCE-Screenshots-e11d48?style=for-the-badge" alt="Evidence"></a>
  <a href="scripts/audit_ftl.py"><img src="https://img.shields.io/badge/LATENCY%20SCRIPT-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Latency Script"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Inbound%20agents-3-0ea5e9?style=flat-square" alt="agents">
  <img src="https://img.shields.io/badge/Live%20calls-2-8b5cf6?style=flat-square" alt="calls">
  <img src="https://img.shields.io/badge/PASS-8-22c55e?style=flat-square" alt="pass">
  <img src="https://img.shields.io/badge/NOT%20PROVEN-1-f59e0b?style=flat-square" alt="not proven">
  <img src="https://img.shields.io/badge/NOT%20TESTED-6-6b7280?style=flat-square" alt="not tested">
  <img src="https://img.shields.io/badge/Avg%20e2e%20latency-1053%20ms-22c55e?style=flat-square" alt="latency">
  <img src="https://img.shields.io/badge/Verdict-Not%20yet%20production--ready-ef4444?style=flat-square" alt="verdict">
</p>

---

## About

QA evidence for **Topic 13: Production Testing, Debugging and Conversation QA** in Retell AI.

The system under test is a front-desk setup: an **AI Receptionist** that routes callers to a **Sales Specialist** or a **Tech Support Specialist**.

Credits were limited, so I ran **2 real web calls** and reported honestly. Scenarios I did not run are marked **NOT TESTED**, never PASS.

## Contents

| Document | What is inside |
|---|---|
| [QA_REPORT.md](QA_REPORT.md) | 15-scenario log, bug and fix log, latency, traceability, verdict |
| [ASSESSMENT_RESPONSES.md](ASSESSMENT_RESPONSES.md) | FAQ Q1 to Q15 and Exercises 1 to 12 |
| [prompts/prompt_patch_diffs.md](prompts/prompt_patch_diffs.md) | Before and after prompt diffs for all 3 agents |
| [docs/ANNOTATIONS.md](docs/ANNOTATIONS.md) | Annotation standard (documented, not applied in the UI) |
| [scripts/audit_ftl.py](scripts/audit_ftl.py) | Latency audit script |
| [evidence/](evidence/) | Retell dashboard screenshots |
| [calls/](calls/) | Exported call JSON (added after running curl) |

## Results at a glance

| Result | Count | Scenarios |
|---|---|---|
| PASS | 8 | SC-001, 002, 003, 005, 006, 009, 012, 014 |
| NOT PROVEN | 1 | SC-004 (interruption: agent was not mid-speech) |
| NOT TESTED | 6 | SC-007, 008, 010, 011, 013, 015 |

Retell call-level end-to-end latency: **1103 ms** (Call A) and **1003 ms** (Call B), average **1053 ms** against a target of under 1200 ms. This is from only 2 calls and is Retell's e2e metric, not a per-turn first-token value.

## Bugs found

| # | Bug | Status |
|---|---|---|
| 1 | Billing question bounced Receptionist to Sales to Tech Support, and transfers needed no consent | Fixed, verified in Calls A and B |
| 2 | Agent invented "sign in to your portal" steps for account balance | Found, fix proposed, not yet applied or retested |
| 3 | "Wait. I have a different question." handled like a hold request | Found, fix proposed, not yet applied or retested |

## How the agents connect

```mermaid
flowchart LR
    C([Caller]) --> R[AI Receptionist]
    R -->|consent, transfer_agent_sales| S[Sales Specialist]
    R -->|consent, transfer_agent_tech_support| T[Tech Support Specialist]
    S -->|consent, transfer_agent_receptionist| R
    T -->|consent, transfer_agent_receptionist| R
    R -->|billing: no transfer| CB[Offer callback]
    R -->|silence x3| E([end_call])
```

## Configuration used (all 3 inbound agents)

| Setting | Value |
|---|---|
| Interruption sensitivity | 0.5 (Medium) |
| Response wait time | 550 ms (target was 600 ms; the slider steps by 50 ms) |
| Reminders | every 5 s, 3 times |
| End call on silence | 30 s |
| Published version | V2 "QA fixes - billing, consent, silence" |

## Evidence gallery

<table>
  <tr>
    <td align="center" width="50%"><b>Call A: Receptionist</b><br><a href="evidence/call-A-receptionist-analysis-transcript.png"><img src="evidence/call-A-receptionist-analysis-transcript.png" alt="Call A" width="100%"></a></td>
    <td align="center" width="50%"><b>Call B: Transfers</b><br><a href="evidence/call-B-transfers-analysis-transcript.png"><img src="evidence/call-B-transfers-analysis-transcript.png" alt="Call B" width="100%"></a></td>
  </tr>
  <tr>
    <td align="center"><b>Speech settings</b><br><a href="evidence/speech-settings-receptionist.png"><img src="evidence/speech-settings-receptionist.png" alt="Speech settings" width="100%"></a></td>
    <td align="center"><b>Call settings</b><br><a href="evidence/call-settings-receptionist.png"><img src="evidence/call-settings-receptionist.png" alt="Call settings" width="100%"></a></td>
  </tr>
  <tr>
    <td align="center"><b>Functions (Receptionist)</b><br><a href="evidence/functions-receptionist.png"><img src="evidence/functions-receptionist.png" alt="Functions" width="100%"></a></td>
    <td align="center"><b>Published V2</b><br><a href="evidence/versions-receptionist.png"><img src="evidence/versions-receptionist.png" alt="Versions" width="100%"></a></td>
  </tr>
</table>

Screenshots for the Sales and Tech Support agents are in [evidence/](evidence/).

## All 15 scenarios

| ID | Scenario | Status |
|---|---|---|
| SC-001 | FAQ (business hours) | PASS |
| SC-002 | Transfer with consent | PASS |
| SC-003 | Account verification | PASS |
| SC-004 | Interruption | NOT PROVEN |
| SC-005 | Silence prompt | PASS |
| SC-006 | Out-of-scope competitor | PASS |
| SC-007 | Background noise | NOT TESTED |
| SC-008 | Slang | NOT TESTED |
| SC-009 | Wrong language | PASS |
| SC-010 | Database offline | NOT TESTED |
| SC-011 | SIP busy on transfer | NOT TESTED |
| SC-012 | Silent call, 3 warnings, disconnect | PASS |
| SC-013 | DNC opt-out | NOT TESTED |
| SC-014 | Spelling confirmation | PASS |
| SC-015 | API timeout | NOT TESTED |

Details, transcripts and latency per scenario are in [QA_REPORT.md](QA_REPORT.md).

## Run the latency audit

```bash
curl -X GET "https://api.retellai.com/get-call/<CALL_ID>" \
  -H "Authorization: Bearer $RETELL_API_KEY" > calls/<CALL_ID>.json
python scripts/audit_ftl.py calls/*.json
```

Never commit your API key.

## Limitations

- Only 2 live calls; SC-007, 008, 010, 011, 013, 015 were not tested, and the full 15-scenario pack was not rerun after patching.
- Barge-in time (under 500 ms) was not measured.
- Retell's `agent_swap` cannot carry `target_agent_id` or `transfer_reason`, so a parameterised `transfer_agent` tool was not created.
- The platform DNC toggle was left unchanged so callers do not hear two different opt-out scripts. DNC is covered by the prompt rule and the `register_dnc_optout` tool on the outbound agent.
- There is no voicemail tool, so the busy-line fallback is a callback offer.
- The annotation standard is documented but not applied inside the Retell UI.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:06b6d4,50:2563eb,100:0f172a&height=120&section=footer" alt="footer" width="100%">
</p>
