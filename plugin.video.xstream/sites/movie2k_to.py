from resources.lib.util import cUtil
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.config import cConfig

SITE_IDENTIFIER = 'movie2k_to'
SITE_NAME = 'Movie2k.to'
SITE_ICON = 'movie2k.jpg'

URL_MAIN = 'http://www.movie2k.to/'
URL_MOVIES = URL_MAIN
URL_MOVIES_ALL = 'http://www.movie2k.to/movies-all'
URL_MOVIES_TOP = 'http://www.movie2k.to/movies-top.html'
URL_MOVIES_GENRE = 'http://www.movie2k.to/genres-movies.html'

URL_SERIES = 'http://www.movie2k.to/tvshows_featured.php'
URL_SERIES_ALL = 'http://www.movie2k.to/tvshows-all'
URL_SERIES_TOP = 'http://www.movie2k.to/tvshows-top.html'
URL_SERIES_GENRE = 'http://www.movie2k.to/genres-tvshows.html'

URL_SEARCH = 'http://www.movie2k.to/movies.php?list=search'

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Filme', '', 'showMovieMenu')
    __createMainMenuItem(oGui, 'Serien', '', 'showSeriesMenu')
    __createMainMenuItem(oGui, 'Suche', '', 'showSearch')
    oGui.setEndOfDirectory()

    
def showMovieMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Kinofilme', URL_MOVIES, 'showFeaturedMovies')
    __createMainMenuItem(oGui, 'Alle Filme', URL_MOVIES_ALL, 'showCharacters')
    __createMainMenuItem(oGui, 'Top Filme', URL_MOVIES_TOP, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_MOVIES_GENRE, 'showGenre')
    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Featured', URL_SERIES, 'showFeaturedSeries')
    __createMainMenuItem(oGui, 'Alle Serien', URL_SERIES_ALL, 'showCharacters')
    __createMainMenuItem(oGui, 'Top Serien', URL_SERIES_TOP, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_SERIES_GENRE, 'showGenre')
    oGui.setEndOfDirectory()

def __getHtmlContent(sUrl = None, sSecurityValue = None):
    oInputParameterHandler = cInputParameterHandler()

    # Test if a url is available and set it
    if sUrl is None and not oInputParameterHandler.exist("siteUrl"):
        log("There is no url we can request.", LOGERROR)
        return False
    else:
        if sUrl is None:
            sUrl = oInputParameterHandler.getValue("siteUrl")

    # Test is a security value is available
    if sSecurityValue is None:
        if oInputParameterHandler.exist("securityCookie"):
            sSecurityValue = oInputParameterHandler.getValue("securityCookie")
        else:
            sSecurityValue = ""
    # preferred language
    sPrefLang = __getPreferredLanguage()
    # Make the request
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sPrefLang+sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://www.movie2k.to/')
    oRequest.addHeaderEntry('Accept', '*/*')
    #oRequest.addHeaderEntry('Host', 'movie2k.to')

    return oRequest.request()
    
def __getPreferredLanguage():
    oConfig = cConfig()
    sLanguage = oConfig.getSetting('prefLanguage')
    if sLanguage == '0':
        sPrefLang = 'lang=de;onlylanguage=de;'
    elif sLanguage == '1':
        sPrefLang = 'lang=us;onlylanguage=en;'
    else:
        sPrefLang = ''
    return sPrefLang

    
def showCharacters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    baseUrl = oInputParameterHandler.getValue('sUrl')
        
    __createCharacters(oGui, '#', baseUrl)
    __createCharacters(oGui, 'A', baseUrl)
    __createCharacters(oGui, 'B', baseUrl)
    __createCharacters(oGui, 'C', baseUrl)
    __createCharacters(oGui, 'D', baseUrl)
    __createCharacters(oGui, 'E', baseUrl)
    __createCharacters(oGui, 'F', baseUrl)
    __createCharacters(oGui, 'G', baseUrl)
    __createCharacters(oGui, 'H', baseUrl)
    __createCharacters(oGui, 'I', baseUrl)
    __createCharacters(oGui, 'J', baseUrl)
    __createCharacters(oGui, 'K', baseUrl)
    __createCharacters(oGui, 'L', baseUrl)
    __createCharacters(oGui, 'M', baseUrl)
    __createCharacters(oGui, 'N', baseUrl)
    __createCharacters(oGui, 'O', baseUrl)
    __createCharacters(oGui, 'P', baseUrl)    
    __createCharacters(oGui, 'Q', baseUrl)
    __createCharacters(oGui, 'R', baseUrl)
    __createCharacters(oGui, 'S', baseUrl)
    __createCharacters(oGui, 'T', baseUrl)
    __createCharacters(oGui, 'U', baseUrl)
    __createCharacters(oGui, 'V', baseUrl)
    __createCharacters(oGui, 'W', baseUrl)
    __createCharacters(oGui, 'X', baseUrl)
    __createCharacters(oGui, 'Y', baseUrl)
    __createCharacters(oGui, 'Z', baseUrl)
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sBaseUrl):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('parseMovieSimpleList') 
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sUrl = sBaseUrl + '-1-1.html'
    else:
        sUrl = sBaseUrl + '-' + str(sCharacter) + '-1.html'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)        
        
def showAllSeasons():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = ''
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        __showAllSeasons(sUrl)
    else:
        return

def __showAllSeasons(sUrl):
    oGui = cGui()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = '<SELECT name="season".*?>(.*?)</SELECT>'
    oParser = cParser()
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sPattern = '<OPTION value="(\d+)".*?>([^<]+)</OPTION>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showAllEpisodes')

                sTitle = aEntry[1].strip()
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('sSeason', aEntry[0])
                
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
        
def showAllEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = ''
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        if (oInputParameterHandler.exist('sSeason')):
            sSeason = oInputParameterHandler.getValue('sSeason')
        
            sPattern = '<FORM name="episodeform' + sSeason + '">(.*?)</FORM>'
            aResult = cParser().parse(sHtmlContent, sPattern)
            sHtmlContent = aResult[1][0]
        
    else:
        return

    sPattern = '<SELECT name="episode".*?>(.*?)</SELECT>'
    oParser = cParser()
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sPattern = '<OPTION value="([^"]+)".*?>([^<]+)</OPTION>'
        aResult = oParser.parse(aResult[1][0],sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                if not sUrl.startswith('http'):
                    sUrl = URL_MAIN + sUrl
                sMovieTitle = aEntry[1].strip()
                
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHostersSeries')
                oGuiElement.setTitle(sMovieTitle)

                oOutputParameterHandler = cOutputParameterHandler()                  
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()    
    
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False and sSearchText != ''):
        __callSearch(sSearchText)
    else:
        return
    oGui.setEndOfDirectory()

def __callSearch(sSearchText):
    # get Security Key
    tmpUrl = 'http://www.movie2k.to/searchAutoCompleteNew.php?search=the'
    oRequest = cRequestHandler(tmpUrl)
    tmpHtml = oRequest.request()
    
    oParser = cParser()
    aResult = oParser.parse(tmpHtml, '<a href="movies\.php\?list=search&securekey=([^&]+)&')
    sKey = ''
    if (aResult[0] == True):
        sKey = aResult[1][0]
    else:
        return   

    import urllib
    searchEscape = urllib.quote(sSearchText, safe='/')
    sUrl = URL_SEARCH + '&securekey=' + sKey + '&search=' + searchEscape
    __parseMovieSimpleList(sUrl, 1)

def __checkForNextPage(sHtmlContent, iCurrentPage):
    iNextPage = int(iCurrentPage) + 1
    iNextPage = str(iNextPage) + ' '

    sPattern = '<a href="([^"]+)">' + iNextPage + '</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
    return False

def showGenre():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<TR>.*?<a href="([^"]+)">(.*?)</a>.*?<TD id="tdmovies" width="50">(.*?)</TD>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = aEntry[0].strip()
                if not (sUrl.startswith('http')):
                    sUrl = URL_MAIN + sUrl
                sTitle = aEntry[1] + ' (' + aEntry[2] + ')'
                
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieSimpleList')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def parseMovieSimpleList():
    oInputParameterHandler = cInputParameterHandler()
    oParser = cParser()
    
    if (oInputParameterHandler.exist('iPage')):
        iPage = oInputParameterHandler.getValue('iPage')
    else:
        iPage = 1

    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        if (sUrl.find('tvshows-season-') != -1):
            sPattern = '<TR>\s*<TD.*?id="tdmovies".*?<a href="([^"]+)">(.*?)\s*</a>.*?<img border=0 src="http://[^/]+/img/([^"]+)".*?</TR>'
            if oInputParameterHandler.exist('sLanguageToken'):
                sLanguageToken = oInputParameterHandler.getValue('sLanguageToken')
                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] == True:
                    for aEntry in aResult[1]:
                        sUrl = str(aEntry[0]).strip()
                        if not (sUrl.startswith('http')):
                            sUrl = URL_MAIN + sUrl
                        if aEntry[2] == sLanguageToken:
                            break
                    oRequest = cRequestHandler(sUrl)
                    sHtmlContent = oRequest.request()
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0] == True:
                        for aEntry in aResult[1]:
                            sUrl = str(aEntry[0]).strip()
                            if not (sUrl.startswith('http')):
                                sUrl = URL_MAIN + sUrl
                            if aEntry[2] == sLanguageToken:
                                break
                                
            else:
                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] == True:
                    sUrl = str(aResult[1][0][0]).strip()
                    if not (sUrl.startswith('http')):
                        sUrl = URL_MAIN + sUrl
                    oRequest = cRequestHandler(sUrl)
                    sHtmlContent = oRequest.request()
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0] == True:
                        sUrl = str(aResult[1][0][0]).strip()
                        if not (sUrl.startswith('http')):
                            sUrl = URL_MAIN + sUrl
            __showAllSeasons(sUrl)
            
        else:
            __parseMovieSimpleList(sUrl, iPage)
      
def __parseMovieSimpleList(sUrl, iPage):
    oGui = cGui()
    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    #oRequest.addHeaderEntry('Cookie', 'lang=us;onlylanguage=en;')
    sHtmlContent = __getHtmlContent(sUrl)
    sPattern = '<TR.*?<TD.*?id="tdmovies".*?<a href="([^"]+)">(.*?)\s*</a>.*?<img border=0 src="http://[^/]+/img/([^"]+)".*?</TR>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            newUrl = aEntry[0].strip()
            if not (newUrl.startswith('http')):
                newUrl = URL_MAIN + newUrl
            sMovieTitle = aEntry[1].strip().replace('\t', '')
            sMovieTitle = sMovieTitle.replace('&amp;','&')
            sLanguageToken = aEntry[2]
            
            sTitle = sMovieTitle + __getLanguage(sLanguageToken.replace('.png','')) 
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()            
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sUrl', newUrl)
            
            type = getTypeFromUrl(newUrl)
            if type == 'Serie':
                if sUrl.find(URL_SERIES_TOP) != -1:
                    oGuiElement.setFunction('showHostersSeries')
                elif sUrl.find('tvshows-') != -1:
                    oOutputParameterHandler.addParameter('sLanguageToken',sLanguageToken)
                    oGuiElement.setFunction('parseMovieSimpleList')
                else:
                    oGuiElement.setFunction('showAllSeasons')
            elif type == 'Film':
                oGuiElement.setFunction('showHosters')
            else:
                oOutputParameterHandler.addParameter('sLanguageToken',sLanguageToken)
                oGuiElement.setFunction('parseMovieSimpleList')
            
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    sNextUrl = __checkForNextPage(sHtmlContent, iPage)
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('parseMovieSimpleList')
        oGuiElement.setTitle('next ..')
        
        if (sNextUrl.startswith(URL_MAIN)):
            sNextUrl = sNextUrl.replace(URL_MAIN,'')
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sUrl', URL_MAIN + sNextUrl)
        oOutputParameterHandler.addParameter('iPage', int(iPage) + 1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getTypeFromUrl(url):
    
    if url.find('tvshows-') != -1:
        return 'Serie'  
    
    #####################################################################
    # Examples:
    # http://www.movie2k.to/Die-Simpsons-online-serie-656673.html
    # http://www.movie2k.to/Die-Simpsons-Der-Film-online-film-783507.html
    # http://www.movie2k.to/The-Simpsons-watch-tvshow-660732.html
    # http://www.movie2k.to/The-Simpsons-Movie-watch-movie-693640.html
    #####################################################################
    sPattern = '([^-]+)-(\d+).html$'
    aResult = cParser().parse(url, sPattern)  
    if aResult[0] == True:
        match = aResult[1][0]
        type = match[0]
        id = match[1]
        if type in ['serie','tvshow']:
            return 'Serie'
        elif type in ['film','movie']:
            return 'Film'

    return ''
    
def showFeaturedMovies():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        oRequest = cRequestHandler(sUrl)
        #oRequest.addHeaderEntry('Cookie', 'lang=us;onlylanguage=en;')
        sHtmlContent = oRequest.request()
        sPattern = '<div style="float:left">\s*<a href="([^"]+)".{0,1}><img src="([^"]+)".*?alt="([^"]+)".*?<img src="http://img.movie2k.to/img/(.*?).png"'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oGui = cGui()
            for aEntry in aResult[1]:
                newUrl = aEntry[0]
                if not (newUrl.startswith('http')):
                    newUrl = URL_MAIN + newUrl
                sThumbnail = aEntry[1]             
                sMovieTitle = aEntry[2].strip().replace('kostenlos', '')
                
                sTitle = sMovieTitle +  __getLanguage(aEntry[3])

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(sThumbnail)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', newUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            oGui.setEndOfDirectory()

def showFeaturedSeries():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        #oRequest.addHeaderEntry('Cookie', 'lang=us;onlylanguage=en;')
        sHtmlContent = oRequest.request()
        
        sPattern = '<div id="maincontenttvshow">(.*?)<BR><BR>'
        aResult = cParser().parse(sHtmlContent,sPattern)
        if aResult[0] == True:
            sPattern = '<div style="float:left"><a href="([^"]+)"><img src="([^"]+)" border=0.*?title="([^"]+)"></a>.*?<img src="http://img.movie2k.to/img/(.*?).png"'
            sHtmlContent = aResult[1][0]
            aResult = cParser().parse(sHtmlContent, sPattern)
            if aResult[0] == True:
                oGui = cGui()
                for aEntry in aResult[1]:
                    newUrl = str(aEntry[0]).strip()
                    if not (newUrl.startswith('http')):
                        newUrl = URL_MAIN + newUrl
                    sThumbnail = aEntry[1]
                    sMovieTitle = aEntry[2].strip().replace('\t', '')    
                     
                    sTitle = sMovieTitle +  __getLanguage(aEntry[3])
                     
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showAllSeasons')
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setThumbnail(sThumbnail)
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', newUrl)
                    
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
                oGui.setEndOfDirectory()
        
        
def __createInfo(oGui, sHtmlContent):
    sPattern = '<img src="(http://img.movie2k.to/thumbs/[^"]+)".*?<div class="moviedescription">(.*?)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(aEntry[0])
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(aEntry[1]).strip())
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def showHostersSeries():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sMovieTitle')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
        
        sHtmlContent = cRequestHandler(sUrl).request()        
        sPattern = '<tr id="tablemoviesindex2".*?<a href="([^"]+)".*? width="16">([^<]+)</a></td></tr>'
        aResult = cParser().parse(sHtmlContent.replace('\\',''), sPattern)       
        if (aResult[0] == True):
            oGui = cGui()
            __createInfo(oGui, sHtmlContent)
            for aEntry in aResult[1]:                
                sHoster = aEntry[1].strip()
                if (cHosterHandler().getHoster2(sHoster.lower())!=False):
                    sUrl = URL_MAIN + aEntry[0]
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showHoster')               
                    oGuiElement.setTitle(sHoster)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sHoster', sHoster)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

            oGui.setEndOfDirectory()   
        

def showHosters():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sMovieTitle')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
        
        sHtmlContent = cRequestHandler(sUrl).request() 
        sPattern = '<tr id="tablemoviesindex2">.*?<a href="([^"]+)">([^<]+)<.*?alt="(.*?) .*?width="16">.*?</a>.*?alt="([^"]+)"'
        aResult = cParser().parse(sHtmlContent.replace('\\',''), sPattern)
        if (aResult[0] == True):
            oGui = cGui()
            __createInfo(oGui, sHtmlContent)
            for aEntry in aResult[1]:
                sHoster = aEntry[2].strip()
                if (cHosterHandler().getHoster2(sHoster.lower())!=False):
                    sUrl = URL_MAIN + aEntry[0]
                    sTitle = aEntry[1] + ' - ' + sHoster + ' - ' + aEntry[3]
                    
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showHoster')               
                    oGuiElement.setTitle(sTitle)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sHoster', sHoster)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

            oGui.setEndOfDirectory()   

def showHoster():
    oInputParameterHandler = cInputParameterHandler()
    if not (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sHoster') and oInputParameterHandler.exist('sMovieTitle')):
        return
    oGui = cGui()                

    sUrl = oInputParameterHandler.getValue('sUrl')
    sHoster = oInputParameterHandler.getValue('sHoster')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    type = getTypeFromUrl(sUrl)
    sHtmlContent = cRequestHandler(sUrl).request()
    
    if type == 'Film':
        sPattern = '<a href="(movie.php\?id=(\d+)&part=(\d+))">'
        aResult = cParser().parse(sHtmlContent, sPattern)
        # if aResult[0] == True:
            # for aEntry in aResult[1]:
                # sUrl = aEntry[0].strip()
                # if not sUrl.startswith('http'):
                    # sUrl = URL_MAIN + sUrl
                # sTitle ='Teil ' +aEntry[2]
                # parseHoster(sUrl, sHoster.lower(), sTitle, sMovieTitle)
        # else:       
        parseHosterDirect(sUrl, sHoster.lower(), sMovieTitle)
        
    elif type == 'Serie':
        sPattern = '<SELECT name="hosterlist"(.*?)</SELECT>'
        aResult = cParser().parse(sHtmlContent,sPattern)
        # if aResult[0] == True:
            # sPattern = '<OPTION value="([^"]+)".*?</OPTION>'
            # aResult = cParser().parse(aResult[1][0],sPattern)
            # if aResult[0] == True:
                # i = 1
                # for aEntry in aResult[1]:
                    # sUrl = aEntry.strip()
                    # if not sUrl.startswith('http'):
                        # sUrl = URL_MAIN + sUrl
                    # sTitle = 'Teil ' + str(i)
                    # parseHoster(sUrl, sHoster.lower(), sTitle, sMovieTitle)
                    # i += 1 
        # else:       
        parseHosterDirect(sUrl, sHoster.lower(), sMovieTitle)
            
    oGui.setEndOfDirectory() 
        
    
def __getMovieTitle(sHtmlContent):
    sPattern = '<title>(.*?) online anschauen.*?</title>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return str(aResult[1][0]).strip()
    else:
        sPattern = 'Watch (.*?) online.*?</title>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            return str(aResult[1][0]).strip()
    return False

def parseHosterDirect(sUrl = '', sHoster = '', sMovieTitle = ''):
    if (sUrl == '' and sHoster == ''):
        return False
        
    oHoster = cHosterHandler().getHoster2(sHoster)
    if (oHoster == False):
        return False
    
    oParser = cParser()
    #Link oder Iframe suchen der den Hosternamen enthaelt
    sPattern = 'id="maincontent5".*?(?:href|src)="([^<]+'+sHoster.lower()+'\.[^<"]+)"'
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]    
        oGui = cGui()
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sMovieTitle)
        #oGui.setEndOfDirectory()
        return True
        
    return False
    
def parseHoster(sUrl = '', sHoster = '', sDisplayName = '', sMovieTitle = ''):
    if (sUrl == '' and sHoster == ''):
        return False
       
    oHoster = cHosterHandler().getHoster2(sHoster)
    if (oHoster == False):
        return False

    oHoster.setFileName(sMovieTitle)
    oHoster.setDisplayName(sDisplayName)

    oParser = cParser()
    sPattern = oHoster.getHosterLinkPattern()

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]        
        oGui = cGui()
        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        return True

    return False

def __getLanguage(sString):
    if (sString == 'us_ger_small'):
        return ' (DE)'
    return ' (EN)'

def __createMainMenuItem(oGui, sTitle, sUrl, sFunction):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
