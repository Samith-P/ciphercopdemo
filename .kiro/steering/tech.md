---
inclusion: always
---

# Technology Stack & Development Guidelines

## Required Technology Stack

- **Python 3.8+** with type hints - all functions must include type annotations
- **PyTorch + torchvision** - GPU-enabled versions required for model inference
- **Detectron2** - Facebook's object detection library (NEVER modify detectron2/ directory)
- **OpenCV** - use cv2 for all image processing operations
- **Pixi** - exclusive package manager (NEVER use pip directly)

## Critical Dependencies

- **numpy==1.23.0** - pinned version, do not upgrade (compatibility constraint)
- **opencv-python + opencv-contrib-python** - both packages required
- **Pillow** - image format handling and conversion
- **Flask** - web interface backend (WEBtool/ directory)

## Package Management (STRICT)

```bash
# ONLY use these commands for dependencies:
pixi add <package>          # Add new dependency
pixi install               # Install environment
pixi run <command>         # Execute any Python command

# FORBIDDEN: pip install, conda install, etc.
```

## Required Code Patterns

```python
# 1. Type annotations (MANDATORY)
from pathlib import Path
from typing import Dict, List, Optional, Any

def process_image(image_path: Path, config: Dict[str, Any]) -> Optional[Dict[str, float]]:
    pass

# 2. Path handling (MANDATORY)
from pathlib import Path
model_path = Path("models") / "rcnn_bet365.pth"  # Not string concatenation

# 3. GPU detection (MANDATORY)
import torch
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# 4. Logging (MANDATORY - no print statements)
import logging
logger = logging.getLogger(__name__)
logger.info("Processing started")  # Not print()

# 5. Error handling (MANDATORY)
try:
    model = load_model(model_path)
except FileNotFoundError:
    logger.error(f"Model not found: {model_path}")
    raise ConfigurationError("Run setup.sh/setup.bat first")
```

## Development Workflow

```bash
# Initial setup
pixi install
pixi run python test_imports.py

# Main operations
pixi run python phishpedia.py --folder <test_folder>
pixi run python create_real_tests.py

# Platform-specific model download
./setup.sh      # Linux/macOS
setup.bat       # Windows
```

## Architecture Constraints

- **Two-stage pipeline**: Detectron2 (Stage 1) → Siamese network (Stage 2)
- **Configuration-driven**: All paths and thresholds in configs.yaml (never hardcode)
- **GPU-first design**: Always check CUDA availability, prefer GPU operations
- **Cross-platform**: Code must work on Windows, Linux, and macOS