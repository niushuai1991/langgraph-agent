## Guidelines for Developing this project

### Project Configuration
To install dependencies, you need to use the `uv` command. For example, to install the langgraph dependency, execute `uv add langgraph`.
This is the LangGraph project; the command to start the project is `uv run langgraph dev --no-browser`.

### Unit Testing
- This project uses the pytest framework for writing unit tests. All tests are unified in the tests directory. The path of unit test scripts should match the path of the scripts being tested. For example, the test script for src/cache/picture.py should be located at tests/cache/test_picture.py.
- To run a single unit test file, use the command `uv run python -m pytest <path_to_test_file>` to avoid Python module import path issues. For example, to run the tests/cache/test_picture.py script, the command would be `uv run python -m pytest tests/cache/test_picture.py`.

### Core Principles
- **Security is Paramount:**
    *   **Never expose secrets.** Do not output the contents of .env anywhere.

### Code inspection
- Code formmating. Use `uv run black .` for code formatting.
- Unit test. Use `uv run pytest .` to perform a complete unit test.
- Static code analyzer. Use `uv run ruff check --fix .` to check and fix any fixable code modifications, and then use `uv run ruff check .` again to check if there is any code that needs to be manually fixed.


### Your Role in Development

When asked to modify the action, you should:

1.  **Analyze the Request:** Understand how the requested change impacts the python scripts, the shell scripts, and the documentation.
2.  **Plan Your Changes:** Propose a plan that includes modifications to all relevant files.
3.  **Implement and Verify:** Make the changes and ensure the action still functions as expected. New and modified interfaces need to be called to ensure they work correctly.The core code needs to have unit tests added, and the unit tests need to be executed to ensure that it works correctly.
4.  **Code inspection:** After modifying the code, a code review is required, including code formatting, unit testing, and static code analysis.
