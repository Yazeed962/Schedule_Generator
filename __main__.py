from resources import Teacher_Grade


def main():
    Teachers = Teacher_Grade.Teachers('Teachers_input.csv')
    Teachers.run()


if __name__ == '__main__':
    main()
