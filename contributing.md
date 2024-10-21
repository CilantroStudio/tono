# Contributing

We will have issues labeled as
[Good First Issue](https://github.com/CilantroStudio/tono/labels/good%20first%20issue)
and
[Help Wanted](https://github.com/CilantroStudio/tono/labels/help%20wanted)
which are good opportunities for new contributors.

## Setup

[Rust](https://rustup.rs/) and [uv](https://docs.astral.sh/uv/) are requirements to build tono.

1. Clone the repository

```bash
git clone https://github.com/CilantroStudio/tono.git
```

2. Install the dependencies

```bash
uv sync --all-extras
```

3. Install the maturin-import-hook
    
```bash
 python -m maturin_import_hook site install
```