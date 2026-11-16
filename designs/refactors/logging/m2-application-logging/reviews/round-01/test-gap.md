# Round 01 test-gap review

Author: independent test-gap reviewer, `gpt-6.1-sol`. Candidate: `2bd162c799cf49c2058b531d7afe340900cb616d`; base: `8895c2dbf6674716656d5b780f8c181a743e44f2`. Contract: `caeb1637bd9aa611447703f4c19c38becacfe412`. Verdict: **CHANGES REQUIRED**. Scope: every LG-01–12 case, meaningful assertions, runtime behavior and execution evidence. No candidate edits or examples access.

## Findings, all open in round 01

| ID | Severity | Expected versus observed; references and disposition |
|---|---|---|
| TG-01 | High | LG-09 excludes raw input from exported diagnostics. `workflow_runner.py:192–199` chains an input-bearing Pydantic ValidationError, while `:142–165` attaches native exception details for every non-configuration error. A real OTel memory export of `run_workflow("wf-02", '"INPUT_SECRET_SENTINEL"')` contains that sentinel in `Workflow failed` `exception.stacktrace`. Preserve application classification/cause but keep the rejected input out of exported records. Add a real-export regression. |
| TG-02 | High | LG-05/06/07 require enabled production logging setup/cleanup, exactly-once execution and containment of emission/flush/shutdown faults. `test_lg05_lg06_lg07_lg09_runner_faults` uses a fixture with logging disabled and externally installed Simple processor; only trace flush fails. `test_lg05_lg06_initialization_and_handler_cleanup` fails exporter construction without a workflow. Enabled scope, partial cleanup, ordering and shared-provider safety have no meaningful assertions. Add focused production-boundary tests. |
| TG-03 | Medium | LG-08 requires native tracing and logs together. `test_lg08_log_only_keeps_global_trace_provider` only invokes the helper under an external handler and compares ambient trace state; the existing native tracing suite runs with logging disabled. Add real coexistence evidence using the production scope and native correlation. |
| TG-04 | Medium | LG-01/02/03 require all five selected identity fields, distinct interleaved run contexts, DEBUG record set, exception message/no locals and exported recovery followed by completion. `test_lg01_lg02_lg11_context_schema_filter_and_replacement` omits workflow ID/run ID/agent type and true interleaved distinct runs. `test_lg03_native_exception_chain` omits exception.message and checks only the absence of a `locals` key. Add meaningful assertions. |
| TG-05 | Medium | LG-04 lacks invalid logging level/YAML configuration classification and enabled/endpoint override precedence; LG-09 lacks credential/auth failure objects, whole-input sentinel and SDK diagnostic recursion; LG-12 lacks proxy isolation and script behavior through actual component check functions. Existing nodes cover only a subset. Add targeted cases without claiming stubbed health proves ingestion. |

## Mapping at round 01

All new test nodes below are in `app/tests/observability/test_application_logging.py`.

| ID | Node/evidence | Assessment |
|---|---|---|
| LG-01 | `test_lg01_lg02_lg11_context_schema_filter_and_replacement` | Partial, TG-04 |
| LG-02 | same; runner-fault repeated calls | Partial, TG-04 |
| LG-03 | `test_lg03_native_exception_chain`; runner-fault failure case | Partial, TG-04 |
| LG-04 | `test_lg04_defaults_and_endpoint_rejection`, `test_lg04_precedence` | Partial, TG-05 |
| LG-05 | `test_lg05_lg06_initialization_and_handler_cleanup`, `test_lg05_langfuse_initialization_warns_and_disables` | Partial, TG-02 |
| LG-06 | `test_lg06_native_fault_preserves_business` entry/update/exit cases; runner faults | Native fault cause/step assertions useful; logging faults partial, TG-02 |
| LG-07 | runner-fault repeats; existing `test_workflow_tracing.py::test_cli_flush_after_close`, `test_repeat_invocations` | Trace evidence useful; production logger lifecycle partial, TG-02 |
| LG-08 | `test_lg08_log_only_keeps_global_trace_provider`; existing native tracing suite | Partial, TG-03 |
| LG-09 | runner/init/native-fault sentinel tests | Concrete failure TG-01 and gaps TG-05 |
| LG-10 | No stored VictoriaLogs record evidence | **NOT RUN**, Docker denied; flush/send mocks do not qualify |
| LG-11 | schema/replacement node; source review of adapter isolation | SDK-level replacement evidence; no second database migration claim |
| LG-12 | `test_lg12_health` status cases, `test_lg12_unreachable_and_script`, `test_lg12_script_reports_failed_enabled_component` | Partial, TG-05 |

Independent command from `app/`: `.venv/bin/pytest tests/observability/test_application_logging.py tests/observability/test_workflow_tracing.py -q` → **16 passed, 9 failed, 24 errors**. CrewAI import tried to write under read-only `/home/agent/.local/share/app`; granting only credentials-directory write access did not fix it. A further run with `XDG_DATA_HOME=/tmp/m2-review-data` and credentials access stalled after four passes; interrupted at 71.67 seconds, reporting **4 passed, KeyboardInterrupt**. These are environment-qualified failures, not proof of implementation regression. The direct real-export TG-01 reproduction succeeded independently. No skipped test was counted as passed; live Docker, release and UI checks were NOT RUN by this reviewer.
