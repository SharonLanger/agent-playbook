# Adapters

`langfuse/connection.py` owns native client creation and the independent read-only project check. `observations.py` retains the explicit mock writer. `runtime.py` initializes native tracing and once-only CrewAI wrappers, and attempts CLI flush without replacing workflow outcomes. Native SDK resources own caching, batching and shutdown; there is no project client registry or tracing facade.

Follow [the guarded project structure](../../../../../designs/project-structure.md).
