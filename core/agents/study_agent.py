import ast
from core.agents.base import Agent

class StudyAgent(Agent):
    def __init__(self, name="StudyAgent"):
        super().__init__(name)
        self.register_skill("study_file", self.study_file)

    def study_file(self, filepath: str):
        print(f"'{self.name}' is studying file: {filepath}")
        try:
            with open(filepath, 'r') as f:
                file_content = f.read()

            tree = ast.parse(file_content)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            print(f"Found functions: {functions}")
            return functions
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None
        except Exception as e:
            print(f"An error occurred while studying the file: {e}")
            return None
