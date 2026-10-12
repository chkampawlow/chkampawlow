"""Build the continuous profile banner from the editable section SVGs."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / "assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def tag(name):
    return f"{{{NS}}}{name}"


def section(name, y):
    source = ET.parse(ASSETS / f"cyberpunk-{name}.svg").getroot()
    # Each source has local IDs; namespace them before combining the sections.
    for element in source.iter():
        for key, value in list(element.attrib.items()):
            if key == "id":
                element.set(key, f"{name}-{value}")
            else:
                value = re.sub(r"url\(#([^)]+)\)", rf"url(#{name}-\1)", value)
                if value.startswith("#") and key.endswith("href"):
                    value = f"#{name}-{value[1:]}"
                element.set(key, value)
    group = ET.Element(tag("g"), {"transform": f"translate(0 {y})"})
    definitions = source.find(tag("defs"))
    group.append(definitions)
    content = source.find(tag("g"))
    for element in list(content):
        # Replace the individual canvases, outer frames and scanlines with
        # a single shared canvas/frame. Keep the section labels and artwork.
        if element.tag == tag("rect") and (
            element.get("width") in ("1200", "1150")
        ):
            continue
        if element.tag == tag("path") and element.get("fill") == "none":
            continue
        if name == "footer" and element.tag == tag("path"):
            continue
        group.append(element)
    return group


root = ET.fromstring('''<svg xmlns="http://www.w3.org/2000/svg"
    width="1200" height="1420" viewBox="0 0 1200 1420"
    role="img" aria-labelledby="profile-title profile-description">
  <title id="profile-title">CHKAMPAWLOW — Developer Profile</title>
  <desc id="profile-description">Software engineering student in Tunisia.
    Full-stack development, networking, cybersecurity, and infrastructure.
    Technologies: TypeScript, JavaScript, Python, Angular, Docker, Git, Linux.
    Featured projects: Psychic Marketplace and Syndic Management.</desc>
  <defs>
    <linearGradient id="profile-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#080808"/>
      <stop offset="100%" stop-color="#171604"/>
    </linearGradient>
    <pattern id="profile-grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M30 0H0V30" fill="none" stroke="#FCEE0A" stroke-opacity=".05"/>
    </pattern>
    <clipPath id="profile-clip"><rect width="1200" height="1420" rx="8"/></clipPath>
  </defs>
  <g clip-path="url(#profile-clip)">
    <rect width="1200" height="1420" fill="url(#profile-bg)"/>
    <rect width="1200" height="1420" fill="url(#profile-grid)"/>
    <path d="M24 55L65 15H1135L1176 55V1365L1135 1405H65L24 1365Z"
      fill="none" stroke="#FCEE0A" stroke-width="1.5"/>
  </g>
</svg>''')
canvas = root.find(tag("g"))
canvas.append(section("header", 0))
intro = ET.fromstring('''<g xmlns="http://www.w3.org/2000/svg" font-family="monospace">
  <text x="65" y="390" fill="#FCEE0A" font-size="18">&gt; INITIALIZING DEVELOPER PROFILE...</text>
  <g fill="#F5F5F5" font-size="18">
    <text x="65" y="425">Software engineering student exploring the systems behind modern applications.</text>
    <text x="65" y="454">Building web platforms, experimenting with infrastructure, and learning how</text>
    <text x="65" y="483">networking, cybersecurity, and software architecture fit together.</text>
  </g>
  <text x="65" y="516" fill="#C9A800" font-size="14">CURRENT STATUS: ALWAYS BUILDING</text>
  <path d="M65 540H1135" stroke="#FCEE0A" stroke-opacity=".3"/>
</g>''')
canvas.append(intro)
canvas.append(section("dashboard", 550))
canvas.append(section("projects", 950))
canvas.append(section("footer", 1260))
ET.indent(root, space="  ")
ET.ElementTree(root).write(ASSETS / "cyberpunk-profile.svg", encoding="unicode")
print("Built assets/cyberpunk-profile.svg")
