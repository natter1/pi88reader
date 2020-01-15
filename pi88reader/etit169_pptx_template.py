from datetime import datetime

from pptx_tools.templates import TemplateExample


# ETIT_16-9.pptx is not part of the repository due to legal restrictions!
class TemplateETIT169(TemplateExample):
    """
    Class handling ETIT 16:9 template.
    """
    TEMPLATE_FILE = '..\\resources\pptx_template\\ETIT_16-9.pptx'

    def __init__(self):
        super().__init__()
        date_time = datetime.now().strftime("%d %B, %Y")
        self.set_author("Nathanael Jöhrmann", city="Chemnitz", date=date_time)
        self.set_website("https://www.tu-chemnitz.de/etit/wetel/")