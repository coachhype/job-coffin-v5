#!/usr/bin/env python3
"""
Job Coffin V5 - Simple Deployment Coordinator
Uses only built-in Python modules - no external dependencies needed
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path

def run_command(command, description=""):
    """Execute PowerShell command and return result"""
    print(f"🔍 {description or command}")
    try:
        result = subprocess.run(
            ["powershell", "-Command", command], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Success: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip() if e.stderr else 'Command failed'}")
        return False, e.stderr.strip() if e.stderr else "Command failed"
    except FileNotFoundError:
        print(f"❌ PowerShell not found")
        return False, "PowerShell not found"

def check_requirements():
    """Check system requirements"""
    print("🔍 CHECKING SYSTEM REQUIREMENTS...")
    
    requirements = {
        "git --version": "Git",
        "node --version": "Node.js", 
        "npm --version": "npm",
        "gh --version": "GitHub CLI"
    }
    
    all_good = True
    for cmd, name in requirements.items():
        success, output = run_command(cmd, f"Checking {name}")
        if not success:
            print(f"❌ {name} not installed")
            all_good = False
    
    return all_good

def create_deployment_structure():
    """Create basic project structure"""
    print("📁 CREATING PROJECT STRUCTURE...")
    
    commands = [
        "New-Item -ItemType Directory -Path 'C:\\dev\\jobcoffin-v5' -Force",
        "Set-Location 'C:\\dev\\jobcoffin-v5'",
        "git init",
        "New-Item -ItemType File -Name 'package.json' -Force",
        "New-Item -ItemType Directory -Name 'src' -Force"
    ]
    
    for cmd in commands:
        success, output = run_command(cmd)
        if not success:
            return False
    
    return True

def create_package_json():
    """Create basic package.json"""
    print("📝 CREATING PACKAGE.JSON...")
    
    package_content = {
        "name": "jobcoffin-v5",
        "version": "5.0.0",
        "description": "ADHD-first job search platform",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js",
            "dev": "node src/index.js"
        },
        "dependencies": {
            "express": "^4.18.2",
            "cors": "^2.8.5"
        }
    }
    
    try:
        with open("C:\\dev\\jobcoffin-v5\\package.json", "w") as f:
            json.dump(package_content, f, indent=2)
        print("✅ Package.json created")
        return True
    except Exception as e:
        print(f"❌ Failed to create package.json: {e}")
        return False

def create_basic_server():
    """Create basic Express server"""
    print("🚀 CREATING BASIC SERVER...")
    
    server_content = '''const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        message: 'Job Coffin V5 is running!',
        timestamp: new Date().toISOString()
    });
});

// Root route
app.get('/', (req, res) => {
    res.json({ 
        message: 'Welcome to Job Coffin V5 - ADHD-first job search platform',
        version: '5.0.0'
    });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Job Coffin V5 running on port ${PORT}`);
    console.log(`🌐 Health check: http://localhost:${PORT}/api/health`);
});
'''
    
    try:
        os.makedirs("C:\\dev\\jobcoffin-v5\\src", exist_ok=True)
        with open("C:\\dev\\jobcoffin-v5\\src\\index.js", "w") as f:
            f.write(server_content)
        print("✅ Basic server created")
        return True
    except Exception as e:
        print(f"❌ Failed to create server: {e}")
        return False

def install_dependencies():
    """Install npm dependencies"""
    print("📦 INSTALLING DEPENDENCIES...")
    
    os.chdir("C:\\dev\\jobcoffin-v5")
    success, output = run_command("npm install", "Installing npm packages")
    return success

def test_local_server():
    """Test the server locally"""
    print("🧪 TESTING LOCAL SERVER...")
    
    # Start server in background
    print("Starting server locally for testing...")
    success, output = run_command("Start-Process -NoNewWindow npm -ArgumentList 'start'", "Starting server")
    
    if success:
        print("✅ Server started locally")
        print("🌐 Test at: http://localhost:3000")
        print("🩺 Health check: http://localhost:3000/api/health")
        return True
    else:
        print("❌ Failed to start server")
        return False

def setup_github_repo():
    """Set up GitHub repository"""
    print("📱 SETTING UP GITHUB REPOSITORY...")
    
    commands = [
        "gh auth status",
        "gh repo create jobcoffin-v5 --private --source=. --remote=origin --push"
    ]
    
    for cmd in commands:
        success, output = run_command(cmd)
        if not success:
            print(f"⚠️  GitHub setup failed: {output}")
            print("💡 You can set up GitHub manually later")
            return False
    
    print("✅ GitHub repository created")
    return True

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚄 DEPLOYING TO RAILWAY...")
    
    # Create railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "npm start"
        }
    }
    
    try:
        with open("C:\\dev\\jobcoffin-v5\\railway.json", "w") as f:
            json.dump(railway_config, f, indent=2)
        print("✅ Railway configuration created")
    except Exception as e:
        print(f"❌ Failed to create railway.json: {e}")
        return False
    
    # Try Railway deployment
    success, output = run_command("railway deploy", "Deploying to Railway")
    if success:
        print("✅ Deployed to Railway!")
        return True
    else:
        print("⚠️  Railway deployment failed - may need manual setup")
        print("💡 Visit railway.app to connect your GitHub repo manually")
        return False

def main():
    """Main deployment process"""
    print("🚀 JOB COFFIN V5 - SIMPLE DEPLOYMENT COORDINATOR")
    print("=" * 60)
    print("Using only built-in Python modules - no external dependencies!")
    print("=" * 60)
    
    start_time = time.time()
    
    # Phase 1: Requirements check
    print("\n📋 PHASE 1: SYSTEM REQUIREMENTS")
    if not check_requirements():
        print("❌ System requirements not met")
        print("💡 Install missing tools and try again")
        return False
    
    # Phase 2: Project setup
    print("\n📁 PHASE 2: PROJECT SETUP")
    if not create_deployment_structure():
        print("❌ Failed to create project structure")
        return False
        
    if not create_package_json():
        print("❌ Failed to create package.json")
        return False
        
    if not create_basic_server():
        print("❌ Failed to create server")
        return False
    
    # Phase 3: Dependencies
    print("\n📦 PHASE 3: DEPENDENCIES")
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Phase 4: Local testing
    print("\n🧪 PHASE 4: LOCAL TESTING")
    test_local_server()  # Non-blocking
    
    # Phase 5: GitHub setup
    print("\n📱 PHASE 5: GITHUB SETUP")
    setup_github_repo()  # Non-blocking if fails
    
    # Phase 6: Railway deployment
    print("\n🚄 PHASE 6: RAILWAY DEPLOYMENT")
    deploy_to_railway()  # Non-blocking if fails
    
    # Success!
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("🎉 DEPLOYMENT PROCESS COMPLETED!")
    print("=" * 60)
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    print("🌐 Local server: http://localhost:3000")
    print("🩺 Health check: http://localhost:3000/api/health")
    print("📁 Project location: C:\\dev\\jobcoffin-v5")
    print("\n💡 Next steps:")
    print("1. Test your local server")
    print("2. Set up Railway deployment manually if needed")
    print("3. Configure your domain")
    print("4. Add your specific Job Coffin features")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Deployment interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
    finally:
        input("\nPress Enter to exit...")
