# fix_pythonanywhere.sh
cd ~

echo "1. Creating virtualenv..."
python3.10 -m venv fseb_env

echo "2. Activating virtualenv..."
source ~/fseb_env/bin/activate

echo "3. Installing packages..."
pip install Flask==2.3.3 pymssql==2.3.11 Flask-CORS==4.0.0 python-dotenv==1.0.0

echo "4. Testing installation..."
python -c "import Flask; import pymssql; print('✅ Packages installed successfully!')"

echo ""
echo "5. NEXT STEPS:"
echo "   - Go to Web tab"
echo "   - Set Virtualenv to: /home/$(whoami)/fseb_env"
echo "   - Click Reload"
echo "   - Test your app"