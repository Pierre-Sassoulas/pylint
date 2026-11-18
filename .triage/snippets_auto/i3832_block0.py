'xxx'

import typing

def main() -> None:
    'collapse rows if the first column is empty'

    rows: typing.Iterable[typing.List[str]] = [['foo', 'bar'], ['', 'baz']]

    itor = iter(rows)
    prev: typing.Optional[typing.List[str]] = None
    while True:
        try:
            row = next(itor)
        except StopIteration:
            break

        if row[0]:
            if prev is not None:
                print(prev)
            prev = row
        else:
            assert prev is not None

            for i, cell in enumerate(row):
                if i == 0:
                    continue

                prev[i] += ' ' + cell

    if prev is not None:
        print(prev)

if __name__ == '__main__':
    main()
