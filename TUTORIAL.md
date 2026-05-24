# Reproducible Tutorial: Kindle Highlights to Markdown CLI

## Step 1: Clone the Repository

```bash
git clone https://github.com/femirins/kindle-highlights-md.git
cd kindle-highlights-md
```

## Step 2: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install click rich
```

## Step 3: Prepare Your Clippings

Copy your Kindle's `My Clippings.txt` to the project directory:

```bash
cp /path/to/your/My\ Clippings.txt .
```

## Step 4: Run the CLI

### Basic Export
```bash
python kindle_highlights.py --input "My Clippings.txt" --output output
```

### Deduplication
```bash
python kindle_highlights.py --input "My Clippings.txt" --output output --dedupe
```

### Obsidian Integration
```bash
python kindle_highlights.py --input "My Clippings.txt" --obsidian "~/obsidian_vault/Kindle"
```

## Step 5: Verify Output

Check the `output` directory for Markdown files:

```bash
ls -l output/
```

## Expected Output

```markdown
# Atomic Habits (James Clear)

> You do not rise to the level of your goals. You fall to the level of your systems.

**Page:** 45

---
```