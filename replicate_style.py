"""
Replicate AI styling for map posters.

Post-processes a generated poster through a Replicate image model
(e.g. dream.district fine-tuned on Midjourney designs).
"""

import time
from pathlib import Path

REPLICATE_RATE_LIMIT_WAIT = 15  # seconds before first try (burst limit)
REPLICATE_RETRY_WAIT = 20       # seconds between 429 retries


def style_with_replicate(
    image_path: str,
    model_id: str = "pxdogbo/dream.district:snedjsxd2xrmr0cwb3hag5kkxw",
    prompt: str | None = None,
    output_suffix: str = "_styled",
) -> str | None:
    """
    Run a Replicate image model on the poster and save the styled output.

    For img2img models: passes the poster as input image.
    For text2img models: uses prompt only (image_path ignored).

    Requires REPLICATE_API_TOKEN in environment.
    Install: pip install replicate

    Args:
        image_path: Path to the poster PNG
        model_id: Replicate model (owner/name), default pxdogbo/dream.district
        prompt: Optional prompt for the model (default describes map poster)
        output_suffix: Suffix for output filename before extension

    Returns:
        Path to the styled output file, or None on failure
    """
    try:
        import replicate
    except ImportError:
        print("⚠ Replicate not installed. Run: pip install replicate")
        return None

    if not Path(image_path).exists():
        print(f"⚠ Image not found: {image_path}")
        return None

    default_prompt = "minimalist map poster, city street network, artistic design, high quality"
    prompt = prompt or default_prompt

    print(f"Styling with Replicate ({model_id})...")
    print(f"  Prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")

    # Rate limit: free tier has burst of 1, so wait before first request
    print(f"  Waiting {REPLICATE_RATE_LIMIT_WAIT}s for rate limit...")
    time.sleep(REPLICATE_RATE_LIMIT_WAIT)

    model_input = {"prompt": prompt, "image": Path(image_path)}
    output = None
    last_error = None
    max_retries = 3

    for attempt in range(2):  # First img2img, then prompt-only fallback
        for retry in range(max_retries):
            try:
                output = replicate.run(model_id, input=model_input)
                break
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                if retry < max_retries - 1 and ("429" in err_str or "throttl" in err_str):
                    print(f"  Rate limited. Waiting {REPLICATE_RETRY_WAIT}s before retry ({retry + 1}/{max_retries})...")
                    time.sleep(REPLICATE_RETRY_WAIT)
                    continue
                if attempt == 0 and ("image" in err_str or "unexpected" in err_str or "invalid" in err_str):
                    print("  Trying prompt-only (model may be text-to-image)...")
                    model_input = {"prompt": prompt}
                    break
                print(f"✗ Replicate error: {e}")
                return None
        if output is not None:
            break

    if output is None and last_error:
        print(f"✗ Replicate error: {last_error}")
        return None

    # Handle output - can be FileOutput, list of FileOutput, or URL string
    out_file = _extract_output_file(output)
    if out_file is None:
        print("✗ Model returned no output")
        return None
    # Save to disk
    p = Path(image_path)
    out_path = p.parent / f"{p.stem}{output_suffix}{p.suffix}"

    with open(out_path, "wb") as f:
        if hasattr(out_file, "read"):
            f.write(out_file.read())
        elif hasattr(out_file, "url"):
            import urllib.request
            with urllib.request.urlopen(out_file.url) as resp:
                f.write(resp.read())
        elif isinstance(out_file, str) and out_file.startswith("http"):
            import urllib.request
            with urllib.request.urlopen(out_file) as resp:
                f.write(resp.read())
        else:
            print("✗ Unexpected output format")
            return None

    print(f"✓ Styled poster saved: {out_path.name}")
    return str(out_path)


def print_model_schema(model_id: str = "pxdogbo/dream.district:snedjsxd2xrmr0cwb3hag5kkxw") -> None:
    """Print the model's input schema (helpful to see param names)."""
    try:
        import replicate
    except ImportError:
        print("Install replicate: pip install replicate")
        return
    try:
        model = replicate.models.get(model_id)
        if model.latest_version:
            schema = model.latest_version.openapi_schema
            props = schema.get("components", {}).get("schemas", {}).get("Input", {}).get("properties", {})
            print(f"Model: {model_id}")
            print("Input parameters:")
            for name, details in props.items():
                t = details.get("type", details.get("title", "?"))
                d = details.get("description", "")
                print(f"  {name}: {t} - {d}")
        else:
            print(f"No version found for {model_id}")
    except Exception as e:
        print(f"Error: {e}")
        print("  Is the model private? Set REPLICATE_API_TOKEN.")


def _extract_output_file(output) -> "object | None":
    """Extract first image file from Replicate output."""
    if output is None:
        return None
    # Single FileOutput
    if hasattr(output, "read") or hasattr(output, "url"):
        return output
    # List of outputs (e.g. multiple images)
    if isinstance(output, (list, tuple)) and output:
        return output[0]
    # URL string
    if isinstance(output, str):
        return output
    return None
