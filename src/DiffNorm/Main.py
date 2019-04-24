from src.DiffNorm.DiffNorm1 import DiffNorm1


if __name__ == '__main__':
    d = DiffNorm1("chess_demo_all", "chess_demo_u")
    #  d = DiffNorm1("gen_all", "gen_u")
    d.run()
