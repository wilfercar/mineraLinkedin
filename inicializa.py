from tkinter import *
import minera as m
from tkinter import filedialog
  
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
  
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()
  
        self.quartoContainer = Frame(master)
        self.quartoContainer["padx"] = 20
        self.quartoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["padx"] = 10
        self.sextoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 15
        self.quintoContainer.pack()

        
  
        self.titulo = Label(self.primeiroContainer, text="DADOS DE ACESSO LINKEDIN")
        self.titulo["font"] = ("Arial", "12", "bold")
        self.titulo.pack()
  
        self.nomeLabel = Label(self.segundoContainer,text="EMAIL:  ", font=self.fontePadrao, anchor=E)
        self.nomeLabel['width']=20
        self.nomeLabel.pack(side=LEFT)
  
        self.nome = Entry(self.segundoContainer)
        self.nome["width"] = 30
        self.nome["font"] = self.fontePadrao
        self.nome.insert(0,"escritoriodecarreiras.sjc@fatec.sp.gov.br");
        self.nome.pack(side=LEFT)
  
        self.senhaLabel = Label(self.terceiroContainer, text="SENHA:", font=self.fontePadrao, anchor=E)
        self.senhaLabel['width']=20
        self.senhaLabel.pack(side=LEFT)

        self.senha = Entry(self.terceiroContainer)
        self.senha["width"] = 30
        self.senha["font"] = self.fontePadrao
        self.senha["show"] = "*"
        self.senha.insert(0,"C4RREIR@S2019")
        self.senha.pack(side=LEFT)

        self.arquivoLabel = Label(self.quartoContainer, text="ARQUIVO ENTRADA:", font=self.fontePadrao, anchor=E)
        self.arquivoLabel['width']=20
        self.arquivoLabel.pack(side=LEFT)

        self.arquivo = Entry(self.quartoContainer)
        self.arquivo["width"] = 28
        self.arquivo["font"] = self.fontePadrao
        self.arquivo.pack(side=LEFT)

        self.file = Button(self.quartoContainer)
        self.file["text"] = "..."
        self.file["font"] = ("Calibri", "6")
        self.file["command"] = self.caminhofile
        self.file.pack(side=LEFT)

        self.espaco = Label(self.quintoContainer)
        self.espaco["width"]=23
        self.espaco.pack(side=LEFT)
  
        self.autenticar = Button(self.quintoContainer)
        self.autenticar["text"] = "INICIAR APLICAÇÃO"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 35
        self.autenticar["command"] = self.verificaSenha
        self.autenticar.pack(side=LEFT)

        
  
        self.mensagem = Label(self.sextoContainer, text="", font=self.fontePadrao)
        self.mensagem["fg"] = 'red'
        self.mensagem.pack()
  
    #Método chama funcao
    def verificaSenha(self):
        usuario = self.nome.get()
        senha = self.senha.get()
        arquivo = self.arquivo.get()
        if usuario != "" and senha != "" and arquivo != "":
            m.minera(usuario, senha)
            m.grafico(arquivo)
        else:
            self.mensagem["text"] = "Digite todos os dados"
    
    def caminhofile(self):
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("xlsx files","*.xlsx"),("all files","*.*")))
        self.arquivo.insert(0, str(root.filename))
    

  
root = Tk()
root.title("Mineração FATEC-SJC")
Application(root)
root.mainloop()