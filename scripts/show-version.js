const fs = require('fs');
const path = require('path');

// Read the root package.json
const rootPackagePath = path.join(__dirname, '..', 'package.json');
const rootPackage = JSON.parse(fs.readFileSync(rootPackagePath, 'utf8'));

console.log('\n📦 OrchestrateIQ Version Information\n');
console.log('━'.repeat(50));
console.log(`Current Version: ${rootPackage.version}`);
console.log('━'.repeat(50));

// Check frontend version
const frontendPackagePath = path.join(__dirname, '..', 'frontend', 'package.json');
if (fs.existsSync(frontendPackagePath)) {
    const frontendPackage = JSON.parse(fs.readFileSync(frontendPackagePath, 'utf8'));
    console.log(`Frontend:        ${frontendPackage.version}`);
}

// Check VERSION file
const versionFilePath = path.join(__dirname, '..', 'VERSION');
if (fs.existsSync(versionFilePath)) {
    const versionFile = fs.readFileSync(versionFilePath, 'utf8').trim();
    console.log(`VERSION file:    ${versionFile}`);
}

console.log('━'.repeat(50));
console.log('\n💡 To update version, run:');
console.log('   npm run version:patch  (1.0.0 → 1.0.1)');
console.log('   npm run version:minor  (1.0.0 → 1.1.0)');
console.log('   npm run version:major  (1.0.0 → 2.0.0)\n');
