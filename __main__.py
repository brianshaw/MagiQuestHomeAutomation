import argparse
import kasalights


def main():
    parser = argparse.ArgumentParser()

    source_ = parser.add_argument_group(title="input source [required]")
    source_args = source_.add_mutually_exclusive_group(required=True)
    # source_args.add_argument(
    #     "-C", "--cam", metavar="cam_id", nargs="?", const=0,
    #     help="Camera or video capture device ID or path. [Default 0]"
    # )
    # source_args.add_argument(
    #     "-I", "--image", type=pathlib.Path, metavar="<path>",
    #     help="Path to image file or directory of images."
    # )
    source_args.add_argument(
        "-L", "--light", action="store", type=str, nargs='?', const='plug',
        help="Test Light 'plug' (default if empty), 'strip'"
    )
    # source_args.add_argument(
    #     "-V", "--video", type=pathlib.Path, metavar="<path>",
    #     help="Path to video file"
    # )

    other_args = parser.add_argument_group(title="Output/display options")
    
    other_args.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )
    other_args.add_argument(
        "-T", "--test", action="store_true", default=False,
        help="test"
    )

    args = vars(parser.parse_args())
    # print(f'args {args}')
    if args["light"]:
        import asyncio
        lights = kasalights.LightControl().start()
        if args["light"] == 'strip':
            asyncio.run(lights.testStrip())
        else:
            asyncio.run(lights.test())
        exit()
    # elif args["image"]:
        


main()