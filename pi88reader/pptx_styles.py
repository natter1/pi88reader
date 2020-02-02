# from pi88reader.plotter_styles import GraphStyler
from pptx_tools.position import PPTXPosition
from pptx_tools.table_style import PPTXTableStyle

def table_style_summary():
    result = PPTXTableStyle()
    result.position = PPTXPosition(0.44, 0.17)
    result.set_width_as_fraction(0.54)
    result.col_ratios = [3.95, 1.05, 1, 1]
    return result

#
# def table_invisible() -> PPTXTableStyle:
#     result = PPTXTableStyle()
#     result.cell_style = PPTXCellStyle()
#     result.cell_style.fill_style.fill_type = FillType.NOFILL
#     # todo: implement control for border lines
#     return result
#
# def table_no_header() -> PPTXTableStyle:
#     result = PPTXTableStyle()
#
#     result.first_row_header = False
#     result.row_banding = True
#     result.col_banding = False
#
#     return result