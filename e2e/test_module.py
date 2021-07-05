from dataclasses import dataclass
import pytest
import pathlib
import os
import subprocess

from agtc.cli import binary_gen_stub

class Constants:
    PROG = ".agt"
    IN = ".in"
    ANS = ".ans"


@dataclass
class _TestInfo:
    in_path: pathlib.Path
    ans_path: pathlib.Path
    prog_path: pathlib.Path


def prepare_test_infos():
    tests = []

    tpath = pathlib.Path() / "e2e"
    for test_dir in tpath.iterdir():
        if not os.path.isdir(test_dir): continue

        ans_mapping = {}
        in_mapping = {}
        prog = None

        for test_item in test_dir.iterdir():
            if test_item.name.endswith(Constants.PROG):
                if prog is not None:
                    raise RuntimeError(f"Multiple programs in same test dir {test_item}")
                prog = test_item.absolute()

            if test_item.name.endswith(Constants.IN):
                key = test_item.name[:-len(Constants.IN)]
                in_mapping[key] = test_item.absolute()

            if test_item.name.endswith(Constants.ANS):
                key = test_item.name[:-len(Constants.ANS)]
                ans_mapping[key] = test_item.absolute()

        if set(in_mapping) != set(ans_mapping):
            raise RuntimeError(f"Some tests don't have defined outputs/inputs")

        for key in in_mapping:
            tests.append(pytest.param(_TestInfo(in_mapping[key], ans_mapping[key], prog)))
    
    return tests


test_infos = prepare_test_infos()

@pytest.mark.parametrize("test_info", test_infos)
def test_e2e(test_info: _TestInfo, tmp_path):
    prog_file = open(test_info.prog_path)
    binary_gen_stub(prog_file, tmp_path / "program.bin")

    output_path = tmp_path / "test.out"

    with open(test_info.in_path) as in_file, open(output_path, "a") as out_file:
        subprocess.run(f"{tmp_path / 'program.bin'}", shell=True, check=True, stdin=in_file, stdout=out_file)
        subprocess.run(f"echo $'\\0\\n'", shell=True, check=True, stdout=out_file)

    subprocess.run(f"diff {test_info.ans_path} {output_path}", shell=True, check=True)
