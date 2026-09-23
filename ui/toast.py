"""
Pop Tuman Tashkilotlari va INN Tizimi
Zamonaviy Toast / Banner Bildirishnomalar Tizimi (Non-blocking Notifications)
"""
import customtkinter as ctk

class ToastNotification:
    """Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma."""
    
    COLORS = {
        "success": {"bg": "#10B981", "fg": "#FFFFFF", "icon": "✓"},
        "info":    {"bg": "#2563EB", "fg": "#FFFFFF", "icon": "ℹ"},
        "warning": {"bg": "#F59E0B", "fg": "#1F2937", "icon": "⚠"},
        "error":   {"bg": "#EF4444", "fg": "#FFFFFF", "icon": "✕"}
    }

    def __init__(self, parent: ctk.CTk, message: str, toast_type: str = "info", duration_ms: int = 2500):
        self.parent = parent
        self.duration_ms = duration_ms
        
        cfg = self.COLORS.get(toast_type, self.COLORS["info"])
        
        # Asosiy konteyner
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=cfg["bg"],
            corner_radius=12,
            border_width=0
        )
        
        # Matn va belgi
        full_text = f"  {cfg['icon']}  {message}  "
        self.label = ctk.CTkLabel(
            self.frame,
            text=full_text,
            text_color=cfg["fg"],
            font=("Segoe UI", 13, "bold"),
            padx=14,
            pady=8
        )
        self.label.pack()

        # Oynaning pastki markaziga joylashtirish
        self.frame.place(relx=0.5, rely=0.92, anchor="center")
        self.frame.lift()

        # Belgilangan vaqtdan keyin yo'q qilish
        self.parent.after(self.duration_ms, self.destroy)

    def destroy(self):
        try:
            if self.frame and self.frame.winfo_exists():
                self.frame.destroy()
        except Exception:
            pass

def show_toast(parent: ctk.CTk, message: str, toast_type: str = "info", duration_ms: int = 2500):
    """Qulay yordamchi funksiya."""
    if parent and parent.winfo_exists():
        ToastNotification(parent, message, toast_type=toast_type, duration_ms=duration_ms)
