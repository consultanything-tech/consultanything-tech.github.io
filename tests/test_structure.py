#!/usr/bin/env python3
"""Automated verification test for site structure, SEO metadata, and design tokens."""

import json
import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestSiteStructure(unittest.TestCase):
    """Test suite verifying presence, semantics, and standards compliance of site assets."""

    @classmethod
    def setUpClass(cls):
        cls.index_path = REPO_ROOT / "index.html"
        cls.css_path = REPO_ROOT / "assets" / "css" / "styles.css"
        cls.js_path = REPO_ROOT / "assets" / "js" / "main.js"
        cls.robots_path = REPO_ROOT / "robots.txt"
        cls.sitemap_path = REPO_ROOT / "sitemap.xml"
        cls.og_png_path = REPO_ROOT / "assets" / "images" / "og-card.png"
        cls.workflow_path = REPO_ROOT / ".github" / "workflows" / "deploy.yml"

    def test_01_index_file_exists(self):
        """Verify index.html exists."""
        self.assertTrue(self.index_path.exists(), "index.html must exist at repo root")

    def test_02_html5_doctype_and_root_attributes(self):
        """Verify HTML5 doctype, lang attribute, charset, and responsive viewport."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        self.assertRegex(
            content,
            r"<!DOCTYPE\s+html>",
            "index.html must declare <!DOCTYPE html>",
        )
        self.assertRegex(
            content,
            r"<html\s+[^>]*lang=[\"']en[\"']",
            "<html> root tag must include lang='en'",
        )
        self.assertRegex(
            content,
            r"<meta\s+charset=[\"']utf-8[\"']",
            "index.html must specify utf-8 charset",
        )
        self.assertRegex(
            content,
            r"<meta\s+name=[\"']viewport[\"']\s+content=[\"']width=device-width,\s*initial-scale=1\.0[\"']",
            "index.html must configure standard responsive viewport",
        )

    def test_03_seo_and_social_metadata(self):
        """Verify essential SEO tags, canonical URL, OpenGraph, and Twitter card tags."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        self.assertRegex(
            content,
            r"<title>.*(?:ConsultAnythingTech|CATech).*</title>",
            "<title> must include 'CATech' or 'ConsultAnythingTech'",
        )
        self.assertRegex(
            content,
            r"<meta\s+name=[\"']description[\"']\s+content=[\"'][^\"']+[\"']",
            "Meta description must be defined and non-empty",
        )
        self.assertRegex(
            content,
            r"<link\s+[^>]*rel=[\"']canonical[\"']\s+[^>]*href=[\"']https://(?:catech\.dev|consultanything-tech\.github\.io)/?[\"']",
            "Canonical link must point to https://catech.dev/ or https://consultanything-tech.github.io/",
        )

        # OpenGraph tags
        for og_prop in ["og:title", "og:description", "og:type", "og:url", "og:image"]:
            self.assertRegex(
                content,
                rf"<meta\s+property=[\"']{re.escape(og_prop)}[\"']\s+content=[\"'][^\"']+[\"']",
                f"Missing or invalid OpenGraph property: {og_prop}",
            )

        # Twitter Card tags
        for twitter_name in ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]:
            self.assertRegex(
                content,
                rf"<meta\s+name=[\"']{re.escape(twitter_name)}[\"']\s+content=[\"'][^\"']+[\"']",
                f"Missing or invalid Twitter Card property: {twitter_name}",
            )

    def test_04_json_ld_structured_data(self):
        """Verify valid JSON-LD schema for Organization / ProfessionalService."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        pattern = r"<script\s+type=[\"']application/ld\+json[\"']>(.*?)</script>"
        matches = re.findall(pattern, content, flags=re.DOTALL)
        self.assertGreater(
            len(matches),
            0,
            "index.html must contain at least one JSON-LD script block",
        )

        parsed_any = False
        for block in matches:
            try:
                data = json.loads(block.strip())
                parsed_any = True
                type_val = data.get("@type", "")
                name_val = data.get("name", "")
                url_val = data.get("url", "")

                is_org_or_service = type_val in ["Organization", "ProfessionalService"]
                has_name = any(n in name_val for n in ["ConsultAnythingTech", "CATech"])
                has_url = any(u in url_val for u in ["consultanything-tech.github.io", "catech.dev"])

                if is_org_or_service and has_name and has_url:
                    break
            except json.JSONDecodeError as err:
                self.fail(f"Invalid JSON in application/ld+json: {err}")
        else:
            self.fail(
                "JSON-LD must specify @type as Organization or ProfessionalService with name 'CATech' or 'ConsultAnythingTech' and URL 'https://catech.dev' or 'https://consultanything-tech.github.io'"
            )

    def test_05_navigation_and_accessibility(self):
        """Verify navigation header, key links, brand, and accessible mobile toggle."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        # Brand name
        has_brand = any(b in content for b in ["ConsultAnythingTech", "CATech"])
        self.assertTrue(has_brand, "Navigation must display CATech or ConsultAnythingTech brand")

        # Required section links
        expected_links = ["#services", "#products", "#capabilities", "#about", "#contact"]
        for target in expected_links:
            self.assertRegex(
                content,
                rf"href=[\"']{re.escape(target)}[\"']",
                f"Navigation must contain link with target {target}",
            )

        # Mobile menu toggle button accessibility attributes
        self.assertRegex(
            content,
            r"<button[^>]*aria-label=[\"'][^\"']+[\"'][^>]*aria-expanded=[\"'](true|false)[\"']",
            "Mobile navigation button must specify accessible aria-label and aria-expanded attributes",
        )
        self.assertRegex(
            content,
            r"<button[^>]*id=[\"']mobile-menu-btn[\"'][^>]*aria-controls=[\"']mobile-menu[\"']|"
            r"<button[^>]*aria-controls=[\"']mobile-menu[\"'][^>]*id=[\"']mobile-menu-btn[\"']",
            "Mobile navigation button must have aria-controls='mobile-menu'",
        )

        # Skip link and main landmark target
        self.assertRegex(
            content,
            r"<a[^>]*href=[\"']#main-content[\"'][^>]*>[^<]*Skip to main content[^<]*</a>",
            "index.html must include accessible skip to main content link",
        )
        self.assertRegex(
            content,
            r"<main[^>]*id=[\"']main-content[\"']",
            "<main> landmark must have id='main-content' as target for skip link",
        )
        self.assertRegex(
            content,
            r"<main[^>]*id=[\"']main-content[\"'][^>]*tabindex=[\"']-1[\"']|<main[^>]*tabindex=[\"']-1[\"'][^>]*id=[\"']main-content[\"']",
            "<main id='main-content'> landmark must have tabindex='-1' for programmatic focus handling",
        )

    def test_06_external_scripts_and_styles(self):
        """Verify Tailwind CSS script and custom stylesheet inclusion."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        self.assertRegex(
            content,
            r"<script[^>]*src=[\"']https://cdn\.tailwindcss\.com[\"']",
            "Tailwind CDN script must be linked in index.html",
        )
        self.assertRegex(
            content,
            r"<link[^>]*href=[\"']assets/css/styles\.css[\"']",
            "Custom stylesheet assets/css/styles.css must be linked in index.html",
        )

    def test_07_css_motion_tokens_and_reduced_motion(self):
        """Verify motion tokens and prefers-reduced-motion media query in styles.css."""
        self.assertTrue(self.css_path.exists(), "assets/css/styles.css must exist")
        css_content = self.css_path.read_text(encoding="utf-8")

        required_tokens = ["--duration-fast", "--ease-standard"]
        for token in required_tokens:
            self.assertIn(token, css_content, f"Missing motion token {token} in styles.css")

        self.assertIn(
            "@media (prefers-reduced-motion: reduce)",
            css_content,
            "styles.css must contain @media (prefers-reduced-motion: reduce) block",
        )

    def test_08_robots_and_sitemap(self):
        """Verify presence and validity of robots.txt and sitemap.xml."""
        self.assertTrue(self.robots_path.exists(), "robots.txt must exist at repo root")
        self.assertTrue(self.sitemap_path.exists(), "sitemap.xml must exist at repo root")

        robots_content = self.robots_path.read_text(encoding="utf-8")
        self.assertRegex(
            robots_content,
            r"Sitemap:\s*https://(?:catech\.dev|consultanything-tech\.github\.io)/sitemap\.xml",
            "robots.txt must reference sitemap.xml",
        )
        self.assertIn("User-agent: *", robots_content, "robots.txt must declare User-agent: *")
        self.assertIn("Allow: /", robots_content, "robots.txt must declare Allow: /")

        sitemap_content = self.sitemap_path.read_text(encoding="utf-8")
        self.assertRegex(
            sitemap_content,
            r"https://(?:catech\.dev|consultanything-tech\.github\.io)",
            "sitemap.xml must specify site url",
        )
        self.assertIn("<urlset", sitemap_content)
        self.assertIn("<url>", sitemap_content)

    def test_09_hero_section(self):
        """Verify hero section has engagement badge, headline, CTAs, and engineering metrics."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        # Hero section exists
        self.assertRegex(content, r'<section\s+[^>]*id=["\']hero["\']', "Missing #hero section")

        # Status / engagement badge (e.g. accepting Q1/Q2 engagements or available for new projects)
        self.assertRegex(
            content,
            r"(?i)(?:Accepting\s+(?:new\s+)?Q[1-4](?:/Q[1-4])?\s+(?:client\s+)?engagements|Available\s+for\s+(?:Q[1-4]|new\s+projects))",
            "Hero section must include status/engagement badge (e.g. accepting Q1/Q2 engagements or available for new projects)",
        )

        # Primary and secondary CTA buttons linking to #contact and #products or #services
        hero_match = re.search(r'<section\s+[^>]*id=["\']hero["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(hero_match, "#hero section content could not be extracted")
        hero_content = hero_match.group(1)

        self.assertRegex(
            hero_content,
            r'href=["\']#contact["\']',
            "Hero section must include a primary CTA linking to #contact",
        )
        self.assertRegex(
            hero_content,
            r'href=["\']#(?:products|services)["\']',
            "Hero section must include a secondary CTA linking to #products or #services",
        )

        # Key technical metric highlights or trust signals
        has_metrics = any(
            metric in hero_content
            for metric in ["99.99%", "50ms", "100%", "7+", "24h", "Full", "Direct"]
        )
        self.assertTrue(
            has_metrics,
            "Hero section must feature key technical metrics or trust signals",
        )

    def test_10_services_section(self):
        """Verify services section contains header and 4 core technical service cards."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        services_match = re.search(r'<section\s+[^>]*id=["\']services["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(services_match, "#services section content could not be extracted")
        services_content = services_match.group(1)

        # Descriptive section header
        self.assertRegex(
            services_content,
            r'(?s)<h2[^>]*>.*?(?:Services|Consulting).*?</h2>',
            "Services section must have descriptive h2 header",
        )

        # 4 core service cards with distinct technical domains
        core_services = [
            "Distributed Cloud & Systems Architecture",
            "High-Performance Native & Web Engineering",
            "AI Systems & Agentic Workflows",
            "Security Hardening & Performance Optimization",
        ]
        for service_title in core_services:
            self.assertIn(
                service_title,
                services_content,
                f"Services section must contain service card for '{service_title}'",
            )

        # Deliverables and technology tags/badges check
        for tag in ["Kubernetes", "Rust", "PyTorch", "eBPF"]:
            self.assertIn(
                tag,
                services_content,
                f"Services section should showcase modern technology tag '{tag}'",
            )

        # Checkmarks in deliverable list must have aria-hidden="true"
        deliverable_svgs = re.findall(r'<li[^>]*>\s*(<svg[^>]*>)', services_content)
        self.assertGreater(len(deliverable_svgs), 0, "Services section must contain deliverable items with checkmark svgs")
        for svg_tag in deliverable_svgs:
            self.assertIn(
                'aria-hidden="true"',
                svg_tag,
                f"Checkmark SVG in deliverable list must include aria-hidden='true': {svg_tag}",
            )

    def test_11_og_card_image(self):
        """Verify assets/images/og-card.png exists and is a valid non-empty file."""
        self.assertTrue(self.og_png_path.exists(), "assets/images/og-card.png must exist on disk")
        self.assertGreater(self.og_png_path.stat().st_size, 0, "assets/images/og-card.png must not be empty")

    def test_12_products_section_portfolio_showcase(self):
        """Verify products section has h2 heading, category tabs, and 4 in-house product cards."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        products_match = re.search(r'<section\s+[^>]*id=["\']products["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(products_match, "#products section must exist")
        products_content = products_match.group(1)

        # Heading check with id="products-heading"
        self.assertRegex(
            products_content,
            r'(?s)<h2[^>]*id=["\']products-heading["\'][^>]*>.*?</h2>',
            "#products section must have an h2 heading with id='products-heading'",
        )

        # Products grid with aria-labelledby="products-heading"
        self.assertRegex(
            products_content,
            r'<div[^>]*id=["\']products-grid["\'][^>]*aria-labelledby=["\']products-heading["\']|<div[^>]*aria-labelledby=["\']products-heading["\'][^>]*id=["\']products-grid["\']',
            "#products-grid must specify aria-labelledby='products-heading'",
        )

        # Accessible category filter tabs (role="tablist", role="tab", aria-selected="true" for active filter)
        self.assertRegex(
            products_content,
            r'role=["\']tablist["\']',
            "#products section must contain category filter tabs with role='tablist'",
        )
        self.assertRegex(
            products_content,
            r'role=["\']tab["\'][^>]*aria-selected=["\']true["\']|aria-selected=["\']true["\'][^>]*role=["\']tab["\']',
            "#products category tabs must have role='tab' and an active filter with aria-selected='true'",
        )

        # Roving tabindex: active tab tabindex="0", inactive tabs tabindex="-1"
        self.assertRegex(
            products_content,
            r'<button[^>]*id=["\']tab-all["\'][^>]*tabindex=["\']0["\']|<button[^>]*tabindex=["\']0["\'][^>]*id=["\']tab-all["\']',
            "Active filter tab #tab-all must have tabindex='0'",
        )
        for inactive_id in ["tab-apps", "tab-ai", "tab-web"]:
            self.assertRegex(
                products_content,
                rf'<button[^>]*id=["\']{inactive_id}["\'][^>]*tabindex=["\']-1["\']|<button[^>]*tabindex=["\']-1["\'][^>]*id=["\']{inactive_id}["\']',
                f"Inactive filter tab #{inactive_id} must have tabindex='-1'",
            )

        # 4 in-house projects
        projects = {
            "HyperFetch": ["Swift", "macOS", "SwiftUI"],
            "ProofPath": ["TypeScript", "Multi-Agent"],
            "IndiaCrafted": ["Next.js", "Edge"],
            "SpendWise": ["Financial planning"],
        }
        for proj_name, keywords in projects.items():
            self.assertIn(
                proj_name,
                products_content,
                f"#products must contain product card for '{proj_name}'",
            )
            for kw in keywords:
                self.assertIn(
                    kw,
                    products_content,
                    f"#products card for '{proj_name}' must include technology/domain keyword '{kw}'",
                )

        # Each product card must have data-category attribute for interactive filtering
        self.assertRegex(
            products_content,
            r'data-category=["\'][^"\']+["\']',
            "#products cards must include data-category attributes for filtering",
        )

        # Links to repositories with descriptive accessible names
        for proj_name in projects.keys():
            self.assertRegex(
                products_content,
                rf'(?s){proj_name}.*?<a\s+[^>]*href=["\'](https://github\.com/[^"\']+|#[^"\']+|https?://[^"\']+)["\']',
                f"#products card for '{proj_name}' must contain a project/repo link",
            )
            self.assertRegex(
                products_content,
                rf'(?s){proj_name}.*?<a\s+[^>]*aria-label=["\']View {proj_name} repository on GitHub \(opens in new tab\)["\']',
                f"#products card for '{proj_name}' must have descriptive aria-label including project name and '(opens in new tab)'",
            )

        # Verify JS implements roving tabindex and 250ms duration matching design tokens
        js_content = self.js_path.read_text(encoding="utf-8")
        self.assertIn(
            'tab.setAttribute("tabindex", isSelected ? "0" : "-1");',
            js_content,
            "main.js must update tabindex on filter tabs during selection",
        )
        self.assertIn(
            "250",
            js_content,
            "main.js hiding transition timeout must align with --duration-normal (250ms)",
        )

    def test_13_capabilities_section(self):
        """Verify capabilities section has h2 and categorized technical stacks."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        cap_match = re.search(r'<section\s+[^>]*id=["\']capabilities["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(cap_match, "#capabilities section must exist")
        cap_content = cap_match.group(1)

        # Has an h2 heading
        self.assertRegex(
            cap_content,
            r'(?s)<h2[^>]*>.*?(?:Technical Capabilities|Tools &amp; Technologies|Capabilities).*?</h2>',
            "#capabilities section must have an h2 heading",
        )

        # Categorized stacks
        categories = [
            r"Languages(?:\s*&|\s+and)?\s+Systems",
            r"Cloud(?:\s*&|\s+and|\s*/)?\s*(?:Edge\s+)?Infrastructure",
            r"(?:Modern\s+)?Web\s+Frameworks",
            r"AI(?:\s*&|\s+and)?\s+Security",
        ]
        for cat_regex in categories:
            self.assertRegex(
                cap_content,
                rf'(?i){cat_regex}',
                f"#capabilities section must contain category matching '{cat_regex}'",
            )

        # Sample technologies in categories
        for tech in ["Rust", "Go", "TypeScript", "Swift", "Kubernetes", "Next.js", "PyTorch"]:
            self.assertIn(
                tech,
                cap_content,
                f"#capabilities section must include technical skill chip '{tech}'",
            )

    def test_14_about_section(self):
        """Verify about section has h2 heading and outlines core engineering principles."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        about_match = re.search(r'<section\s+[^>]*id=["\']about["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(about_match, "#about section must exist")
        about_content = about_match.group(1)

        # Has an h2 heading
        self.assertRegex(
            about_content,
            r'(?s)<h2[^>]*>.*?About (?:CATech|ConsultAnythingTech).*?</h2>',
            "#about section must have an h2 heading",
        )

        # Core engineering principles
        principles = [
            r"Zero-Bloat|Minimal\s+Dependencies|keep\s+things\s+simple|Less\s+is\s+more",
            r"Production\s+Verification|Test-Driven|test\s+before\s+we\s+ship|Tested",
            r"Senior(?:\s+Technical)?\s+Leadership|Engineering\s+Pragmatism|work\s+directly\s+with\s+us|Senior\s+engineers",
        ]
        for principle in principles:
            self.assertRegex(
                about_content,
                rf'(?i){principle}',
                f"#about section must outline core principle matching '{principle}'",
            )

    def test_15_contact_section_and_form(self):
        """Verify contact section has h2, accessible form with required inputs, and direct contact links."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        contact_match = re.search(r'<section\s+[^>]*id=["\']contact["\'][^>]*>(.*?)</section>', content, re.DOTALL)
        self.assertIsNotNone(contact_match, "#contact section must exist")
        contact_content = contact_match.group(1)

        # Has an h2 heading
        self.assertRegex(
            contact_content,
            r'(?s)<h2[^>]*>.*?</h2>',
            "#contact section must have an h2 heading",
        )

        # Contact form with id="contact-form"
        self.assertRegex(
            contact_content,
            r'<form\s+[^>]*id=["\']contact-form["\']',
            "#contact section must contain a form with id='contact-form'",
        )

        # Accessible inputs: Name, Email, Service, Message, Submit button
        self.assertRegex(
            contact_content,
            r'<input[^>]*id=["\']contact-name["\'][^>]*required|<input[^>]*required[^>]*id=["\']contact-name["\']',
            "Name input with id='contact-name' and required attribute must exist",
        )
        self.assertRegex(
            contact_content,
            r'<input[^>]*id=["\']contact-email["\'][^>]*type=["\']email["\'][^>]*required|'
            r'<input[^>]*type=["\']email["\'][^>]*id=["\']contact-email["\'][^>]*required|'
            r'<input[^>]*required[^>]*id=["\']contact-email["\'][^>]*type=["\']email["\']',
            "Email input with id='contact-email', type='email', and required attribute must exist",
        )
        self.assertRegex(
            contact_content,
            r'id=["\']contact-service["\']',
            "Service selection input/select with id='contact-service' must exist",
        )
        self.assertRegex(
            contact_content,
            r'<textarea[^>]*id=["\']contact-message["\'][^>]*required|<textarea[^>]*required[^>]*id=["\']contact-message["\']',
            "Message textarea with id='contact-message' and required attribute must exist",
        )
        self.assertRegex(
            contact_content,
            r'<button[^>]*type=["\']submit["\']',
            "Submit button with type='submit' must exist in contact section",
        )

        # Accessible error/status container
        self.assertRegex(
            contact_content,
            r'(?:aria-live=["\'](?:polite|assertive)["\']|role=["\']alert["\'])',
            "Contact section must include accessible live region or alert container for status messages",
        )

        # Direct mailto, phone, WhatsApp, and GitHub links
        has_email = any(
            email in contact_content
            for email in ["hello@catech.dev", "consultanythingtech@gmail.com"]
        )
        self.assertTrue(
            has_email,
            "Contact section must display email hello@catech.dev or consultanythingtech@gmail.com",
        )
        self.assertRegex(
            contact_content,
            r'href=["\']mailto:(?:hello@catech\.dev|consultanythingtech@gmail\.com)["\']',
            "Contact section must provide direct mailto link",
        )
        self.assertIn(
            "+65 88240325",
            contact_content,
            "Contact section must display contact number +65 88240325",
        )
        self.assertRegex(
            contact_content,
            r'href=["\']tel:\+6588240325["\']',
            "Contact section must provide direct tel:+6588240325 link",
        )
        self.assertRegex(
            contact_content,
            r'href=["\']https://wa\.me/6588240325\?text=[^"\']+["\']',
            "Contact section must provide direct WhatsApp initiator link with pre-filled message",
        )
        self.assertRegex(
            contact_content,
            r'href=["\']https://github\.com/consultanything-tech["\']',
            "Contact section must provide link to GitHub organization",
        )

    def test_16_footer_and_interactions(self):
        """Verify footer dynamic copyright year, back-to-top button, and JS/CSS validation handlers."""
        self.assertTrue(self.index_path.exists(), "index.html missing")
        content = self.index_path.read_text(encoding="utf-8")

        # Footer element
        footer_match = re.search(r'<footer\s*[^>]*>(.*?)</footer>', content, re.DOTALL)
        self.assertIsNotNone(footer_match, "<footer> element must exist")
        footer_content = footer_match.group(1)

        # Dynamic copyright year element
        self.assertRegex(
            footer_content,
            r'id=["\']copyright-year["\']',
            "Footer must contain element with id='copyright-year'",
        )

        # Back-to-top button
        self.assertRegex(
            content,
            r'<button[^>]*id=["\']back-to-top["\']|<a[^>]*id=["\']back-to-top["\']|<a[^>]*href=["\']#main-content["\'][^>]*class=["\'][^"\']*back-to-top',
            "Page must contain back-to-top button with id='back-to-top'",
        )

        # main.js handlers for form validation, copyright year, and back-to-top
        js_content = self.js_path.read_text(encoding="utf-8")
        self.assertIn("contact-form", js_content, "main.js must reference #contact-form for validation")
        self.assertIn("copyright-year", js_content, "main.js must update #copyright-year")
        self.assertIn("getFullYear()", js_content, "main.js must compute current year using getFullYear()")
        self.assertIn("back-to-top", js_content, "main.js must handle back-to-top button interaction")

        # styles.css form focus and error states
        css_content = self.css_path.read_text(encoding="utf-8")
        self.assertIn(".input-error", css_content, "styles.css must define .input-error styling")

    def test_17_github_actions_workflow(self):
        """Verify GitHub Actions deployment workflow and HTML polish attributes."""
        # 1. Workflow file exists
        self.assertTrue(
            self.workflow_path.exists(),
            ".github/workflows/deploy.yml must exist",
        )
        workflow_content = self.workflow_path.read_text(encoding="utf-8")

        # 2. Push trigger for main and workflow_dispatch
        self.assertRegex(
            workflow_content,
            r'push:\s*\n\s*branches:\s*\n\s*-\s*main',
            "Workflow must trigger on push to main branch",
        )
        self.assertIn(
            "workflow_dispatch:",
            workflow_content,
            "Workflow must support workflow_dispatch trigger",
        )

        # 3. Permissions: pages: write, id-token: write, contents: read
        self.assertRegex(
            workflow_content,
            r'pages:\s*write',
            "Workflow must specify pages: write permission",
        )
        self.assertRegex(
            workflow_content,
            r'id-token:\s*write',
            "Workflow must specify id-token: write permission",
        )
        self.assertRegex(
            workflow_content,
            r'contents:\s*read',
            "Workflow must specify contents: read permission",
        )

        # 4. Executes test suite python3 tests/test_structure.py
        self.assertIn(
            "python3 tests/test_structure.py",
            workflow_content,
            "Workflow must execute python3 tests/test_structure.py",
        )

        # 5. Uses actions/upload-pages-artifact@v3 and actions/deploy-pages@v4
        self.assertIn(
            "actions/upload-pages-artifact@v3",
            workflow_content,
            "Workflow must use actions/upload-pages-artifact@v3",
        )
        self.assertIn(
            "actions/deploy-pages@v4",
            workflow_content,
            "Workflow must use actions/deploy-pages@v4",
        )

        # 6. Verify index.html tabindex="-1" on #form-status and native fallback on #contact-form
        index_content = self.index_path.read_text(encoding="utf-8")
        self.assertRegex(
            index_content,
            r'<div[^>]*id=["\']form-status["\'][^>]*tabindex=["\']-1["\']|<div[^>]*tabindex=["\']-1["\'][^>]*id=["\']form-status["\']',
            "#form-status must have tabindex='-1' for programmatic accessibility focus",
        )
        self.assertRegex(
            index_content,
            r'<form[^>]*id=["\']contact-form["\'][^>]*action=["\'](?:https://api\.web3forms\.com/submit|mailto:[^"\']+)["\']|<form[^>]*action=["\'](?:https://api\.web3forms\.com/submit|mailto:[^"\']+)["\'][^>]*id=["\']contact-form["\']',
            "#contact-form must have valid submission action (Web3Forms endpoint or mailto fallback)",
        )
        self.assertRegex(
            index_content,
            r'<form[^>]*id=["\']contact-form["\'][^>]*method=["\']POST["\']|<form[^>]*method=["\']POST["\'][^>]*id=["\']contact-form["\']',
            "#contact-form must have method='POST' as fallback or submission method",
        )
        self.assertRegex(
            index_content,
            r'<form[^>]*id=["\']contact-form["\'][^>]*enctype=["\']text/plain["\']|<form[^>]*enctype=["\']text/plain["\'][^>]*id=["\']contact-form["\']|<form[^>]*id=["\']contact-form["\'][^>]*novalidate|<form[^>]*novalidate[^>]*id=["\']contact-form["\']',
            "#contact-form must configure fallback or validation attributes",
        )

    def test_18_brand_logos_and_concepts(self):
        """Verify presence of 4 distinct logo SVG options, primary logos, and interactive preview modal."""
        logo_dir = REPO_ROOT / "assets" / "logos"
        self.assertTrue(logo_dir.exists(), "assets/logos directory must exist")

        expected_logos = [
            "option-1-hex-prism.svg",
            "option-2-interlocking-monogram.svg",
            "option-3-circuit-delta.svg",
            "option-4-infinity-code.svg",
            "logo.svg",
            "logo-mark.svg",
        ]

        for filename in expected_logos:
            logo_path = logo_dir / filename
            self.assertTrue(logo_path.exists(), f"Missing logo file: assets/logos/{filename}")
            content = logo_path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 100, f"Logo {filename} appears too small or empty")
            self.assertIn("<svg", content, f"Logo {filename} must be valid SVG")
            self.assertIn("</svg>", content, f"Logo {filename} must have closing svg tag")

        # Verify index.html uses primary logo SVG in header and footer
        index_content = self.index_path.read_text(encoding="utf-8")
        self.assertRegex(
            index_content,
            r'assets/logos/(?:logo-mark\.svg|logo\.svg)',
            "index.html must embed or link assets/logos/logo-mark.svg or logo.svg",
        )

        # Verify interactive logo concepts modal / preview element exists
        self.assertRegex(
            index_content,
            r'id=["\']logo-modal["\']|id=["\']logo-drawer["\']|id=["\']logo-concepts["\']',
            "index.html must contain an interactive modal or drawer for exploring logo concepts",
        )
        for opt in ["option-1-hex-prism", "option-2-interlocking-monogram", "option-3-circuit-delta", "option-4-infinity-code"]:
            self.assertIn(
                opt,
                index_content,
                f"Logo concepts modal in index.html must reference {opt}",
            )

        # Verify logo-mark.svg reflects Option 4 Möbius Infinity Code emblem
        logo_mark_content = (logo_dir / "logo-mark.svg").read_text(encoding="utf-8")
        self.assertRegex(
            logo_mark_content,
            r'(?i)(?:inf-grad|Möbius|infinity|stroke-width=["\']10["\'])',
            "assets/logos/logo-mark.svg must reflect Option 4 Möbius Infinity Code emblem",
        )

        # Verify Option 4 is marked as Active Official Logo in the modal
        self.assertIn(
            "Active Official Logo",
            index_content,
            "index.html #logo-modal must display 'Active Official Logo' badge on Option 4",
        )

    def test_19_floating_whatsapp_initiator(self):
        """Verify floating quick-contact WhatsApp initiator button exists and is configured properly."""
        index_content = self.index_path.read_text(encoding="utf-8")

        # Floating WhatsApp initiator button
        self.assertRegex(
            index_content,
            r'id=["\']floating-whatsapp["\']|<a[^>]*href=["\']https://wa\.me/6588240325\?text=[^"\']+["\'][^>]*class=["\'][^"\']*fixed',
            "index.html must contain a floating WhatsApp quick-contact initiator button",
        )
        self.assertRegex(
            index_content,
            r'https://wa\.me/6588240325\?text=Hello%20(?:ConsultAnythingTech|CATech)%2C%20I%27m%20reaching%20out%20from%20your%20official%20website',
            "WhatsApp link must contain pre-filled message identifying visitor from official website",
        )

    def test_20_expanded_project_portfolio(self):
        """Verify portfolio showcase contains all live client platforms and open-source public repos."""
        index_content = self.index_path.read_text(encoding="utf-8")

        # Required public platforms & repositories
        portfolio_items = {
            "SPSLNT": "https://www.spslnt.org.sg/",
            "The 1494": "https://the1494.com/",
            "ScienceHub": "https://sciencehub.experthub.store/",
            "HyperFetch": "https://github.com/consultanything-tech/hyperfetch-app",
            "ProofPath": "https://github.com/consultanything-tech/ProofPath",
            "IndiaCrafted": "https://github.com/consultanything-tech/indiacrafted-homepage-mockup",
            "SpendWise": "https://spendwise.experthub.store/",
        }

        for name, expected_url in portfolio_items.items():
            self.assertIn(
                name,
                index_content,
                f"index.html must feature project '{name}' in portfolio showcase",
            )
            self.assertIn(
                expected_url,
                index_content,
                f"index.html must link project '{name}' to public URL '{expected_url}'",
            )

        # Retain SpendWise GitHub repo link
        self.assertIn(
            "https://github.com/consultanything-tech/spendwise",
            index_content,
            "index.html must retain SpendWise repository link",
        )

    def test_21_hero_canvas_constellation(self):
        """Verify ambient 2D canvas constellation field in hero section."""
        index_content = self.index_path.read_text(encoding="utf-8")
        js_content = self.js_path.read_text(encoding="utf-8")
        css_content = self.css_path.read_text(encoding="utf-8")

        # 1. Canvas element exists inside #hero with aria-hidden="true"
        self.assertRegex(
            index_content,
            r'<canvas[^>]*id=["\']hero-canvas["\'][^>]*aria-hidden=["\']true["\']',
            "index.html must contain <canvas id='hero-canvas' aria-hidden='true'> inside hero section",
        )

        # 2. JS contains particle animation, mouse interaction, and reduced motion guard
        self.assertIn("initHeroCanvas", js_content, "main.js must define or invoke initHeroCanvas")
        self.assertIn("requestAnimationFrame", js_content, "main.js canvas must use requestAnimationFrame")
        self.assertRegex(
            js_content,
            r'addEventListener\(\s*["\']mousemove["\']|mousemove|pointermove',
            "main.js canvas must track pointer movement for interactive constellation attraction",
        )
        self.assertRegex(
            js_content,
            r'prefers-reduced-motion:\s*reduce',
            "main.js canvas must respect prefers-reduced-motion: reduce",
        )

        # 3. CSS positions #hero-canvas with pointer-events: none and z-index
        self.assertRegex(
            css_content,
            r'#hero-canvas\s*\{[^}]*pointer-events:\s*none',
            "styles.css must style #hero-canvas with pointer-events: none",
        )
        self.assertRegex(
            css_content,
            r'#hero-canvas\s*\{[^}]*z-index:\s*0',
            "styles.css must style #hero-canvas with z-index: 0",
        )


if __name__ == "__main__":
    unittest.main()
