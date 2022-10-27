from pathlib import Path, PosixPath
from types import ClassMethodDescriptorType

# def hello_decorator(func):

#     # inner1 is a Wrapper function in
#     # which the argument is called

#     # inner function can access the outer local
#     # functions like in this case "func"
#     def inner():
#         print('================================================================')
#         print('============             TREE STRUCTURE             ============')
#         print('================================================================')

#         # calling the actual function now
#         # inside the wrapper function.
#         func()

#         print("This is after function execution")

#     return inner

class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0


    @property
    def _displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name


    @property
    def get_absolute_path(self):
        if not self.path.is_dir() and self.path.name.endswith('.py'):
            return self.path.absolute()


    @classmethod
    def _default_criteria(cls, path):
        return True


    @classmethod
    def _make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria
        displayable_root = cls(root, parent, is_last)

        yield displayable_root

        children = sorted(
            list(
                path
                for path in root.iterdir()
                if criteria(path)
            ),
            key=lambda s: str(s).lower()
        )

        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                if not str(path).endswith('__pycache__'):
                    yield from cls._make_tree(path,
                                            parent=displayable_root,
                                            is_last=is_last,
                                            criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)

            count += 1


    def _displayable(self):
        if self.parent is None:
            return self._displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self._displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                    if parent.is_last
                    else self.display_parent_prefix_last)
            parent = parent.parent
        return ''.join(reversed(parts))


    @classmethod
    def getPaths(cls, filename):
        paths = cls._make_tree(Path(filename))

        return [
            path.get_absolute_path
            for path in paths
            if path.get_absolute_path
        ]


    @classmethod
    def getMarkdownPath(cls, filename):
        paths = cls._make_tree(
            Path(filename),
        )
        return [path._displayable() for path in paths]


    @classmethod
    def printTree(cls, filename):

        paths = cls._make_tree(
            Path(filename),
        )

        for path in paths:
            print(path._displayable())

