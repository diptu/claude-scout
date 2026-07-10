---
name: media-library-organizer
description: Guides Claude through organizing a personal self-hosted media collection (scanning files, deduplicating, tagging, and building a browsable metadata index), modeled on self-hosted library managers like Stash; use when a user wants to catalog, tag, and deduplicate a folder of video/image files into a searchable local library.
---

# Media Library Organizer

This skill helps Claude act as a self-hosted media library organizer: scanning
a folder tree of video or image files, extracting/attaching metadata, tagging
and deduplicating content, and producing a structured, searchable index —
the same pattern used by self-hosted library managers (e.g. Stash) for
personal media collections.

## When to apply this skill

Apply this skill when a user asks to:

- Organize a large, messy folder of video/image files into a structured library
- Deduplicate files that represent the same content under different names
- Build or update a metadata index (tags, performers/people, titles, dates, source) for a personal media collection
- Design a schema or folder convention for a self-hosted media catalog
- Write a scraper/import script that pulls metadata for local files from a filename pattern or a sidecar file
- Generate a static or lightweight browsable index (HTML page, JSON, or SQLite/CSV) for personal media

Do not apply this skill to public content moderation, generating or describing
explicit content, or any task beyond organizing metadata for files that
already exist on the user's own system. The scope here is strictly file
organization and metadata engineering — not content generation or content
description.

## Step-by-step guidance

1. **Inventory the source tree.**
   - Walk the target directory recursively, listing every media file with its
     extension, size, and modification time.
   - Group files by extension/type (video vs. image) since metadata handling
     differs per type.

2. **Establish a metadata schema before writing any code.**
   - Minimum useful fields: `id`, `path`, `title`, `tags[]`, `people[]` (or
     any user-defined entity list), `date`, `source`, `duration`/`resolution`
     (for video), `checksum`.
   - Keep the schema in one flat file (JSON or CSV/SQLite for larger sets) —
     don't stand up a database for a few hundred files.

3. **Deduplicate before tagging.**
   - Compute a content hash (e.g. file hash, or a perceptual/partial hash for
     videos/images that may be re-encoded copies) for each file.
   - Group files by hash; within a group, keep the highest-resolution/largest
     file and record the others as duplicates rather than deleting
     automatically — always let the user confirm deletions.

4. **Extract or infer metadata.**
   - Parse structured hints from the filename, folder name, or any sidecar
     `.nfo`/`.json` file sitting next to the media file.
   - If the user has an existing tagging convention (folder-per-tag,
     filename delimiters, etc.), infer tags from that convention rather than
     inventing a new one.
   - Flag files with no extractable metadata for manual tagging instead of
     guessing.

5. **Apply tags and relationships consistently.**
   - Normalize tag names (case, singular/plural, synonyms) against a single
     controlled tag list so the same concept isn't tagged three different
     ways across the library.
   - Record many-to-many relationships (a file can have multiple tags/people)
     in the flat schema rather than duplicating file entries per tag.

6. **Generate a browsable index.**
   - Produce a single JSON or CSV index file as the source of truth.
   - Optionally render a static HTML page (or a small local script) that
     lists/filters entries by tag, person, or date, reading from that index —
     no server or database required for a personal library.

7. **Make re-runs incremental.**
   - On subsequent runs, only process files not already present in the index
     (match by path + checksum), and only re-tag files whose checksum
     changed. Never silently overwrite user-edited metadata fields — only
     fill in fields that are still empty.

8. **Confirm before destructive actions.**
   - Never delete, move, or rename files automatically as part of
     organizing. Report proposed duplicate removals or file moves and wait
     for explicit user confirmation before executing them.
