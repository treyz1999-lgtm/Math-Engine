"""
services package

Purpose:
    Contains the calculator's core computational engine.

Responsibilities:
    - Mathematical operations
    - Symbolic expression handling
    - Plot generation
    - Statistical analysis
    - Linear algebra
    - Geometry calculations

This layer contains business logic only.

Important:
    Service modules should NOT:
        - define FastAPI routes
        - parse HTTP requests
        - return HTTP responses

Flow:
    Frontend
        -> routes
        -> services
        -> result
"""