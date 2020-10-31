import os

is_windows = os.name == "nt"

if not is_windows:
    from cairosvg import svg2png

svg_path = "model/bpmn/diagram.svg"
png_path = "model/bpmn/diagram.png"


def convert():
    if not is_windows:
        svg2png(url=svg_path, write_to=png_path)
        print("PNG created.\n")
    else:
        print(
            "svg2png conversion is disabled on windows due to cairo installation issues\n"
        )


if __name__ == "__main__":
    convert()
