const fs = require('fs');
const path = require('path');

// Read the root package.json to get the new version
const rootPackagePath = path.join(__dirname, '..', 'package.json');
const rootPackage = JSON.parse(fs.readFileSync(rootPackagePath, 'utf8'));
const newVersion = rootPackage.version;

console.log(`\n🔄 Updating version to ${newVersion} across all packages...\n`);

// Update frontend package.json
const frontendPackagePath = path.join(__dirname, '..', 'frontend', 'package.json');
if (fs.existsSync(frontendPackagePath)) {
  const frontendPackage = JSON.parse(fs.readFileSync(frontendPackagePath, 'utf8'));
  frontendPackage.version = newVersion;
  fs.writeFileSync(frontendPackagePath, JSON.stringify(frontendPackage, null, 2) + '\n');
  console.log(`✅ Updated frontend/package.json to version ${newVersion}`);
}

// Update CHANGELOG.md
const changelogPath = path.join(__dirname, '..', 'CHANGELOG.md');
if (fs.existsSync(changelogPath)) {
  const changelog = fs.readFileSync(changelogPath, 'utf8');
  const today = new Date().toISOString().split('T')[0];
  
  // Check if this version already exists in the changelog
  if (!changelog.includes(`## [${newVersion}]`)) {
    const newEntry = `\n## [${newVersion}] - ${today}\n\n### Changed\n- Version bump to ${newVersion}\n- [Add your changes here]\n`;
    
    // Insert after the first header
    const lines = changelog.split('\n');
    const insertIndex = lines.findIndex(line => line.startsWith('## ['));
    
    if (insertIndex !== -1) {
      lines.splice(insertIndex, 0, newEntry);
      fs.writeFileSync(changelogPath, lines.join('\n'));
      console.log(`✅ Updated CHANGELOG.md with version ${newVersion}`);
    }
  }
}

// Create/Update VERSION file
const versionFilePath = path.join(__dirname, '..', 'VERSION');
fs.writeFileSync(versionFilePath, newVersion);
console.log(`✅ Updated VERSION file to ${newVersion}`);

console.log(`\n✨ Version update complete! Current version: ${newVersion}\n`);
console.log('📝 Don\'t forget to:');
console.log('   1. Update CHANGELOG.md with your changes');
console.log('   2. Commit these changes');
console.log('   3. Create a git tag: git tag v' + newVersion);
console.log('   4. Push with tags: git push origin --tags\n');
