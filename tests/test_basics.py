from .. import main

# placeholders for major functions
class TestBasics:
    def test_randomwal(self):
        assert main.random_wal
    
    def test_gencolors(self):
        assert main.gen_colors

    def test_walengine(self):
        assert main.wal_engine