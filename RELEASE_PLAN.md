# Island in the Sky — release plan

**Planning only. No game release, website deployment, or backend service is authorized by this plan.** The public repository name is `island-in-the-sky`, maintained by spinjitsu12. The game's current working title and existing technical assets can remain Floating Island Sanctuary until a separate game-branding decision.

## What exists now

The current project is a Godot 4.7.2 asset inspection prototype: a floating landform, lighting/atmosphere, review camera, and pipeline tests. It has no landscape-building gameplay, progression, save system, wildlife, or finished sanctuary. There is no packaged executable or browser game. The public repository can showcase the foundation; its permission-required license does not grant general rights to run, modify, or reuse it beyond applicable law and GitHub's terms.

## Recommended release direction

Build the core experience as an offline, single-player desktop game with local saves. That suits the calm sanctuary concept and preserves the native Forward+ visual baseline. Networking is not required for terrain building, planting, water, decoration, or wildlife. Keep accounts, cloud services, and multiplayer outside the first playable slice.

Online island visiting is a planned future feature: players will eventually be able to visit other people's sanctuaries. The offline foundation is the first stage, not a permanent restriction on online features. No networking implementation or hosting setup is included now.

| Surface | Planned role | Gate before delivery |
| --- | --- | --- |
| Public GitHub repository | Project presentation, public documentation, and permitted technical review | Re-run privacy/history audit; keep proprietary notice and third-party notices |
| Windows `.exe` package | Native playable build for Windows players | Matching Godot export templates, actual Windows testing, complete package/assets, clear build label |
| macOS `.app` package | Native playable build for Mac players | Matching templates, Mac testing, packaging, signing/notarization plan for public distribution |
| Vercel website | Screenshots, trailer, project information, and links to approved downloads | Separate site review and deployment approval |
| Render services | Candidate backend for future island publishing, visiting permissions, accounts, and optional cloud saves | Backend design, privacy/access rules, costs and operations reviewed; provider selection deferred |
| Browser demo | Optional small, optimized experience later | Separate Compatibility/WebGL 2 visual/performance pass and browser testing |

Render can also host a static website; use one website host initially rather than adding infrastructure without a feature that needs it. Native Windows/Mac builds run on players' devices, not on Vercel or Render. The website can link to approved release downloads, for example GitHub Releases, when builds are ready.

## Why desktop first

Godot's current web export uses Compatibility/WebGL 2, not Forward+/Mobile. A browser version therefore needs a separate quality and performance target; deploying existing Forward+ content to a website does not preserve its rendering features automatically. Keep the premium desktop target primary, and evaluate a lightweight browser preview later.

## Milestone sequence

1. Finish the original visual-language study: terrain/rock transitions, foliage, water, atmospheric cloud depth, and a restrained architecture motif.
2. Build and test one satisfying playable sanctuary transformation with local saves and reversible edits. Avoid adding accounts or management complexity.
3. Produce private Windows and Mac test packages after installing matching export templates. Label preliminary packages as prototypes, not a finished game. Test on both target platforms.
4. Define player distribution terms. The current repository license requires express written permission; before offering public play, add a separate narrow player license allowing installation and personal play while reserving source/asset reuse rights. Choose free/paid distribution separately.
5. Only after explicit release approval, publish tested desktop packages and an optional website with download links. For a smooth Mac download experience, arrange signing/notarization rather than assuming local execution proves distribution readiness.
6. Develop the planned online island-visiting feature after the local sanctuary experience is stable. Its release timing and backend provider remain undecided. Evaluate a browser demo separately.

## Future island visits — planned, not implemented

- Give islands and reusable assets stable identifiers and versioned, render-independent save data so a future service can share island state without uploading arbitrary executable Godot scenes.
- Proposed first version: an owner publishes an island snapshot, and permitted visitors explore it read-only. Owners control visibility, update publication, and revoke access. Live co-presence is a later design decision, not implied by snapshot visits.
- Keep visitor sessions separate from the owner's editable local island. Visiting must not alter the owner's terrain, placed objects, or progress without an explicitly designed permission model.
- Add authentication, server-side ownership/access checks, validated island data, and bounded downloads in that later stage. Visiting consent and content access must be clear to both owners and visitors.
- Preserve offline creation and local saving. A service outage must not prevent players from tending their own local sanctuary.

These are architecture and product plans only. No accounts, server, online synchronization, visitor editing, or live multiplayer have been built.

No release date, price, backend, hosting purchase, player-license grant, or deployment is selected by this plan. Repository publication and playable-game release are separate decisions.

## Technical references

- [Godot Windows export](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_windows.html)
- [Godot macOS export and signing](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html)
- [Godot web rendering and browser limitations](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html)
- [Vercel hosting documentation](https://vercel.com/docs)
- [Render static sites](https://render.com/docs/static-sites)
