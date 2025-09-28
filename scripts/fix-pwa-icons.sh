#!/bin/bash

# ========================================
# PWA Icons Fix - Automated Deployment
# ========================================

set -e  # Exit on error

echo ""
echo "======================================"
echo "   PWA PUSH NOTIFICATIONS ICON FIX"
echo "======================================"
echo ""

# Шаг 1: Генерация иконок
echo "[1/5] Generating PWA icons..."
python3 scripts/generate_pwa_icons.py
echo "✅ Icons generated successfully!"
echo ""

# Шаг 2: Проверка созданных файлов
echo "[2/5] Verifying icon files..."
required_files=(
    "static/icons/icon-96x96.png"
    "static/icons/icon-128x128.png"
    "static/icons/icon-144x144.png"
    "static/icons/icon-384x384.png"
    "static/icons/badge-72x72.png"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        exit 1
    fi
done
echo "✅ All icon files verified!"
echo ""

# Шаг 3: Сборка статики
echo "[3/5] Collecting static files..."
python3 manage.py collectstatic --noinput
echo "✅ Static files collected!"
echo ""

# Шаг 4: Git add
echo "[4/5] Adding files to Git..."
git add static/icons/icon-96x96.png \
        static/icons/icon-128x128.png \
        static/icons/icon-144x144.png \
        static/icons/icon-384x384.png \
        static/icons/badge-72x72.png \
        static/sw.js \
        static/manifest.json \
        scripts/generate_pwa_icons.py \
        docs/PWA_ICONS_GUIDE.md \
        docs/DEPLOY_PWA_ICONS.md \
        PWA_FIX_README.md
echo "✅ Files added to Git!"
echo ""

# Шаг 5: Git commit
echo "[5/5] Creating Git commit..."
git commit -m "🔔 Fix PWA push notification icons

- Added all necessary icon sizes (96, 128, 144, 384)
- Created badge icon for notifications (72x72)
- Updated Service Worker with explicit icon paths
- Updated manifest.json with complete icon set
- Added automatic icon generation script
- Added PWA icons documentation

Push notifications will now show site icon instead of bell"

echo "✅ Commit created successfully!"
echo ""

echo "======================================"
echo "   ✨ PWA Icons Fix Complete! ✨"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Review changes: git log -1"
echo "2. Push to remote: git push origin main"
echo "3. Deploy to server (see docs/DEPLOY_PWA_ICONS.md)"
echo ""

# Спрашиваем про push
read -p "Push to remote repository now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing to remote repository..."
    if git push origin main; then
        echo "✅ Successfully pushed to remote!"
        echo ""
        echo "🚀 Now deploy to server:"
        echo "   ssh user@server"
        echo "   cd /path/to/pravoslavie_portal"
        echo "   git pull origin main"
        echo "   python3 manage.py collectstatic --noinput"
        echo "   sudo systemctl restart gunicorn nginx"
    else
        echo "❌ Failed to push to remote!"
        echo "Please push manually: git push origin main"
        exit 1
    fi
else
    echo "Skipped push. Push manually when ready:"
    echo "   git push origin main"
fi

echo ""
echo "Done! 🎉"
