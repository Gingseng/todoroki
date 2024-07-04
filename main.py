# main.py

import tkinter as tk
from tkinter import messagebox
from kb_suggester import KBSuggester
from task_management import Task, TaskGroup, Timeline

class TaskApp:
    def __init__(self, root, suggester):
        self.root = root
        self.root.title("Task Checklist and Timeline")

        self.timeline = Timeline()
        self.suggester = suggester

        self.label = tk.Label(root, text="Descrição do Atendimento:")
        self.label.pack()

        self.description_entry = tk.Entry(root, width=50)
        self.description_entry.pack()

        self.start_button = tk.Button(root, text="Iniciar Atendimento", command=self.start_attendance)
        self.start_button.pack()

        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(fill=tk.BOTH, expand=True)

        self.task_checkbuttons = []

        self.feedback_button = tk.Button(root, text="Enviar Feedback", command=self.ask_feedback, state=tk.DISABLED)
        self.feedback_button.pack()

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

            # Habilitar o botão de feedback após iniciar o atendimento
            self.feedback_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_task_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        self.task_checkbuttons.clear()

        for group in self.timeline.task_groups:
            group_label = tk.Label(self.tasks_frame, text=group.name, font=('Helvetica', 14, 'bold'))
            group_label.pack(anchor='w', pady=(10, 0))

            for task in group.tasks:
                var = tk.BooleanVar(value=task.done)
                checkbutton = tk.Checkbutton(self.tasks_frame, text=task.name, variable=var, command=lambda t=task, v=var: self.toggle_task_done(t, v))
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
        else:
            messagebox.showwarning("Aviso", "Encaminhando chamado para o time de nível dois.")

if __name__ == "__main__":
    # Inicializar o sugeridor de KB
    suggester = KBSuggester()

    # Inicializar a interface gráfica
    root = tk.Tk()
    app = TaskApp(root, suggester)
    root.mainloop()
