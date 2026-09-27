from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage


def find_separator(projection: np.ndarray, expected: int, radius: int) -> int:
    """Find the lowest-density separator near an expected grid boundary."""
    lo = max(1, expected - radius)
    hi = min(len(projection) - 2, expected + radius)
    segment = projection[lo:hi + 1]
    minimum = segment.min()
    candidates = np.flatnonzero(segment == minimum) + lo
    # Pick the minimum closest to the expected grid line.
    return int(candidates[np.argmin(np.abs(candidates - expected))])


def find_row_boundaries(mask: np.ndarray, rows: int) -> list[int]:
    h = mask.shape[0]
    projection = mask.sum(axis=1)
    radius = max(20, int(h / rows * 0.28))
    bounds = [0]
    for i in range(1, rows):
        expected = round(i * h / rows)
        bounds.append(find_separator(projection, expected, radius))
    bounds.append(h)
    return bounds


def find_col_boundaries(row_mask: np.ndarray, cols: int) -> list[int]:
    w = row_mask.shape[1]
    projection = row_mask.sum(axis=0)
    radius = max(20, int(w / cols * 0.28))
    bounds = [0]
    for i in range(1, cols):
        expected = round(i * w / cols)
        bounds.append(find_separator(projection, expected, radius))
    bounds.append(w)
    return bounds


def keep_largest_component(cell: Image.Image, alpha_threshold: int = 24) -> Image.Image:
    """Remove detached fragments from neighboring sprites / generation specks."""
    rgba = np.array(cell.convert("RGBA"))
    mask = rgba[:, :, 3] > alpha_threshold
    if not mask.any():
        return cell

    labels, count = ndimage.label(mask, structure=np.ones((3, 3), dtype=np.uint8))
    if count <= 1:
        return cell

    sizes = ndimage.sum(mask, labels, index=np.arange(1, count + 1))
    largest_label = int(np.argmax(sizes)) + 1
    keep = labels == largest_label

    # Preserve antialiased pixels immediately touching the main component.
    keep = ndimage.binary_dilation(keep, iterations=2) & (rgba[:, :, 3] > 0)
    rgba[~keep, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def robust_bbox(cell: Image.Image, alpha_threshold: int = 24, min_occupancy: int = 3):
    """Return a bbox while ignoring tiny isolated alpha specks."""
    alpha = np.array(cell.getchannel("A"))
    mask = alpha > alpha_threshold
    if not mask.any():
        return None

    col_counts = mask.sum(axis=0)
    row_counts = mask.sum(axis=1)

    xs = np.flatnonzero(col_counts >= min_occupancy)
    ys = np.flatnonzero(row_counts >= min_occupancy)

    if len(xs) == 0 or len(ys) == 0:
        ys2, xs2 = np.nonzero(mask)
        return (int(xs2.min()), int(ys2.min()), int(xs2.max()) + 1, int(ys2.max()) + 1)

    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def extract_frames(image: Image.Image, rows: int, cols: int, alpha_threshold: int):
    rgba = image.convert("RGBA")
    alpha = np.array(rgba.getchannel("A"))
    mask = alpha > alpha_threshold

    row_bounds = find_row_boundaries(mask, rows)
    frames = []

    for row in range(rows):
        y0, y1 = row_bounds[row], row_bounds[row + 1]
        row_mask = mask[y0:y1, :]
        col_bounds = find_col_boundaries(row_mask, cols)

        row_frames = []
        for col in range(cols):
            x0, x1 = col_bounds[col], col_bounds[col + 1]
            cell = rgba.crop((x0, y0, x1, y1))
            cell = keep_largest_component(cell, alpha_threshold=alpha_threshold)
            bbox = robust_bbox(cell, alpha_threshold=alpha_threshold)
            if bbox is None:
                sprite = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            else:
                sprite = cell.crop(bbox)
            row_frames.append(sprite)
        frames.append(row_frames)

    return frames


def normalize_frames(frames, cell_size: int, padding: int):
    normalized = []
    max_content = cell_size - padding * 2

    for row in frames:
        out_row = []
        for sprite in row:
            # Only shrink if a generated sprite is unexpectedly too large.
            if sprite.width > max_content or sprite.height > max_content:
                scale = min(max_content / sprite.width, max_content / sprite.height)
                new_size = (
                    max(1, round(sprite.width * scale)),
                    max(1, round(sprite.height * scale)),
                )
                sprite = sprite.resize(new_size, Image.Resampling.NEAREST)

            canvas = Image.new("RGBA", (cell_size, cell_size), (0, 0, 0, 0))

            # Game anchor: horizontal center + feet/bottom baseline.
            x = (cell_size - sprite.width) // 2
            y = cell_size - padding - sprite.height

            canvas.alpha_composite(sprite, (x, y))
            out_row.append(canvas)
        normalized.append(out_row)

    return normalized


def save_sheet(frames, output: Path):
    rows = len(frames)
    cols = len(frames[0])
    cell_w, cell_h = frames[0][0].size

    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (0, 0, 0, 0))
    for row in range(rows):
        for col in range(cols):
            sheet.alpha_composite(frames[row][col], (col * cell_w, row * cell_h))

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def save_individual_frames(frames, output_dir: Path):
    directions = ["down", "left", "right", "up"]
    output_dir.mkdir(parents=True, exist_ok=True)

    for row, direction in enumerate(directions[:len(frames)]):
        direction_dir = output_dir / direction
        direction_dir.mkdir(parents=True, exist_ok=True)
        for col, frame in enumerate(frames[row]):
            frame.save(direction_dir / f"{col}.png")


def process(input_path: Path, output_path: Path, frames_dir: Path | None,
            rows: int, cols: int, cell_size: int, padding: int, alpha_threshold: int):
    image = Image.open(input_path).convert("RGBA")
    frames = extract_frames(image, rows, cols, alpha_threshold)
    frames = normalize_frames(frames, cell_size, padding)
    save_sheet(frames, output_path)
    if frames_dir is not None:
        save_individual_frames(frames, frames_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Extract, crop and align a transparent RPG spritesheet."
    )
    parser.add_argument("input", type=Path, help="Input PNG spritesheet")
    parser.add_argument("output", type=Path, help="Aligned output PNG")
    parser.add_argument("--frames-dir", type=Path, default=None,
                        help="Optional folder for individual frames")
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--cell-size", type=int, default=340,
                        help="Square size of every output frame")
    parser.add_argument("--padding", type=int, default=10)
    parser.add_argument("--alpha-threshold", type=int, default=24)
    args = parser.parse_args()

    process(
        args.input,
        args.output,
        args.frames_dir,
        args.rows,
        args.cols,
        args.cell_size,
        args.padding,
        args.alpha_threshold,
    )

    print(f"Aligned sheet: {args.output}")
    if args.frames_dir:
        print(f"Individual frames: {args.frames_dir}")


if __name__ == "__main__":
    main()
