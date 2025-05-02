# Deploying Your Pygame Game to GitHub Pages

This guide explains how to deploy your Pygbag-powered Pygame game to GitHub Pages so others can play it in their browsers.

## Building Your Game for Web

1. **Install Pygbag** (if not already installed):
   ```
   pip install pygbag
   ```

2. **Build your game for web**:
   ```
   python run_with_pygbag.py
   ```
   
   Or run pygbag directly:
   ```
   pygbag --build main.py
   ```

   This will create a `build/web` directory containing your game's web version.

## Method 1: Manual GitHub Pages Deployment

1. **Create a `gh-pages` branch**:
   ```
   git checkout --orphan gh-pages
   git rm -rf .
   git checkout main -- build/web
   mv build/web/* .
   rmdir build /s /q
   git add .
   git commit -m "Deploy game to GitHub Pages"
   git push origin gh-pages
   git checkout main
   ```

2. **Enable GitHub Pages**:
   - Go to your GitHub repository settings
   - Scroll down to "GitHub Pages" section
   - Select the `gh-pages` branch as the source
   - Click Save

3. Your game will be available at: `https://[your-username].github.io/online-pygame/`

## Method 2: GitHub Actions Automated Deployment

1. **Create GitHub Actions workflow file**:

   Create a file named `.github/workflows/deploy.yml` with the following content:

   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [ main ]

   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install pygbag

         - name: Build with Pygbag
           run: |
             python -m pygbag --build main.py

         - name: Deploy to GitHub Pages
           uses: JamesIves/github-pages-deploy-action@v4
           with:
             folder: build/web
             branch: gh-pages
   ```

2. **Push the workflow file**:
   ```
   git add .github/workflows/deploy.yml
   git commit -m "Add GitHub Pages deployment workflow"
   git push origin main
   ```

3. GitHub Actions will automatically build and deploy your game whenever you push changes to the main branch.

## Testing Your Deployed Game

After deployment, your game will be available at:
`https://[your-username].github.io/online-pygame/`

## Troubleshooting

If your game doesn't work when deployed:

1. **Check browser console** (F12) for errors
2. **Verify all assets are loading** correctly (images, sounds, etc.)
3. **Test locally** with `python run_with_pygbag.py` before deploying
4. **Ensure proper paths** - use relative paths for all assets

## Tips for Better Performance

1. **Optimize images** and other assets to reduce download size
2. **Minimize DOM interactions** from Python code
3. **Use asyncio.sleep(0)** strategically to prevent browser from becoming unresponsive
4. **Test on multiple browsers** (Chrome, Firefox, Safari)
5. **Add loading indicators** to improve user experience