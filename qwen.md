# Bash commands
- uv run main.py: Run the project
- npm run typecheck: Run the typechecker



# 包管理工具
这个项目使用的是uv包管理。如果要运行程序需要使用uv命令。比如要运行`langgraph`命令则需要运行`uv run langgraph dev`

# 代码检查
- 单元测试。执行命令：`uv run pytest`进行单元测试，如果报错按提示信息进行修复。
- 代码检查。代码检查并且自动修复命令：`uv run ruff check --fix`。如果自动修复失败，执行`uv run ruff check`然后按照提示进行修复。

# 代码格式化
项目使用black包进行代码格式化，使用`uv run black .`命令对整个项目进行代码格式化。

# Workflow
- 在进行一系列的代码修改后，务必进行代码检查和代码格式化。
- 在代码修改时，如果修改的代码有单元测试代码，则单独运行它的单元测试，而不是全部运行。
