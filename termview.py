import argparse
import asyncio
import os
import pathlib
import sys
import tempfile

from PIL import Image
from playwright.async_api import async_playwright

RESET = "\033[0m"
COLOR = sys.stdout.isatty()  # False when piped to a file


def get_terminal_size():
    size = os.get_terminal_size(sys.stderr.fileno())
    return size.columns, size.lines


def rgb(text, r, g, b):
    if not COLOR:
        return text
    return f"\033[38;2;{r};{g};{b}m{text}{RESET}"


ASCII_RAMP = " .,:;i1tfLCG08@#"


def image_to_ascii(image_path, width, height):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((width, height), Image.LANCZOS)

    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = ASCII_RAMP[int(brightness / 255 * (len(ASCII_RAMP) - 1))]
            line += rgb(char, r, g, b)
        lines.append(line)

    return "\n".join(lines)


async def take_screenshot(url, width, height, output_path):
    # Scale viewport so one pixel-column ≈ one character column.
    # Terminal chars are roughly 2x taller than wide, so multiply height by 2.
    viewport_w = width * 8
    viewport_h = height * 16

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": viewport_w, "height": viewport_h}
        )
        print(f"Loading {url} ...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.screenshot(path=str(output_path), full_page=False)
        await browser.close()

    print(f"Screenshot saved: {output_path}  ({viewport_w}x{viewport_h}px)")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a webpage to ASCII art in your terminal"
    )
    parser.add_argument("url", help="The URL to snapshot")
    parser.add_argument("--width", type=int, help="Override terminal width")
    parser.add_argument("--height", type=int, help="Override terminal height")
    args = parser.parse_args()

    term_width, term_height = get_terminal_size()
    width = args.width or term_width
    height = args.height or term_height

    print(f"URL:      {args.url}")
    print(f"Terminal: {term_width} cols x {term_height} lines")
    print(f"Output:   {width} x {height}")

    snapshot = pathlib.Path(tempfile.mkdtemp()) / "snapshot.png"
    asyncio.run(take_screenshot(args.url, width, height, snapshot))

    print(image_to_ascii(snapshot, width, height))


if __name__ == "__main__":
    main()
