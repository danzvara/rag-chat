from langchain_experimental.utilities import PythonREPL
from langchain.tools import Tool


def create_python_repl_tool():
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )

    return repl_tool
