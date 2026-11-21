# Revised design round 1 independent test coverage review

Role: test coverage reviewer. Configured model gpt-6.2-sol; served ID unavailable. Candidate: d96dc81b960e4296446c068646f30acb349417a3. Verdict: **CHANGES REQUIRED**. Static review; no runtime, Compose or Mac tests.

| ID | Severity | Finding |
|---|---|---|
| TG-SC-01 | High | SC-05/08 need ambient project override and separate container, each volume, empty and failed-inventory cases. |
| TG-SC-02 | High | SC-06/07 need stop continuation after Langfuse failure, distinct Ctrl-C policy, and no calls/sleep after deadline. |
| TG-SC-03 | Medium | Evidence mapping should distinguish pytest, opt-in Compose, live Mac and diff/docs; live readback needs exact unique IDs, queries and volume identity. |

Selection/disabled explicit start and workflow isolation are meaningful. All findings open for round 2. [Reviewed tests](https://github.com/SharonLanger/agent-playbook/blob/d96dc81b960e4296446c068646f30acb349417a3/designs/refactors/logging/m3-service-composition/test-cases.md).
