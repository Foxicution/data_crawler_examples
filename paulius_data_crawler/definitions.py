from pathlib import Path

definitions_file = Path(__file__)
module_dir = definitions_file.parent
project_root = module_dir.parent
test_dir = project_root / "tests"
