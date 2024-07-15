import subprocess
import sys


def apply_tc() -> None:
    if not is_tc_applied():
        subprocess.run(
            ["tc", "qdisc", "add", "dev", "eth0", "root", "netem", "loss", "100%"],
            check=True,
        )


def remove_tc() -> None:
    if is_tc_applied():
        subprocess.run(
            ["tc", "qdisc", "del", "dev", "eth0", "root", "netem"], check=True
        )


def is_tc_applied() -> bool:
    result = subprocess.run(
        ["tc", "qdisc", "show", "dev", "eth0"], capture_output=True, text=True
    )
    return "netem" in result.stdout


if __name__ == "__main__":
    if sys.argv[1] == "apply":
        apply_tc()
    elif sys.argv[1] == "remove":
        remove_tc()
