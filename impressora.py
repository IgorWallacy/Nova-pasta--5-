import ctypes
import platform

if platform.system() == "Windows":
    ffi = ctypes.WinDLL("./E1_Impressora01.dll")
else:
    ffi = ctypes.cdll.LoadLibrary("./libE1_Impressora.so")

def AbreConexaoImpressora(tipo, modelo, conexao, param):
    fn = ffi.AbreConexaoImpressora
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]

    modelo = ctypes.c_char_p(bytes(modelo, "utf-8"))
    conexao = ctypes.c_char_p(bytes(conexao, "utf-8"))

    return fn(tipo, modelo, conexao, param)


def FechaConexaoImpressora():
    fn = ffi.FechaConexaoImpressora
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

def ImpressaoTexto(dados, posicao, stilo, tamanho):
    fn = ffi.ImpressaoTexto
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(dados, posicao, stilo, tamanho)

def Corte(avanco):
    fn = ffi.Corte
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(avanco)

def CorteTotal(avanco):
    fn = ffi.CorteTotal
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(avanco)
    
def DirecaoImpressao(direcao):
    fn = ffi.DirecaoImpressao
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(direcao)

def ImpressaoQRCode(dados, tamanho, nivelCorrecao):
    fn = ffi.ImpressaoQRCode
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(dados, tamanho, nivelCorrecao)

def ImpressaoPDF417(numCols, numRows, width, heigth, errCorLvl, options, dados):
    fn = ffi.ImpressaoPDF417
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(numCols, numRows, width, heigth, errCorLvl, options, dados)

def ImpressaoCodigoBarras(tipo, dados, altura, largura, HRI):
    fn = ffi.ImpressaoCodigoBarras
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(tipo, dados, altura, largura, HRI)

def AvancaPapel(linhas):
    fn = ffi.AvancaPapel
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(linhas)

def StatusImpressora(param):
    fn = ffi.StatusImpressora
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(param)

def AbreGavetaElgin():
    fn = ffi.AbreGavetaElgin
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

def AbreGaveta(pino, ti, tf):
    fn = ffi.AbreGaveta
    fn.restype = ctypes.c_int
    fn.argtypes = [ ctypes.c_int, ctypes.c_int, ctypes.c_int]

    return fn( pino, ti, tf)

def InicializaImpressora():
    fn = ffi.InicializaImpressora
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

def SinalSonoro(qtd, tempoinicio, tempofim):
    fn = ffi.SinalSonoro
    fn.restype = ctypes.c_int
    fn.argtypes = [ ctypes.c_int, ctypes.c_int, ctypes.c_int]

    return fn(qtd, tempoinicio, tempofim)

def ImprimeImagemMemoria(key, scala):
    fn = ffi.ImprimeImagemMemoria
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int]

    dados = ctypes.c_char_p(key.encode("utf-8"))

    return fn(dados, scala)


def ImprimeXMLSAT(dados, param):
    fn = ffi.ImprimeXMLSAT
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(dados, param)

def ImprimeXMLCancelamentoSAT(dados, assQRCode, param):
    fn = ffi.ImprimeXMLCancelamentoSAT
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))
    assQRCode = ctypes.c_char_p(bytes(assQRCode, "utf-8"))

    return fn(dados, assQRCode, param)

def ImprimeXMLNFCe(dados, indexcsc, csc, param):
    fn = ffi.ImprimeXMLNFCe
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))
    csc = ctypes.c_char_p(bytes(csc, "utf-8"))

    return fn(dados, indexcsc, csc, param)    

def ImprimeXMLCancelamentoNFCe(dados, param):
    fn = ffi.ImprimeXMLCancelamentoNFCe
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p, ctypes.c_int]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(dados, param)


def ImprimeCupomTEF(dados):
    fn = ffi.ImprimeCupomTEF
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p]

    dados = ctypes.c_char_p(bytes(dados, "utf-8"))

    return fn(dados)    

def ImprimeImagem(path):
    fn = ffi.ImprimeImagem
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_char_p]

    path = ctypes.c_char_p(bytes(path, "utf-8"))

    return fn(path)  
    
def ModoPagina():
    fn = ffi.ModoPagina
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()    


def LimpaBufferModoPagina():
    fn = ffi.LimpaBufferModoPagina
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()    
    
def ImprimeModoPagina():
    fn = ffi.ImprimeModoPagina
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

def ImprimeMPeRetornaPadrao():
    fn = ffi.ImprimeMPeRetornaPadrao
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

def PosicaoImpressaoHorizontal(nLnH):
    fn = ffi.PosicaoImpressaoHorizontal
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(nLnH)

def PosicaoImpressaoVertical(nLnH):
    fn = ffi.PosicaoImpressaoVertical
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int]

    return fn(nLnH)

def GetVersaoDLL():
    fn = ffi.GetVersaoDLL
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()
    


def DefineAreaImpressao(oHorizontal, oVertical, dHorizontal, dVertical):
    fn = ffi.DefineAreaImpressao
    fn.restype = ctypes.c_int
    fn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

    return fn(oHorizontal, oVertical, dHorizontal, dVertical)


def ModoPadrao():
    fn = ffi.ModoPadrao
    fn.restype = ctypes.c_int
    fn.argtypes = []

    return fn()

