"""
AXIMA Web Generator — Single-file HTML/CSS/JS website generator
Built by: Ghias + Kiro | 2026

Input: "build a landing page for a coffee shop"
Output: Complete, deployable HTML file with embedded CSS + JS

No frameworks. No dependencies. Just clean HTML that works.
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass, field


@dataclass
class WebSpec:
    """Parsed specification for the website."""
    business_type: str = ""       # coffee shop, portfolio, restaurant, etc.
    business_name: str = ""       # extracted or generated name
    style: str = "modern"         # modern, minimal, bold, elegant
    color_scheme: str = "warm"    # warm, cool, dark, light, vibrant
    sections: List[str] = field(default_factory=list)  # hero, about, menu, contact, etc.
    features: List[str] = field(default_factory=list)  # animations, form, gallery, etc.
    page_type: str = "landing"    # landing, portfolio, blog, ecommerce


class WebParser:
    """Parse user request into WebSpec."""

    BUSINESS_TYPES = {
        'coffee': 'coffee shop', 'cafe': 'cafe', 'restaurant': 'restaurant',
        'pizza': 'pizza place', 'bakery': 'bakery', 'bar': 'bar',
        'gym': 'gym', 'fitness': 'fitness studio', 'yoga': 'yoga studio',
        'salon': 'salon', 'spa': 'spa', 'barber': 'barbershop',
        'portfolio': 'portfolio', 'agency': 'agency', 'startup': 'startup',
        'saas': 'saas', 'app': 'app landing', 'product': 'product',
        'photography': 'photography', 'music': 'music artist',
        'doctor': 'medical clinic', 'dentist': 'dental clinic',
        'lawyer': 'law firm', 'real estate': 'real estate',
        'school': 'school', 'course': 'online course',
        'ecommerce': 'ecommerce', 'shop': 'online shop', 'store': 'store',
    }

    def parse(self, request: str) -> WebSpec:
        spec = WebSpec()
        req = request.lower()

        # Detect business type
        for key, btype in self.BUSINESS_TYPES.items():
            if key in req:
                spec.business_type = btype
                break
        if not spec.business_type:
            spec.business_type = "business"

        # Extract business name (if in quotes or after "called")
        name_match = re.search(r'["\']([^"\']+)["\']', request)
        if name_match:
            spec.business_name = name_match.group(1)
        else:
            called_match = re.search(r'called\s+([A-Z][A-Za-z\s&]+)', request)
            if called_match:
                spec.business_name = called_match.group(1).strip()
            else:
                named_match = re.search(r'named\s+([A-Z][A-Za-z\s&]+)', request)
                if named_match:
                    spec.business_name = named_match.group(1).strip()
                else:
                    spec.business_name = self._generate_name(spec.business_type)

        # Detect style
        if any(w in req for w in ['minimal', 'clean', 'simple']): spec.style = "minimal"
        elif any(w in req for w in ['bold', 'loud', 'vibrant']): spec.style = "bold"
        elif any(w in req for w in ['elegant', 'luxury', 'premium']): spec.style = "elegant"
        elif any(w in req for w in ['dark', 'night', 'black']): spec.style = "dark"

        # Detect color scheme
        if any(w in req for w in ['dark', 'black', 'night']): spec.color_scheme = "dark"
        elif any(w in req for w in ['blue', 'cool', 'tech']): spec.color_scheme = "cool"
        elif any(w in req for w in ['green', 'nature', 'organic']): spec.color_scheme = "nature"
        elif any(w in req for w in ['red', 'bold', 'energy']): spec.color_scheme = "vibrant"

        # Decide sections based on business type
        spec.sections = self._decide_sections(spec.business_type, spec.page_type)

        # Detect features
        if any(w in req for w in ['form', 'contact', 'email']): spec.features.append("contact_form")
        if any(w in req for w in ['gallery', 'photos', 'images']): spec.features.append("gallery")
        if any(w in req for w in ['animation', 'animated', 'scroll']): spec.features.append("animations")
        if any(w in req for w in ['testimonial', 'review']): spec.features.append("testimonials")

        return spec

    def _generate_name(self, btype: str) -> str:
        names = {
            'coffee shop': 'Brew & Co', 'cafe': 'The Daily Grind',
            'restaurant': 'Saveur', 'pizza place': 'Slice House',
            'bakery': 'Golden Crust', 'bar': 'The Nightcap',
            'gym': 'Iron Core', 'fitness studio': 'PulseFit',
            'yoga studio': 'Still Waters', 'salon': 'Luxe Studio',
            'spa': 'Serenity', 'barbershop': 'Sharp Edge',
            'portfolio': 'Alex Chen', 'agency': 'Pixel & Code',
            'startup': 'LaunchPad', 'saas': 'FlowStack',
            'app landing': 'AppName', 'product': 'ProductX',
            'photography': 'Lens & Light', 'music artist': 'The Artist',
            'medical clinic': 'CareFirst', 'dental clinic': 'BrightSmile',
            'law firm': 'Sterling & Associates', 'real estate': 'HomeVault',
        }
        return names.get(btype, 'MyBusiness')

    def _decide_sections(self, btype: str, page_type: str) -> List[str]:
        base = ["hero", "about"]
        if btype in ('coffee shop', 'cafe', 'restaurant', 'pizza place', 'bakery', 'bar'):
            return base + ["menu", "gallery", "testimonials", "contact"]
        elif btype in ('gym', 'fitness studio', 'yoga studio'):
            return base + ["classes", "pricing", "trainers", "contact"]
        elif btype in ('salon', 'spa', 'barbershop'):
            return base + ["services", "pricing", "gallery", "contact"]
        elif btype in ('portfolio', 'photography', 'music artist'):
            return base + ["work", "skills", "contact"]
        elif btype in ('agency', 'startup', 'saas', 'app landing', 'product'):
            return base + ["features", "pricing", "testimonials", "cta"]
        elif btype in ('medical clinic', 'dental clinic', 'law firm'):
            return base + ["services", "team", "testimonials", "contact"]
        else:
            return base + ["services", "contact"]


# ═══════════════════════════════════════════════════════════════
# STYLE ENGINE — Colors, fonts, CSS
# ═══════════════════════════════════════════════════════════════

class StyleEngine:
    """Generate CSS from spec."""

    COLORS = {
        "warm": {"primary": "#c8553d", "secondary": "#f28f3b", "bg": "#fefae0", "text": "#2b2d42", "accent": "#588b8b"},
        "cool": {"primary": "#2563eb", "secondary": "#7c3aed", "bg": "#f8fafc", "text": "#1e293b", "accent": "#06b6d4"},
        "dark": {"primary": "#8b5cf6", "secondary": "#ec4899", "bg": "#0f172a", "text": "#f1f5f9", "accent": "#22d3ee"},
        "nature": {"primary": "#16a34a", "secondary": "#65a30d", "bg": "#f0fdf4", "text": "#1a2e05", "accent": "#84cc16"},
        "vibrant": {"primary": "#dc2626", "secondary": "#f97316", "bg": "#fffbeb", "text": "#1c1917", "accent": "#eab308"},
    }

    FONTS = {
        "modern": ("'Inter', sans-serif", "'Inter', sans-serif"),
        "minimal": ("'DM Sans', sans-serif", "'DM Sans', sans-serif"),
        "bold": ("'Poppins', sans-serif", "'Space Grotesk', sans-serif"),
        "elegant": ("'Playfair Display', serif", "'Lato', sans-serif"),
        "dark": ("'JetBrains Mono', monospace", "'Inter', sans-serif"),
    }

    def generate_css(self, spec: WebSpec) -> str:
        colors = self.COLORS.get(spec.color_scheme, self.COLORS["warm"])
        heading_font, body_font = self.FONTS.get(spec.style, self.FONTS["modern"])

        css = f"""* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary: {colors['primary']};
    --secondary: {colors['secondary']};
    --bg: {colors['bg']};
    --text: {colors['text']};
    --accent: {colors['accent']};
    --heading-font: {heading_font};
    --body-font: {body_font};
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: var(--body-font);
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
}}

h1, h2, h3 {{
    font-family: var(--heading-font);
    line-height: 1.2;
}}

a {{
    color: var(--primary);
    text-decoration: none;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Navigation */
nav {{
    position: fixed;
    top: 0;
    width: 100%;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
    background: {'rgba(15,23,42,0.95)' if spec.color_scheme == 'dark' else 'rgba(255,255,255,0.95)'};
    backdrop-filter: blur(10px);
    border-bottom: 1px solid {'rgba(255,255,255,0.1)' if spec.color_scheme == 'dark' else 'rgba(0,0,0,0.05)'};
}}

nav .logo {{
    font-family: var(--heading-font);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}}

nav .nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

nav .nav-links a {{
    color: var(--text);
    font-weight: 500;
    transition: color 0.3s;
}}

nav .nav-links a:hover {{
    color: var(--primary);
}}

/* Hero Section */
.hero {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 6rem 2rem;
    background: {'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)' if spec.color_scheme == 'dark' else f'linear-gradient(135deg, {colors["bg"]} 0%, white 100%)'};
}}

.hero h1 {{
    font-size: clamp(2.5rem, 6vw, 5rem);
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.hero p {{
    font-size: 1.25rem;
    max-width: 600px;
    margin: 0 auto 2rem;
    opacity: 0.8;
}}

.btn {{
    display: inline-block;
    padding: 0.875rem 2rem;
    background: var(--primary);
    color: white;
    border-radius: 0.5rem;
    font-weight: 600;
    transition: transform 0.3s, box-shadow 0.3s;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

.btn-outline {{
    background: transparent;
    border: 2px solid var(--primary);
    color: var(--primary);
}}

/* Sections */
section {{
    padding: 5rem 2rem;
}}

section h2 {{
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
}}

/* Grid layouts */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}}

.card {{
    background: {'rgba(30,41,59,0.5)' if spec.color_scheme == 'dark' else 'white'};
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card h3 {{
    margin-bottom: 0.75rem;
    color: var(--primary);
}}

/* Contact Form */
.contact-form {{
    max-width: 500px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.contact-form input,
.contact-form textarea {{
    padding: 0.875rem 1rem;
    border: 2px solid {'rgba(255,255,255,0.1)' if spec.color_scheme == 'dark' else '#e2e8f0'};
    border-radius: 0.5rem;
    font-size: 1rem;
    background: {'rgba(15,23,42,0.5)' if spec.color_scheme == 'dark' else 'white'};
    color: var(--text);
    transition: border-color 0.3s;
}}

.contact-form input:focus,
.contact-form textarea:focus {{
    outline: none;
    border-color: var(--primary);
}}

/* Footer */
footer {{
    text-align: center;
    padding: 2rem;
    opacity: 0.6;
    font-size: 0.875rem;
}}

/* Responsive */
@media (max-width: 768px) {{
    nav .nav-links {{
        display: none;
    }}
    .hero h1 {{
        font-size: 2.5rem;
    }}
    section {{
        padding: 3rem 1rem;
    }}
}}

/* Animations */
.fade-in {{
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s, transform 0.6s;
}}

.fade-in.visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""
        return css


# ═══════════════════════════════════════════════════════════════
# SECTION GENERATORS
# ═══════════════════════════════════════════════════════════════

class SectionGenerator:
    """Generate HTML sections from spec."""

    def generate_nav(self, spec: WebSpec) -> str:
        links = ''.join(f'<li><a href="#{s}">{s.capitalize()}</a></li>' for s in spec.sections[1:])
        return f'''<nav>
    <div class="logo">{spec.business_name}</div>
    <ul class="nav-links">{links}</ul>
</nav>'''

    def generate_hero(self, spec: WebSpec) -> str:
        taglines = {
            'coffee shop': 'Where every cup tells a story',
            'cafe': 'Your neighborhood escape',
            'restaurant': 'A culinary experience like no other',
            'pizza place': 'Crafted with passion, baked to perfection',
            'bakery': 'Fresh from the oven, made with love',
            'gym': 'Transform your body. Transform your life.',
            'fitness studio': 'Push your limits. Find your strength.',
            'yoga studio': 'Find your center. Find your peace.',
            'salon': 'Where beauty meets artistry',
            'spa': 'Relax. Restore. Renew.',
            'portfolio': 'Designer & Developer',
            'agency': 'We build digital experiences that matter',
            'startup': 'The future starts here',
            'saas': 'Simplify your workflow. Amplify your results.',
        }
        tagline = taglines.get(spec.business_type, 'Excellence in everything we do')

        return f'''<section class="hero" id="hero">
    <div class="container">
        <h1>{spec.business_name}</h1>
        <p>{tagline}</p>
        <a href="#contact" class="btn">Get Started</a>
    </div>
</section>'''

    def generate_about(self, spec: WebSpec) -> str:
        descriptions = {
            'coffee shop': 'We source the finest beans from around the world and roast them to perfection. Every cup is a journey — from the highlands of Ethiopia to your morning ritual.',
            'restaurant': 'Our chefs blend tradition with innovation, creating dishes that honor the ingredients while surprising your palate. Farm to table, heart to plate.',
            'gym': 'More than a gym — a community. State-of-the-art equipment, expert trainers, and a culture that pushes you to be your best.',
            'salon': 'Our team of stylists brings years of expertise and creative vision to every appointment. Your look, elevated.',
            'agency': 'We combine strategy, design, and technology to create digital products that people love. From concept to launch, we are your partner.',
            'startup': 'We are on a mission to solve real problems with elegant solutions. Built by engineers, designed for humans.',
        }
        desc = descriptions.get(spec.business_type,
            f'Welcome to {spec.business_name}. We are passionate about what we do and committed to delivering exceptional experiences to our customers.')

        return f'''<section id="about" class="fade-in">
    <div class="container">
        <h2>About Us</h2>
        <p style="max-width:700px;margin:0 auto;text-align:center;font-size:1.1rem;">{desc}</p>
    </div>
</section>'''

    def generate_menu(self, spec: WebSpec) -> str:
        items = [
            ("Espresso", "Rich, bold, and smooth", "$4"),
            ("Cappuccino", "Perfectly frothed, perfectly balanced", "$5"),
            ("Latte", "Silky milk meets golden espresso", "$5.50"),
            ("Cold Brew", "Slow-steeped for 18 hours", "$5"),
            ("Matcha Latte", "Ceremonial grade, oat milk", "$6"),
            ("Pastries", "Fresh-baked daily, rotating selection", "$4"),
        ]
        cards = ''.join(f'''<div class="card">
            <h3>{name}</h3><p>{desc}</p><p style="font-weight:700;color:var(--primary);margin-top:0.5rem;">{price}</p>
        </div>''' for name, desc, price in items)
        return f'''<section id="menu" class="fade-in">
    <div class="container">
        <h2>Our Menu</h2>
        <div class="grid">{cards}</div>
    </div>
</section>'''

    def generate_services(self, spec: WebSpec) -> str:
        service_map = {
            'gym': [("Personal Training", "1-on-1 sessions tailored to your goals"),
                   ("Group Classes", "HIIT, Spin, Boxing, Yoga & more"),
                   ("Nutrition Coaching", "Custom meal plans that fuel results")],
            'salon': [("Cuts & Styling", "From classic to contemporary"),
                     ("Color", "Balayage, highlights, vivids"),
                     ("Treatments", "Keratin, deep conditioning, scalp therapy")],
            'agency': [("Web Design", "Beautiful, responsive, conversion-focused"),
                      ("Development", "Full-stack engineering that scales"),
                      ("Branding", "Strategy, identity, and voice")],
        }
        services = service_map.get(spec.business_type, [
            ("Service One", "Excellence delivered consistently"),
            ("Service Two", "Quality you can count on"),
            ("Service Three", "Results that speak for themselves"),
        ])
        cards = ''.join(f'<div class="card"><h3>{name}</h3><p>{desc}</p></div>' for name, desc in services)
        return f'''<section id="services" class="fade-in">
    <div class="container">
        <h2>Our Services</h2>
        <div class="grid">{cards}</div>
    </div>
</section>'''

    def generate_features(self, spec: WebSpec) -> str:
        features = [
            ("Lightning Fast", "Built for speed. Every millisecond counts."),
            ("Secure by Default", "Enterprise-grade security out of the box."),
            ("Scales Infinitely", "From 10 users to 10 million. No changes needed."),
        ]
        cards = ''.join(f'<div class="card"><h3>{name}</h3><p>{desc}</p></div>' for name, desc in features)
        return f'''<section id="features" class="fade-in">
    <div class="container">
        <h2>Features</h2>
        <div class="grid">{cards}</div>
    </div>
</section>'''

    def generate_pricing(self, spec: WebSpec) -> str:
        plans = [
            ("Starter", "$29/mo", ["5 projects", "Basic analytics", "Email support"]),
            ("Pro", "$79/mo", ["Unlimited projects", "Advanced analytics", "Priority support", "Custom integrations"]),
            ("Enterprise", "Custom", ["Dedicated account manager", "SLA guarantee", "Custom development", "On-premise option"]),
        ]
        cards = ''
        for name, price, feats in plans:
            feat_html = ''.join(f'<li>{f}</li>' for f in feats)
            highlight = ' style="border:2px solid var(--primary);transform:scale(1.05);"' if name == "Pro" else ''
            cards += f'<div class="card"{highlight}><h3>{name}</h3><p style="font-size:2rem;font-weight:700;color:var(--primary);margin:1rem 0;">{price}</p><ul style="list-style:none;margin-bottom:1.5rem;">{feat_html}</ul><a href="#contact" class="btn" style="width:100%;text-align:center;">Choose Plan</a></div>'
        return f'''<section id="pricing" class="fade-in">
    <div class="container">
        <h2>Pricing</h2>
        <div class="grid">{cards}</div>
    </div>
</section>'''

    def generate_testimonials(self, spec: WebSpec) -> str:
        testimonials = [
            ("Best experience I have ever had. Absolutely recommend.", "Sarah M."),
            ("Changed my life. I tell everyone about this place.", "James K."),
            ("Professional, friendly, and consistently excellent.", "Priya R."),
        ]
        cards = ''.join(f'<div class="card"><p style="font-style:italic;margin-bottom:1rem;">"{text}"</p><p style="font-weight:700;">— {name}</p></div>' for text, name in testimonials)
        return f'''<section id="testimonials" class="fade-in">
    <div class="container">
        <h2>What People Say</h2>
        <div class="grid">{cards}</div>
    </div>
</section>'''

    def generate_contact(self, spec: WebSpec) -> str:
        return f'''<section id="contact" class="fade-in">
    <div class="container">
        <h2>Get In Touch</h2>
        <form class="contact-form" onsubmit="handleSubmit(event)">
            <input type="text" placeholder="Your Name" required>
            <input type="email" placeholder="Your Email" required>
            <textarea rows="4" placeholder="Your Message" required></textarea>
            <button type="submit" class="btn">Send Message</button>
        </form>
    </div>
</section>'''

    def generate_cta(self, spec: WebSpec) -> str:
        return f'''<section id="cta" style="text-align:center;padding:5rem 2rem;background:linear-gradient(135deg,var(--primary),var(--secondary));">
    <div class="container">
        <h2 style="color:white;margin-bottom:1rem;">Ready to get started?</h2>
        <p style="color:rgba(255,255,255,0.8);margin-bottom:2rem;">Join thousands who already trust us.</p>
        <a href="#contact" class="btn" style="background:white;color:var(--primary);">Start Free Trial</a>
    </div>
</section>'''

    def generate_section(self, section_name: str, spec: WebSpec) -> str:
        generators = {
            'hero': self.generate_hero,
            'about': self.generate_about,
            'menu': self.generate_menu,
            'services': self.generate_services,
            'features': self.generate_features,
            'pricing': self.generate_pricing,
            'testimonials': self.generate_testimonials,
            'contact': self.generate_contact,
            'cta': self.generate_cta,
        }
        gen = generators.get(section_name)
        if gen:
            return gen(spec)
        return ""


# ═══════════════════════════════════════════════════════════════
# MAIN ENGINE
# ═══════════════════════════════════════════════════════════════

class WebGenerator:
    """Generate complete HTML page from request."""

    def __init__(self):
        self.parser = WebParser()
        self.style_engine = StyleEngine()
        self.section_gen = SectionGenerator()

    def generate(self, request: str) -> str:
        """Generate a complete HTML page from natural language request."""
        spec = self.parser.parse(request)
        css = self.style_engine.generate_css(spec)
        nav = self.section_gen.generate_nav(spec)

        sections_html = '\n\n'.join(
            self.section_gen.generate_section(s, spec)
            for s in spec.sections
        )

        js = self._generate_js(spec)

        # Pick Google Font imports based on style
        font_imports = {
            "modern": "Inter:wght@400;500;600;700",
            "minimal": "DM+Sans:wght@400;500;700",
            "bold": "Poppins:wght@400;600;700|Space+Grotesk:wght@400;700",
            "elegant": "Playfair+Display:wght@400;700|Lato:wght@400;700",
            "dark": "JetBrains+Mono:wght@400;700|Inter:wght@400;500",
        }
        font = font_imports.get(spec.style, font_imports["modern"])

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{spec.business_name} — {spec.business_type.title()}</title>
    <link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>

{nav}

{sections_html}

<footer>
    <p>&copy; 2026 {spec.business_name}. All rights reserved.</p>
</footer>

<script>
{js}
</script>

</body>
</html>'''
        return html

    def _generate_js(self, spec: WebSpec) -> str:
        return '''// Scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Form handler
function handleSubmit(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.textContent = 'Sent!';
    btn.style.background = 'var(--accent)';
    setTimeout(() => {
        btn.textContent = 'Send Message';
        btn.style.background = 'var(--primary)';
        e.target.reset();
    }, 2000);
}

// Nav background on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        nav.style.boxShadow = 'none';
    }
});'''


def get_web_generator():
    return WebGenerator()
