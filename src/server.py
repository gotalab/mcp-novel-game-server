from collections import defaultdict
from datetime import datetime, timezone
import glob
import pathlib
import yaml
import os

from fastmcp import FastMCP, Image
from PIL import Image as PILImage
import io

ROOT = pathlib.Path(__file__).parent
NOVEL_DIR = ROOT / "stories"  # src/stories/<STORY_ID>/<scene_id>.yaml


mcp = FastMCP("NovelGame-MCP-Server")

# ---------------------------------------------------------------------------
# 1) Load all stories (YAML → in‑mem)
# ---------------------------------------------------------------------------
META: dict[str, dict] = {}
SCENES: dict[str, dict[str, dict]] = defaultdict(dict)
IMAGES: dict[str, dict[str, str]] = {}
STATE: dict[str, dict] = {}

# 全てのストーリーディレクトリを確認
story_dirs = [p for p in NOVEL_DIR.glob("*") if p.is_dir()]
# print(f"[DEBUG] ROOT={ROOT}, NOVEL_DIR={NOVEL_DIR}, story_dirs={[str(p) for p in story_dirs]}")
for story_dir in story_dirs:
    story_id = story_dir.name
    
    # メタデータの読み込み
    meta_path = os.path.join(str(story_dir), "meta.yaml")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                META[story_id] = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading meta file for {story_id}: {e}")
            META[story_id] = {"title": story_id}  # 最低限のメタデータ
    else:
        print(f"Warning: No meta.yaml found for {story_id}")
        META[story_id] = {"title": story_id}  # メタファイルがない場合のフォールバック
    
    # シーンの読み込み
    for scene_file in story_dir.glob("*.yaml"):
        if scene_file.name == "meta.yaml":
            continue
        try:
            with open(scene_file, "r", encoding="utf-8") as f:
                doc = yaml.safe_load(f)
            scene_id = doc.pop("id", scene_file.stem)  # ファイル名をフォールバックとして使用
            SCENES.setdefault(story_id, {})[scene_id] = {"type": "preset", **doc}

            # 画像ファイルの読み込み（PNG優先、なければJPG）
            images_dir = os.path.join(str(story_dir), "images")
            png_file = os.path.join(images_dir, f"{scene_id}.png")
            jpg_file = os.path.join(images_dir, f"{scene_id}.jpg")
            image_path = None
            if os.path.exists(png_file):
                image_path = png_file
            elif os.path.exists(jpg_file):
                image_path = jpg_file
            if image_path:
                IMAGES.setdefault(story_id, {})[scene_id] = os.path.abspath(image_path)
        except Exception as e:
            print(f"Error loading scene file {scene_file}: {e}")

# 各ストーリーの初期状態を設定
for story_id in META.keys():
    if story_id in SCENES:
        intro_scene = "intro" if "intro" in SCENES[story_id] else sorted(SCENES[story_id].keys())[0] if SCENES[story_id] else None
        if intro_scene:
            STATE[story_id] = {"scene_id": intro_scene, "flags": {}, "summary": ""}
        else:
            print(f"Warning: No scenes found for {story_id}")
    else:
        print(f"Warning: META exists but no SCENES for {story_id}")

# デバッグ用に読み込まれたデータを表示
print(f"Loaded META: {list(META.keys())}")
print(f"Loaded SCENES: {[(k, list(v.keys())) for k, v in SCENES.items()]}")
print(f"Initialized STATE: {list(STATE.keys())}")

# ---------------------------------------------------------------------------
# 2) Per‑player context
# ---------------------------------------------------------------------------
PLAYER_PATH: dict[str, list[str]] = defaultdict(list)  # player_id → visited scene list
CURRENT_STORY: dict[str, str] = {}  # player_id → current story_id
LOG: dict[str, list[dict]] = defaultdict(list)  # story_id → event list

now_ts = lambda: datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# 3) MCP Resources
# ---------------------------------------------------------------------------

@mcp.resource("novelgame://stories")
def stories_index() -> list[dict]:
    """Return list of available stories with minimal metadata (story_id, title…)."""
    result = []
    for story_id in META:
        # SCENESにもあるストーリーのみ返す（整合性チェック）
        if story_id in SCENES and SCENES[story_id]:
            story_data = {"story_id": story_id}
            story_data.update(META[story_id])
            result.append(story_data)
    
    print(f"stories_index returning: {result}")
    return result


@mcp.resource("novelgame://story/{story_id}/meta")
def story_meta(story_id: str) -> dict:
    """Metadata for the specified story (title, author, language)."""
    if story_id not in META:
        return {}
    return META[story_id]

@mcp.resource("novelgame://story/{story_id}/images")
def story_images(story_id: str) -> list[str]:
    """Return list of available images for the specified story."""
    return list(IMAGES.get(story_id, {}).keys())

@mcp.resource("novelgame://story/{story_id}/state")
def story_state(story_id: str) -> dict:
    """Current global state of the story (scene_id, flags, summary)."""
    if story_id not in STATE:
        return {}
    return STATE[story_id]


@mcp.resource("novelgame://story/{story_id}/scenes/{scene_id}")
def story_scene(story_id: str, scene_id: str) -> dict:
    """Scene document (body Markdown, choices) for given story & scene."""
    if story_id not in SCENES or scene_id not in SCENES[story_id]:
        return {}
    return SCENES[story_id][scene_id]


@mcp.resource("novelgame://player/{player_id}/path")
def player_path(player_id: str) -> list[str]:
    """Visited scene_id list for the player in current playthrough."""
    return PLAYER_PATH[player_id]


@mcp.resource("novelgame://log/{story_id}")
def story_log(story_id: str) -> list[dict]:
    """Chronological event log (start, choices…) for the specified story."""
    return LOG[story_id]


# ---------------------------------------------------------------------------
# 4) Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def select_story(player_id: str, story_id: str) -> dict:
    """Bind a story to the player and return its opening scene."""
    if story_id not in SCENES or not SCENES[story_id]:
        raise ValueError(f"Unknown story_id or story has no scenes: {story_id}")
    
    if story_id not in STATE:
        # STATE が初期化されていない場合（ファイル読み込み後に追加されたストーリーなど）
        intro_scene = "intro" if "intro" in SCENES[story_id] else sorted(SCENES[story_id].keys())[0]
        STATE[story_id] = {"scene_id": intro_scene, "flags": {}, "summary": ""}
    
    CURRENT_STORY[player_id] = story_id
    PLAYER_PATH[player_id].clear()
    LOG[story_id].append({"ts": now_ts(), "event": "start", "player_id": player_id})
    
    first_scene = STATE[story_id]["scene_id"]
    return {"story_id": story_id, "scene_id": first_scene, "scene": SCENES[story_id][first_scene]}


@mcp.tool()
def choose(
    player_id: str,
    current_scene_id: str,
    choice_id: str,
    free_text: str | None = None,
) -> str:
    """Record player's choice within their selected story."""
    story_id = CURRENT_STORY.get(player_id)
    if story_id is None:
        raise ValueError("Story not selected. Call select_story first.")
    
    if story_id not in SCENES:
        raise ValueError(f"Invalid story_id: {story_id}")
        
    if current_scene_id not in SCENES[story_id]:
        raise ValueError(f"Invalid scene id {current_scene_id} for story {story_id}")
    
    # 選択肢の検証（オプション）
    scene = SCENES[story_id][current_scene_id]
    if "choices" in scene and choice_id not in [c.get("id") for c in scene.get("choices", [])]:
        print(f"Warning: Potentially invalid choice_id {choice_id} for scene {current_scene_id}")

    PLAYER_PATH[player_id].append(current_scene_id)
    LOG[story_id].append(
        {
            "ts": now_ts(),
            "event": "choice",
            "payload": {
                "player_id": player_id,
                "current": current_scene_id,
                "choice": choice_id,
                "free": free_text,
            },
        }
    )
    return "ok"


@mcp.tool()
def load_scene_image(player_id: str, scene_id: str, max_width: int = 1024, max_height: int = 1024) -> Image:
    """Return the image for the player's current story and scene. Resize and compress until data size <= 1MB."""
    story_id = CURRENT_STORY.get(player_id)
    if story_id is None:
        raise ValueError("Story not selected. Call select_story first.")
    image_path = IMAGES.get(story_id, {}).get(scene_id)
    if not image_path:
        raise FileNotFoundError(f"No image found for story={story_id}, scene={scene_id}")

    with PILImage.open(image_path) as img:
        ext = (img.format or "PNG").upper()
        width, height = img.size
        cur_width, cur_height = min(width, max_width), min(height, max_height)
        min_size = 100
        quality = 85 if ext in ("JPEG", "JPG") else None

        while True:
            img_copy = img.copy()
            img_copy.thumbnail((cur_width, cur_height), PILImage.LANCZOS)
            buf = io.BytesIO()
            if ext in ("JPEG", "JPG"):
                img_copy.save(buf, format="JPEG", quality=quality)
            else:
                img_copy.save(buf, format="PNG", optimize=True, compress_level=9)
            size = buf.tell()
            if size <= 1048576 or (cur_width <= min_size or cur_height <= min_size):
                break
            # さらに縮小
            cur_width = int(cur_width * 0.8)
            cur_height = int(cur_height * 0.8)
        buf.seek(0)
        if size > 1048576:
            raise ValueError("Image is too large even after repeated resizing/compression.")
        return Image(data=buf.read())


# ---------------------------------------------------------------------------
# 5) Prompt
# ---------------------------------------------------------------------------

@mcp.prompt("narrator_prompt")
def narrator_prompt() -> str:
    """Single system prompt used by the narrator LLM."""
    return (
        "Run the novel game."
        "First, select a story in stories_index and call select_story."
        "Then, select a scene in story_state and call choose."
        "<Constraints>"
        "Speak Japanese."
        "Write vivid Japanese prose (max 1000 chars). "
        "Use image of current scene in load_scene_image."
        "Keep continuity with the existing story world and flags. "
        "Do not reveal hidden game mechanics or internal data."
        "</Constraints>"
    )


# ---------------------------------------------------------------------------
# 6) Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()