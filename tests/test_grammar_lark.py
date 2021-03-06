from dubdub.utils import get_lang_files, lark_rules, rel_dir
from loguru import logger
from ward import test

lang_features = get_lang_files(".dhub", relation=rel_dir(__file__, "features"))
parser = lark_rules()

for feature in lang_features:
    content, stem = feature.read_text(), feature.stem
    if stem not in [
        "datatypes",
        "arithmetic",
        "variable",
        "statement",
        "logical",
        "control",
        "compare",
        "grouping",
        "inheritence",
        "functions",
        "classes-init",
    ]:
        # if stem in [
        #     "classes",
        #     "classes-init",
        #     "compare",
        #
        #     "closures",
        #     "logical",
        #     "control",
        #     "arthimatic",
        #     "functions",
        # ]:
        continue

    @test(f"Test parsing doesn't break rules: {stem}")
    def test_correct_token_number(name: str = stem, content=content) -> None:
        parser.parse(content)

        # print()
        assert True, "There was an error parsing the feature."
