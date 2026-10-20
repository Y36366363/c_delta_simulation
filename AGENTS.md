# Private author materials and Git publication

- Keep emails to or from supervisors, working-paper drafts, and related private
  author materials local only. Put new materials under `private/` (ignored), or
  in an author-artifact directory outside this repository.
- Preserve existing local private files. Do not upload them, force-add ignored
  files, or rewrite Git history unless the user explicitly authorizes it.
- Before every commit, inspect the staged file list AND staged content for
  correspondence, manuscript text, private feedback, and attachments. Check new
  filenames against `.gitignore`; do not assume filename rules catch everything.
- Before every push, review all outgoing commits for private material, including
  files added and then deleted within those commits. A clean final tree alone is
  insufficient. If private material is found, stop publication and explain it.
- Keep research code and simulation results intact when excluding private files.
  Use `git rm --cached` rather than deleting local files when untracking is needed.
- Current user preference: leave existing remote history unchanged. This policy
  applies to future work and does not authorize a historical purge or force push.
