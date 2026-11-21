import sys

PAD = 9
EMPTY = 0
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6
VAL = {PAWN: 100, KNIGHT: 320, BISHOP: 330, ROOK: 500, QUEEN: 900, KING: 20000}

DIRS = {
    KNIGHT: (-21, -19, -12, -8, 8, 12, 19, 21),
    BISHOP: (-11, -9, 9, 11),
    ROOK: (-10, -1, 1, 10),
    QUEEN: (-11, -10, -9, -1, 1, 9, 10, 11),
    KING: (-11, -10, -9, -1, 1, 9, 10, 11),
}

FILE_MAP = {c: i for i, c in enumerate("abcdefgh")}
RANK_MAP = {c: i for i, c in enumerate("12345678")}
INV_FILE = "abcdefgh"
INV_RANK = "12345678"

def sq(f, r):
    return 21 + r * 10 + f

def fr(s):
    return (s - 21) % 10, (s - 21) // 10

def sq_to_uci(s):
    f, r = fr(s)
    return INV_FILE[f] + INV_RANK[r]

def uci_to_sq(u):
    return sq(FILE_MAP[u[0]], RANK_MAP[u[1]])

class Engine:
    def __init__(self):
        self.position()

    def position(self, moves=None):
        b = [PAD] * 120
        back = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        for r in range(8):
            for f in range(8):
                s = sq(f, r)
                if r == 0:
                    b[s] = back[f]
                elif r == 1:
                    b[s] = PAWN
                elif r == 6:
                    b[s] = -PAWN
                elif r == 7:
                    b[s] = -back[f]
                else:
                    b[s] = EMPTY
        self.board = b
        self.side = 1
        if moves:
            for m in moves:
                self.make_uci(m)

    def make_uci(self, u):
        f_sq = uci_to_sq(u[:2])
        t_sq = uci_to_sq(u[2:4])
        promo = u[4:5]
        p = self.board[f_sq]
        self.board[f_sq] = EMPTY
        if promo:
            pmap = {"q": QUEEN, "r": ROOK, "b": BISHOP, "n": KNIGHT}
            p = self.side * pmap.get(promo, QUEEN)
        self.board[t_sq] = p
        self.side = -self.side

    def pseudo_moves(self, side):
        out = []
        for s in range(21, 99):
            p = self.board[s]
            if p == PAD or p * side <= 0:
                continue
            pt = abs(p)
            if pt == PAWN:
                step = -10 * side
                nxt = s + step
                if self.board[nxt] == EMPTY:
                    out.append((s, nxt))
                    _, r = fr(s)
                    start_r = 6 if side == 1 else 1
                    if r == start_r and self.board[s + 2 * step] == EMPTY:
                        out.append((s, s + 2 * step))
                for d in (-1, 1):
                    cap = nxt + d
                    t = self.board[cap]
                    if t != PAD and t * side < 0:
                        out.append((s, cap))
            elif pt in (KNIGHT, KING):
                for d in DIRS[pt]:
                    t = self.board[s + d]
                    if t != PAD and t * side <= 0:
                        out.append((s, s + d))
            else:
                for d in DIRS[pt]:
                    cur = s + d
                    while self.board[cur] == EMPTY:
                        out.append((s, cur))
                        cur += d
                    t = self.board[cur]
                    if t != PAD and t * side < 0:
                        out.append((s, cur))
        return out

    def eval_board(self):
        tot = 0
        for s in range(21, 99):
            p = self.board[s]
            if p != PAD and p != EMPTY:
                tot += (1 if p > 0 else -1) * VAL[abs(p)]
        return tot * self.side

    def search(self, depth, alpha, beta):
        if depth <= 0:
            return self.eval_board(), None
        moves = self.pseudo_moves(self.side)
        if not moves:
            return -15000, None
        best_m = moves[0]
        best_v = -10**9
        for f_sq, t_sq in moves:
            old_f = self.board[f_sq]
            old_t = self.board[t_sq]
            self.board[f_sq] = EMPTY
            self.board[t_sq] = old_f
            self.side = -self.side
            v, _ = self.search(depth - 1, -beta, -alpha)
            v = -v
            self.side = -self.side
            self.board[f_sq] = old_f
            self.board[t_sq] = old_t
            if v > best_v:
                best_v = v
                best_m = (f_sq, t_sq)
            if v > alpha:
                alpha = v
            if alpha >= beta:
                break
        return best_v, best_m

    def go(self, depth=2):
        _, m = self.search(max(1, min(depth, 3)), -10**9, 10**9)
        if not m:
            ms = self.pseudo_moves(self.side)
            m = ms[0] if ms else None
        print("bestmove " + (sq_to_uci(m[0]) + sq_to_uci(m[1]) if m else "0000"), flush=True)

def main():
    eng = Engine()
    for line in sys.stdin:
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "uci":
            print("id name TinyChess\nid author Hermes\nuciok", flush=True)
        elif cmd == "isready":
            print("readyok", flush=True)
        elif cmd == "position":
            mv = parts[parts.index("moves") + 1:] if "moves" in parts else []
            eng.position(mv)
        elif cmd == "go":
            d = int(parts[parts.index("depth") + 1]) if "depth" in parts else 2
            eng.go(d)
        elif cmd == "quit":
            break

if __name__ == "__main__":
    main()
