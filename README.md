# Online Pygame Demo

A simple game made with Pygame that can be played directly in a web browser.

## How to Play

- **Controls**: Use the left and right arrow keys to move your character
- **Objective**: Avoid the falling red blocks
- **Scoring**: Each block you successfully avoid adds to your score
- **Game Over**: If you hit a block, press SPACE to restart

## Play Online

Once deployed, the game will be available at: `https://basemodmaker.github.io/online-pygame/`

## Local Development

To run the game locally:

1. Install the required packages:
   ```
   pip install pygame pygbag
   ```

2. Run the game:
   ```
   python main.py
   ```

3. Test the web version:
   ```
   pygbag main.py
   ```
   Then open your browser to `http://localhost:8000`

## How It Works

This game uses:
- Pygame for game logic and rendering
- Pygbag to compile the Python code to WebAssembly
- GitHub Actions for automatic deployment to GitHub Pages

## License

This project is licensed under the MIT License - see the LICENSE file for details.