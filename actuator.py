import argparse

from instrument import JSONActuator

DEFAULT_MIN_BOUND = 0.
DEFAULT_MAX_BOUND = 1000.

class BoundAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if not hasattr(namespace, 'bounds') or namespace.bounds is None:
            namespace.bounds = {}
        if option_string in ("--min", "-m"):
            namespace.bounds['min'] = value
        elif option_string in ("--max", "-M"):
            namespace.bounds['max'] = value

def get_args() -> dict:
    parser = argparse.ArgumentParser(description="Parse arguments to build an actuator and use it with JSON-LECO")

    parser.add_argument(
        "-m", "--min",
        type=float,
        default=DEFAULT_MIN_BOUND,
        help="Min bound of the actuator",
        action=BoundAction,
        dest=argparse.SUPPRESS 
    )

    parser.add_argument(
        "-M", "--max",
        type=float,
        default=DEFAULT_MAX_BOUND,
        help="Max bound of the actuator",
        action=BoundAction,
        dest=argparse.SUPPRESS 
    )

    parser.add_argument(
        "-u", "--units",
        type=str,
        help="Units of the actuator (optional)"
    )


    args = parser.parse_args()

    if not hasattr(args, 'bounds') or args.bounds is None:
        args.bounds = {'min': DEFAULT_MIN_BOUND, 'max': DEFAULT_MAX_BOUND}
    else:
        if 'min' not in args.bounds:
            args.bounds['min'] = DEFAULT_MIN_BOUND
        if 'max' not in args.bounds:
            args.bounds['max'] = DEFAULT_MAX_BOUND


    return vars(args)


def main():
    args  = get_args()
    actuator = JSONActuator('actuator', **args)
 
    actuator.run()


if __name__ == "__main__":
    main()