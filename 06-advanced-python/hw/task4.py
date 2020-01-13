"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной, например так:
> print(folder1)
V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1
А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True
"""


class PrintableFolder:
    def __init__(self, name, content=None):
        self.name = name
        self.content = content

    def __str__(self, stage=0):
        answer = f'V {self.name}\n'
        arrow = '|-> '
        space = '|   '

        if self.content:
            if isinstance(self.content, PrintableFile):
                answer += \
                    f'{space * stage}{arrow}{self.content.__str__(stage + 1)}'
            else:
                for item in self.content:
                    answer += \
                        f'{space * stage}{arrow}{item.__str__(stage + 1)}'
        return answer

    def __repr__(self):
        return self.name

    def __contains__(self, item):
        if not self.content:
            return False
        elif isinstance(self.content, PrintableFile) and self.content != item:
            return False
        elif self.content == item or item in self.content:
            return True
        else:
            for folder in filter(lambda f: isinstance(f, PrintableFolder),
                                 self.content):
                if item in folder:
                    return True
                print(folder)


class PrintableFile:
    def __init__(self, name):
        self.name = name

    def __str__(self, stage=0):
        answer = f'{self.name}\n'
        return answer

    def __repr__(self):
        return self.name


if __name__ == "__main__":
    file1 = PrintableFile('file1')
    file2 = PrintableFile('file2')
    file3 = PrintableFile('file3')
    folder3 = PrintableFolder('folder3', file3)
    folder2 = PrintableFolder('folder2', [folder3, file2])
    folder1 = PrintableFolder('folder1', [folder2, file1])

    print(folder1)
    print(file3 in folder2)
    print(file1 in folder3)
