import os
import fnmatch

import glob
import ntpath

from xml.dom.minidom import parse
import xml.dom.minidom


def find_test_case_files(test_cases_paths, test_suffix='Test.php'):
    """
    @param test_cases_paths: list
    """
    test_case_files = []
    for test_case_path in test_cases_paths:
        for root, dir_names, file_names in os.walk(test_case_path):
            for filename in fnmatch.filter(file_names, '*%s' % test_suffix):
                test_case_files.append(os.path.join(root, filename))

    return test_case_files

def find_test_case_files_from_config(config_path, test_suite_name=None):

    if test_suite_name is None:
        return []

    paths = []
    DOMTree = xml.dom.minidom.parse(config_path)
    testsuites = DOMTree.getElementsByTagName("testsuite")

    for testsuite in testsuites:
        if testsuite.hasAttribute("name") and testsuite.getAttribute("name") == test_suite_name:
            for directory in testsuite.getElementsByTagName("directory"):
                extracted_path = os.path.join(ntpath.dirname(config_path), directory.childNodes[0].data)
                for possible_path in glob.glob(extracted_path):
                    paths.append(possible_path)

    return find_test_case_files(paths)