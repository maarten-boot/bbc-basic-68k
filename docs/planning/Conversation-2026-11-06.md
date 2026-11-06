# Conversation log, 2026-11-06

Continues `Conversation-2026-11-04.md`.

## 10. Status

* **User:** "status?" planning/session-docs = origin = ae287f6 (pushed),
  tree clean; main still 6628baf (the branch is not merged, so CI has
  not run t19z80file). `git fetch` failed (no access from here); the
  remote state is as last fetched. Open: P5, P7, later P9, P10; P3 on
  hold, P4 parked.

## 11. Commit

* **User:** "commit". Committed this log.

## 12. Artifacts: one level less; releases on a tag

* **User:** "pushed; we currently build artifacts (the linux is a tar.gz
  inside a zip can we remove one level?; could we introduce a tag so
  that when we see a tag we publish a release so people can start
  playing with it?"
* Checked: upload-artifact v7.0.2 (the latest, cf430e0, the pinned one)
  has `archive: false` for a single file; download-artifact's latest is
  v8.0.2 (9000827, a commit).
* `.github/workflows/windows-exe.yml`: the Linux artifact is the
  `.tar.gz` itself (`archive: false`; the artifact takes the file's
  name). Runs also on a tag `v*`; the READMEs' version line is then the
  tag. New job `release` (needs build, only on a tag, the only job with
  `contents: write`; the workflow default is now read): downloads the
  release files and runs `gh release create TAG --verify-tag`, a
  pre-release for a tag with a `-`, with notes listing the files.
* `tools/ci-windows.sh`: also `bbc68k-rosco.zip` (a release asset).
  README: the releases page. Spec S6.2, new S6.4; Tests T20; Plan P11.
* Checked locally: the YAML parses, `sh -n`, a dry run of the release
  script (notes, --prerelease). Not run on GitHub yet. Not committed.

## 13. Commit

* **User:** "commit". Committed the workflow, ci-windows.sh, README and
  planning changes (P11). Next: merge to main, then a first tag
  (v0.1-beta suggested) for T20.
