num_list = [1, [1.1, 1.2, 1.3], 2, 3, [[4, 5, 6], [7, 8, 9]]]


def get_num(nl: list):
    def extract_num(current_list):
        for e in current_list:
            if isinstance(e, list):
                extract_num(e)
            else:
                print(f"[LOG] {e}")

    extract_num(nl)


get_num(num_list)
