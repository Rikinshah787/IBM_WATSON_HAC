const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('\n🔍 Checking version consistency before commit...\n');

// Get the root package.json version
const rootPackagePath = path.join(__dirname, '..', 'package.json');
const rootPackage = JSON.parse(fs.readFileSync(rootPackagePath, 'utf8'));
const rootVersion = rootPackage.version;

// Check if there are staged changes
let stagedFiles = [];
try {
    const output = execSync('git diff --cached --name-only', { encoding: 'utf8' });
    stagedFiles = output.trim().split('\n').filter(f => f);
} catch (error) {
    console.log('⚠️  Could not check staged files');
    process.exit(0);
}

// If no staged files, exit
if (stagedFiles.length === 0) {
    console.log('ℹ️  No staged files to check');
    process.exit(0);
}

// Check if package.json or source files are being committed
const hasCodeChanges = stagedFiles.some(file =>
    file.endsWith('.js') ||
    file.endsWith('.jsx') ||
    file.endsWith('.py') ||
    file.endsWith('.ts') ||
    file.endsWith('.tsx') ||
    file.includes('package.json')
);

if (hasCodeChanges) {
    console.log('📝 Code changes detected in commit');
    console.log(`📦 Current version: ${rootVersion}`);
    console.log('\n⚠️  REMINDER: Have you updated the version?');
    console.log('\nIf this is a new feature or fix, run:');
    console.log('   npm run version:patch  (for bug fixes)');
    console.log('   npm run version:minor  (for new features)');
    console.log('   npm run version:major  (for breaking changes)');
    console.log('\nThen stage and commit the version changes.\n');

    // Don't block the commit, just warn
    console.log('✅ Proceeding with commit...\n');
}

process.exit(0);
