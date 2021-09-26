const { hot } = require("react-hot-loader/root")

// prefer default export if available
const preferDefault = m => (m && m.default) || m


exports.components = {
  "component---cache-dev-404-page-js": hot(preferDefault(require("/mnt/c/Users/arjit39/Desktop/projects/Group10Project/Group10Project/.cache/dev-404-page.js"))),
  "component---src-pages-about-ts": hot(preferDefault(require("/mnt/c/Users/arjit39/Desktop/projects/Group10Project/Group10Project/src/pages/about.ts"))),
  "component---src-pages-help-ts": hot(preferDefault(require("/mnt/c/Users/arjit39/Desktop/projects/Group10Project/Group10Project/src/pages/help.ts"))),
  "component---src-pages-index-ts": hot(preferDefault(require("/mnt/c/Users/arjit39/Desktop/projects/Group10Project/Group10Project/src/pages/index.ts")))
}

