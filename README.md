<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=240&section=header&text=Voice%20Agent%20QA&fontSize=68&animation=fadeIn&fontAlignY=36&desc=Production%20Testing%2C%20Debugging%20%26%20Conversation%20QA&descAlignY=58&descSize=19" alt="Voice Agent QA banner" width="100%"/>

<a href="https://github.com/shaikshahid777/retell-voice-agent-qa-topic13">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=800&color=36BCF7&center=true&vCenter=true&width=760&lines=Retell+AI+Voice+Agent+QA;15-Scenario+Test+Pack+%7C+Real+Call+Evidence;Prompt+Patch+Debugging+%28Before+%2F+After%29;Latency+Audit+%7C+Honest+Results" alt="Typing animation" />
</a>

<br/><br/>

[![Watch Demo](https://img.shields.io/badge/WATCH_DEMO-Loom-625DF5?style=for-the-badge&logo=loom&logoColor=white)](LOOM_LINK_HERE)
[![QA Report](https://img.shields.io/badge/QA_REPORT-Open-2ea44f?style=for-the-badge&logo=readthedocs&logoColor=white)](QA_REPORT.md)
[![Responses](https://img.shields.io/badge/ASSESSMENT_RESPONSES-Open-0366d6?style=for-the-badge&logo=bookstack&logoColor=white)](ASSESSMENT_RESPONSES.md)
[![Prompt Diffs](https://img.shields.io/badge/PROMPT_DIFFS-Open-f97316?style=for-the-badge&logo=git&logoColor=white)](prompts/prompt_patch_diffs.md)
[![Evidence](https://img.shields.io/badge/EVIDENCE-Screenshots-e11d48?style=for-the-badge&logo=googlephotos&logoColor=white)](evidence/)
[![Latency Script](https://img.shields.io/badge/LATENCY_SCRIPT-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](scripts/audit_ftl.py)

![Retell AI](https://img.shields.io/badge/Retell_AI-Voice_Agents-111827?style=flat-square)
![Agents](https://img.shields.io/badge/Inbound_agents-3-0ea5e9?style=flat-square)
![Live calls](https://img.shields.io/badge/Live_calls-2-8b5cf6?style=flat-square)
![Pass](https://img.shields.io/badge/PASS-8-22c55e?style=flat-square)
![Not proven](https://img.shields.io/badge/NOT_PROVEN-1-f59e0b?style=flat-square)
![Not tested](https://img.shields.io/badge/NOT_TESTED-6-6b7280?style=flat-square)
![Latency](https://img.shields.io/badge/Avg_e2e_latency-1053_ms-22c55e?style=flat-square)
![Verdict](https://img.shields.io/badge/Verdict-Not_yet_production--ready-ef4444?style=flat-square)

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=6,11,20&height=3&section=header" width="100%" alt=""/>

</div>

## 🧭 Quick navigation

| 📄 Document | What is inside |
|---|---|
| [QA_REPORT.md](QA_REPORT.md) | 15-scenario log, bug/fix log, latency, traceability, verdict |
| [ASSESSMENT_RESPONSES.md](ASSESSMENT_RESPONSES.md) | FAQ Q1-Q15 and Exercises 1-12 |
| [prompts/prompt_patch_diffs.md](prompts/prompt_patch_diffs.md) | Before/after prompt diffs for all 3 agents |
| [docs/ANNOTATIONS.md](docs/ANNOTATIONS.md) | Annotation standard (documented, not applied in the UI) |
| [scripts/audit_ftl.py](scripts/audit_ftl.py) | First-token / latency audit script |
| [evidence/](evidence/) | Retell dashboard screenshots |
| [calls/](calls/) | Exported call JSON (added after running curl) |

## 🎯 About

QA evidence for **Topic 13: Production Testing, Debugging & Conversation QA**. System under test: a Retell AI front desk, with an **AI Receptionist** that routes callers to a **Sales Specialist** or a **Tech Support Specialist**.

Credits were limited, so I ran **2 real web calls** and reported honestly: scenarios I did not run are marked **NOT TESTED**, never PASS.

## 📊 Results at a glance

| Result | Count | Scenarios |
|---|---|---|
| ✅ PASS | 8 | SC-001, 002, 003, 005, 006, 009, 012, 014 |
| ⚠️ NOT PROVEN | 1 | SC-004 (interruption: agent was not mid-speech) |
| ⏸️ NOT TESTED | 6 | SC-007, 008, 010, 011, 013, 015 |

⏱️ Retell call-level end-to-end latency: **1103 ms** (Call A), **1003 ms** (Call B), average **1053 ms** (target < 1200 ms). Only 2 calls, and this is Retell's e2e metric, not a per-turn first-token value.

## 🐞 Bugs found

| # | Bug | Status |
|---|---|---|
| 1 | Billing question bounced Receptionist → Sales → Tech Support, and transfers needed no consent | ✅ Fixed, verified in Calls A and B |
| 2 | Agent invented "sign in to your portal" steps for account balance | 🔧 Found, fix proposed, not yet applied or retested |
| 3 | "Wait. I have a different question." handled like a hold request | 🔧 Found, fix proposed, not yet applied or retested |

## 🔀 How the agents connect

```mermaid
flowchart LR
    C([Caller]) --> R[AI Receptionist]
    R -- "consent, then transfer_agent_sales" --> S[Sales Specialist]
    R -- "consent, then transfer_agent_tech_support" --> T[Tech Support Specialist]
    S -- "consent, then transfer_agent_receptionist" --> R
    T -- "consent, then transfer_agent_receptionist" --> R
    R -- "billing: no transfer" --> CB[Offer callback]
    R -- "silence x3" --> E([end_call])
```

## ⚙️ Configuration used (all 3 inbound agents)

| Setting | Value |
|---|---|
| Interruption sensitivity | 0.5 (Medium) |
| Response wait time | 550 ms (target was 600 ms; slider steps by 50 ms) |
| Reminders | every 5 s, 3 times |
| End call on silence | 30 s |
| Published version | V2 "QA fixes - billing, consent, silence" |

## 🖼️ Evidence gallery

<table>
  <tr>
    <td align="center"><b>Call A: Receptionist</b><br/><a href="evidence/call-A-receptionist-analysis-transcript.png"><img src="evidence/call-A-receptionist-analysis-transcript.png" width="100%" alt="Call A"/></a></td>
    <td align="center"><b>Call B: Transfers</b><br/><a href="evidence/call-B-transfers-analysis-transcript.png"><img src="evidence/call-B-transfers-analysis-transcript.png" width="100%" alt="Call B"/></a></td>
  </tr>
  <tr>
    <td align="center"><b>Speech settings</b><br/><a href="evidence/speech-settings-receptionist.png"><img src="evidence/speech-settings-receptionist.png" width="100%" alt="Speech settings"/></a></td>
    <td align="center"><b>Call settings</b><br/><a href="evidence/call-settings-receptionist.png"><img src="evidence/call-settings-receptionist.png" width="100%" alt="Call settings"/></a></td>
  </tr>
  <tr>
    <td align="center"><b>Functions (Receptionist)</b><br/><a href="evidence/functions-receptionist.png"><img src="evidence/functions-receptionist.png" width="100%" alt="Functions"/></a></td>
    <td align="center"><b>Published V2</b><br/><a href="evidence/versions-receptionist.png"><img src="evidence/versions-receptionist.png" width="100%" alt="Versions"/></a></td>
  </tr>
</table>

More screenshots for Sales and Tech Support are in [evidence/](evidence/).

<details>
<summary><b>📋 Full 15-scenario result table (click to expand)</b></summary>

| ID | Scenario | Status |
|---|---|---|
| SC-001 | FAQ (business hours) | ✅ PASS |
| SC-002 | Transfer with consent | ✅ PASS |
| SC-003 | Account verification | ✅ PASS |
| SC-004 | Interruption | ⚠️ NOT PROVEN |
| SC-005 | Silence prompt | ✅ PASS |
| SC-006 | Out-of-scope competitor | ✅ PASS |
| SC-007 | Background noise | ⏸️ NOT TESTED |
| SC-008 | Slang | ⏸️ NOT TESTED |
| SC-009 | Wrong language | ✅ PASS |
| SC-010 | Database offline | ⏸️ NOT TESTED |
| SC-011 | SIP busy on transfer | ⏸️ NOT TESTED |
| SC-012 | Silent call, 3 warnings, disconnect | ✅ PASS |
| SC-013 | DNC opt-out | ⏸️ NOT TESTED |
| SC-014 | Spelling confirmation | ✅ PASS |
| SC-015 | API timeout | ⏸️ NOT TESTED |

Details, transcripts and latency per scenario: [QA_REPORT.md](QA_REPORT.md).

</details>

## 🗂️ Repository structure

```
.
├── README.md
├── QA_REPORT.md
├── ASSESSMENT_RESPONSES.md
├── prompts/prompt_patch_diffs.md
├── scripts/audit_ftl.py
├── docs/ANNOTATIONS.md
├── calls/
└── evidence/
```

## ▶️ Run the latency audit

```bash
curl -X GET "https://api.retellai.com/get-call/<CALL_ID>" \
  -H "Authorization: Bearer $RETELL_API_KEY" > calls/<CALL_ID>.json
python scripts/audit_ftl.py calls/*.json
```

Never commit your API key.

## ⚠️ Limitations

- Only 2 live calls; SC-007, 008, 010, 011, 013, 015 not tested; no full 15-scenario regression rerun.
- Barge-in time (< 500 ms) not measured.
- Retell's `agent_swap` cannot carry `target_agent_id` / `transfer_reason`, so a parameterised `transfer_agent` tool was not created.
- Platform DNC toggle left unchanged so callers do not hear two different opt-out scripts; DNC is covered by the prompt rule and the `register_dnc_optout` tool on the outbound agent.
- No voicemail tool, so busy-line fallback is a callback offer.
- Annotation standard documented but not applied inside the Retell UI.

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=130&section=footer" width="100%" alt="footer"/>
</div>
