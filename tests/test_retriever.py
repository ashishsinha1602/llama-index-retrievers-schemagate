"""The retriever against the real llama-index-core, on schemagate's bundled demo schema."""
import asyncio

import pytest
from llama_index.core.retrievers import BaseRetriever
from schemagate import Principal
from schemagate.demo_schema import demo_catalog

from llama_index.retrievers.schemagate import SchemagateRetriever, prompt_fragment

CATALOG = demo_catalog()   # 42 tables and views; hr_compensation readable by the payroll role only


def test_is_a_llamaindex_retriever():
    assert isinstance(SchemagateRetriever(CATALOG), BaseRetriever)


def test_returns_ddl_nodes_with_metadata():
    nodes = SchemagateRetriever(CATALOG, top_k=3, expand_fks=False).retrieve("which customers owe us money")
    assert len(nodes) == 3
    for n in nodes:
        assert n.node.get_content().startswith(("TABLE", "VIEW", "--"))
        assert {"name", "kind", "reason", "columns"} <= set(n.node.metadata)


def test_async():
    nodes = asyncio.run(SchemagateRetriever(CATALOG).aretrieve("late shipments by carrier"))
    assert "ship_shipment" in prompt_fragment(nodes)


@pytest.mark.parametrize("roles, visible", [((), False), (("payroll",), True)])
def test_a_table_the_caller_may_not_read_never_reaches_the_prompt(roles, visible):
    r = SchemagateRetriever(CATALOG, principal=Principal("okta:x", roles=set(roles)))
    assert ("hr_compensation" in prompt_fragment(r.retrieve("salary and pay grade by employee"))) is visible
