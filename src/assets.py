
from enums import Border


goblin = r"""       ,      ,
      /(.-""-.)\
  |\  \/      \/  /|
  | \ / =.  .= \ / |
  \( \   o\/o   / )/
   \_, '-/  \-' ,_/
     /   \__/   \
     \ \__/\__/ /
   ___\ \|--|/ /___
 /`    \      /    `\
/       '----'       \
"""


def add_border(text: str) -> str:

    # Get the maximum length of any line
    lines = text.split("\n")
    max_length = max(len(line) for line in lines)

    # Create the top and bottom borders
    horizontal_border = Border.TBM * (max_length + 2)
    top_border = f"{Border.LTC}{horizontal_border}{Border.RTC}"
    bottom_border = f"{Border.LBC}{horizontal_border}{Border.RBC}"

    # Add the horizontal borders to the top and bottom of the text
    bordered_lines = [
        f"{Border.LRM} {line.ljust(max_length)} {Border.LRM}" for line in lines
    ]
    bordered_text = "\n".join(bordered_lines)

    # Combine everything into the final result
    result = f"{top_border}\n{bordered_text}\n{bottom_border}"
    return result


if __name__ == '__main__':

    print(add_border(goblin))

    # In case we want to store them in the db.
    goblin = """       ,      ,\n      /(.-""-.)\\\n  |\\  \\/      \\/  /|\n  | \\ / =.  .= \\ / |\n  \\( \\   o\\/o   / )/\n   \\_, \'-/  \\-\' ,_/\n     /   \\__/   \\\n     \\ \\__/\\__/ /\n   ___\\ \\|--|/ /___\n /`    \\      /    `\\\n/       \'----\'       \\\n"""
    print(add_border(goblin))
