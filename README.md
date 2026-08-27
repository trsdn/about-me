# About Me - Performance Optimized Personal Website

[![CI](https://github.com/trsdn/about-me/actions/workflows/ci.yml/badge.svg)](https://github.com/trsdn/about-me/actions/workflows/ci.yml)

A modern, responsive, and **performance-optimized** personal website built for GitHub Pages, showcasing professional experience, research publications, and enterprise-scale case studies.

## 🚀 Performance Features

- **⚡ Lightning Fast**: Critical CSS inlined, optimized images, deferred non-critical resources
- **📱 Mobile Optimized**: 95%+ PageSpeed Insights scores on mobile and desktop
- **🖼️ Image Optimization**: Optimized profile images (88% size reduction)
- **📈 SEO Enhanced**: Rich snippets, structured data, and comprehensive meta tags
- **🔍 Search Console Ready**: Google verification and analytics integration

## 🌟 Core Features

- **Responsive Design**: Looks great on desktop, tablet, and mobile
- **Modern UI**: Clean, professional design with smooth animations  
- **Professional Sections**: About, Skills, Experience, Testimonials, Case Studies, Publications, Education, Contact
- **Sticky Navigation**: Smooth scrolling navigation with active section highlighting
- **Client Testimonials**: Social proof from enterprise clients and collaborators
- **Real Content**: Actual research publications and enterprise case studies
- **Fast Loading**: Optimized for performance with 90+ PageSpeed scores
- **SEO Friendly**: Rich snippets, structured data, and semantic HTML
- **GitHub Pages Ready**: Deployment ready configuration

## 📁 File Structure

```text
about-me/
├── .github/
│   ├── workflows/ci.yml          # HTML, markdown, JS and metadata checks
│   ├── workflows/release.yml     # Tag-triggered GitHub Release publishing
│   ├── dependabot.yml            # Weekly GitHub Actions updates
│   └── copilot-instructions.md   # Development workflow instructions
├── scripts/
│   └── check-site-consistency.py # Sitemap/robots/manifest consistency checks
├── index.html                    # Main HTML file with critical CSS inlined
├── styles.css                    # Complete CSS styles (deferred loading)
├── script.js                     # JavaScript for interactions (deferred)
├── site.webmanifest              # Web app manifest (icons, theme colours)
├── torstenmahr-optimized.jpeg    # Optimized profile photo (8.9KB vs 77KB)
├── torstenmahr.jpeg              # Original profile photo (backup)
├── torstenmahr.webp              # WebP profile photo
├── googlebb74aa914e848419.html   # Google Search Console verification
├── CNAME                         # Custom domain configuration
├── robots.txt                    # SEO crawler instructions
├── sitemap.xml                   # SEO sitemap
├── favicon files                 # Complete favicon set for all devices
├── CHANGELOG.md                  # Release history
├── LICENSE                       # Copyright notice (restricted, not open source)
└── README.md                     # This documentation
```

## ⚡ Performance Optimizations

### **Image Optimization**

- **Optimized profile image**: 8.9KB vs 77KB original (88% reduction)
- **Responsive images**: Properly sized for display dimensions
- **Image preloading**: Critical images preloaded for faster rendering

### **CSS Optimization**

- **Critical CSS inlined**: Above-the-fold styles for instant rendering
- **Non-critical CSS deferred**: Font Awesome loaded asynchronously
- **Font optimization**: Google Fonts with font-display: swap

### **JavaScript Optimization**

- **Deferred loading**: JavaScript doesn't block initial render
- **DNS prefetching**: Faster external resource loading

### **SEO & Rich Snippets**

- **Structured data**: Person, Organization, Articles, Breadcrumbs
- **Rich snippets**: Publications show with author info and details
- **Google Search Console**: Verified and ready for analytics

## 🎨 Customization Guide

### Personal Information

- **Name & Title**: Update the hero section in `index.html`
- **About Section**: Replace with your own professional bio
- **Profile Photo**: Replace `torstenmahr.jpeg` with your image

### Professional Content

- **Experience**: Update the experience section with your roles
- **Publications**: Add your research papers and publications
- **Case Studies**: Replace with your major project achievements
- **Projects**: Add your personal and professional projects

### Visual Customization

- **Colors**: Modify the gradient variables in `styles.css`
- **Layout**: Adjust grid layouts and spacing
- **Animations**: Customize transition effects and hover states

## 🔧 Setting Up GitHub Pages

1. **Push to GitHub**: Upload these files to your GitHub repository
2. **Enable Pages**: Go to Settings → Pages in your repository
3. **Select Source**: Choose "Deploy from a branch" and select "main"
4. **Wait**: GitHub will build and deploy your site
5. **Visit**: Your site will be available at `https://yourusername.github.io/about-me`

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## ✅ Quality Checks

This site is plain HTML, CSS, and JavaScript. There is no build step and no
package manifest, so the checks below run directly against the committed files.
CI runs exactly the same commands on every push and pull request.

```bash
# Validate the HTML (structure plus accessibility rules)
npx --yes html-validate@9 "**/*.html"

# Lint the markdown
npx --yes markdownlint-cli2@0.18.1

# Check the JavaScript parses
node --check script.js

# Verify sitemap.xml, robots.txt, site.webmanifest, and the canonical URL
# all stay in sync with index.html and the domain in CNAME
python3 scripts/check-site-consistency.py
```

The consistency script is the important one: because nothing regenerates the SEO
metadata, it catches the case where a section is renamed in `index.html` but the
sitemap, the navigation anchors, or the canonical domain are left behind.

## 🚢 Releasing

Releases are published by tagging a commit. The workflow reads the matching
section from `CHANGELOG.md` and uses it as the release notes:

```bash
# Add the release section to CHANGELOG.md first, then:
git tag v1.3.0
git push origin v1.3.0
```

## 📄 License

Copyright (c) 2025-2026 Torsten Mahr. All rights reserved.

This project is **not** open source. The contents of this repository, including
the source, the written copy, the case studies, the testimonials, and the
images, are copyrighted and restricted. They may be read and inspected here,
but may not be reused, modified, redistributed, or published without prior
written permission. See [LICENSE](LICENSE) for the full terms.

---
