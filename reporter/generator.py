import datetime
import dateutil.parser
import logging
import os
import pdfkit
import tempfile
import time

from pygal import Pie, Line
from pygal.style import LightStyle, CleanStyle
from utils import parse_xml_for_pdf, process_xml_xslt, _get_path, get_file_name

__author__ = "Burak KÖSE"
__email__ = "burakks41@gmail.com"


class ReportGenarator(object):

    def __init__(self, inputf, outputf):
        self.input = inputf
        self.output = os.path.join(outputf,
                                   "{}.pdf".format(get_file_name(inputf)))
        self.datas, self.options = parse_xml_for_pdf(inputf)

    def _generate_pie_chart(self, datas):
        """
        After generate the pie chart,save to file and return the chart path

        Keyword arguments:
        datas -- Dict object of parsed information for a pie chart
        """
        if not datas:
            return ""

        pie_chart = Pie(fill=True, interpolate="cubic", style=LightStyle)

        for key, value in datas.items():
            pie_chart.add(key, value)

        path = os.path.join(tempfile.gettempdir(),
                            "pie{}.svg".format(str(int(time.time()))))
        pie_chart.render_to_file(path)
        logging.info("Pie chart was created successfully.")

        return path

    def _generate_time_chart(self, datas):
        """
        After generate a time chart,save to file and return the chart path

        Keyword arguments:
        datas -- Dict object of parsed information for a time chart
        """
        if not datas:
            return ""

        line_chart = Line(x_label_rotation=30,
                          sstyle=LightStyle,
                          human_readable=True)

        indices = sorted(datas.keys())
        time_format = self.options['time_format']
        line_chart.x_labels = map(lambda x: dateutil.parser.parse(x)
                                  .strftime(time_format), indices)

        chart_data = {}
        for index in indices:
            for data in datas[index]:
                if chart_data.get(data[0]):
                    chart_data.get(data[0]).append(data[1])
                else:
                    chart_data[data[0]] = [data[1]]

        for key in chart_data:
            line_chart.add(key, chart_data[key])

        path = os.path.join(tempfile.gettempdir(),
                            "time{}.svg".format(str(int(time.time()))))
        line_chart.render_to_file(path)
        logging.info("Time chart was created successfully.")

        return path

    def create_pdf(self):
        """Create PDF file"""
        locale = self.options['locale']
        title = self.options['title']
        data_type = self.options['data_type']
        report_type = self.options['report_type']

        p_img_path = self._generate_pie_chart(self.datas['Pie'])
        t_img_path = self._generate_time_chart(self.datas['Time'])

        html_xslt = _get_path("resources/pdf/{}-{}-{}.xsl"
                              .format(data_type, report_type, locale))
        if not os.path.isfile(html_xslt):
            html_xslt = _get_path("resources/pdf/{}-{}-en.xsl"
                                  .format(data_type, report_type))

        bootstrap = _get_path("resources/css/bootstrap.css")
        fontaw = _get_path("resources/css/font-awesome.min.css")

        out_html = process_xml_xslt(self.input, html_xslt,
                                    {"title": "'{}'".format(title),
                                     "imgPieChart": "'{}'".format(p_img_path),
                                     "imgTimeChart": "'{}'".format(t_img_path),
                                     "bootstrap": "'{}'".format(bootstrap),
                                     "fontawesome": "'{}'".format(fontaw)})

        pdfkit.from_string(out_html,
                           self.output,
                           options={'orientation': self.options['orient'],
                                    'quiet': '',
                                    'margin-top': '0.5in',
                                    'margin-right': '0.5in',
                                    'margin-bottom': '0.5in',
                                    'margin-left': '0.5in'})
        logging.info("PDF was created successfully.")
