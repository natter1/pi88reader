from datetime import datetime
from pathlib import Path
from pptx_tools.templates import TemplateExample


# ETIT_16-9.pptx is not part of the repository due to legal restrictions!
class TemplateETIT169(TemplateExample):
    """
    Class handling ETIT 16:9 template.
    """
    TEMPLATE_FILE = Path('..\\resources\\pptx_template\\ETIT_16-9.pptx')

    def __init__(self):
        assert TemplateETIT169.TEMPLATE_FILE.is_file(), \
            "ETIT_16-9.pptx is not part of pi88reader package due to legal restrictions. You have to define the path " \
            "to the file in TemplateETIT169.TEMPLATE_FILE before using TemplateETIT169()."
        super().__init__()
        date_time = datetime.now().strftime("%d %B, %Y")
        self.set_author("Nathanael Jöhrmann", city="Chemnitz", date=date_time)
        self.set_website("https://www.tu-chemnitz.de/etit/wetel/")

    def set_confidential(self, flag: bool = True):
        # todo: add confidential marker in master layout when flag == True
        pass