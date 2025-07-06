# How to Push Your Project Folder to GitHub Using VS Code

1. **Open VS Code**  
   Open VS Code and use `File > Open Folder...` to open your `soundmind_fullstack` folder.

2. **Initialize Git (if not already done)**  
   Open the terminal in VS Code (`Ctrl+``) and run:
   ```
   git init
   ```

3. **Add All Files to Git**  
   ```
   git add .
   ```

4. **Commit Your Changes**  
   ```
   git commit -m "Initial commit"
   ```

5. **Create a New Repository on GitHub**  
   - Go to [https://github.com](https://github.com) and log in.
   - Click the "+" icon > "New repository".
   - Name your repo (e.g., `soundmind_fullstack`), set visibility, and click "Create repository".

6. **Connect Local Repo to GitHub**  
   Copy the URL GitHub gives you (e.g., `https://github.com/yourusername/soundmind_fullstack.git`) and run:
   ```
   git remote add origin https://github.com/yourusername/soundmind_fullstack.git
   ```

7. **Push to GitHub**  
   ```
   git branch -M main
   git push -u origin main
   ```

8. **Done!**  
   Refresh your GitHub repo page to see your files.

---

**Tip:**  
You can also use the Source Control panel in VS Code (left sidebar) for basic Git operations.
