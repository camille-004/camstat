import argparse
from pathlib import Path

from camstat.config import Config
from camstat.output import output

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.toml"


def main() -> None:
    """Entry-point."""
    parser = argparse.ArgumentParser(
        prog="camstat", description="Camfetch: Display System Information"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file: "
        + "(default: config.toml in the same directory).",
    )
    args = parser.parse_args()

    config = Config()
    config.load_config(args.config)
    output(config)


if __name__ == "__main__":
    main()
