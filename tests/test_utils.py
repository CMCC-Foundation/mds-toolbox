from mds.core import utils


def test_split_list_into_parts():
    # Test case 1: Splitting a list into 3 different parts
    lst1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_threads1 = 3
    expected_parts1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]
    assert utils.split_list_into_parts(lst1, num_threads1) == expected_parts1

    # Test case 2: Splitting a list into 2 equal parts
    lst2 = [1, 2, 3, 4, 5, 6]
    num_threads2 = 2
    expected_parts2 = [[1, 2, 3], [4, 5, 6]]
    assert utils.split_list_into_parts(lst2, num_threads2) == expected_parts2

    # Test case 3: Splitting an empty list
    lst3 = []
    num_threads3 = 3
    expected_parts3 = [[], [], []]
    assert utils.split_list_into_parts(lst3, num_threads3) == expected_parts3
