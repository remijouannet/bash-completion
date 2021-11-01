import pytest

from conftest import assert_complete


class TestUlimit:
    @pytest.mark.complete("ulimit ")
    def test_1(self, completion):
        assert not completion

    @pytest.mark.complete("ulimit -", require_cmd=True)
    def test_2(self, completion):
        assert completion

    @pytest.mark.complete("ulimit -S -")
    def test_3(self, completion):
        """Test modes are completed after -S (-S not treated as mode)."""
        assert completion

    @pytest.mark.complete("ulimit -u -")
    def test_4(self, completion):
        """Test modes are NOT completed if one is specified."""
        assert not completion

    @pytest.mark.complete("ulimit -c ")
    def test_5(self, completion):
        assert completion
        assert not any(x.startswith("-") for x in completion)

    @pytest.mark.complete("ulimit -a ")
    def test_6(self, completion):
        assert completion == sorted("-S -H".split())

    @pytest.mark.complete("ulimit -a -H -")
    def test_7(self, completion):
        """Test modes are NOT completed with -a given somewhere."""
        assert not completion

    @pytest.mark.parametrize("flag", ["-S", "-H"])
    def test_no_special_values_after_soft_or_hard(self, bash, flag):
        completion = assert_complete(bash, "ulimit %s " % flag)
        assert not completion

    @pytest.mark.complete("ulimit -c 0 -n ")
    def test_special_not_just_first(self, completion):
        """Test we offer limit values not only for the first option."""
        assert completion
