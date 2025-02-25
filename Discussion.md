Solutions Considered

1. Sequential Read

Reads file line-by-line and filters logs.

Pros: Simple, low memory usage.

Cons: Slow for very large files.

2. Binary Search (if indexed)

Jump to approximate location using binary search.

Pros: Faster lookup time.

Cons: Requires an index file.

3. Parallel Processing

Split file into chunks and process in parallel.

Pros: Faster execution.

Cons: Requires multi-threading setup.

Final Solution Summary

Chose sequential read due to its simplicity and ability to handle large files efficiently without extra indexing.
