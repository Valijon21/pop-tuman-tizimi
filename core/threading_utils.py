"""
core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi.
UI ning qotib qolishini (Not Responding) oldini olish uchun og'ir amallarni fon oqimida bajarish.
"""
from typing import Callable, Any, Optional
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    """
    Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread.
    Signallar:
      - result_ready(object): Muvaffaqiyatli yakunlanganda natijani uzatadi
      - error_occurred(str): Xatolik yuz berganda xatolik matnini uzatadi
      - progress(int, str): Jarayon foizi va holat matnini uzatadi
    """
    result_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, target_func: Callable[..., Any], *args: Any, parent: Optional[Any] = None, **kwargs: Any):
        super().__init__(parent)
        self.target_func = target_func
        self.args = args
        self.kwargs = kwargs
        self._is_cancelled = False

    def cancel(self) -> None:
        """Oqimni to'xtatish bayrog'ini o'rnatish."""
        self._is_cancelled = True

    def run(self) -> None:
        try:
            # Agar funksiya progress_callback ni qo'llab-quvvatlasa
            if hasattr(self.target_func, "__code__") and "progress_callback" in self.target_func.__code__.co_varnames:
                self.kwargs["progress_callback"] = lambda pct, msg: self.progress.emit(pct, msg)

            result = self.target_func(*self.args, **self.kwargs)
            if not self._is_cancelled:
                self.result_ready.emit(result)
        except Exception as e:
            if not self._is_cancelled:
                self.error_occurred.emit(str(e))
