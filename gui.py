import flet as ft
import os
import subprocess
import webbrowser
import threading
from extract_paths import extract_from_project, check_existence

# Stable version for Flet 0.25.2
def main(page: ft.Page):
    page.title = "Bitwig Path Extractor"
    page.window_width = 800
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    
    # State
    current_file_path = None
    all_results = []
    generated_txt_path = None
    generated_html_path = None

    # --- UI Elements ---
    
    status_text = ft.Text("Select a .bwproject file to begin", size=16, color=ft.Colors.GREY_400)
    
    missing_check = ft.Checkbox(label="Perform missing file scan", value=True)
    txt_check = ft.Checkbox(label="Generate .txt output", value=True)
    html_check = ft.Checkbox(label="Generate .html output", value=True)
    
    progress_bar = ft.ProgressBar(width=float("inf"), color=ft.Colors.BLUE_400, bgcolor=ft.Colors.GREY_900, visible=False)

    search_field = ft.TextField(
        label="Search paths...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True
    )

    results_list = ft.ListView(expand=1, spacing=10, padding=10)
    
    select_file_btn = ft.ElevatedButton(
        "Select .bwproject File",
        icon=ft.Icons.FILE_OPEN,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["bwproject"])
    )
    
    def open_file(file_path):
        if file_path and os.path.exists(file_path):
            # For Windows, os.startfile is the safest to avoid console popping
            if os.name == 'nt':
                os.startfile(file_path)
            else:
                webbrowser.open(f"file://{os.path.abspath(file_path)}")

    # Buttons for specific files
    open_html_btn = ft.ElevatedButton("Open HTML Report", icon=ft.Icons.HTML, on_click=lambda _: open_file(generated_html_path), visible=False)
    open_txt_btn = ft.ElevatedButton("Open TXT List", icon=ft.Icons.DESCRIPTION, on_click=lambda _: open_file(generated_txt_path), visible=False)
    clear_btn = ft.ElevatedButton("Clear", icon=ft.Icons.CLEAR, on_click=lambda _: clear_all(None), visible=False)

    action_buttons = ft.Row([
        open_html_btn,
        open_txt_btn,
        clear_btn
    ], alignment=ft.MainAxisAlignment.CENTER)

    # --- Logic ---

    def process_file(file_path):
        nonlocal current_file_path, all_results, generated_txt_path, generated_html_path
        if not file_path.endswith('.bwproject'):
            status_text.value = "Error: Please provide a .bwproject file."
            page.update()
            return

        current_file_path = file_path
        status_text.value = f"Processing: {os.path.basename(file_path)}..."
        status_text.color = ft.Colors.BLUE_200
        progress_bar.visible = True
        progress_bar.value = None
        
        # Reset relative paths
        generated_txt_path = None
        generated_html_path = None
        open_html_btn.visible = False
        open_txt_btn.visible = False
        clear_btn.visible = False
        
        missing_check.disabled = True
        txt_check.disabled = True
        html_check.disabled = True
        select_file_btn.disabled = True
        
        page.update()

        def extraction_task():
            nonlocal all_results, generated_txt_path, generated_html_path
            try:
                paths = extract_from_project(file_path)
                if paths is None:
                    status_text.value = "Error: File not found or invalid."
                    status_text.color = ft.Colors.RED_400
                    finish_processing()
                    return

                project_dir = os.path.dirname(file_path)
                found_paths = []
                missing_paths = []

                if missing_check.value:
                    found_paths, missing_paths = check_existence(paths, project_dir)
                    all_results = [{"path": p, "status": "Found"} for p in found_paths] + \
                                  [{"path": p, "status": "Missing"} for p in missing_paths]
                else:
                    all_results = [{"path": p, "status": "N/A"} for p in paths]

                # Generate Outputs
                if txt_check.value:
                    generated_txt_path = os.path.join(project_dir, "extracted_sample_paths.txt")
                    with open(generated_txt_path, "w", encoding="utf-8") as f:
                        for p in paths:
                            f.write(p + "\n")
                    open_txt_btn.visible = True

                if html_check.value:
                    generated_html_path = os.path.join(project_dir, "sample_report.html")
                    generate_html_report(generated_html_path, all_results, os.path.basename(file_path))
                    open_html_btn.visible = True

                status_text.value = f"Done! Found {len(paths)} paths."
                status_text.color = ft.Colors.GREEN_400
                clear_btn.visible = True
                
                filter_results("")
            except Exception as e:
                status_text.value = f"Error: {str(e)}"
                status_text.color = ft.Colors.RED_400
            
            finish_processing()

        def finish_processing():
            progress_bar.visible = False
            missing_check.disabled = False
            txt_check.disabled = False
            html_check.disabled = False
            select_file_btn.disabled = False
            page.update()

        threading.Thread(target=extraction_task, daemon=True).start()

    def generate_html_report(file_path, results, project_name):
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Path Report - {project_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #121212; color: #e0e0e0; padding: 40px; }}
        h1 {{ color: #bb86fc; }}
        .stats {{ margin-bottom: 20px; font-size: 1.1em; }}
        table {{ width: 100%; border-collapse: collapse; background: #1e1e1e; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #333; }}
        th {{ background: #2d2d2d; color: #03dac6; }}
        tr:hover {{ background: #252525; }}
        .status-Found {{ color: #4caf50; font-weight: bold; }}
        .status-Missing {{ color: #f44336; font-weight: bold; }}
        .status-NA {{ color: #888; }}
        .path {{ word-break: break-all; font-family: monospace; }}
    </style>
</head>
<body>
    <h1>Bitwig Sample Report</h1>
    <div class="stats">
        <p>Project: <strong>{project_name}</strong></p>
        <p>Total Paths: {len(results)}</p>
    </div>
    <table>
        <thead>
            <tr>
                <th>Path</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
        """
        for r in results:
            status_class = r['status'].replace('/', '')
            html_content += f"""
            <tr>
                <td class="path">{r['path']}</td>
                <td class="status-{status_class}">{r['status']}</td>
            </tr>
            """
        html_content += "</tbody></table></body></html>"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def filter_results(query):
        results_list.controls.clear()
        query = query.lower()
        for r in all_results:
            if query in r['path'].lower():
                color = ft.Colors.GREEN_400 if r['status'] == "Found" else (ft.Colors.RED_400 if r['status'] == "Missing" else ft.Colors.GREY_400)
                icon = ft.Icons.CHECK_CIRCLE if r['status'] == "Found" else (ft.Icons.ERROR if r['status'] == "Missing" else ft.Icons.QUESTION_MARK)
                results_list.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(icon, color=color),
                        title=ft.Text(r['path'], size=13, font_family="monospace"),
                        subtitle=ft.Text(f"Status: {r['status']}", color=color, size=11),
                        dense=True,
                    )
                )
        page.update()

    def clear_all(e):
        nonlocal current_file_path, all_results, generated_txt_path, generated_html_path
        current_file_path = None
        all_results = []
        generated_txt_path = None
        generated_html_path = None
        status_text.value = "Select a .bwproject file to begin"
        status_text.color = ft.Colors.GREY_400
        results_list.controls.clear()
        open_html_btn.visible = False
        open_txt_btn.visible = False
        clear_btn.visible = False
        search_field.value = ""
        page.update()

    file_picker = ft.FilePicker(on_result=lambda e: process_file(e.files[0].path) if e.files else None)
    page.overlay.append(file_picker)
    
    search_field.on_change = lambda e: filter_results(e.control.value)

    page.add(
        ft.Column([
            ft.Text("Bitwig Project Sample Audit", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
            ft.Text("Quickly find and verify audio files used in your Bitwig project.", size=14, color=ft.Colors.GREY_500),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(
                content=ft.Column([
                    select_file_btn,
                    ft.Container(height=10),
                    status_text
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                border=ft.border.all(1, ft.Colors.GREY_800),
                border_radius=5,
                width=float("inf"),
            ),
            ft.Row([
                missing_check,
                txt_check,
                html_check,
            ], alignment=ft.MainAxisAlignment.CENTER),
            progress_bar,
            ft.Divider(height=20),
            ft.Row([search_field]),
            ft.Container(
                content=results_list,
                border=ft.border.all(1, ft.Colors.GREY_800),
                border_radius=5,
                expand=True,
            ),
            action_buttons
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main)
