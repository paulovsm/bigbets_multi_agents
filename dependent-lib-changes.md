# List of the changes made in the dependent libs to make the app run

## CrewAi
### crewai/knowledge/knowledge.py

Change the query limit paramenter from 3 to 10

**Originial version**
```def query(self, query: List[str], limit: int = 10) -> List[Dict[str, Any]]:```

**Update to this project**
```def query(self, query: List[str], limit: int = 10) -> List[Dict[str, Any]]:```

### crewai/knowledge/source/crew_docling_source.py

Change the Chunker implementation to support the chunk size limitation

**Original Version**
```
from docling_core.transforms.chunker.hierarchical_chunker import HierarchicalChunker
```

```
def _chunk_doc(self, doc: "DoclingDocument") -> Iterator[str]:
        chunker = HierarchicalChunker()
        for chunk in chunker.chunk(doc):
            yield chunk.text
```

**Update to this project**
```
from docling.chunking import HybridChunker
```

```
def _chunk_doc(self, doc: "DoclingDocument") -> Iterator[str]:
        chunker = HybridChunker(max_tokens=self.chunk_size)
        for chunk in chunker.chunk(doc):
            yield chunk.text
```