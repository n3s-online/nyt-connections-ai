# Setup

1. If you don't have chrome + chromedriver set up
   - create a `setup` folder to host files
   - Follow [this tutorial](https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2)
     - you only need to install chrome, not chromedriver.
2. Run `source venv/bin/activate`
3. Run `pip install -r requirements.txt`
   - Use `pip freeze > requirements.txt` to update requirements.txt after you install new dependencies

# TODOs

- Try randomizing the order of the input words each attempt as it seems the AI is generating groups based on order of input words
- Set up debugger
