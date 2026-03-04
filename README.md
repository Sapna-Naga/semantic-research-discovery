# Semantic Research Article Classification & Recommendation Engine



## Engineering Learnings

During development several failure modes were identified and documented.

| Failure Mode | Cause | Fix |
|--------------|------|-----|
Embedding drift | Model upgrade changed vector distribution | Rebuilt FAISS index |
Training instability | High LR during transformer fine-tuning | LR scheduler + gradient clipping |
Recommendation bias | Papers from dominant domain over-ranked | Diversity re-ranking |

Detailed reports are available in `docs/postmortems/`.
