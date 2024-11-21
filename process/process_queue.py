import queue
from typing import Callable, Any

class ProcessQueue:
    _instance = None
    _initialized = False

    def __new__(cls):
        # Eğer instance yoksa yeni bir instance oluştur
        if cls._instance is None:
            cls._instance = super(ProcessQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # __init__ metodunun sadece bir kez çalışmasını sağla
        if not ProcessQueue._initialized:
            self.task_queue = queue.Queue()
            ProcessQueue._initialized = True

    @classmethod
    def get_instance(cls):
        """Singleton instance'ı döndüren sınıf metodu"""
        if cls._instance is None:
            cls._instance = ProcessQueue()
        return cls._instance

    def add_task(self, func: Callable, *args, **kwargs):
        """Kuyruğa yeni bir görev ekler"""
        print("Kuyruğa görev ekleniyor...")
        task = (func, args, kwargs)
        self.task_queue.put(task)

    def execute_all(self):
        """Kuyruktaki tüm görevleri sırayla çalıştırır"""
        results = []
        while not self.task_queue.empty():
            try:
                func, args, kwargs = self.task_queue.get()
                result = func(*args, **kwargs)
                results.append(result)
                self.task_queue.task_done()
            except Exception as e:
                results.append(f"Hata: {str(e)}")
        return results

    def size(self):
        """Kuyruktaki görev sayısını döndürür"""
        return self.task_queue.qsize()

    def is_empty(self):
        """Kuyruk boş mu kontrolü yapar"""
        return self.task_queue.empty()