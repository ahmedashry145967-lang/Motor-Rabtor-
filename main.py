import flet as ft

def main(page: ft.Page):
    # إعدادات الشاشة الأساسية
    page.title = "Motor Rabtor"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # أداة الاهتزاز (Haptic Feedback) عند الضغط على الأزرار
    haptic = ft.HapticFeedback()
    page.overlay.append(haptic)

    # متغيرات لحفظ حالة الاتصال والروبوت
    connection_type = ft.Text("غير متصل", color=ft.Colors.RED_ACCENT, weight=ft.FontWeight.BOLD)
    robot_power = False
    radar_obstacle = False

    # دالة عامة لإرسال الأوامر وتشغيل الهزاز
    def send_command(cmd_name):
        haptic.heavy_impact()  # تشغيل الهزاز عند الضغط
        page.snack_bar = ft.SnackBar(ft.Text(f"تم إرسال أمر: {cmd_name}"), duration=800)
        page.snack_bar.open = True
        page.update()
        # ملاحظة: هنا يتم وضع كود إرسال الأمر الفعلي للـ ESP32 أو الـ Arduino

    # ==========================================
    # الشريط العلوي (الاتصال بالبلوتوث والواي فاي)
    # ==========================================
    def connect_ble(e):
        haptic.medium_impact()
        connection_type.value = "متصل (BLE Bluetooth)"
        connection_type.color = ft.Colors.BLUE_ACCENT
        page.update()

    def connect_wifi(e):
        haptic.medium_impact()
        connection_type.value = "متصل (Wi-Fi 802.11 b/g/n)"
        connection_type.color = ft.Colors.GREEN_ACCENT
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("MOTOR RABTOR", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_ACCENT),
        bgcolor=ft.Colors.GREY_900,
        actions=[
            ft.IconButton(ft.Icons.BLUETOOTH, tooltip="اتصال بلوتوث BLE", on_click=connect_ble),
            ft.IconButton(ft.Icons.WIFI, tooltip="اتصال واي فاي Wi-Fi 4", on_click=connect_wifi),
        ]
    )

    status_bar = ft.Container(
        content=ft.Row([ft.Text("حالة الاتصال:"), connection_type], alignment=ft.MainAxisAlignment.CENTER),
        padding=8,
        bgcolor=ft.Colors.GREY_900,
        border_radius=8
    )

    # ==========================================
    # الصفحة الأولى: التحكم في حركة الروبوت
    # ==========================================
    page1_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Text("التحكم في الحركة", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton("أمام", icon=ft.Icons.ARROW_UPWARD, width=120, height=60, on_click=lambda e: send_command("تحرك للأمام")),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    ft.ElevatedButton("يسار", icon=ft.Icons.ARROW_BACK, width=120, height=60, on_click=lambda e: send_command("اتجه لليسار")),
                    ft.ElevatedButton("يمين", icon=ft.Icons.ARROW_FORWARD, width=120, height=60, on_click=lambda e: send_command("اتجه لليمين")),
                ]
            ),
            ft.ElevatedButton("خلف", icon=ft.Icons.ARROW_DOWNWARD, width=120, height=60, on_click=lambda e: send_command("تحرك للخلف")),
        ]
    )

    # ==========================================
    # الصفحة الثانية: الصوتيات والإضاءة والطاقة
    # ==========================================
    robot_response_text = ft.Text("رد الروبوت: في انتظار الأوامر...", color=ft.Colors.AMBER)

    def toggle_power(e):
        nonlocal robot_power
        robot_power = not robot_power
        e.control.text = "إيقاف الروبوت" if robot_power else "تشغيل الروبوت"
        e.control.bgcolor = ft.Colors.RED_700 if robot_power else ft.Colors.GREEN_700
        send_command("تشغيل الروبوت" if robot_power else "إيقاف الروبوت")

    def simulate_speaker(e):
        # محاكاة رد الروبوت
        responses = ["حاضر", "تمام", "شكراً", "لا"]
        import random
        reply = random.choice(responses)
        robot_response_text.value = f"رد الروبوت: {reply}"
        send_command(f"سبيكر: {reply}")

    page2_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        controls=[
            ft.Text("الأوامر والصوتيات", size=20, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("1. الكلكس", icon=ft.Icons.CAMPAIGN, width=260, height=45, on_click=lambda e: send_command("تشغيل الكلكس")),
            ft.ElevatedButton("2. الميكروفون (تسجيل أمر)", icon=ft.Icons.MIC, width=260, height=45, on_click=lambda e: send_command("بدء تسجيل صوتي")),
            ft.ElevatedButton("3. الإسبيكر (رد الروبوت)", icon=ft.Icons.VOLUME_UP, width=260, height=45, on_click=simulate_speaker),
            robot_response_text,
            ft.ElevatedButton("4. الضوء", icon=ft.Icons.LIGHTBULB, width=260, height=45, on_click=lambda e: send_command("تشغيل/إطفاء الضوء")),
            ft.ElevatedButton("5. تشغيل الروبوت", icon=ft.Icons.POWER_SETTINGS_NEW, width=260, height=50, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=toggle_power),
        ]
    )

    # ==========================================
    # الصفحة الثالثة: التحكم في أطراف الروبوت
    # ==========================================
    page3_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Text("التحكم في الأطراف", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("1. حركة الرأس", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.ElevatedButton("رأس شمال", width=130, on_click=lambda e: send_command("رأس شمال")),
                ft.ElevatedButton("رأس يمين", width=130, on_click=lambda e: send_command("رأس يمين")),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Text("2. اليد اليمنى", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.ElevatedButton("يد يمنى فوق", width=130, on_click=lambda e: send_command("يد يمنى فوق")),
                ft.ElevatedButton("يد يمنى تحت", width=130, on_click=lambda e: send_command("يد يمنى تحت")),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Text("3. اليد اليسرى", weight=ft.FontWeight.W_500),
            ft.Row([
                ft.ElevatedButton("يد يسرى فوق", width=130, on_click=lambda e: send_command("يد يسرى فوق")),
                ft.ElevatedButton("يد يسرى تحت", width=130, on_click=lambda e: send_command("يد يسرى تحت")),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ]
    )

    # ==========================================
    # الصفحة الرابعة: الرادار وكشف العوائق
    # ==========================================
    radar_status_text = ft.Text("الطريق آمن - لا يوجد عوائق", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    
    radar_screen = ft.Container(
        width=220,
        height=220,
        bgcolor=ft.Colors.GREEN_900,
        border=ft.border.all(3, ft.Colors.GREEN_ACCENT),
        border_radius=12,
        alignment=ft.alignment.center,
        content=radar_status_text
    )

    # دالة لتجربة محاكاة وجود جسم أمام الروبوت
    def toggle_obstacle_test(e):
        nonlocal radar_obstacle
        radar_obstacle = not radar_obstacle
        if radar_obstacle:
            radar_screen.bgcolor = ft.Colors.RED_800
            radar_screen.border = ft.border.all(3, ft.Colors.RED_ACCENT)
            radar_status_text.value = "تحذير! يوجد جسم أمام الروبوت"
            haptic.heavy_impact()
        else:
            radar_screen.bgcolor = ft.Colors.GREEN_900
            radar_screen.border = ft.border.all(3, ft.Colors.GREEN_ACCENT)
            radar_status_text.value = "الطريق آمن - لا يوجد عوائق"
        page.update()

    page4_content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Text("نظام الرادار", size=20, weight=ft.FontWeight.BOLD),
            radar_screen,
            ft.Row([
                ft.ElevatedButton("1. رادار شمال", icon=ft.Icons.ROTATE_LEFT, width=140, on_click=lambda e: send_command("تحريك الرادار شمال")),
                ft.ElevatedButton("2. رادار يمين", icon=ft.Icons.ROTATE_RIGHT, width=140, on_click=lambda e: send_command("تحريك الرادار يمين")),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.TextButton("تجربة إنذار الرادار (محاكاة عائق)", on_click=toggle_obstacle_test)
        ]
    )

    # ==========================================
    # نظام التنقل بين الصفحات الأربع
    # ==========================================
    pages = [page1_content, page2_content, page3_content, page4_content]
    body_container = ft.Container(content=pages[0], expand=True, padding=10)

    def change_tab(e):
        haptic.light_impact()
        body_container.content = pages[e.control.selected_index]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=change_tab,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.GAMEPAD, label="الحركة"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_VOICE, label="الأوامر"),
            ft.NavigationBarDestination(icon=ft.Icons.ACCESSIBILITY_NEW, label="الأطراف"),
            ft.NavigationBarDestination(icon=ft.Icons.RADAR, label="الرادار"),
        ]
    )

    # إضافة العناصر النهائية للصفحة
    page.add(status_bar, body_container)

ft.app(target=main)
