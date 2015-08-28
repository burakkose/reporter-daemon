import logging
import os
import xmltodict

from lxml import etree

__author__ = "Burak KÖSE"
__email__ = "burakks41@gmail.com"

# Defaults
namespaces = {'inse': "http://ws.inseptra.com/"}


def parse_xml_for_pdf(inputf):
    """
    Parse XML document for creating chart and return a dict object.

    Keyword arguments:
    inputf -- The path of input XML document
    """
    with open(inputf) as fd:
        obj = xmltodict.parse(fd.read())["inse:PdfGeneration"]

    datas = {}
    logging.info("%s is parsing for creating pdf.", inputf)

    data_type = list(obj["inse:Data"].keys())[0].split(':')[1]
    report_type = obj["@reportType"]

    options = {'locale': obj.get('@locale', 'en').strip().lower(),
               'orient': obj.get('@orientation',
                                 'Landscape').strip().title(),
               'title': obj.get('@title', 'Report').strip().title(),
               'chart': obj.get('@chartType', ""),
               'data_type': data_type,
               'report_type': report_type,
               'time_format': obj.get('@timeFormat', "%d/%m/%Y-%H:%M")
               }

    chart_type = options['chart'].lower()
    pie_datas, time_datas = {}, {}

    if chart_type == 'pie':
        pie_xslt = _get_path("resources/chart/{}/{}-{}.xsl"
                             .format(chart_type, data_type, report_type))

        if os.path.exists(pie_xslt):
            pie_datas.update(_get_pie_chart_data(inputf, pie_xslt, {}))

    elif chart_type == 'time':
        time_xslt = _get_path("resources/chart/{}/{}-{}.xsl"
                              .format(chart_type, data_type, report_type))
        pie_xslt = _get_path("resources/chart/{}/{}-{}.xsl"
                             .format('pie', data_type, report_type))

        if os.path.exists(time_xslt):
            time_datas.update(_get_time_chart_data(inputf, time_xslt, {}))
            pie_datas.update(_get_pie_chart_data(inputf, pie_xslt, {}))

    datas['Pie'], datas['Time'] = pie_datas, time_datas
    logging.info("%s was parsed for creating pdf.", inputf)
    return datas, options


def process_xml_xslt(xml, xslt, param):
    """
    Transform XML document into other format and return a new document string.

    Keyword arguments:
    xml -- The path of xml document
    xslt -- The path of xslt document
    param -- Dictionary object of parameter for transformation
    """
    logging.info("%s is reading for transformation.", xslt)
    transform = etree.XSLT(etree.parse(xslt))

    logging.info("%s is reading for transformation.", xml)
    result = transform(etree.parse(xml), **param)
    logging.info("Transformation was finished successfully.")

    return str(result)


def get_file_name(file):
    """
    Return a file name of path.

    Keyword arguments:
    file -- The string of file path
    """
    return os.path.splitext(os.path.basename(file))[0]


def _get_path(s):
    """
    Return a new merged path string.

    Keyword arguments:
    s -- The string of second path
    """
    return os.path.join(os.path.dirname(__file__), s)


def _get_pie_chart_data(inputf, xslt, param):
    """
    Return a new dictionary object for pie chart.

    Keyword arguments:
    inputf -- The path of input XML document
    xslt -- The path of xslt document
    param -- Dictionary object of parameter for transformation
    """
    tmp_xml_chart = process_xml_xslt(inputf, xslt, {})
    chart_inf = xmltodict.parse(tmp_xml_chart)['Chart']['Slice']

    return {el.get('@label'): int(el.get('@value'))
            for el in chart_inf}


def _get_time_chart_data(inputf, xslt, param):
    """
    Return a new dictionary object for time chart.

    Keyword arguments:
    inputf -- The path of input XML document
    xslt -- The path of xslt document
    param -- Dictionary object of parameter for transformation
    """
    tmp_xml_chart = process_xml_xslt(inputf, xslt, {})
    chart_inf = xmltodict.parse(tmp_xml_chart)['Chart']['TimeSeries']

    return {el1.get('@date'): [(el2.get('@label'), int(el2.get('@value')))
                               for el2 in el1.get('Item')]
            for el1 in chart_inf if el1.get('@date')}
