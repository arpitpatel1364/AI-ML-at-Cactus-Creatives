def create_task_class(task_type):
    """Generates a customised class for a specific task."""
    
    def perform(self):
        return f"Executing {self.task_name} logic for {task_type}..."

    class_name = f"{task_type.capitalize()}Task"
    
    return type(class_name, (object,), {
        "task_name": "MainTask",
        "execute": perform
    })

# Usage
PDFTask = create_task_class("pdf")
enc_task = create_task_class("encryption")
for_name=create_task_class("for_name")


my_pdf_job = PDFTask()
print(my_pdf_job.execute()) 