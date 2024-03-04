from tkinter import filedialog as fd 
import shutil
import customtkinter
import tkinter
import os


filedict = {}
world_dstFolder = {}
current_drt = '' 
bossrushfiles = []
current_bossrush_boss = 0

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')



class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # add widgets onto the frame...
        self.folder_select_frame = customtkinter.CTkFrame(self)
        self.folder_select_frame.grid(pady = 5, padx=10, column= 0)

        self.world_dst_label_frame = customtkinter.CTkFrame(self, height = 50)
        self.world_dst_label_frame.grid(pady = 5, padx=10, column= 0)

        self.world_dst_button_frame = customtkinter.CTkScrollableFrame(self, width= 350)
        self.world_dst_button_frame.grid(pady = 5, padx=10, column= 0)

        self.saves_label_frame = customtkinter.CTkFrame(self)
        self.saves_label_frame.grid(pady = 5, padx=10, column= 0)

        self.saves_button_frame = customtkinter.CTkScrollableFrame(self, width= 350)
        self.saves_button_frame.grid(pady = 5, padx=10, column= 0)
        self.saves_button_frame.columnconfigure(0, weight = 1)

        self.current_save_label_frame = customtkinter.CTkFrame(self)
        self.current_save_label_frame.grid(pady = 5, padx=10, column= 0)

        self.current_save_frame = customtkinter.CTkFrame(self, height = 50)
        self.current_save_frame.grid(pady = 5, padx=10, column= 0)

        self.reload_save_frame = customtkinter.CTkFrame(self, height = 50)
        self.reload_save_frame.grid(pady = 5, padx=10, column= 0)

        self.reset_button_frame = customtkinter.CTkFrame(self, height = 50)
        self.reset_button_frame.grid(pady = 5, padx=10, column= 0)

        a = customtkinter.CTkButton(master= self.folder_select_frame, text ='Click to Select Saves Folder', font = ('arial', 18 ), 
                            height = 30, width = 250, command = lambda: [self.callbackSaves()])
        a.grid(pady=12, padx=10)

        b = customtkinter.CTkButton(master= self.folder_select_frame, text ='Click to Select "autosave.dat" File', font = ('arial', 18 ), 
                                    height = 30, width = 250, command = lambda: [self.enableworld_dst()])
        b.grid(pady=12, padx=10)


        label1 = customtkinter.CTkLabel(master= self.world_dst_label_frame, text = 'Worlds', 
                                    font = ('arial', 24 ))
        label1.grid(pady=12, padx=10)

        label2 = customtkinter.CTkLabel(master= self.saves_label_frame, text = 'Saves', 
                                    font = ('arial', 24 ))
        label2.grid(pady=12, padx=10)

        currentSaveLabel1 = customtkinter.CTkLabel(master= self.current_save_label_frame, text = 'Current Save Is', 
                                    font = ('arial', 24 ))
        currentSaveLabel1.grid(pady=12, padx=10)

    def callbackSaves(self):
        save_dir_name = fd.askdirectory()
        filedict['src'] = save_dir_name

    def enableworld_dst(self):
        i = 0
        r = 1
        savedata_name = fd.askopenfilename()
        filedict['dst'] = str(savedata_name)
        folderWalker = os.walk(filedict['src'])
        saves_folders = next(folderWalker)[1]
        world_names = []
        world_dst = []
        for folder in saves_folders:
            customtkinter.CTkButton(self.world_dst_button_frame, text = folder, 
                                command = lambda name = folder: self.enableSaves(name, world_dstFolder)).grid(row = r, column = i, 
                                                                                                    padx = 10, pady = 10, sticky="news")
            world_dst.append(folder)
            i = i+1
            if i == 2:
                i = 0
                r = r + 1

        for line in [x[0] for x in os.walk(filedict['src'])]:
            world_names.append(line)
        world_names = world_names[1:]
        world_dstFolder = dict(zip(world_dst, world_names))

    def enableSaves(self, folder, world_dstFolder):
        i = 0
        r = 1
        global bossrushfiles
        bossrushfiles = []
        for widgets in self.saves_button_frame.winfo_children():
            if isinstance(widgets, customtkinter.CTkButton):
                widgets.destroy()
        folderWalker = os.walk(world_dstFolder[folder])
        folders = next(folderWalker)[2]
        for file in folders:
                bossrushfiles.append(file)
                entry = file
                entry = entry.split('.')[0]
                if '_' in entry:
                    entry = entry[4:]
                customtkinter.CTkButton(self.saves_button_frame, text = entry, 
                                    command= lambda name = file: self.loadSave(name, world_dstFolder[folder])).grid(row = r, column = i, 
                                                                                                            padx = 10, pady = 10, sticky="news")
                i = i+1 
                if i == 1:
                    i = 0
                    r = r + 1

    def loadSave(self, file, filepath):
        current_drt = f'{filepath}/{file}'
        shutil.copyfile(current_drt, filedict['dst'])
        for widgets in self.reload_save_frame.winfo_children():
            if isinstance(widgets, customtkinter.CTkButton):
                widgets.destroy()

        if filepath[-4:] != 'Rush':
            reloadSaveButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Reload Save', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: [self.reloadSave(current_drt)])
            reloadSaveButton.grid(pady=12, padx=10)
        else:
            nextBossButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Next Boss', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: self.nextBoss(current_drt, file, filepath))
            nextBossButton.grid(pady=12, padx=10)

            reset_button = customtkinter.CTkButton(master = self.reset_button_frame, text = 'Reset', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: self.resetButton(file, filepath))
            reset_button.grid(pady=12, padx=10)

        if len(self.current_save_frame.winfo_children())  >  0:
            self.current_save_frame.winfo_children()[0].destroy()
        if len(self.reset_button_frame.winfo_children())  >  1:
            self.reset_button_frame.winfo_children()[0].destroy()

        entry = file
        entry = entry.split('.')[0]
        if '_' in entry:
            entry = entry[4:]
        currentSaveLabel2 = customtkinter.CTkLabel(master= self.current_save_frame, text = entry, 
                                font = ('arial', 24 ))
        currentSaveLabel2.grid(pady=12, padx=10)


    def reloadSave(self, current_drt):
        shutil.copyfile(current_drt, filedict['dst'])


    def nextBoss(self, current_drt, file, filepath):
        global current_bossrush_boss
        global bossrushfiles
        last_boss = bossrushfiles[-1]
        if last_boss == file:
            current_bossrush_boss = -1
        current_bossrush_boss += 1
        file = bossrushfiles[current_bossrush_boss]
        current_drt = f'{filepath}/{file}'
        shutil.copyfile(current_drt, filedict['dst'])
        for widgets in self.reload_save_frame.winfo_children():
            if isinstance(widgets, customtkinter.CTkButton):
                widgets.destroy()

        if filepath[-4:] != 'Rush':
            reloadSaveButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Reload Save', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: [self.reloadSave(current_drt)])
            reloadSaveButton.grid(pady=12, padx=10)
        else:
            nextBossButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Next Boss', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: self.nextBoss(current_drt, file, filepath))
            nextBossButton.grid(pady=12, padx=10)
        
        if len(self.current_save_frame.winfo_children())  >  0:
            self.current_save_frame.winfo_children()[0].destroy()
        entry = file
        entry = entry.split('.')[0]
        if '_' in entry:
            entry = entry[4:]
        currentSaveLabel2 = customtkinter.CTkLabel(master= self.current_save_frame, text = entry, 
                                font = ('arial', 24 ))
        currentSaveLabel2.grid(pady=12, padx=10)

    def resetButton(self, file, filepath):
        global current_bossrush_boss
        self.current_save_frame.winfo_children()[0].destroy()
        self.reset_button_frame.winfo_children()[0].destroy()
        for widgets in self.reload_save_frame.winfo_children():
            if isinstance(widgets, customtkinter.CTkButton):
                widgets.destroy()
        current_bossrush_boss = 0
        file = bossrushfiles[current_bossrush_boss]
        current_drt = f'{filepath}/{file}'
        shutil.copyfile(current_drt, filedict['dst'])
        for widgets in self.reload_save_frame.winfo_children():
            if isinstance(widgets, customtkinter.CTkButton):
                widgets.destroy()

        if filepath[-4:] != 'Rush':
            reloadSaveButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Reload Save', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: [self.reloadSave(current_drt)])
            reloadSaveButton.grid(pady=12, padx=10)
        else:
            nextBossButton = customtkinter.CTkButton(master= self.reload_save_frame, text ='Next Boss', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: self.nextBoss(current_drt, file, filepath))
            nextBossButton.grid(pady=12, padx=10)

            reset_button = customtkinter.CTkButton(master = self.reset_button_frame, text = 'Reset', font = ('arial', 18 ), 
                                height = 30, width = 250, command = lambda: self.resetButton(file, filepath))
            reset_button.grid(pady=12, padx=10)
        
        if len(self.current_save_frame.winfo_children())  >  0:
            self.current_save_frame.winfo_children()[0].destroy()
        
        entry = file
        entry = entry.split('.')[0]
        if '_' in entry:
            entry = entry[4:]
        currentSaveLabel2 = customtkinter.CTkLabel(master= self.current_save_frame, text = entry, 
                                font = ('arial', 24 ))
        currentSaveLabel2.grid(pady=12, padx=10)


class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = MyFrame(master=self, width=600, height=1000, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")
        print(self.my_frame)

# class Root(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         root = customtkinter.CTk()
#         root.geometry('600x1000')
#         root.title('Kingdom Hearts Practice Helper')
#         root.columnconfigure(0, weight = 1)


root = Root()
root.mainloop()