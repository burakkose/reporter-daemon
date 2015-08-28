<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:inse="http://ws.inseptra.com/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <Chart>
            <xsl:for-each select="inse:PdfGeneration/inse:Data/inse:Ranking/inse:Rank/inse:DataTraffic">
                <xsl:choose>
                    <xsl:when test="not(../../@date)">
                        <Slice label="{../@category}" value="{@download}"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
        </Chart>
    </xsl:template>
</xsl:stylesheet>
