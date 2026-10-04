# ShipPDF for Claude

Create reusable PDF templates, revise their layouts and data fields, and generate
PDFs through ShipPDF's hosted MCP server. This plugin uses the shared Claude
plugin format for Claude Code and Claude Cowork.

## Connect

Enable the plugin, then authenticate the ShipPDF connection in Claude's MCP or
connector controls. Sign in to ShipPDF and choose the workspace you want Claude
to access. In Claude Code, run `/mcp` and select the ShipPDF server to authenticate.
The plugin connects to `https://mcp.shippdf.com/` over HTTP with OAuth; it contains
no API keys and requires no local server or package installation.

Tools are limited to the selected workspace and granted scopes:

| Workflow | Scopes |
| --- | --- |
| Discover projects and published templates | `projects:read`, `templates:read` |
| Create, edit, preview, or publish templates | `templates:write` |
| Generate PDFs and retrieve results | `documents:create`, `documents:read` |

## Workflows

Ask naturally, or invoke a skill directly in Claude Code:

| Skill | Example |
| --- | --- |
| `/shippdf:create-template` | Create an A4 invoice template with line items, a logo, and a calculated total. |
| `/shippdf:edit-template` | Update template tmpl_… to use our new branding and leave it as a draft. |
| `/shippdf:generate-document` | Generate a PDF using template tmpl_… and this invoice data. |

Skills follow the server's current authoring guide and JSON schemas. Drafts are
validated before publishing, edits preserve concurrent changes through optimistic
locking, and generation retries reuse an idempotency key. A generation costs one
credit. Browser draft previews cost no credits and do not verify PDF pagination.

The current MCP tools support discovery, template authoring, public-URL image
import, publishing, individual generation, and generation status. Local asset
upload, batch generation, and webhook setup are not exposed by this plugin.

## Claude Code installation

From the plugin repository root, test without installing:

```sh
claude --plugin-dir .
```

For a persistent installation, run these commands inside Claude Code from the
repository root:

```text
/plugin marketplace add .
/plugin install shippdf@shippdf
```

Restart the session after installing, then use `/mcp` to authenticate. The
marketplace is local to this repository; these commands do not publish a plugin
to Anthropic's directory.

## Claude Cowork installation

Build an upload archive from the repository root:

```sh
python3 scripts/package_claude_plugin.py
```

Upload the resulting `dist/shippdf-claude-plugin-0.1.0.zip` through Claude's
Customize plugin upload flow. Organization administrators can instead use
Organization settings → Plugins & skills → Add → Upload a plugin. Enable the
plugin and authenticate its ShipPDF connection in Claude's connector controls.
Availability of uploads and connectors depends on your Claude account settings.

## Validation and release

From the repository root:

```sh
claude plugin validate --strict .claude-plugin/plugin.json
claude plugin validate --strict .claude-plugin/marketplace.json
claude plugin validate --strict skills
python3 scripts/package_claude_plugin.py
```

The archive includes only the manifest, README, and skill files, with the manifest
at `.claude-plugin/plugin.json` in the archive root. Bump the plugin manifest
version before distributing an update. Test authentication, template creation,
draft editing, publishing, and one authorized generation in a test workspace
before public distribution. Manifest validation does not test the hosted service
or complete OAuth sign-in.

References: [Claude plugin format](https://code.claude.com/docs/en/plugins-reference),
[MCP connections](https://code.claude.com/docs/en/mcp), and
[plugin uploads](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization).
