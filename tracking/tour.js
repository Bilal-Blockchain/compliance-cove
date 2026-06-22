// ============================================================
// COMPLIANCE COVE — Guided Tour Engine (Placeholder)
// ============================================================
// React Joyride-style guided walkthrough in vanilla JS.
// SAs/CSMs/AEs can practice the demo flow before customer calls.
//
// Architecture:
//   - tourSteps[] array per demo defines target, title, text, position
//   - Floating tooltip div positions next to the target element
//   - Backdrop overlay with CSS cutout around highlighted element  
//   - Next/Back/Skip/Finish buttons
//   - Spotlight effect (darken everything except target)
//   - Step counter (1/6, 2/6...)
//   - Keyboard nav (→ next, ← back, Esc skip)
//
// Usage in any demo:
//   <script src="tour.js"></script>
//   const steps = [
//     { target: '#connectBtn', title: 'Connect Wallet', text: 'Click here to start...' },
//     { target: '.swap-card', title: 'Token Swap', text: 'Users swap tokens here...' },
//   ];
//   startTour(steps);
//
// Trigger: Add a "?" help button in the nav that calls startTour()
//
// Implementation: ~200 lines vanilla JS
// See ROADMAP.md T2 (SA Presenter Mode) for full task breakdown
// ============================================================
