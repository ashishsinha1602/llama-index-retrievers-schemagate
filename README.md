# llama-index-retrievers-schemagate

A LlamaIndex retriever for text-to-SQL. Each question gets only the tables it needs, picked from
the tables the caller may read. A table the caller can't read is never a candidate, so it can't
reach the prompt.

```bash
pip install llama-index-retrievers-schemagate
```

```python
from schemagate import Catalog, Principal
from llama_index.retrievers.schemagate import SchemagateRetriever, prompt_fragment

cat = Catalog().bootstrap("postgresql://localhost/app")
retriever = SchemagateRetriever(cat, top_k=6, principal=Principal("okta:jdoe", roles={"finance"}))

nodes = retriever.retrieve("revenue by month")   # one node of DDL per selected table
schema_for_prompt = prompt_fragment(nodes)
```

Selection runs offline (BM25 plus a small embedder) and calls no model. `aretrieve` works too.

On Spider 2.0's public BigQuery and Snowflake schemas, the median database with 50+ tables went from
the full schema to a selection 92.9% smaller, in prompt tokens. On small databases there is little to
cut: 8.8% on BIRD's seven-table ones. The script and the recall trade-off are in
[schemagate's BENCHMARKS.md](https://github.com/ashishsinha1602/schemagate/blob/main/BENCHMARKS.md#prompt-tokens-on-public-schemas-the-saving-grows-with-the-schema).

The retriever itself is maintained in [schemagate](https://github.com/ashishsinha1602/schemagate),
which also has the guide: [docs/llamaindex.md](https://github.com/ashishsinha1602/schemagate/blob/main/docs/llamaindex.md).

Apache-2.0.
