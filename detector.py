import argparse
import math

from instrument import Axis, JSONDetector


def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Parse arguments to build a detector and use it with JSON-LECO")

    parser.add_argument(
        "-d", "--dimension",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Dimension of the data (0, 1, or 2)"
    )



    parser.add_argument(
        "-x", "--x_axis_len",
        type=int,
        help="Length of x-axis (required if dimension >= 1)"
    )

    parser.add_argument(
        "-y", "--y_axis_len",
        type=int,
        help="Length of y-axis (required if dimension == 2)"
    )

    parser.add_argument(
        "-l", "--labels",
        type=str,
        nargs='+',
        help="Label of each channel of acquired data"
    )

    parser.add_argument('--rgb', action='store_true', help='Enable RGB mode')

    args = parser.parse_args()

    if args.rgb:
        args.dimension = 2

    if args.dimension >= 1 and args.x_axis_len is None:
        parser.error("x_axis_len is required when dimension is 1 or 2.")
    if args.dimension == 2 and args.y_axis_len is None:
        parser.error("y_axis_len is required when dimension is 2.")

    return vars(args)


def main():
    args  = get_args()
    args['axes'] = [
        Axis.from_data((lambda l : [((math.exp(i / (l - 1)) - 1) / (math.e - 1)) * l for i in range(l)])(args['x_axis_len']), label="the x axis", units="cm"),
        Axis.from_size(args['y_axis_len'], label="the y axis", units="pixels")
    ]
    detector = JSONDetector('detector', **args)
 
    detector.run()


if __name__ == "__main__":
    main()
