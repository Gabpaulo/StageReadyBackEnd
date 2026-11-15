# StageReady ERD

- `fig_erd_stageready.png` / `.svg`: the figure (rendered with Mermaid 11.6 + ELK layout).
- `stageready_erd.mmd`: source used for the figure (paste into mermaid.live to edit).
- `stageready_erd_annotated.mmd`: same model with notes on each field (paths, enums, units).

## Where each entity lives
| Entity | Store | Path / location | Written by |
|---|---|---|---|
| USER | Firestore | users/{uid} | Ionic app (onboarding, profile); admin sets `role` |
| SPEECH | Firestore | users/{uid}/speeches/{id} | Ionic app after each analysis (full backend response in `feedback`) |
| SPEECH_HISTORY | Firestore | users/{uid}/speechHistory/{id} | Ionic app; read/deleted by admin |
| PRACTICE_SESSION | Firestore | users/{uid}/practice_sessions/{id} | Ionic practice mode |
| PRACTICE_SCRIPT | Firestore | practiceScripts/{id} | Admin app (CRUD + seed) |
| USER_GAMIFICATION | Firestore | userGamification/{uid} | Ionic app; admin can edit |
| USER_BADGES / BADGE_PROGRESS | Firestore | userBadges/{uid}, `badges[]` array | Ionic app; admin can edit |
| BADGE_DEFINITION | Firestore | badgeDefinitions/{id} | Admin app |
| AUDIO_FILE | Firebase Storage | users/{uid}/speeches/{id}.ext, users/{uid}/speechHistory/{id}.ext | Ionic app |
| SPEECH_REFERENCE | FastAPI backend (CSV, in memory) | RAGBackEnd/speech_features_augmented.csv (Corpus 1) | Offline dataset |
| KNOWLEDGE_CHUNK | ChromaDB `corpus2` (in-memory) | built from 7 PDFs at startup (Corpus 2) | Backend ingest.py |

Dashed lines = logical link only (retrieved during RAG analysis, recorded in `feedback.rag_metadata`), not a stored foreign key.
Firestore is schemaless: PK = document id; FK = parent path or id field. BADGE_PROGRESS is embedded, not its own collection.
