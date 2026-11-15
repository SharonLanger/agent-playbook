# Observability

The Langfuse adapter owns configuration/client setup, the independent project check, the explicit mock span writer and native tracing initialization/CLI flush. The application runner uses native scope/propagation under the approved narrow integration exception. Automatic Flow observations are blocked by the pinned instrumentor's quiet-mode behavior; see the maintained workflow guide. Context stays data-only, business steps provider-free, and logging is deferred.

Follow [the guarded project structure](../../../../designs/project-structure.md).
