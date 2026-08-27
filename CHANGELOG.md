# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Note on historical versions:** this repository had no Git tags when the
> changelog was introduced. The entries below were reconstructed from the commit
> history, so the version numbers are retroactive labels for meaningful
> milestones rather than tags that existed at the time.

## [Unreleased]

### Added

- `LICENSE` declaring the repository copyrighted and restricted, with all rights
  reserved, referenced from `README.md`.
- Continuous integration workflow that validates HTML, markdown, JavaScript
  syntax and site metadata on every push and pull request.
- Tag-triggered release workflow that publishes a GitHub Release using the
  matching section of this changelog as the release notes.
- Dependabot configuration that keeps GitHub Actions dependencies current on a
  weekly schedule.
- `scripts/check-site-consistency.py`, which verifies that `sitemap.xml`,
  `robots.txt`, `site.webmanifest` and the canonical URL stay in sync with
  `index.html` and the domain declared in `CNAME`.
- Canonical link tag on the home page, matching the existing `og:url` and
  `twitter:url` metadata.
- `.gitignore` covering macOS and local tooling output.
- This changelog.

### Fixed

- Encoded six raw `&` characters as `&amp;` in the page title and body copy.
- Added an explicit `type="button"` attribute to the mobile navigation toggle so
  it cannot behave as an implicit submit button.
- Repaired two corrupted characters (U+FFFD replacement characters) in
  `README.md`.
- Corrected the `README.md` license section, which advertised an MIT license and
  linked to a `LICENSE` file that did not exist. The repository is not open
  source, and the README now states the restricted terms and links to the new
  `LICENSE`.

## [1.2.0] - 2026-02-01

### Changed

- Expanded the Deutsche Börse case study with data platform and AI foundation
  details ([#2](https://github.com/trsdn/about-me/pull/2)).

## [1.1.0] - 2025-12-18

### Changed

- Redesigned the site around the "Structured Elegance" theme, introducing a dark
  hero section, gold accents and editorial typography.

## [1.0.0] - 2025-07-03

### Added

- Rich snippets and expanded Schema.org structured data for publications.
- Google Search Console verification file.
- Complete favicon set generated with favicon.io, replacing the inline SVG
  favicon.
- GitHub Copilot instructions describing the development workflow.

### Changed

- Major performance pass targeting PageSpeed Insights: critical CSS inlined,
  non-critical resources deferred and the profile image reduced by 88%.
- Reordered sections so that case studies follow skills, and moved Education
  ahead of Publications in both the navigation and the sitemap.
- Reduced the testimonials to three optimised quotes.
- Cleaned up the case studies section by removing emojis and redundant buttons.

### Fixed

- Restored profile image scaling to 150px with `object-fit: cover`.
- Corrected a typo and improved wording consistency in the testimonials.

## [0.2.0] - 2025-06-27

### Added

- SEO foundation: `robots.txt`, `sitemap.xml`, Open Graph tags, Twitter Cards
  and Schema.org structured data.
- Education section.
- Mobile navigation menu.
- Content Security Policy that enforces HTTPS and removes mixed content
  warnings.

### Fixed

- Mobile responsiveness, covering text sizing, small-screen layout and content
  padding.
- Case study loading on mobile, by throttling scroll events and improving the
  `IntersectionObserver` fallbacks.
- Content visibility while scrolling.
- Accessibility defects, alongside the first favicon.

## [0.1.0] - 2025-06-26

### Added

- Initial personal website presenting case studies, experience and
  publications.
- Custom domain configuration for `www.aitorsten.com`.
- Project README.

[Unreleased]: https://github.com/trsdn/about-me/compare/d30ad31...HEAD
[1.2.0]: https://github.com/trsdn/about-me/compare/d20bf57...d30ad31
[1.1.0]: https://github.com/trsdn/about-me/compare/2dd1ca4...d20bf57
[1.0.0]: https://github.com/trsdn/about-me/compare/fb1804e...2dd1ca4
[0.2.0]: https://github.com/trsdn/about-me/compare/9d41204...fb1804e
[0.1.0]: https://github.com/trsdn/about-me/commits/9d41204
