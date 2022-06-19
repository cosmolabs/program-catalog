def add_line_breaks(line: str, char_length: int):
    if type(line) is str:
        a_new_line = ""
        length_of_line = len(line)
        line_break_chars = char_length
        while line_break_chars < length_of_line:
            line = line[:line_break_chars].strip()  + "-\n-" + line[line_break_chars:].strip()
            line_break_chars = line_break_chars + char_length
        return line