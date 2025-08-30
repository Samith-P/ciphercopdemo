---
inclusion: always
---

# Project Structure & File Organization

## Directory Layout (IMMUTABLE)

```
Phishpedia/                 # Working directory - all operations here
├── models/                 # Model weights and brand database
├── datasets/              # Test data (standardized structure)
├── WEBtool/               # Flask web interface
└── detectron2/            # External dependency (NEVER MODIFY)
```

## Core Modules (by Function)

- **phishpedia.py** - CLI entry point, batch processing
- **configs.py** - Model initialization (modify for new models)
- **logo_recog.py** - Stage 1: Detectron2 logo detection
- **logo_matching.py** - Stage 2: Siamese network brand matching
- **utils.py** - Shared utilities (image processing, file I/O)
- **models.py** - Neural network architectures

## Required Files (Must Exist)

### Model Files
```
models/
├── rcnn_bet365.pth              # Faster R-CNN weights (Stage 1)
├── resnetv2_rgb_new.pth.tar     # Siamese network weights (Stage 2)
├── domain_map.pkl               # URL-to-brand mapping
└── expand_targetlist/           # Exactly 277 brand folders
    ├── brand1/
    ├── brand2/
    └── ...
```

### Configuration Files
```
├── configs.yaml          # Primary config (paths, thresholds)
├── pixi.toml            # Dependencies and environment
└── faster_rcnn.yaml     # Detectron2 model configuration
```

### Cache Files (Auto-generated)
```
├── LOGO_FEATS.npy       # Cached brand features
└── LOGO_FILES.npy       # Cached file paths
```

## Input Data Format (STRICT)

Every test case must follow this structure:
```
test_folder/
├── info.txt     # Single line containing target URL
└── shot.png     # Screenshot in PNG format only
```

## Path Handling Rules

```python
# ALWAYS use pathlib.Path
from pathlib import Path

# Model paths (relative to Phishpedia/)
model_dir = Path("models")
rcnn_path = model_dir / "rcnn_bet365.pth"

# Brand logos (relative to models/expand_targetlist/)
brand_dir = Path("models/expand_targetlist") / brand_name

# Config loading
config_path = Path("configs.yaml")
```

## File Validation (MANDATORY)

Before any operation, validate:
```python
# Model files exist
assert Path("models/rcnn_bet365.pth").exists(), "Missing Stage 1 model"
assert Path("models/resnetv2_rgb_new.pth.tar").exists(), "Missing Stage 2 model"

# Input format correct
assert Path(test_folder / "info.txt").exists(), "Missing info.txt"
assert Path(test_folder / "shot.png").exists(), "Missing shot.png"

# Brand database integrity
brand_folders = list(Path("models/expand_targetlist").iterdir())
assert len(brand_folders) == 277, f"Expected 277 brands, found {len(brand_folders)}"
```