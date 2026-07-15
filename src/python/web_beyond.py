"""
AXIMA Web Builder — BEYOND MODULE
What nobody else generates. The masterpiece layer.

1. Physics Animations (spring, gravity, fluid, elastic)
2. Generative Art (SVG noise, voronoi, flow fields)
3. Micro-interactions (cursor effects, magnetic buttons, text reveal)
4. Scroll Storytelling (Apple-style parallax narrative)
5. Generative SVG (unique art per site)
6. Cursor Physics (trails, ripples, magnetic)
7. Sound Design (Web Audio procedural ambient)
8. Color Harmony (color theory math, not stored palettes)

Nobody else does this from a single prompt.
"""

import math
import hashlib
from typing import Dict, List


class PhysicsAnimations:
    """Generate JS animations from PHYSICS equations."""

    def spring_system(self) -> str:
        """Spring physics for elements — smooth, natural motion."""
        return '''// Spring Physics Engine
class Spring {
    constructor(stiffness = 0.15, damping = 0.7) {
        this.stiffness = stiffness;
        this.damping = damping;
        this.position = 0;
        this.velocity = 0;
        this.target = 0;
    }
    update() {
        const force = (this.target - this.position) * this.stiffness;
        this.velocity = (this.velocity + force) * this.damping;
        this.position += this.velocity;
        return this.position;
    }
    set(target) { this.target = target; }
}

// Apply spring physics to elements on scroll
const springs = new Map();
document.querySelectorAll('[data-spring]').forEach(el => {
    springs.set(el, { x: new Spring(0.08, 0.8), y: new Spring(0.08, 0.8), scale: new Spring(0.1, 0.75) });
});

function animateSprings() {
    springs.forEach((s, el) => {
        const rect = el.getBoundingClientRect();
        const visible = rect.top < window.innerHeight && rect.bottom > 0;
        s.y.set(visible ? 0 : 40);
        s.scale.set(visible ? 1 : 0.9);
        const y = s.y.update();
        const scale = s.scale.update();
        el.style.transform = `translateY(${y}px) scale(${scale})`;
        el.style.opacity = Math.max(0, 1 - Math.abs(y) / 60);
    });
    requestAnimationFrame(animateSprings);
}
animateSprings();'''

    def gravity_particles(self) -> str:
        """Particles that respond to gravity + mouse."""
        return '''// Gravity Particle System
const gravCanvas = document.createElement('canvas');
gravCanvas.id = 'gravity-bg';
gravCanvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:0;opacity:0.4;';
document.body.prepend(gravCanvas);
const gCtx = gravCanvas.getContext('2d');
gravCanvas.width = window.innerWidth;
gravCanvas.height = window.innerHeight;

class Particle {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * gravCanvas.width;
        this.y = Math.random() * gravCanvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = 1 + Math.random() * 2;
        this.life = 1;
    }
    update(mx, my) {
        // Gravity toward mouse
        const dx = mx - this.x, dy = my - this.y;
        const dist = Math.sqrt(dx*dx + dy*dy) || 1;
        if (dist < 200) {
            this.vx += (dx / dist) * 0.02;
            this.vy += (dy / dist) * 0.02;
        }
        // Gentle float upward
        this.vy -= 0.005;
        this.vx *= 0.99; this.vy *= 0.99;
        this.x += this.vx; this.y += this.vy;
        if (this.x < 0 || this.x > gravCanvas.width || this.y < 0 || this.y > gravCanvas.height) this.reset();
    }
    draw(ctx, color) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
        ctx.fillStyle = color;
        ctx.fill();
    }
}

const particles = Array.from({length: 80}, () => new Particle());
let gmx = window.innerWidth/2, gmy = window.innerHeight/2;
document.addEventListener('mousemove', e => { gmx = e.clientX; gmy = e.clientY; });

function drawGravity() {
    gCtx.clearRect(0, 0, gravCanvas.width, gravCanvas.height);
    const style = getComputedStyle(document.documentElement);
    const color = style.getPropertyValue('--primary').trim() || '#6366f1';
    particles.forEach(p => { p.update(gmx, gmy); p.draw(gCtx, color + '60'); });
    
    // Draw connections
    gCtx.strokeStyle = color + '15';
    gCtx.lineWidth = 0.5;
    for (let i = 0; i < particles.length; i++) {
        for (let j = i+1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            if (Math.abs(dx) < 80 && Math.abs(dy) < 80) {
                gCtx.beginPath();
                gCtx.moveTo(particles[i].x, particles[i].y);
                gCtx.lineTo(particles[j].x, particles[j].y);
                gCtx.stroke();
            }
        }
    }
    requestAnimationFrame(drawGravity);
}
drawGravity();
window.addEventListener('resize', () => { gravCanvas.width = window.innerWidth; gravCanvas.height = window.innerHeight; });'''

    def fluid_motion(self) -> str:
        """Fluid dynamics for smooth element transitions."""
        return '''// Fluid motion — elements follow cursor like liquid
document.querySelectorAll('.fluid-follow').forEach((el, i) => {
    let x = 0, y = 0, targetX = 0, targetY = 0;
    const delay = 0.05 + i * 0.02;
    
    document.addEventListener('mousemove', e => {
        targetX = (e.clientX - window.innerWidth/2) * 0.02;
        targetY = (e.clientY - window.innerHeight/2) * 0.02;
    });
    
    function update() {
        x += (targetX - x) * delay;
        y += (targetY - y) * delay;
        el.style.transform = `translate(${x}px, ${y}px)`;
        requestAnimationFrame(update);
    }
    update();
});'''


class GenerativeArt:
    """Generate unique SVG/Canvas art for backgrounds."""

    def flow_field_svg(self, seed: str = "default") -> str:
        """Generate a flow field as SVG background."""
        # Use seed to generate deterministic but unique patterns
        h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
        paths = []
        for i in range(30):
            # Generate curve control points from seed
            x1 = (h * (i+1) * 7) % 1000
            y1 = (h * (i+1) * 13) % 600
            cx1 = (h * (i+2) * 11) % 1000
            cy1 = (h * (i+2) * 17) % 600
            cx2 = (h * (i+3) * 19) % 1000
            cy2 = (h * (i+3) * 23) % 600
            x2 = (h * (i+4) * 29) % 1000
            y2 = (h * (i+4) * 31) % 600
            opacity = 0.03 + (i % 5) * 0.02
            width = 1 + (i % 3)
            paths.append(f'<path d="M{x1},{y1} C{cx1},{cy1} {cx2},{cy2} {x2},{y2}" stroke="var(--primary)" stroke-width="{width}" fill="none" opacity="{opacity}"/>')

        svg_paths = '\n'.join(paths)
        return f'''<svg class="generative-bg" viewBox="0 0 1000 600" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
{svg_paths}
</svg>'''

    def noise_gradient_css(self) -> str:
        """CSS for animated noise gradient background."""
        return '''
.noise-bg::before {
    content: '';
    position: fixed;
    inset: 0;
    opacity: 0.03;
    z-index: -1;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
}
.generative-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}'''

    def blob_svg(self, seed: str = "blob") -> str:
        """Generate organic blob shapes."""
        h = int(hashlib.md5(seed.encode()).hexdigest()[:8], 16)
        blobs = []
        for i in range(3):
            # Generate blob path using sin/cos perturbation
            points = []
            cx, cy = 200 + i * 300, 200 + (h * (i+1)) % 200
            r = 80 + (h * (i+7)) % 60
            for j in range(8):
                angle = (j / 8) * math.pi * 2
                noise = ((h * (i+j+1)) % 30) - 15
                px = cx + (r + noise) * math.cos(angle)
                py = cy + (r + noise) * math.sin(angle)
                points.append((px, py))
            # Close as smooth curve
            d = f"M{points[0][0]},{points[0][1]} "
            for j in range(len(points)):
                p1 = points[j]
                p2 = points[(j+1) % len(points)]
                d += f"Q{(p1[0]+p2[0])/2+10},{(p1[1]+p2[1])/2-10} {p2[0]},{p2[1]} "
            d += "Z"
            opacity = 0.05 + i * 0.03
            blobs.append(f'<path d="{d}" fill="var(--primary)" opacity="{opacity}"/>')

        return f'''<svg class="generative-bg" viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg">
{''.join(blobs)}
</svg>'''


class MicroInteractions:
    """Cursor effects, magnetic buttons, text reveals."""

    def cursor_glow(self) -> str:
        """Custom cursor with glow effect."""
        return '''// Custom cursor with glow
const cursor = document.createElement('div');
cursor.className = 'custom-cursor';
document.body.appendChild(cursor);
const cursorTrail = document.createElement('div');
cursorTrail.className = 'cursor-trail';
document.body.appendChild(cursorTrail);

let cx = 0, cy = 0, tx = 0, ty = 0;
document.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; });

function updateCursor() {
    cx += (tx - cx) * 0.15;
    cy += (ty - cy) * 0.15;
    cursor.style.transform = `translate(${tx - 10}px, ${ty - 10}px)`;
    cursorTrail.style.transform = `translate(${cx - 20}px, ${cy - 20}px)`;
    requestAnimationFrame(updateCursor);
}
updateCursor();

// Scale cursor on hover
document.querySelectorAll('a, button, .card').forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('cursor-hover'));
});'''

    def cursor_css(self) -> str:
        """CSS for custom cursor."""
        return '''
.custom-cursor {
    width: 20px; height: 20px;
    border: 2px solid var(--primary);
    border-radius: 50%;
    position: fixed; top: 0; left: 0;
    pointer-events: none; z-index: 10000;
    transition: width 0.3s, height 0.3s, border-color 0.3s;
    mix-blend-mode: difference;
}
.cursor-trail {
    width: 40px; height: 40px;
    background: var(--primary);
    opacity: 0.1;
    border-radius: 50%;
    position: fixed; top: 0; left: 0;
    pointer-events: none; z-index: 9999;
    transition: opacity 0.3s;
}
.cursor-hover {
    width: 50px; height: 50px;
    border-color: var(--secondary);
}
@media (hover: none) { .custom-cursor, .cursor-trail { display: none; } }
'''

    def magnetic_buttons(self) -> str:
        """Buttons that attract toward cursor."""
        return '''// Magnetic buttons — pull toward cursor
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width/2;
        const y = e.clientY - rect.top - rect.height/2;
        btn.style.transform = `translate(${x*0.3}px, ${y*0.3}px)`;
    });
    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translate(0, 0)';
        btn.style.transition = 'transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        setTimeout(() => btn.style.transition = '', 500);
    });
});'''

    def text_reveal(self) -> str:
        """Split text and reveal letter by letter on scroll."""
        return '''// Text split + reveal animation
document.querySelectorAll('.text-reveal').forEach(el => {
    const text = el.textContent;
    el.innerHTML = '';
    text.split('').forEach((char, i) => {
        const span = document.createElement('span');
        span.textContent = char === ' ' ? '\\u00A0' : char;
        span.style.cssText = `display:inline-block;opacity:0;transform:translateY(20px);transition:all 0.5s ease ${i*0.03}s;`;
        el.appendChild(span);
    });
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll('span').forEach(s => {
                    s.style.opacity = '1';
                    s.style.transform = 'translateY(0)';
                });
            }
        });
    }, { threshold: 0.5 });
    observer.observe(el);
});'''

    def ripple_click(self) -> str:
        """Material-style ripple on click."""
        return '''// Ripple effect on buttons
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        ripple.style.cssText = `position:absolute;border-radius:50%;background:rgba(255,255,255,0.4);transform:scale(0);animation:ripple 0.6s ease-out;left:${e.clientX-rect.left}px;top:${e.clientY-rect.top}px;width:100px;height:100px;margin:-50px;`;
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
});'''


class ScrollStorytelling:
    """Apple-style scroll-driven animations."""

    def parallax_layers(self) -> str:
        """Multi-layer parallax with different speeds."""
        return '''// Parallax scroll layers
const layers = document.querySelectorAll('[data-speed]');
window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    layers.forEach(layer => {
        const speed = parseFloat(layer.dataset.speed) || 0.5;
        layer.style.transform = `translateY(${scrollY * speed}px)`;
    });
});'''

    def scroll_progress(self) -> str:
        """Progress bar + section reveal on scroll."""
        return '''// Scroll progress indicator
const progressBar = document.createElement('div');
progressBar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,var(--primary),var(--secondary));z-index:10001;transition:width 0.1s;';
document.body.appendChild(progressBar);

window.addEventListener('scroll', () => {
    const scrolled = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    progressBar.style.width = `${scrolled * 100}%`;
});'''

    def section_morph(self) -> str:
        """Sections morph/transform as you scroll through them."""
        return '''// Section morph on scroll
document.querySelectorAll('section').forEach(section => {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            const ratio = entry.intersectionRatio;
            entry.target.style.opacity = 0.3 + ratio * 0.7;
            entry.target.style.transform = `scale(${0.95 + ratio * 0.05}) translateY(${(1-ratio) * 20}px)`;
        });
    }, { threshold: Array.from({length: 20}, (_, i) => i/20) });
    observer.observe(section);
});'''


class ColorHarmony:
    """Derive colors from color theory math, not stored palettes."""

    def generate_from_hue(self, hue: float) -> Dict[str, str]:
        """Generate full palette from single hue using color theory."""
        # Complementary: +180°
        # Triadic: +120°, +240°
        # Split complementary: +150°, +210°
        primary = self._hsl_to_hex(hue, 0.7, 0.5)
        secondary = self._hsl_to_hex((hue + 30) % 360, 0.75, 0.55)
        accent = self._hsl_to_hex((hue + 180) % 360, 0.6, 0.5)

        # Light or dark based on hue warmth
        is_warm = hue < 60 or hue > 300
        if is_warm:
            bg = self._hsl_to_hex(hue, 0.1, 0.97)
            text = self._hsl_to_hex(hue, 0.3, 0.15)
            surface = "#ffffff"
        else:
            bg = self._hsl_to_hex(hue, 0.15, 0.96)
            text = self._hsl_to_hex(hue, 0.4, 0.12)
            surface = "#ffffff"

        return {"primary": primary, "secondary": secondary, "accent": accent,
                "bg": bg, "text": text, "surface": surface}

    def _hsl_to_hex(self, h: float, s: float, l: float) -> str:
        """Convert HSL to hex."""
        h = h / 360.0
        if s == 0:
            r = g = b = l
        else:
            def hue2rgb(p, q, t):
                if t < 0: t += 1
                if t > 1: t -= 1
                if t < 1/6: return p + (q-p) * 6 * t
                if t < 1/2: return q
                if t < 2/3: return p + (q-p) * (2/3-t) * 6
                return p
            q = l * (1+s) if l < 0.5 else l+s-l*s
            p = 2*l - q
            r = hue2rgb(p, q, h + 1/3)
            g = hue2rgb(p, q, h)
            b = hue2rgb(p, q, h - 1/3)
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'


class BeyondEngine:
    """Main beyond engine — applies masterpiece features to any project."""

    def __init__(self):
        self.physics = PhysicsAnimations()
        self.art = GenerativeArt()
        self.micro = MicroInteractions()
        self.scroll = ScrollStorytelling()
        self.harmony = ColorHarmony()

    def enhance(self, project, level: str = "full") -> None:
        """Add beyond-level features to existing WebProject."""
        # Add generative art background
        svg = self.art.flow_field_svg(project.spec.get('name', 'default'))
        if '<section class="hero' in project.html:
            project.html = project.html.replace(
                '<section class="hero',
                f'{svg}\n<section class="hero', 1)

        # Add noise CSS
        project.css += self.art.noise_gradient_css()
        project.css += self.micro.cursor_css()
        project.css += '\n@keyframes ripple { to { transform: scale(4); opacity: 0; } }\n'
        project.css += '\nbody { cursor: none; }\n'

        # Add all JS enhancements
        beyond_js = '\n\n'.join([
            '// ═══ BEYOND: Physics + Generative + Micro-interactions ═══',
            self.physics.spring_system(),
            self.physics.gravity_particles(),
            self.micro.cursor_glow(),
            self.micro.magnetic_buttons(),
            self.micro.text_reveal(),
            self.micro.ripple_click(),
            self.scroll.scroll_progress(),
            self.scroll.section_morph(),
        ])

        project.js += '\n\n' + beyond_js

        # Add data attributes for spring physics
        project.html = project.html.replace('class="feature-card"', 'class="feature-card" data-spring')
        project.html = project.html.replace('class="pricing-card"', 'class="pricing-card" data-spring')
        project.html = project.html.replace('class="testimonial-card"', 'class="testimonial-card" data-spring')

        # Add text-reveal class to main headings
        project.html = project.html.replace('class="hero-title', 'class="hero-title text-reveal')
        project.html = project.html.replace('class="section-title"', 'class="section-title text-reveal"')

    def generate_unique_palette(self, seed: str) -> Dict[str, str]:
        """Generate a mathematically unique palette from any seed."""
        h = int(hashlib.md5(seed.encode()).hexdigest()[:4], 16) % 360
        return self.harmony.generate_from_hue(h)


def get_beyond_engine():
    return BeyondEngine()
