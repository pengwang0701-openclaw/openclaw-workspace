---
name: ppt-creator
description: Create professional PowerPoint presentations from scratch or outlines. Use when the user needs to generate PPT files, convert text/content to slides, design presentations, or work with .pptx files.
---

# PPT 制作

Create professional PowerPoint presentations using python-pptx.

## Quick Start

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor

# Create presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add blank slide
blank_layout = prs.slide_layouts[6]  # Blank layout
slide = prs.slides.add_slide(blank_layout)

# Add title
left = Inches(0.5)
top = Inches(0.5)
width = Inches(12)
height = Inches(1)
title_box = slide.shapes.add_textbox(left, top, width, height)
title_frame = title_box.text_frame
title_frame.text = "Your Title Here"
title_frame.paragraphs[0].font.size = Pt(44)
title_frame.paragraphs[0].font.bold = True

# Save
prs.save('output.pptx')
```

## Slide Layouts

| Layout Index | Type | Use For |
|-------------|------|---------|
| 0 | Title Slide | Opening/cover slide |
| 1 | Title and Content | Main content slides |
| 2 | Section Header | Section dividers |
| 3 | Two Content | Side-by-side content |
| 4 | Comparison | Comparison layouts |
| 5 | Title Only | Custom layouts |
| 6 | Blank | Full control |

## Common Operations

### Add Text

```python
# Method 1: Text box
textbox = slide.shapes.add_textbox(left, top, width, height)
textbox.text_frame.text = "Hello World"

# Method 2: Placeholder (if using layouts with placeholders)
title = slide.shapes.title
title.text = "Slide Title"
body = slide.placeholders[1]
body.text = "Content here"
```

### Format Text

```python
paragraph = text_frame.paragraphs[0]
paragraph.text = "Text"
paragraph.font.size = Pt(24)
paragraph.font.name = "Microsoft YaHei"
paragraph.font.bold = True
paragraph.font.color.rgb = RgbColor(255, 0, 0)

# Alignment
from pptx.enum.text import PP_ALIGN
paragraph.alignment = PP_ALIGN.CENTER  # or LEFT, RIGHT
```

### Add Images

```python
from pptx.util import Inches

# Add image
img_path = 'image.jpg'
left = Inches(1)
top = Inches(2)
height = Inches(4.5)
pic = slide.shapes.add_picture(img_path, left, top, height=height)

# Add image with original aspect ratio
pic = slide.shapes.add_picture(img_path, left, top)
```

### Add Shapes

```python
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR

# Rectangle
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, left, top, width, height
)
shape.fill.solid()
shape.fill.fore_color.rgb = RgbColor(52, 152, 219)

# Line
line = slide.shapes.add_connector(
    MSO_CONNECTOR.STRAIGHT, start_x, start_y, end_x, end_y
)
line.line.color.rgb = RgbColor(0, 0, 0)
line.line.width = Pt(2)
```

### Add Tables

```python
# Add table
rows, cols = 3, 4
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Set content
for i in range(rows):
    for j in range(cols):
        cell = table.cell(i, j)
        cell.text = f"Row {i+1}, Col {j+1}"
        cell.text_frame.paragraphs[0].font.size = Pt(12)

# Set column widths
table.columns[0].width = Inches(2)
table.columns[1].width = Inches(3)
```

## Color Schemes

### Professional Palettes

```python
# Blue theme
PRIMARY_BLUE = RgbColor(52, 152, 219)
DARK_BLUE = RgbColor(41, 128, 185)
LIGHT_BLUE = RgbColor(174, 214, 241)

# Dark theme
DARK_BG = RgbColor(44, 62, 80)
DARK_TEXT = RgbColor(236, 240, 241)
ACCENT = RgbColor(231, 76, 60)

# Warm theme
WARM_PRIMARY = RgbColor(230, 126, 34)
WARM_SECONDARY = RgbColor(211, 84, 0)
CREAM = RgbColor(253, 245, 230)
```

## Content Structure

### Presentation Outline to Slides

```
1. Title Slide
   - Title: Main topic
   - Subtitle: Brief description

2. Agenda/Overview
   - 3-5 bullet points of what's covered

3-5. Section Slides (repeat as needed)
   - Section header
   - Key points (3-5 bullets)
   - Supporting details

6. Summary/Key Takeaways
   - 3-5 main points

7. Thank You / Q&A
   - Contact info
   - Call to action
```

## Best Practices

1. **Slide Count**: 10-15 slides for 15-min presentation
2. **Text**: Max 6 bullets per slide, 6 words per bullet
3. **Fonts**: Minimum 24pt for body, 32pt+ for headers
4. **Images**: Use high-res, compress if file too large
5. **Colors**: 3-4 colors max, ensure contrast
6. **Consistency**: Same fonts, colors, spacing throughout

## Resources

### scripts/
- `create_from_outline.py` - Generate PPT from text outline
- `batch_slides.py` - Create multiple slides from data
- `apply_template.py` - Apply consistent styling

### assets/
- `templates/` - Starter presentation templates
- `palettes/` - Color scheme files

### references/
- `python-pptx-docs.md` - API reference
- `design-patterns.md` - Common slide layouts