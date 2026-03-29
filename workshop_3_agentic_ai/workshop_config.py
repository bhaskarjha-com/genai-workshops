"""
🔧 Workshop 3 — Shared Backend Configuration
==============================================
Handles backend selection (Gemini / Ollama / Demo) for all modules.
Import this at the top of each module to get the selected backend.

Usage:
    from workshop_config import BACKEND, get_ollama_response, get_ollama_vision_response

    # BACKEND will be "gemini", "ollama", or "demo"
"""

import os
import sys
import json
import base64
import inspect
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for emoji/unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

# ─── Configuration ────────────────────────────────────────────
GEMINI_MODEL = "gemini-2.5-flash"
# MedGemma: medical vision + text (Modules 1, 2, 5, and the X-ray tool in M3)
OLLAMA_MODEL = os.environ.get(
    "OLLAMA_MODEL", "dcarrascosa/medgemma-1.5-4b-it:Q8_0"
)
# Qwen3: tool-calling orchestrator for the agentic loop in Module 3.
# MedGemma doesn't support Ollama's native tool calling; Qwen3 does.
OLLAMA_TOOL_MODEL = os.environ.get(
    "OLLAMA_TOOL_MODEL", "qwen3:8b"
)

# ─── Backend Detection ────────────────────────────────────────
def _check_gemini():
    """Check if Gemini API key is available."""
    return bool(os.environ.get("GEMINI_API_KEY", ""))


def _check_ollama():
    """Check if Ollama is running and our model is available."""
    try:
        import ollama as _ollama
        models = _ollama.list()
        model_names = [m.model for m in models.models]
        # Check exact match or prefix match
        target = OLLAMA_MODEL
        for name in model_names:
            if name == target or name.startswith(target.split(":")[0]):
                return True
        return False
    except Exception:
        return False


def select_backend():
    """
    Determine backend. Priority:
    1. WORKSHOP_BACKEND env var (if set explicitly)
    2. Interactive prompt (if running in a terminal)
    """
    env_backend = os.environ.get("WORKSHOP_BACKEND", "").lower().strip()

    if env_backend in ("gemini", "ollama", "demo"):
        # Validate the choice
        if env_backend == "gemini" and not _check_gemini():
            print("  ⚠️  WORKSHOP_BACKEND=gemini but no GEMINI_API_KEY — falling to demo")
            return "demo"
        if env_backend == "ollama" and not _check_ollama():
            print(f"  ⚠️  WORKSHOP_BACKEND=ollama but Ollama not available — falling to demo")
            print(f"      Expected model: {OLLAMA_MODEL}")
            return "demo"
        return env_backend

    # Auto-detect or interactive prompt
    has_gemini = _check_gemini()
    has_ollama = _check_ollama()

    if not sys.stdin.isatty():
        # Non-interactive: auto-detect
        if has_gemini:
            return "gemini"
        if has_ollama:
            return "ollama"
        return "demo"

    # Interactive prompt
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║        🤖 WORKSHOP 3 — Backend Selection            ║")
    print("╠══════════════════════════════════════════════════════╣")
    g_status = "✅ API key found" if has_gemini else "❌ No API key"
    o_status = f"✅ {OLLAMA_MODEL}" if has_ollama else "❌ Not available"
    print(f"║  [1] ☁️  Gemini 2.5 Flash   ({g_status})    ║")
    print(f"║  [2] 🖥️  Ollama Local GPU   ({o_status})  ║")
    print("║  [3] 📋 Demo Mode (pre-recorded — always works)    ║")
    print("╚══════════════════════════════════════════════════════╝")

    try:
        choice = input("  Select [1/2/3] (default=1): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "1"

    if choice == "2":
        if has_ollama:
            return "ollama"
        print("  ⚠️  Ollama not available — using demo mode")
        return "demo"
    elif choice == "3":
        return "demo"
    else:
        if has_gemini:
            return "gemini"
        print("  ⚠️  No GEMINI_API_KEY — using demo mode")
        return "demo"


# ─── Select on import ─────────────────────────────────────────
BACKEND = select_backend()

_backend_labels = {
    "gemini": "☁️  Gemini 2.5 Flash (Cloud API)",
    "ollama": f"🖥️  Ollama Local (medgemma-1.5 + qwen3)",
    "demo": "📋 Demo Mode (pre-recorded output)",
}
print(f"  → Backend: {_backend_labels.get(BACKEND, BACKEND)}")
if BACKEND == "ollama":
    print(f"    Vision/Text: {OLLAMA_MODEL}")
    print(f"    Tool Calling: {OLLAMA_TOOL_MODEL}")
print()


# ─── Ollama Helper Functions ──────────────────────────────────
def get_ollama_response(prompt, system=""):
    """Generate text using Ollama. Returns the response text."""
    import ollama
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
    return response["message"]["content"]


def get_ollama_vision_response(prompt, image_path_or_bytes, system=""):
    """Generate text from image + text using Ollama (multimodal MedGemma)."""
    import ollama
    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    # Handle image: can be a file path or raw bytes
    # NOTE: The Ollama Python library handles base64 encoding internally.
    #       Pass raw bytes directly — do NOT pre-encode to base64.
    if isinstance(image_path_or_bytes, (str, Path)):
        # Read file to bytes — more reliable than passing path strings
        with open(str(image_path_or_bytes), "rb") as f:
            images = [f.read()]
    elif isinstance(image_path_or_bytes, bytes):
        images = [image_path_or_bytes]
    else:
        images = []

    messages.append({"role": "user", "content": prompt, "images": images})
    response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
    return response["message"]["content"]


def run_ollama_agent(scenario, system_instruction, tools_schema, tool_functions,
                     max_iterations=10, print_steps=True):
    """
    Run an agentic tool-calling loop with Ollama.

    Unlike Gemini's automatic_function_calling, Ollama requires manual orchestration:
    1. Send prompt + tool schemas → model returns tool_calls
    2. Execute matching Python function
    3. Feed result back as 'tool' message
    4. Repeat until model returns plain text (no more tool_calls)

    Args:
        scenario: The user prompt/scenario
        system_instruction: System prompt for the agent
        tools_schema: List of Ollama-format tool definitions
        tool_functions: Dict mapping function names to callables
        max_iterations: Safety limit for the loop
        print_steps: Whether to print each step as it happens

    Returns:
        The agent's final text response, or None if failed
    """
    import ollama

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": scenario},
    ]

    step = 0
    for _ in range(max_iterations):
        response = ollama.chat(
            model=OLLAMA_TOOL_MODEL,
            messages=messages,
            tools=tools_schema,
            options={"temperature": 0.2},  # low temp for reliable tool calls
        )

        msg = response["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            # No more tool calls — agent is done
            content = msg.get("content", "")
            # Qwen3 may include <think>...</think> reasoning — strip it
            import re
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
            return content

        # Process each tool call
        for tc in tool_calls:
            step += 1
            func_name = tc["function"]["name"]
            func_args = tc["function"]["arguments"]

            if print_steps:
                args_str = ", ".join(f'{k}="{v}"' for k, v in func_args.items())
                print(f"\n  🤖 Step {step} — Agent calls: {func_name}({args_str})")

            if func_name in tool_functions:
                try:
                    result = tool_functions[func_name](**func_args)
                except Exception as e:
                    result = {"error": str(e)}
            else:
                result = {"error": f"Unknown tool: {func_name}"}

            result_str = json.dumps(result) if isinstance(result, dict) else str(result)

            if print_steps:
                # Show truncated result
                display = result_str[:200] + ("..." if len(result_str) > 200 else "")
                print(f"  📋 Tool returned: {display}")

            messages.append({
                "role": "tool",
                "content": result_str,
            })

    return "Agent reached maximum iterations without completing."


def build_ollama_tool_schema(func):
    """
    Convert a Python function to Ollama-compatible tool schema
    by inspecting its signature and docstring.
    """
    sig = inspect.signature(func)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        ptype = "string"  # default
        if param.annotation == int:
            ptype = "integer"
        elif param.annotation == float:
            ptype = "number"
        elif param.annotation == bool:
            ptype = "boolean"

        properties[name] = {
            "type": ptype,
            "description": f"Parameter: {name}",
        }
        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip().split("\n")[0],
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }
