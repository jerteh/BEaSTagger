# Windows tagging compatibility

The previous dependency metadata contains an invalid `requests~>` requirement, and the two requirement lists disagree. This change provides a tested editable-install path on CPython 3.11 and fixes tagging state/output handling needed for repeatable local inference.

## Changes

- Replace the invalid requests specifier, remove the deprecated `sklearn` package alias, and align dependency metadata around the tested NumPy 1.26 / pandas 2.2 / spaCy 3.7 / PyTorch 2.6 runtime. Declare Click explicitly because spaCy imports it.
- Keep Stanza optional and import that backend only when selected. No Stanza models are needed for the released Serbian ensemble.
- Copy optional model/lemmatizer collections per call, avoiding shared mutable defaults and changes to caller collections. Propagate batch failures with the failing source path.
- Join lexicon and TreeTagger executable paths with `os.path.join`.
- Create the requested output directory, write `answers.json` there, and refuse an existing final output before processing. Append behavior remains available for chunks produced by the same invocation.
- Load the stacked classifier state dictionary with `weights_only=True`.

## Tested environment

CPython 3.11.15 on Windows; spaCy 3.7.5, PyTorch 2.6.0+cpu, NumPy 1.26.4, pandas 2.2.3, scikit-learn 1.6.1, requests 2.32.5, Typer 0.27.3 and Click 8.1.8. The complete installed wheel versions are pinned in `requirements-windows-eval.lock.txt`.

```powershell
.\scripts\install-windows-eval.ps1
.\.venv\Scripts\python.exe scripts\test_compat.py
```

The install script uses a project-local `.venv` and `.uv-cache`. It installs the CPU PyTorch wheel from its official index first, then the locked PyPI wheel dependencies, and finally this checkout as an editable package. This avoids uv selecting incomplete dependency versions from the PyTorch index. No global Python/package changes are needed.

The three focused regression tests cover independent call defaults, stale-output refusal, and executable paths without a trailing separator. `uv pip check` and source compilation pass.

## Synthetic inference smoke test

The public [Serbian release](https://github.com/jerteh/BEaSTagger/releases/tag/Serbian) archive was tested locally without modifying its weights. The asset is `beast_serbian.zip`, 30,432,350 bytes, SHA-256 `c4af65f7ae4620e25c750e22c466da43f8981d36512241f3442a4a9549b3847a`. The archive passed its CRC test. Model files and the archive are not included in this change.

After extracting that archive to `artifacts/serbian`, run the synthetic two-sentence / eight-token check in a fresh output directory:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_beast.py --output runs\smoke-new
```

The check uses `UD.pt`, pretokenized input, lemmatization enabled, and disables tokenization, transliteration and lexicon-magic changes. It asserts exact input/output token count, order, forms, and the POS/lemma column count. It tests execution and alignment, not model accuracy.

The `UD.pt` feature list uses `Spacy_ud`, `Spacy_ud_right`, `TreeTagger_ud.par`, and `TreeTagger_ud_right.par`. The spaCy components have metadata `lang=sr`, `name=pipeline`, `version=0.0.0`, pipeline `tok2vec,tagger`, and declare spaCy `>=3.0.7,<3.1.0`. Their configurations use MultiHashEmbed and MaxoutWindowEncoder (width 96, depth 4). Loading and inference succeeded with spaCy 3.7.5; equivalence with the historical runtime is not established. The training corpus is not identified by their metadata.

## Scope and limitations

Only editable local installation, the focused tests and the released Serbian tagging path were validated. Training, Stanza execution, Linux/macOS, building distributable wheels, and other model/runtime combinations remain untested. The newer dependency floors narrow historical compatibility and should be reviewed by the maintainer before adoption. Existing temporary filenames still require separate output directories for concurrent jobs. The bundled TreeTagger code has its own license; this change adds or redistributes no executable binaries, lexicons or model weights.

No corpus content, corpus predictions, corpus metrics or private examples are part of this change.
