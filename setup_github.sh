#!/usr/bin/env bash
set -e

echo "=== Praman (प्रमाण) Git & GitHub Setup for bhosaleone ==="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "⚠️  Git is not yet installed on this system."
    echo "👉 Please run this single command in your terminal first:"
    echo "    sudo apt update && sudo apt install -y git"
    exit 1
fi

echo "1. Configuring Git identity..."
git config --global user.name "bhosaleone"
git config --global user.email "bhosaleone@gmail.com"
git config --global init.defaultBranch main

echo "2. Initializing Git repository in $(pwd)..."
if [ ! -d ".git" ]; then
    git init
fi

echo "3. Staging all project files..."
git add .
git commit -m "feat: Praman launch release - Indic & English keyword demand engine" || echo "Files already committed"

echo "4. Setting remote origin to GitHub..."
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:bhosaleone/praman.git

echo ""
echo "=========================================================="
echo "✅ Local Git configuration complete!"
echo "=========================================================="
echo "Next steps:"
echo "1. Create an empty repository named 'praman' on GitHub:"
echo "   👉 https://github.com/new"
echo "2. Push your project to GitHub:"
echo "   git push -u origin main"
echo "=========================================================="
