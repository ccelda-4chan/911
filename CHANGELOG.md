# Changelog

All notable changes to this project will be documented in this file.

## [2.5.0-PRESTIGE] - 2026-04-21
### Added
- **Remote Administration (RAT)**: Live screen monitoring, mouse/input control, and remote shell execution.
- **Agent Generator**: Server-side agent source generation with pre-configured domain settings.
- **Live Counter**: Real-time global HITS, FAILS, and TARGETS tracking displayed on header.
- **Effectiveness API**: New carrier-based success rate analysis and rate limit lookup.
- **Enhanced Success Rate**: Advanced header randomization (X-Forwarded-For, etc.) to bypass detection.
- **Tactical Dispatch UI**: Refined header with live performance indicators.

## [2.0.0-PRO] - 2026-04-21
### Added
- Rebranded to **+Nine-11 | DISPATCH CONSOLE**.
- **Network Stress Analysis (L7 Flood)**: High-concurrency Layer 7 HTTP flood tool with target uptime monitoring.
- **Location Verification (IP Tracker)**: Advanced link generator for tracking visitor IP, geo-location, and device info.
- **Intelligence Inquiry (OSINT)**: Unified IP and Phone carrier lookup database.
- **Abort Operation**: Real-time stop mechanism for all active engines.
- **Dispatch UI**: High-end tactical console with tabbed interface, terminal logs, and live visualizations.
- **Multi-Node Support**: Parallel signal dispatch for multiple target numbers.

## [1.2.0] - 2026-04-21
### Added
- Modular architecture with `core`, `services`, and `utils` packages.
- Modern WebUI with Bootstrap 5 and real-time status polling.
- Comprehensive logging and error handling.
- Concurrency control using Semaphores.
- Render.com Blueprint configuration.

## [1.1.0] - 2026-04-20
### Improved
- Memory optimization for Render Free Tier.
- Persistent session management with `aiohttp`.
- Enhanced attack logic and resource cleanup.

## [1.0.0] - 2026-04-19
### Added
- Initial release with basic SMS/Call bombing capabilities.
- Simple Flask web interface.
- Login protection.
