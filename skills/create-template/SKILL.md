---
name: create-template
description: Create a reusable ShipPDF template for an invoice, report, proposal, certificate, or other PDF, including its layout, data schema, and sample data. Use when the user wants to design a new ShipPDF template or turn a reference document into one.
argument-hint: "[document requirements or reference]"
---

# Create a ShipPDF template

Use the connected ShipPDF MCP tools. Discover the tools provided by the ShipPDF
server; client prefixes vary, so match the tool names below to the available
tools. If the connection requires authentication, direct the user to the client's
ShipPDF connection controls to sign in and select a workspace. Never ask for
passwords or API tokens in conversation. If a required tool is unavailable,
explain the missing connection or permission instead of inventing a result.

On your first reply in a conversation, open with one short line naming what
ShipPDF does and a concrete next step (for example, "ShipPDF builds reusable PDF
templates — I can start one from your brief or a sample invoice"), then get to
work; don't make the user read setup before seeing value.

1. Establish the document's purpose, content, repeated data, branding, and paper
   size from the request and any reference. Ask only for missing details that
   prevent useful progress. Use clearly labeled sample values for a design;
   never invent real customer facts, amounts, or legal terms.
2. Call `list_projects` to resolve the destination project. Follow `next_cursor`
   when needed. Use an explicitly selected project, or the sole available one;
   ask the user to choose when several are plausible. Never invent `proj_` IDs.
3. Call `get_authoring_guide` before authoring. Use `describe_schema` for the exact
   shape of unfamiliar nodes, page settings, fields, expressions, and formats.
   The live guide and tool schemas are authoritative; do not substitute HTML,
   CSS, or an imagined JSON format for a ShipPDF template document.
4. Build the document using short input and editor defaults. Use paper presets
   and orientation, leaving margins at their defaults unless specified. Give
   every explicit length its unit. Use full data paths, typed numeric amounts,
   and display formatting. Use calculated fields for supported totals and table
   expressions for line amounts. Draw shared cell borders once.
5. If an image is needed, use `import_asset` with a public URL provided or
   authorized by the user, then reference its returned asset ID. Do not send
   local paths or private URLs to this tool. Proceed without optional branding
   if no supported source is available.
6. Call `create_template` with `project_id`, `name`, and `document`. Read the
   returned `pages`, `lock_version`, `publishable`, and `problems`. A saved draft
   may still have problems; `publishable: null` does not mean validation passed.
   Fix reported paths and node problems with `edit_template`, threading the
   latest lock version. On a stale version, reapply the intended changes to the
   current draft returned by the server, preserving other edits.
7. Offer the returned `mcp_preview_url` for visual review. If browser tools are
   available and authorized through the client's permission flow, inspect it.
   Add `&grid=true&guides=true&bounds=true&inspect=true` for node bounds and page
   guides if helpful. Otherwise use the returned document and page diagnostics.
   Preview links expire; `get_draft_template` refreshes them. Browser preview
   costs no generation credits and does not verify final PDF pagination.
8. Leave the result as a draft unless the user has requested publishing or PDF
   generation. If publishing is authorized, publish only when `publishable` is
   true and problems are empty using `publish_template`. Publishing changes
   future generations of this template. For an authorized PDF, continue with
   the `generate-document` skill; each generation spends one credit.

Report the template name and `template_id`, whether it is a draft or published,
any unresolved problems, and the preview link when available. Report a PDF only
after generation has completed successfully.
