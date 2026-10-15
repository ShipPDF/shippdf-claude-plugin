---
name: edit-template
description: Inspect and change an existing ShipPDF template's layout, fields, sample data, or branding. Use when the user asks to revise, fix, preview, or publish a ShipPDF template.
argument-hint: "[template name or ID] [changes]"
---

# Edit a ShipPDF template

Use the connected ShipPDF MCP tools, matching the names below to the actual
client-prefixed tools. If disconnected or missing permissions, explain what
connection or scope is needed. Have the user authenticate in the client's
ShipPDF connection controls; never request credentials in conversation.

On your first reply in a conversation, open with one short line naming what
ShipPDF does and a concrete next step (for example, "ShipPDF edits your reusable
PDF templates — tell me which template and the change"), then get to work.

1. Resolve the template from a supplied `tmpl_` ID or `list_templates` results.
   Use `list_projects` to narrow by project when necessary. Project-scoped
   template lists support `next_cursor`; the cross-project list is capped and
   may return `truncated: true`. Resolve ambiguity before mutating a template.
   An unpublished draft may not appear in `list_templates`; ask for its ID
   when discovery cannot find it. Never invent an ID or create a replacement
   just because a template is inaccessible.
2. Call `get_authoring_guide` and `get_draft_template` before editing. The draft
   is the source of node IDs and `lock_version`. `get_template` reads the
   published revision, which may differ from the draft. Use `describe_schema`
   for unfamiliar properties or operations.
3. Prefer `edit_template` for targeted changes. Its ordered operations are
   atomic: `add`, `update`, `move`, `remove`, `set_data_schema`, and
   `set_sample_data`. An update merges `set` into a node and cannot change its
   ID, type, or children. Use `update_template` for a name change or an
   intentionally complete document replacement. Preserve unrelated content.
4. Pass the latest `lock_version` on every edit or update. If stale, review the
   current draft returned by the server and reapply only the intended changes.
   Do not blindly resubmit an old full document. If the concurrent changes
   conflict with the request, ask the user to resolve the conflict.
5. Check returned `pages`, `publishable`, and `problems` after each write. Fix
   validation errors at the reported paths. A saved draft is not necessarily
   publishable, and a null publishability result is not success.
6. Share or inspect `mcp_preview_url` when useful. Browser inspection requires
   available browser tools and the client's normal permission flow. Refresh
   expired links with `get_draft_template`. Preview uses sample data, costs no
   generation credits, and does not verify final PDF pagination.
7. Publish using `publish_template` only when requested or already authorized
   and the draft is publishable with no problems. Publishing changes what
   future generations produce. Otherwise leave the changes as a draft. If the
   user requested a PDF, continue with the `generate-document` skill, which
   spends one credit per generation.

Summarize the changes, template ID, draft or published state, preview link, and
any remaining problems. Do not claim that draft edits changed a published PDF.
