
def test_myfunction_raises_if_wrong_input():
    with pytest.raises(ValueError):
        assert myfunction("something")
