import tkinter as tk
from tkinter import messagebox, ttk
from kb_suggester import KBSuggester
from task_management import Task, TaskGroup, Timeline

class TaskApp:
    def __init__(self, root, suggester):
        self.root = root
        self.root.title("Task Checklist and Timeline")

        self.timeline = Timeline()
        self.suggester = suggester

        # Estilo para os widgets
        s = ttk.Style()
        s.configure('TFrame', background='#E0E0E0')  # Cor de fundo do frame principal
        s.configure('TLabel', background='#E0E0E0')  # Cor de fundo para labels
        s.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 12))  # Botões com fundo verde e texto branco
        s.configure('TCheckbutton', background='#E0E0E0', font=('Helvetica', 12))  # Checkbuttons com fundo claro

        # Frame principal
        self.main_frame = ttk.Frame(root, padding=(20, 20))
        self.main_frame.pack()

        # Título
        self.title_label = ttk.Label(self.main_frame, text="Atendimento de Chamado", font=('Helvetica', 18, 'bold'))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Descrição do Atendimento
        self.label = ttk.Label(self.main_frame, text="Descrição do Atendimento:")
        self.label.grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)

        self.description_entry = ttk.Entry(self.main_frame, width=50)
        self.description_entry.grid(row=1, column=1, padx=(0, 10), pady=5)

        # Número do Chamado
        self.chamado_label = ttk.Label(self.main_frame, text="Número do Chamado:")
        self.chamado_label.grid(row=2, column=0, sticky='w', padx=(0, 10), pady=5)

        self.chamado_entry = ttk.Entry(self.main_frame, width=20)
        self.chamado_entry.grid(row=2, column=1, padx=(0, 10), pady=5)

        # Botão Iniciar Atendimento
        self.start_button = ttk.Button(self.main_frame, text="Iniciar Atendimento", command=self.start_attendance, width=20)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Lista de Tarefas
        self.tasks_frame = ttk.Frame(self.main_frame)
        self.tasks_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

        self.task_checkbuttons = []

        # Botão de Feedback
        self.feedback_button = ttk.Button(self.main_frame, text="Enviar Feedback", command=self.ask_feedback, state=tk.DISABLED, width=20)
        self.feedback_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Botão Salvar Procedimento
        self.save_button = ttk.Button(self.main_frame, text="Salvar Procedimento", command=self.save_procedure, state=tk.DISABLED, width=20)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def start_attendance(self):
        description = self.description_entry.get()
        if not description:
            messagebox.showwarning("Aviso", "Por favor, insira a descrição do atendimento.")
            return

        try:
            # Sugerir KB com base na descrição
            suggested_kb = self.suggester.suggest_kb(description)

            if not suggested_kb:
                messagebox.showwarning("Aviso", "Nenhum KB encontrado para a descrição fornecida.")
                return

            # Adicionar tarefas baseadas no KB sugerido
            atendimento_group = TaskGroup(suggested_kb["title"])
            for task_name in suggested_kb["tasks"]:
                atendimento_group.add_task(Task(task_name))
            self.timeline.add_task_group(atendimento_group)

            # Atualizar a lista de tarefas na interface
            self.update_task_list()

            # Habilitar os botões de feedback e salvar procedimento após iniciar o atendimento
            self.feedback_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_task_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        self.task_checkbuttons.clear()

        for group in self.timeline.task_groups:
            group_label = ttk.Label(self.tasks_frame, text=group.name, font=('Helvetica', 14, 'bold'))
            group_label.pack(anchor='w', pady=(10, 0))

            for task in group.tasks:
                var = tk.BooleanVar(value=task.done)
                checkbutton = ttk.Checkbutton(self.tasks_frame, text=task.name, variable=var, command=lambda t=task, v=var: self.toggle_task_done(t, v))
                checkbutton.pack(anchor='w', padx=20)
                self.task_checkbuttons.append((task, var))

    def toggle_task_done(self, task, var):
        task.toggle_done()
        var.set(task.done)

        if all(group.all_tasks_done() for group in self.timeline.task_groups):
            self.ask_feedback()

    def ask_feedback(self):
        response = messagebox.askyesno("Feedback", "O problema foi resolvido com sucesso?")
        if response:
            messagebox.showinfo("Informação", "Atendimento concluído com sucesso!")
            self.save_procedure()  # Salvar procedimento se o atendimento foi concluído com sucesso
        else:
            messagebox.showwarning("Aviso", "Encaminhando chamado para o time de nível dois.")

    def save_procedure(self):
        if self.timeline.task_groups:
            chamado_number = self.chamado_entry.get().strip()
            if not chamado_number:
                messagebox.showwarning("Aviso", "Por favor, insira o número do chamado.")
                return

            file_name = f"Procedimento_{chamado_number}.txt"

            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(f"Procedimento para chamado número {chamado_number}:\n\n")
                    for group in self.timeline.task_groups:
                        file.write(f"{group.name}:\n")
                        for task in group.tasks:
                            file.write(f"- {task.name}\n")
                        file.write("\n")
                messagebox.showinfo("Informação", f"Procedimento salvo em '{file_name}'.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Aviso", "Nenhum procedimento para salvar.")

if __name__ == "__main__":
    # Inicializar o sugeridor de KB
    suggester = KBSuggester()

    # Inicializar a interface gráfica
    root = tk.Tk()
    app = TaskApp(root, suggester)
    root.mainloop()
