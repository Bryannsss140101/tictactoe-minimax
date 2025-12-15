import subprocess


def IA(board, turn, diff, timeout=2.0):
    data = [f"{turn} {diff}"] + [str(x) for x in board]
    inp = ("\n".join(data) + "\n").encode("utf-8")

    p = subprocess.run(
        ["ai.exe"],
        input=inp,
        capture_output=True,
        timeout=timeout,
        check=True,
    )

    out = p.stdout.decode("utf-8").strip()
    r, c = map(int, out.split())
    return r, c
