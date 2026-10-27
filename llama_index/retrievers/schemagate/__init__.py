# Copyright 2026 Ashish Sinha. Licensed under the Apache License, Version 2.0.
"""LlamaIndex integration for schemagate: an identity-scoped schema retriever for text-to-SQL.

    from schemagate import Catalog, Principal
    from llama_index.retrievers.schemagate import SchemagateRetriever, prompt_fragment

    cat = Catalog().bootstrap("postgresql://localhost/app")
    retriever = SchemagateRetriever(cat, top_k=6, principal=Principal("okta:jdoe", roles={"finance"}))
    ddl = prompt_fragment(retriever.retrieve("revenue by month"))

The retriever is maintained in schemagate itself (``schemagate.integrations.llamaindex``); this
package is the ``llama-index-retrievers-<name>`` distribution.
"""
from schemagate.integrations.llamaindex import SchemagateRetriever, prompt_fragment

__all__ = ["SchemagateRetriever", "prompt_fragment"]
