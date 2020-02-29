from app import app
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Host address")
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to run with")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    app.run(host=args.host, debug=True, port=args.port)


if  __name__ == "__main__":
    main()