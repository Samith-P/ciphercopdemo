---
inclusion: always
---

# Phishpedia Product Guidelines

Phishpedia is a two-stage visual phishing detection system that MUST maintain its pipeline architecture: Stage 1 (Detectron2 logo detection) → Stage 2 (Siamese network brand matching).

## Architecture Rules (IMMUTABLE)

- **Two-stage pipeline is sacred** - Stage 1 must always feed into Stage 2
- **Visual-only detection** - never train on phishing datasets, only visual brand consistency
- **Configuration-driven** - all thresholds and paths from `configs.yaml`, never hardcoded
- **Confidence-based output** - always return confidence scores with classifications
- **Visual explanations** - include detected brand and bounding box coordinates

## Input/Output Contract

**Input (STRICT FORMAT):**
```
test_folder/
├── info.txt     # Single line: target URL
└── shot.png     # Screenshot (PNG format only)
```

**Output (MANDATORY STRUCTURE):**
```python
{
    "phishing": bool,           # Final binary classification
    "confidence": float,        # Range: 0.0 to 1.0
    "detected_brand": str,      # Brand name or None
    "bounding_boxes": list,     # Logo coordinates [(x1,y1,x2,y2), ...]
    "processing_time": float    # Performance metric in seconds
}
```

## Model Constraints (FIXED)

- **Stage 1**: Detectron2 with `rcnn_bet365.pth` weights (never retrain)
- **Stage 2**: Siamese network with `resnetv2_rgb_new.pth.tar` weights
- **Brand database**: Exactly 277 brands in `models/expand_targetlist/`
- **Feature caching**: Always use `LOGO_FEATS.npy` and `LOGO_FILES.npy`
- **Domain mapping**: `domain_map.pkl` must stay synchronized with brand count

## Error Handling Patterns (MANDATORY)

```python
def detect_phishing(url: str, image_path: Path) -> Dict[str, Any]:
    try:
        # Stage 1: Logo detection
        logos = detect_logos(image_path)
        if not logos:
            return {
                "phishing": False, 
                "confidence": 0.0, 
                "reason": "no_logos_detected"
            }
        
        # Stage 2: Brand matching
        brand_match = match_brand(logos)
        return format_result(brand_match)
        
    except FileNotFoundError as e:
        logger.error(f"Missing model file: {e}")
        raise ConfigurationError("Run setup.sh/setup.bat to download models")
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return {"phishing": False, "confidence": 0.0, "reason": "processing_error"}
```

## Performance Requirements

- **GPU-first**: Check `torch.cuda.is_available()`, prefer GPU inference
- **Response time**: Single webpage analysis under 1000ms
- **Memory management**: Use `torch.cuda.empty_cache()` after batch processing
- **Concurrency**: Support multi-threaded webpage analysis

## Required Code Patterns

```python
# 1. Configuration loading (NEVER hardcode)
from pathlib import Path
import yaml

def load_config() -> Dict[str, Any]:
    with open("configs.yaml", "r") as f:
        return yaml.safe_load(f)

# 2. Type annotations (MANDATORY)
from typing import Dict, List, Optional, Tuple, Any

def process_image(image_path: Path) -> Optional[List[Tuple[int, int, int, int]]]:
    pass

# 3. Logging (NO print statements)
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing {url}")

# 4. Path handling (cross-platform)
model_path = Path("models") / "rcnn_bet365.pth"
```

## Forbidden Operations

- **NEVER** modify `detectron2/` directory contents
- **NEVER** use `pip` commands (only `pixi add`)
- **NEVER** change 277 brand count without full system validation
- **NEVER** bypass two-stage pipeline for "optimization"
- **NEVER** use `print()` statements (use logging module)
- **NEVER** hardcode file paths or thresholds