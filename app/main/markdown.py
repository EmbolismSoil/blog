from markdown import markdown
from os.path import basename

class Markdown:
    def __init__(self, path):
        self.path = path
        self.name = basename(path)

        with open(self.path) as f:
            lines = f.readlines()
            idx = 0
            line = ''

            if not len(lines) > 6:
                return

            for idx, line in enumerate(lines):
                if line.strip() == '---':
                    break
            title = lines[idx+1]
            subtitle = lines[idx+2]
            tags = lines[idx+3]
            meta = lines[idx+4]
            data = ''
            for line in lines:
                data += line
            data = markdown(data, output_format='html')
            self.data = data
            self.title = title.split(':')[1].strip()
            self.subtitle = subtitle.split(':')[1].strip()
            self.tags = tags.split(':')[1].strip()
            self.meta = meta.split(':')[1].strip()