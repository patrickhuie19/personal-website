const fs = require('fs');
const path = require('path');

// Create a minimal routes-manifest.json for Vercel
const routesManifest = {
  version: 3,
  pages404: true,
  basePath: '',
  redirects: [],
  rewrites: [],
  headers: []
};

const outDir = path.join(process.cwd(), 'out');
const manifestPath = path.join(outDir, 'routes-manifest.json');

// Ensure out directory exists
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Write the manifest file
fs.writeFileSync(manifestPath, JSON.stringify(routesManifest, null, 2));
console.log('Created routes-manifest.json for Vercel');


