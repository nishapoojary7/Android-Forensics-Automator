import filecmp
import os

def compare_snapshots(folder1, folder2):
    comparison = filecmp.dircmp(folder1, folder2)

    differences = {
        "only_in_first_snapshot": comparison.left_only,
        "only_in_second_snapshot": comparison.right_only,
        "common_but_different_files": []
    }

    for filename in comparison.common_files:
        file1 = os.path.join(folder1, filename)
        file2 = os.path.join(folder2, filename)

        if not filecmp.cmp(file1, file2, shallow=False):
            differences["common_but_different_files"].append(filename)

    return differences
