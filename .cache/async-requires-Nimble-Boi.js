// prefer default export if available
const preferDefault = m => (m && m.default) || m

exports.components = {
  "component---cache-dev-404-page-js": () => import("./../../dev-404-page.js" /* webpackChunkName: "component---cache-dev-404-page-js" */),
  "component---src-pages-about-ts": () => import("./../../../src/pages/about.ts" /* webpackChunkName: "component---src-pages-about-ts" */),
  "component---src-pages-help-ts": () => import("./../../../src/pages/help.ts" /* webpackChunkName: "component---src-pages-help-ts" */),
  "component---src-pages-index-ts": () => import("./../../../src/pages/index.ts" /* webpackChunkName: "component---src-pages-index-ts" */)
}

