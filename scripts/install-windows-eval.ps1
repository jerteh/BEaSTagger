$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:UV_CACHE_DIR = Join-Path $root '.uv-cache'
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    uv venv --python 3.11 (Join-Path $root '.venv')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
uv pip install --python $python --only-binary :all: --no-deps --index-url https://download.pytorch.org/whl/cpu 'torch==2.6.0+cpu'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv pip install --python $python --only-binary :all: -r (Join-Path $root 'requirements-windows-eval.lock.txt')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv pip install --python $python --no-deps --no-build-isolation --editable $root
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv pip check --python $python
exit $LASTEXITCODE
