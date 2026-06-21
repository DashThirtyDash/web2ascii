# web2ascii

Takes a URL, screenshots it with a headless browser, and renders it as colored ASCII art sized to fit your terminal.

```
termview https://example.com
```

## Install

Requires Python 3.8+ and pip.

```bash
git clone https://github.com/DashThirtyDash/web2ascii.git
cd web2ascii
pip install -e .
playwright install chromium
```

## Usage

```bash
termview <url>
```

**Options**

| Flag | Description |
|---|---|
| `--width N` | Override output width (default: terminal width) |
| `--height N` | Override output height (default: terminal height) |

**Examples**

```bash
# Render a page at your current terminal size
termview https://example.com

# Render at a fixed size
termview https://example.com --width 80 --height 40

# Save plain ASCII (no color) to a file
termview https://example.com > snapshot.txt
```

## How it works

1. Launches a headless Chromium browser sized to match your terminal dimensions
2. Navigates to the URL and waits for the page to fully load
3. Takes a screenshot and resizes it to the terminal's column/row count
4. Maps each pixel's brightness to a character from an ASCII ramp
5. Wraps each character in a true-color ANSI escape code using the pixel's RGB value

When output is piped to a file, color codes are automatically stripped and plain ASCII is written instead.

## Dependencies

- [Playwright](https://playwright.dev/python/) — headless browser for screenshots
- [Pillow](https://python-pillow.org/) — image resizing and pixel access
