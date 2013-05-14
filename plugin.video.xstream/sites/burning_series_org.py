import logger
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from xbmc import log
from xbmc import LOGDEBUG
from xbmc import LOGERROR

SITE_IDENTIFIER = 'burning_series_org'
SITE_NAME = 'Burning-Series.to'
SITE_ICON = 'burning_series.jpg'

URL_MAIN = 'http://www.burning-series.to'
URL_SERIES = 'http://www.burning-series.to/andere-serien'
URL_ZUFALL = 'http://www.burning-series.to/zufall'
def load():
    logger.info("Load %s" % SITE_NAME)
    # Create main menu
    oGui = cGui()   
    __createMenuEntry(oGui, 'showSeries', 'Alle Serien', [['siteUrl', URL_SERIES]])
        
    oGui.setEndOfDirectory()
 
 
def __createMenuEntry(oGui, sFunction, sLabel, lOutputParameter):
  oOutputParameterHandler = cOutputParameterHandler()

  # Create all paramter auf the lOuputParameter
  try:
    for outputParameter in lOutputParameter:
      oOutputParameterHandler.addParameter(outputParameter[0], outputParameter[1])
      oOutputParameterHandler.addParameter(outputParameter[0], outputParameter[1])
  except Exception, e:
    log("Can't add parameter to menu entry with label: %s: %s" % (sLabel, e), LOGERROR)
    oOutputParameterHandler = ""

  # Create the gui element
  oGuiElement = cGuiElement()
  oGuiElement.setSiteName(SITE_IDENTIFIER)
  oGuiElement.setFunction(sFunction)
  oGuiElement.setTitle(sLabel)
  oGui.addFolder(oGuiElement, oOutputParameterHandler)


def showSeries():
    oGui = cGui()    
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();

    sPattern = "<ul id='serSeries'>(.*?)</ul>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">(.*?)</a></li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                sTitle = cUtil().unescape(aEntry[1])
                
                __createMenuEntry(oGui, 'showSeasons', sTitle,
                  [['siteUrl', URL_MAIN + '/' + str(aEntry[0])],['Title', sTitle]])

    oGui.setEndOfDirectory()

    
def showSeasons():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('Title')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();
	
    sPattern = '<ul class="pages">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)">(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                
                __createMenuEntry(oGui, 'showEpisodes', 'Staffel ' + str(aEntry[1]),
                  [['siteUrl', URL_MAIN + '/' + str(aEntry[0])], ['Title', sTitle + 'S' + str(aEntry[1])]])

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sTitleFull = oInputParameterHandler.getValue('Title')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<table>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sPattern = '<td>([^<]+)</td>.*?<a href="([^"]+)">(.*?)<span lang="en">(.*?)</span>.*?</tr>'
        #'<td>([^<]+)</td>\s*<td>\s*<a href="([^"]+)">.*?<span lang="en">(.*?)</span></a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                sNumber = str(aEntry[0]).strip()
                sTitleEnglish = str(aEntry[3]).strip()
                sPattern = '<strong>(.*?)</strong>'
                aResultTitleGerman = oParser.parse(str(aEntry[2]), sPattern)
                if (aResultTitleGerman[0]== True):
                    sTitleGerman = str(aResultTitleGerman[1][0])
                else:
                    sTitleGerman = ''
                sTitle = sNumber
                if sTitleGerman != '':
                    sTitle = sTitle + ' - ' + sTitleGerman
                elif sTitleEnglish != '':
                    sTitle = sTitle + ' - ' + sTitleEnglish                 
                sTitle = cUtil().unescape(sTitle.decode('utf-8')).encode('utf-8') 
                __createMenuEntry(oGui, 'showHosters', sTitle,
                  [['siteUrl', URL_MAIN + '/' + str(aEntry[1])], ['Title', sTitleFull+'E'+sTitle]])

    oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent, sTitle):
    sPattern = '<meta name="description" lang="de" content="([^"]+)"\s*/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sDescription = aEntry.strip().replace('&quot;','"')
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            sMovieTitle = __getMovieTitle(sHtmlContent)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(sDescription)
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()
            
def showHosters():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('Title')	
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();    
    
    __createInfo(oGui, sHtmlContent, sTitle)
    
    sPattern = '<h3>Hoster dieser Episode(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">.*?class="icon ([^"]+)"></span> ([^<]+?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oHoster = cHosterHandler().getHoster2(str(aEntry[1]).lower())              
                if (oHoster != False):
                    __createMenuEntry(oGui, 'getHosterUrlandPlay', str(aEntry[2]),
                      [['siteUrl', URL_MAIN + '/' + str(aEntry[0])], ['Title', sTitle],
                      ['hosterName', oHoster]])
                    
    oGui.setEndOfDirectory()

def __getMovieTitle(sHtmlContent):
    sPattern = '</ul><h2>(.*?)<small id="titleEnglish" lang="en">(.*?)</small>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
	for aEntry in aResult[1]:
	    return str(aEntry[0]).strip() + ' - ' + str(aEntry[1]).strip()

    return ''

def getHosterUrlandPlay():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('Title')	
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHoster = oInputParameterHandler.getValue('hosterName')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
	
    sPattern = '<div id="video_actions">.*?<a href="([^"]+)" target="_blank">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sHoster)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
        return
    oGui.setEndOfDirectory()


