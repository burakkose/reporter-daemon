<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:inse="http://ws.inseptra.com/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <Chart>
            <xsl:for-each select="inse:PdfGeneration/inse:Data/inse:Ranking">
                <xsl:choose>
                    <xsl:when test="@date">
                        <TimeSeries date="{@date}"> <!--Tıme Value-->
                            <xsl:for-each select="inse:Rank/inse:DataTraffic">
                                <Item label="{../@category}" value="{@download}"/>
                            </xsl:for-each>
                        </TimeSeries>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
        </Chart>
    </xsl:template>
</xsl:stylesheet>
