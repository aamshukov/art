#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text.text import Text
from art.framework.core.algorithm.suffix_array import SuffixArray


class Test(unittest.TestCase):
    """
    """

    def test_naive_implementation_cabbage_success(self):
        string = 'cabbage'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(7, ''), (1, 'abbage'), (4, 'age'), (3, 'bage'),
                            (2, 'bbage'), (0, 'cabbage'), (6, 'e'), (5, 'ge')]
        print(suffixes)
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 0, 1, 0, 0, 0, 0]

    def test_naive_implementation_rikki_tikki_tikka_success(self):
        string = 'rikki-tikki-tikka'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [17, 11, 5, 16, 10, 4, 13, 7, 1, 15, 9, 3, 14, 8, 2, 0, 12, 6]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(17, ''), (11, '-tikka'), (5, '-tikki-tikka'), (16, 'a'), (10, 'i-tikka'),
                            (4, 'i-tikki-tikka'), (13, 'ikka'), (7, 'ikki-tikka'), (1, 'ikki-tikki-tikka'),
                            (15, 'ka'), (9, 'ki-tikka'), (3, 'ki-tikki-tikka'), (14, 'kka'), (8, 'kki-tikka'),
                            (2, 'kki-tikki-tikka'), (0, 'rikki-tikki-tikka'), (12, 'tikka'), (6, 'tikki-tikka')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 5, 0, 0, 6, 1, 3, 9, 0, 1, 7, 1, 2, 8, 0, 0, 4, 0]

    def test_naive_implementation_baabaabac_success(self):
        string = 'baabaabac'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [9, 1, 4, 2, 5, 7, 0, 3, 6, 8]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(9, ''), (1, 'aabaabac'), (4, 'aabac'), (2, 'abaabac'), (5, 'abac'),
                            (7, 'ac'), (0, 'baabaabac'), (3, 'baabac'), (6, 'bac'), (8, 'c')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 4, 1, 3, 1, 0, 5, 2, 0, 0]

    def test_naive_implementation_abracadabra_success(self):
        string = 'ABRACADABRA'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(11, ''), (10, 'A'), (7, 'ABRA'), (0, 'ABRACADABRA'), (3, 'ACADABRA'),
                            (5, 'ADABRA'), (8, 'BRA'), (1, 'BRACADABRA'), (4, 'CADABRA'),
                            (6, 'DABRA'), (9, 'RA'), (2, 'RACADABRA')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2, 0]

    def test_naive_implementation_mississippi_success(self):
        string = 'mississippi'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(11, ''), (10, 'i'), (7, 'ippi'), (4, 'issippi'), (1, 'ississippi'),
                            (0, 'mississippi'), (9, 'pi'), (8, 'ppi'), (6, 'sippi'), (3, 'sissippi'),
                            (5, 'ssippi'), (2, 'ssissippi')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3, 0]

    def test_naive_implementation_mmiissiissiippii_success(self):
        string = 'mmiissiissiippii'
        sa = SuffixArray.build_suffix_array(string)
        assert sa == [16, 15, 14, 10, 6, 2, 11, 7, 3, 1, 0, 13, 12, 9, 5, 8, 4]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(16, ''), (15, 'i'), (14, 'ii'), (10, 'iippii'), (6, 'iissiippii'),
                            (2, 'iissiissiippii'), (11, 'ippii'), (7, 'issiippii'), (3, 'issiissiippii'),
                            (1, 'miissiissiippii'), (0, 'mmiissiissiippii'), (13, 'pii'), (12, 'ppii'),
                            (9, 'siippii'), (5, 'siissiippii'), (8, 'ssiippii'), (4, 'ssiissiippii')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 2, 2, 6, 1, 1, 5, 0, 1, 0, 1, 0, 3, 1, 4, 0]

    def test_build_suffix_array_induced_sorting_cabbage_success(self):
        string = 'cabbage'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [7, 1, 4, 3, 2, 0, 6, 5]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(7, ''), (1, 'abbage'), (4, 'age'), (3, 'bage'),
                            (2, 'bbage'), (0, 'cabbage'), (6, 'e'), (5, 'ge')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 0, 1, 0, 0, 0, 0]

    def test_build_suffix_array_induced_sorting_rikki_tikki_tikka_success(self):
        string = 'rikki-tikki-tikka'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [17, 11, 5, 16, 10, 4, 13, 7, 1, 15, 9, 3, 14, 8, 2, 0, 12, 6]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(17, ''), (11, '-tikka'), (5, '-tikki-tikka'), (16, 'a'), (10, 'i-tikka'),
                            (4, 'i-tikki-tikka'), (13, 'ikka'), (7, 'ikki-tikka'), (1, 'ikki-tikki-tikka'),
                            (15, 'ka'), (9, 'ki-tikka'), (3, 'ki-tikki-tikka'), (14, 'kka'), (8, 'kki-tikka'),
                            (2, 'kki-tikki-tikka'), (0, 'rikki-tikki-tikka'), (12, 'tikka'), (6, 'tikki-tikka')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 5, 0, 0, 6, 1, 3, 9, 0, 1, 7, 1, 2, 8, 0, 0, 4, 0]

    def test_build_suffix_array_induced_sorting_baabaabac_success(self):
        string = 'baabaabac'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [9, 1, 4, 2, 5, 7, 0, 3, 6, 8]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(9, ''), (1, 'aabaabac'), (4, 'aabac'), (2, 'abaabac'), (5, 'abac'),
                            (7, 'ac'), (0, 'baabaabac'), (3, 'baabac'), (6, 'bac'), (8, 'c')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 4, 1, 3, 1, 0, 5, 2, 0, 0]

    def test_build_suffix_array_induced_sorting_abracadabra_success(self):
        string = 'ABRACADABRA'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(11, ''), (10, 'A'), (7, 'ABRA'), (0, 'ABRACADABRA'), (3, 'ACADABRA'),
                            (5, 'ADABRA'), (8, 'BRA'), (1, 'BRACADABRA'), (4, 'CADABRA'),
                            (6, 'DABRA'), (9, 'RA'), (2, 'RACADABRA')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 4, 1, 1, 0, 3, 0, 0, 0, 2, 0]

    def test_build_suffix_array_induced_sorting_mississippi_success(self):
        string = 'mississippi'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(11, ''), (10, 'i'), (7, 'ippi'), (4, 'issippi'), (1, 'ississippi'),
                            (0, 'mississippi'), (9, 'pi'), (8, 'ppi'), (6, 'sippi'), (3, 'sissippi'),
                            (5, 'ssippi'), (2, 'ssissippi')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 1, 4, 0, 0, 1, 0, 2, 1, 3, 0]

    def test_build_suffix_array_induced_sorting_mmiissiissiippii_success(self):
        string = 'mmiissiissiippii'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [16, 15, 14, 10, 6, 2, 11, 7, 3, 1, 0, 13, 12, 9, 5, 8, 4]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(16, ''), (15, 'i'), (14, 'ii'), (10, 'iippii'), (6, 'iissiippii'),
                            (2, 'iissiissiippii'), (11, 'ippii'), (7, 'issiippii'), (3, 'issiissiippii'),
                            (1, 'miissiissiippii'), (0, 'mmiissiissiippii'), (13, 'pii'), (12, 'ppii'),
                            (9, 'siippii'), (5, 'siissiippii'), (8, 'ssiippii'), (4, 'ssiissiippii')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 2, 2, 6, 1, 1, 5, 0, 1, 0, 1, 0, 3, 1, 4, 0]

    def test_build_suffix_array_induced_sorting_gccttaacattattacgccta_success(self):
        string = 'GCCTTAACATTATTACGCCTA'
        sa = SuffixArray.build_suffix_array_induced_sorting(string)
        assert sa == [21, 20, 5, 6, 14, 11, 8, 7, 17, 1, 15, 18, 2, 16, 0, 19, 4, 13, 10, 3, 12, 9]
        suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
        assert suffixes == [(21, ''), (20, 'A'), (5, 'AACATTATTACGCCTA'), (6, 'ACATTATTACGCCTA'),
                            (14, 'ACGCCTA'), (11, 'ATTACGCCTA'), (8, 'ATTATTACGCCTA'),
                            (7, 'CATTATTACGCCTA'), (17, 'CCTA'), (1, 'CCTTAACATTATTACGCCTA'),
                            (15, 'CGCCTA'), (18, 'CTA'), (2, 'CTTAACATTATTACGCCTA'),
                            (16, 'GCCTA'), (0, 'GCCTTAACATTATTACGCCTA'), (19, 'TA'),
                            (4, 'TAACATTATTACGCCTA'), (13, 'TACGCCTA'), (10, 'TATTACGCCTA'),
                            (3, 'TTAACATTATTACGCCTA'), (12, 'TTACGCCTA'), (9, 'TTATTACGCCTA')]
        lcp = SuffixArray.build_longest_common_prefixes(string, sa)
        assert lcp == [0, 1, 1, 2, 1, 4, 0, 1, 3, 1, 1, 2, 0, 4, 0, 2, 2, 2, 1, 3, 3, 0]

    def test_build_suffix_array_random_success(self):
        def test_case(length):
            string = Text.generate_random_string(length)
            sa_naive = SuffixArray.build_suffix_array(string)
            suffixes_naive = [suffix for suffix in SuffixArray.collect_suffixes(string, sa_naive)]
            lcp_naive = SuffixArray.build_longest_common_prefixes(string, sa_naive)
            assert len(sa_naive) == length + 1
            assert len(lcp_naive) == length + 1
            sa = SuffixArray.build_suffix_array_induced_sorting(string)
            suffixes = [suffix for suffix in SuffixArray.collect_suffixes(string, sa)]
            lcp = SuffixArray.build_longest_common_prefixes(string, sa)
            assert len(sa) == length + 1
            assert len(lcp) == length + 1
            assert sa_naive == sa
            assert suffixes_naive == suffixes
            assert lcp_naive == lcp

        for k in range(1000):
            test_case(k)
        for k in range(1, 1001):
            test_case(11 * k)

    def test_find_longest_repeated_substring_success(self):
        """
        https://algs4.cs.princeton.edu/63suffix/tinyTale.txt
        """
        string = "it was the best of times it was the worst of times it was the age of wisdom " \
                 "it was the age of foolishness it was the epoch of belief " \
                 "it was the epoch of incredulity it was the season of light " \
                 "it was the season of darkness it was the spring of hope it was the winter of despair"
        lrs = SuffixArray.find_longest_repeated_substring(string, algorithm=None)
        start = lrs[0]
        length = lrs[1]
        assert string[start:start + length] == 'st of times it was the '
        assert lrs == (39, 23)
        string = 'aaaaaaaaa'
        lrs = SuffixArray.find_longest_repeated_substring(string, algorithm=None)
        start = lrs[0]
        length = lrs[1]
        assert string[start:start + length] == 'aaaaaaaa'
        assert lrs == (1, 8)
        string = 'abcdefg'
        lrs = SuffixArray.find_longest_repeated_substring(string, algorithm=None)
        start = lrs[0]
        length = lrs[1]
        assert string[start:start + length] == ''
        assert lrs == (0, 0)
        string = 'mississippi'
        lrs = SuffixArray.find_longest_repeated_substring(string, algorithm=None)
        start = lrs[0]
        length = lrs[1]
        assert string[start:start + length] == 'issi'
        assert lrs == (4, 4)
        string = 'aabaabaaba'
        lrs = SuffixArray.find_longest_repeated_substring(string, algorithm=None)
        start = lrs[0]
        length = lrs[1]
        assert string[start:start + length] == 'aabaaba'
        assert lrs == (3, 7)


if __name__ == '__main__':
    """
    """
    unittest.main()
