# Auto Reporter
Creating auto reports from XML files. Pie chart and time chart are available.

##Install

Before the beginning, you must install python3.

```
git clone https://github.com/burakkose/reporter-daemon.git
cd reporter-deamon
virtualenv env
pip install -r requirement.txt
```

##Usage

You can create a PDF file from a single XML file.

`python reporter.py [input_xml_file] [output_folder]`

You can create PDFs by watching folder (always watching for new files).

`python reporter.py [input_folder] [output_folder] -f`

or

`python reporter.py [input_folder] [output_folder] --folder`

##Test

There are test data in the test folder. You can run code like that.

For a pie chart
```
source env/bin/active
python reporter/reporter.py tests/datas/pie.xml .
```

For a time chart and pie chart together
```
source env/bin/active
python reporter/reporter.py tests/datas/time.xml .
```

## Customization

The project based on XSL technology. If you want to create your personal report, you should change some files, so you have to know some basic XSL. The structure of resource folder is like this.
```
Project/
|-- resources/
|   |-- chart/
|   |   |-- pie/
|   |   |   |-- Ranking-report1.xsl
|   |   |-- time/
|   |   |   |-- Ranking-report1.xsl
|   |
|   |-- css/
|   |   |-- bootstrap.css
|   |   |-- font-awesome.min
|   |-- pdf/
|   |   |-- Ranking-report1-en.xsl
|   |   |-- Ranking-report1-tr.xsl
```

You can think that the resources folder is like a repository of config files. Your config files of pie chart reports are in `chart/pie and time charts are in `chart/time` folder. However, you must be careful about its format.

The format is like this.

`{project-name}-{reportType}.xsl`

`pdf` folder is a repository of your output styles, and It allows many languages that you want. However, again, you must be careful about its format. You can examine the difference of files between `Ranking-report1-en.xsl` and `Ranking-report1-tr.xsl`.

`{project-name}-{reportType}-{locale}.xsl` In the next sections, you will see what it means.

You can set some settings in your input XML file that you can see at `tests/datas/pie.xml` or `time.xml`.

>`timeFormat` (example : timeFormat="%d/%m/%y")

>`reportType` (example : reportType="report1")

> `locale` (example : locale="tr" )

>`orientation` (example : orientation="portrait")

>`title` (example : title="Your Report Title" )

>`chartType` (example : chartType:"PIE" or "TIME")

Now let's examine our test data for understanding better.

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>

<inse:PdfGeneration timeFormat="%d/%m/%y" reportType="report1" locale="tr" orientation="portrait" title="tset" chartType="PIE" xmlns:inse="http://ws.inseptra.com/">

    <inse:Data>

        <inse:Ranking xmlns:inse="http://ws.inseptra.com/">
            <inse:Rank category="HTTPS">
                <inse:DataTraffic download="1769193" duration="17146"/>
            </inse:Rank>
            .
            .
            .
        </inse:Ranking>

    </inse:Data>

</inse:PdfGeneration>
```
According to this example, our project name is `Ranking` because of the path of `inse:PdfGeneration/inse:Data/inse:Ranking`.

and

>timeFormat="%d/%m/%y"

>reportType="report1"

>locale="tr"

>orientation="portrait"

>title="Your Report Title"

>chartType:"PIE"

so the application uses `resources/chart/pie/Ranking-report1.xsl` for transforming input data and after transformation uses `resources/pdf/Ranking-report1-tr.xsl` for creating a pdf file.

##TODOs
* Adjust namespaces of the XML input files, I know it is complicated.
* Do human readable config setting
