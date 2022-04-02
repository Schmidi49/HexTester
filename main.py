import Domain


def main(cols, rows):
    field = Domain.Field(cols, rows)
    cords = Domain.Coordinate(True, 0, 0)

    for i in range(10):
        for j in range(8):
            field[True, i, j] = str(i) + ".5   " + str(j) + ".5"
            field[False, i, j] = " " + str(i) + "     " + str(j)
    """
    name = "Jim"
    Jim = Domain.Piece(field, name)
    Jim.place(cords)
    Jim.step(Domain.DOWN, Domain.CENTER)
    print(Jim.isPlaced())
    """

    test = field.__str__()
    field.print()


if __name__ == '__main__':
    main(10, 8)
