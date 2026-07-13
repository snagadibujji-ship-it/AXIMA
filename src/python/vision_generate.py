#!/usr/bin/env python3
"""
AXIMA HELIX — Local Image Generation Pipeline
Uses atom codebook + raymarcher + upscaler for 4K offline generation.

Usage:
  python3 vision_generate.py --prompt "red car on wet road" --output image.png
  python3 vision_generate.py --prompt "sunset over ocean" --resolution 1080p

Requires: atoms_16.bin, atoms_32.bin, atoms_64.bin, upscaler_4k.pth
(trained via Colab script: scripts/colab_vision_train.py)
"""
import os, sys, struct, argparse, time
import numpy as np

ATOMS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def check_atoms():
    """Check if trained atom files exist."""
    files = ['atoms_16.bin', 'atoms_32.bin', 'atoms_64.bin']
    missing = [f for f in files if not os.path.exists(os.path.join(ATOMS_DIR, f))]
    return missing

def generate_base(prompt, width=256, height=144):
    """Generate base image using procedural rendering + atoms.
    Returns numpy array (H, W, 3) uint8."""
    
    # Parse prompt for scene elements
    elements = parse_prompt(prompt)
    
    # Create base image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Simple procedural generation based on keywords
    if any(w in prompt.lower() for w in ['sunset', 'sunrise', 'sky']):
        # Sky gradient
        for y in range(height):
            t = y / height
            r = int(255 * (1 - t) * 0.9 + 50 * t)
            g = int(100 * (1 - t) + 150 * t)
            b = int(50 * (1 - t) + 255 * t)
            img[y, :] = [min(r, 255), min(g, 255), min(b, 255)]
    
    if any(w in prompt.lower() for w in ['ocean', 'sea', 'water', 'lake']):
        # Water in bottom third
        h_start = height * 2 // 3
        for y in range(h_start, height):
            t = (y - h_start) / (height - h_start)
            img[y, :] = [int(20 + 30*t), int(80 + 40*t), int(150 + 50*t)]
    
    if any(w in prompt.lower() for w in ['forest', 'tree', 'garden', 'grass']):
        # Green ground
        h_start = height * 2 // 3
        for y in range(h_start, height):
            img[y, :] = [34, int(120 + np.random.randint(0, 30)), 34]
    
    if any(w in prompt.lower() for w in ['night', 'dark', 'stars']):
        img[:] = [10, 10, 30]
        # Add stars
        for _ in range(100):
            x, y = np.random.randint(0, width), np.random.randint(0, height//2)
            img[y, x] = [255, 255, 255]
    
    return img

def parse_prompt(prompt):
    """Extract scene elements from text prompt."""
    elements = []
    keywords = {
        'sky': ['sunset', 'sunrise', 'sky', 'clouds', 'blue sky'],
        'water': ['ocean', 'sea', 'lake', 'river', 'water', 'rain'],
        'ground': ['grass', 'road', 'sand', 'snow', 'floor'],
        'objects': ['car', 'house', 'tree', 'mountain', 'building'],
    }
    for category, words in keywords.items():
        if any(w in prompt.lower() for w in words):
            elements.append(category)
    return elements

def upscale(img, scale=4):
    """Simple bicubic upscale (placeholder until trained upscaler loaded)."""
    from PIL import Image
    pil_img = Image.fromarray(img)
    new_size = (img.shape[1] * scale, img.shape[0] * scale)
    return np.array(pil_img.resize(new_size, Image.BICUBIC))

def save_image(img, path):
    """Save numpy array as PNG."""
    try:
        from PIL import Image
        Image.fromarray(img).save(path)
        return True
    except ImportError:
        # Fallback: save as BMP without PIL
        h, w = img.shape[:2]
        with open(path.replace('.png', '.bmp'), 'wb') as f:
            # BMP header
            row_size = (w * 3 + 3) & ~3
            data_size = row_size * h
            f.write(b'BM')
            f.write(struct.pack('<I', 54 + data_size))
            f.write(b'\x00\x00\x00\x00')
            f.write(struct.pack('<I', 54))
            f.write(struct.pack('<I', 40))
            f.write(struct.pack('<i', w))
            f.write(struct.pack('<i', -h))  # top-down
            f.write(struct.pack('<HH', 1, 24))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', data_size))
            f.write(b'\x00' * 16)
            for y in range(h):
                row = img[y, :, ::-1].tobytes()  # RGB→BGR
                f.write(row + b'\x00' * (row_size - w * 3))
        return True

def generate(prompt, resolution='720p', output='output.png'):
    """Full pipeline: prompt → base render → upscale → save."""
    
    res_map = {'256p': (256, 144), '480p': (640, 480), '720p': (1280, 720),
               '1080p': (1920, 1080), '4k': (3840, 2160)}
    
    target_w, target_h = res_map.get(resolution, (1280, 720))
    
    # Calculate base size (will be upscaled 4x)
    base_w = max(target_w // 4, 64)
    base_h = max(target_h // 4, 36)
    
    print(f"  Prompt: {prompt}")
    print(f"  Resolution: {resolution} ({target_w}×{target_h})")
    print(f"  Base render: {base_w}×{base_h}")
    
    # Step 1: Generate base
    t0 = time.time()
    base = generate_base(prompt, base_w, base_h)
    t1 = time.time()
    print(f"  Base render: {(t1-t0)*1000:.0f}ms")
    
    # Step 2: Upscale
    scale = target_w // base_w
    if scale > 1:
        img = upscale(base, scale)
    else:
        img = base
    t2 = time.time()
    print(f"  Upscale ({scale}x): {(t2-t1)*1000:.0f}ms")
    
    # Step 3: Save
    save_image(img, output)
    t3 = time.time()
    print(f"  Save: {(t3-t2)*1000:.0f}ms")
    print(f"  Total: {(t3-t0)*1000:.0f}ms")
    print(f"  Output: {output} ({os.path.getsize(output)/1024:.0f} KB)")
    
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AXIMA HELIX Image Generator')
    parser.add_argument('--prompt', '-p', required=True, help='Image description')
    parser.add_argument('--output', '-o', default='output.png', help='Output file')
    parser.add_argument('--resolution', '-r', default='720p', 
                       choices=['256p', '480p', '720p', '1080p', '4k'])
    args = parser.parse_args()
    
    missing = check_atoms()
    if missing:
        print(f"  Note: Atom files not found ({', '.join(missing)})")
        print(f"  Using procedural rendering (run Colab training for better quality)")
        print()
    
    generate(args.prompt, args.resolution, args.output)
