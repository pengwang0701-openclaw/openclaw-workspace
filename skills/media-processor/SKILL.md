---
name: media-processor
description: Process images and videos including resize, compress, convert, crop, filter, and basic editing. Use when the user needs to manipulate images (JPG, PNG, GIF, WebP) or videos (MP4, MOV, etc.) including format conversion, size optimization, or simple edits.
---

# 媒体处理器

Process images and videos with common operations like resize, compress, convert, and basic editing.

## Quick Start

### Image Operations

```python
from PIL import Image
import os

# Open image
img = Image.open('input.jpg')

# Basic info
print(img.size, img.mode, img.format)

# Resize (maintain aspect ratio)
img.thumbnail((800, 600))

# Resize (exact dimensions)
img_resized = img.resize((800, 600), Image.LANCZOS)

# Save with compression
img.save('output.jpg', quality=85, optimize=True)
```

### Video Operations

```python
import ffmpeg

# Get video info
probe = ffmpeg.probe('input.mp4')
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
print(f"Duration: {probe['format']['duration']}")
print(f"Resolution: {video_info['width']}x{video_info['height']}")

# Compress video
(
    ffmpeg
    .input('input.mp4')
    .output('output.mp4', vcodec='h264', crf=23, preset='medium')
    .run()
)
```

## Image Processing

### Resize Images

```python
from PIL import Image

def resize_image(input_path, output_path, width=None, height=None, 
                 maintain_ratio=True, quality=85):
    """Resize image with options."""
    with Image.open(input_path) as img:
        if maintain_ratio and (width or height):
            # Calculate new size maintaining aspect ratio
            w, h = img.size
            if width and height:
                # Fit within box
                ratio = min(width/w, height/h)
                new_size = (int(w*ratio), int(h*ratio))
            elif width:
                ratio = width / w
                new_size = (width, int(h*ratio))
            else:
                ratio = height / h
                new_size = (int(w*ratio), height)
            img = img.resize(new_size, Image.LANCZOS)
        elif width and height:
            # Exact dimensions
            img = img.resize((width, height), Image.LANCZOS)
        
        img.save(output_path, quality=quality, optimize=True)

# Usage
resize_image('photo.jpg', 'thumb.jpg', width=300, height=300)
```

### Convert Formats

```python
from PIL import Image
import os

def convert_image(input_path, output_path=None, format=None):
    """Convert image to different format."""
    img = Image.open(input_path)
    
    if not output_path:
        ext = format.lower() if format else 'png'
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.{ext}"
    
    if format:
        img.save(output_path, format=format)
    else:
        img.save(output_path)
    
    return output_path

# Convert to different formats
convert_image('photo.jpg', 'photo.png')           # JPG to PNG
convert_image('photo.png', 'photo.webp', 'WEBP') # PNG to WebP
convert_image('photo.jpg', 'photo.gif', 'GIF')    # JPG to GIF
```

### Batch Processing

```python
import os
from PIL import Image

def batch_resize(directory, output_dir, width=800, height=None):
    """Resize all images in a directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(output_dir, filename)
            
            with Image.open(input_path) as img:
                if height:
                    img.thumbnail((width, height))
                else:
                    ratio = width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((width, new_height), Image.LANCZOS)
                
                img.save(output_path, quality=85, optimize=True)
            print(f"Processed: {filename}")

# Usage
batch_resize('./photos', './thumbs', width=300)
```

### Image Filters & Effects

```python
from PIL import Image, ImageFilter, ImageEnhance

img = Image.open('photo.jpg')

# Apply filters
img_blur = img.filter(ImageFilter.GaussianBlur(radius=2))
img_sharpen = img.filter(ImageFilter.SHARPEN)
img_edges = img.filter(ImageFilter.FIND_EDGES)

# Enhance
enhancer = ImageEnhance.Brightness(img)
img_bright = enhancer.enhance(1.2)  # 20% brighter

enhancer = ImageEnhance.Contrast(img)
img_contrast = enhancer.enhance(1.3)  # 30% more contrast

enhancer = ImageEnhance.Color(img)
img_saturated = enhancer.enhance(1.5)  # More saturated
```

### Create Thumbnails

```python
from PIL import Image
import os

def create_thumbnail(input_path, size=(150, 150), crop=True):
    """Create square thumbnail, optionally cropping to center."""
    with Image.open(input_path) as img:
        if crop:
            # Crop to center for square
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img = img.crop((left, top, right, bottom))
        
        img.thumbnail(size, Image.LANCZOS)
        
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_thumb{ext}"
        img.save(output_path, quality=85)
        return output_path

# Usage
create_thumbnail('photo.jpg', size=(200, 200))
```

## Video Processing

### Extract Frame

```python
import ffmpeg

def extract_frame(video_path, time_seconds, output_path):
    """Extract frame at specific time."""
    (
        ffmpeg
        .input(video_path, ss=time_seconds)
        .output(output_path, vframes=1)
        .run()
    )

# Extract frame at 5 seconds
extract_frame('video.mp4', 5, 'frame_at_5s.jpg')
```

### Trim Video

```python
import ffmpeg

def trim_video(input_path, start_time, duration, output_path):
    """Trim video segment."""
    (
        ffmpeg
        .input(input_path, ss=start_time, t=duration)
        .output(output_path, c='copy')
        .run()
    )

# Extract 30 seconds starting at 1 minute
trim_video('video.mp4', '00:01:00', 30, 'clip.mp4')
```

### Compress Video

```python
import ffmpeg

def compress_video(input_path, output_path, crf=23):
    """Compress video with H.264 codec.
    
    CRF values: 18-28 (lower = better quality, larger file)
    23 is default, 18 is visually lossless
    """
    (
        ffmpeg
        .input(input_path)
        .output(output_path, 
                vcodec='libx264',
                crf=crf,
                preset='medium',
                movflags='faststart')
        .run()
    )

# High quality compression
compress_video('input.mp4', 'output.mp4', crf=20)
```

### Convert Format

```python
import ffmpeg

def convert_video(input_path, output_path):
    """Convert video to different format."""
    (
        ffmpeg
        .input(input_path)
        .output(output_path)
        .run()
    )

# Convert MOV to MP4
convert_video('video.mov', 'video.mp4')

# Convert to GIF (lower quality, smaller)
(
    ffmpeg
    .input('video.mp4')
    .output('output.gif', vf='fps=10,scale=480:-1:flags=lanczos')
    .run()
)
```

### Extract Audio

```python
import ffmpeg

def extract_audio(video_path, output_path, format='mp3'):
    """Extract audio from video."""
    (
        ffmpeg
        .input(video_path)
        .output(output_path, vn=True, acodec='libmp3lame' if format == 'mp3' else 'aac')
        .run()
    )

# Extract as MP3
extract_audio('video.mp4', 'audio.mp3')

# Extract as AAC
extract_audio('video.mp4', 'audio.m4a', format='aac')
```

## Common Workflows

### Optimize for Web

```python
def optimize_for_web(image_path, output_path, max_width=1200):
    """Optimize image for web use."""
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        
        # Save as progressive JPEG
        img.save(output_path, 'JPEG', quality=80, optimize=True, progressive=True)

# Usage
optimize_for_web('large_photo.jpg', 'web_optimized.jpg')
```

### Create GIF from Images

```python
from PIL import Image
import os

def create_gif(image_paths, output_path, duration=500):
    """Create animated GIF from images.
    
    duration: milliseconds per frame
    """
    images = [Image.open(p) for p in image_paths]
    
    # Save first image, append rest
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )

# Usage
image_files = sorted([f for f in os.listdir('frames') if f.endswith('.jpg')])
create_gif(image_files, 'animation.gif', duration=300)
```

## Best Practices

### Images
- **Web**: Use WebP or optimized JPEG (quality 75-85)
- **Thumbnails**: 150x150px, crop to center for consistency
- **Full size**: Keep original aspect ratio, max 1920px width
- **Compression**: Always use `optimize=True` for JPEG
- **Color mode**: Convert RGBA to RGB before JPEG save

### Videos
- **Compression**: CRF 20-23 for web, 18 for archival
- **Formats**: MP4 (H.264) for compatibility, WebM for web
- **Thumbnails**: Extract at meaningful moments (not just start)
- **Audio**: Extract separately if reusing
- **Mobile**: Consider portrait 9:16 for TikTok/Reels

## Resources

### scripts/
- `optimize_image.py` - Web optimization script
- `batch_convert.py` - Bulk format conversion
- `create_thumbnails.py` - Generate thumbnail gallery
- `compress_video.py` - Video compression with presets

### references/
- `pillow-docs.md` - PIL/Pillow reference
- `ffmpeg-guide.md` - Common ffmpeg commands
- `format-guide.md` - Best formats for different use cases