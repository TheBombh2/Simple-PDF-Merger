import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from icon import ICON
import merger as merge
import webbrowser

class pdfMerger:
    def __init__(self) -> None:
        self.width = 600
        self.height = 300
        self.window = tk.Tk()
        self.defaultFont =("Helvetica", 10,"bold")
        self.smallFont =("Helvetica", 13,"bold")

        self.pdfTV = None
        self.lastIndex = 0


        self.mergeBTN = None
        self.delBTN = None
        self.upBTN = None
        self.downBTN = None

        self.allowCopiesCB = tk.IntVar()

        self.pdfPaths = {}

        self.URL = "https://github.com/TheBombh2/Simple-PDF-Merger"


        #Methods to setup everything
        self.prepareWindow() # Call the function to prepare window size and location
        self.setupButtons()
        self.setupLabel()   #Only one label right now which the pdfmerger
        self.setupTreeView()
        self.changeDimensions() # change cols and rows dimensions
        self.setupOthers()

    
    def openRepo(self) -> None:
        webbrowser.open_new_tab(self.URL)

    def changeDimensions(self) -> None:
    # Set the minimum size of all columns to 150 pixels
        for i in range(self.window.grid_size()[0]):
            self.window.columnconfigure(i, minsize=150)

        # Set the minimum size of all rows to 50 pixels
        for i in range(self.window.grid_size()[1]):
            self.window.rowconfigure(i, minsize=50)

    def setupOthers(self)->None:
        alCPCB = ttk.Checkbutton(self.window,text="Allow Copies?",onvalue=1,offvalue=0,variable=self.allowCopiesCB)
        alCPCB.grid(row=1,column=3,sticky="e")

    def setupTreeView(self)-> None:
        itemsTreeView = ttk.Treeview(self.window,height=8,show="headings",selectmode="browse")
        itemsTreeView['columns'] = ("Pdfs")
        itemsTreeView.column("#0",width=0)
        itemsTreeView.column("Pdfs",width=260)
        itemsTreeView.heading("Pdfs",text="Pdfs")
        verscrlbar = ttk.Scrollbar(self.window, orient ="vertical", command = itemsTreeView.yview)
        verscrlbar.grid(row=2,column=1,rowspan=3,sticky="ens")
        itemsTreeView.configure(yscrollcommand= verscrlbar.set)
        self.pdfTV = itemsTreeView
        itemsTreeView.grid(row=2,column=0,rowspan=3,columnspan=2)
        
    def setupLabel(self) -> None:
        titleLBL = ttk.Label(self.window,text="PDFMerger",font=("Helvetica", 24,"bold"))
        copyrightLBL = ttk.Label(self.window,text="Github Repository",foreground="red",font=self.smallFont,cursor="hand2")
        copyrightLBL.bind("<Button-1>", lambda e:self.openRepo())
        copyrightLBL.grid(row=1,column=1,sticky="n",columnspan=2)
        titleLBL.grid(row=0,column=1,columnspan=2)
        
    def setupButtons(self) -> None:
        mergeBTN = tk.Button(self.window,text="Merge",font=self.defaultFont,height=2,width=16,command=self.mergPDF)
        addBTN = tk.Button(self.window,text="Add PDF",font=self.defaultFont,height=2,width=16,command=self.addPDF)
        delBTN = tk.Button(self.window,text="Remove PDF",font=self.defaultFont,height=2,width=16,command=self.delPDF)
        upBTN = tk.Button(self.window,text="↑",font=self.defaultFont,height=2,width=16, command=self.moveUp)
        downBTN = tk.Button(self.window,text="↓",font=self.defaultFont,height=2,width=16,command=self.moveDown)
        mergeBTN.grid(row=4,column=2,columnspan=2)
        addBTN.grid(row=2,column=3)
        delBTN.grid(row=3,column=3)
        upBTN.grid(row=2,column=2)
        downBTN.grid(row=3,column=2)

        self.mergeBTN = mergeBTN
        self.delBTN = delBTN
        self.upBTN = upBTN
        self.downBTN = downBTN

    def prepareWindow(self) -> None:
        self.window.resizable(0,0)
        self.window.title("PDFMerger")
        self.window.iconphoto(True,tk.PhotoImage(data=ICON))
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        x = ((screenWidth // 2)- (self.width // 2) )
        y = ((screenHeight// 2) -( self.height // 2))
        self.window.geometry("{}x{}+{}+{}".format(self.width,self.height,x,y))

    def runProgram(self) -> None:
        self.triggerBtns()
        self.window.mainloop()

    def triggerBtns(self) -> None:
        if len(self.pdfTV.get_children()) > 0 :
            self.mergeBTN.config(state="active")
            self.delBTN.config(state="active")
            self.upBTN.config(state="active")
            self.downBTN.config(state="active")
        else:
            self.mergeBTN.config(state="disabled")
            self.delBTN.config(state="disabled")
            self.upBTN.config(state="disabled")
            self.downBTN.config(state="disabled")

    def addPDF(self) -> None:
        filePath = filedialog.askopenfilename(title="Select a File", filetypes=[("PDF Document", "*.pdf")])
        if(filePath):
            fileName = filePath.split("/")[-1].replace(" ","")
            original_name = fileName.replace(".pdf","")
            copy_count = 1
            while fileName in self.pdfPaths:
                if self.allowCopiesCB.get() == 1:
                    fileName = f"{original_name}_copy{copy_count}.pdf"
                    copy_count += 1
                else:
                    return
            self.pdfPaths[fileName] = filePath
            self.pdfTV.insert(parent="",index="end",iid=self.lastIndex,values=(fileName))
            self.lastIndex += 1
            self.triggerBtns()

    def delPDF(self) -> None:
        itemsTBD = self.pdfTV.selection()
        for item in itemsTBD:
                itemKey = self.pdfTV.item(item,'values')[0]
                self.pdfPaths.pop(itemKey)
                self.pdfTV.delete(item)
        self.triggerBtns()

    def moveUp(self) -> None:
    # Get the selected item(s)
        selected_items = self.pdfTV.selection()

        # Move the selected item(s) up by changing the position
        for item in selected_items:
            current_position = self.pdfTV.index(item)
            if current_position > 0:
                new_position = current_position - 1
                self.pdfTV.move(item, "", new_position)
    
    def moveDown(self) -> None:
        # Get the selected item(s)
        selected_items = self.pdfTV.selection()

        # Move the selected item(s) down by changing the position
        for item in reversed(selected_items):  # Reverse the order to avoid conflicts during movement
            current_position = self.pdfTV.index(item)
            if current_position < self.pdfTV.index(self.pdfTV.get_children()[-1]):
                new_position = current_position + 1
                self.pdfTV.move(item, "", new_position)

    def mergPDF(self) -> None:
        savePath = filedialog.askdirectory(title="Select a Directory To Save To.")
        if savePath:
            pdfsInOrder = []
            for item in self.pdfTV.get_children():
                pdfsInOrder.append(self.pdfTV.item(item,'values')[0])

            success = merge.mergePDFs(self.pdfPaths,pdfsInOrder,savePath)
            if(success):
                messagebox.showinfo("Success!","\"merged.pdf\" Created Successfully!")
            else:
                messagebox.showerror("Error!","Something went wrong while merging.")
            
            for item in self.pdfTV.get_children():
                    itemKey = self.pdfTV.item(item,'values')[0]
                    self.pdfPaths.pop(itemKey)
                    self.pdfTV.delete(item)
            self.triggerBtns()
        else:
            pass

if __name__ == "__main__":
    program = pdfMerger()
    program.runProgram()