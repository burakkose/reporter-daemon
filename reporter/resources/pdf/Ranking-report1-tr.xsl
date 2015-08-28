<?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet version="1.0" xmlns:inse="http://ws.inseptra.com/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:param name="title" />
        <xsl:param name="imgPieChart" />
        <xsl:param name="imgTimeChart" />
        <xsl:param name="bootstrap" />
        <xsl:param name="fontawesome" />
        <xsl:template match="/">
            <html>

            <head>
                <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link href="{$bootstrap}" rel="stylesheet" type="text/css"/>
                <link href="{$fontawesome}" rel="stylesheet" type="text/css"/>
            </head>

            <body>
        <div class="section">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <h1 class="text-center text-primary"><xsl:value-of select="$title"/></h1>
                    </div>
                </div>
            </div>
        </div>
        <div class="section text-center">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <table class="table table-bordered table-striped table-hover">
                            <tbody>
                                <xsl:for-each select="inse:PdfGeneration/inse:Data/inse:Ranking/inse:Rank/inse:DataTraffic">
                                    <xsl:choose>
                                        <xsl:when test="not(../../@date)">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="../@category"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="@download"/>
                                        </td>
                                    </tr>
                                        </xsl:when>
                                    </xsl:choose>
                                </xsl:for-each>
                            </tbody>
                            <thead>
                                <tr>
                                    <th>Kategori</th>
                                    <th>İndirme</th>
                                </tr>
                            </thead>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div class="section text-center">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <xsl:choose>
                            <xsl:when test="$imgPieChart">
                                <img>
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="$imgPieChart"/>
                                    </xsl:attribute>
                                    <xsl:attribute name="class">
                                        center-block img-responsive
                                    </xsl:attribute>
                                </img>
                                <p></p>
                            </xsl:when>
                        </xsl:choose>
                        <xsl:choose>
                            <xsl:when test="$imgTimeChart">
                                <img>
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="$imgTimeChart"/>
                                    </xsl:attribute>
                                    <xsl:attribute name="class">
                                        center-block img-responsive
                                    </xsl:attribute>
                                </img>
                            </xsl:when>
                        </xsl:choose>
                    </div>
                </div>
            </div>
        </div>
    </body>
            </html>
        </xsl:template>
    </xsl:stylesheet>
