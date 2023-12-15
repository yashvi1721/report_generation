import re
import subprocess
import tkinter as tk
from tkinter import filedialog
import platform
import socket
import psutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus.frames import Frame

class Header(Paragraph):
    def __init__(self, text, style):
        super().__init__(text, style)

def create_header(canvas, doc):
    header_text = "Compliance Master Report"
    header = Header(header_text, doc.styles['Heading1'])
    frame = doc.frames[0]
    frame.add(header, canvas)

def get_memory_info():
    try:
        result = subprocess.run(["dmidecode", "--type", "17"], capture_output=True, text=True, check=True)
        form_factor_match = re.search(r"Form Factor:\s*(.+)", result.stdout)
        locator_match = re.search(r"Locator:\s*(.+)", result.stdout)

        form_factor = form_factor_match.group(1).strip() if form_factor_match else "N/A"
        locator = locator_match.group(1).strip() if locator_match else "N/A"

        return form_factor, locator
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving memory information: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return "N/A", "N/A"
def get_memorydevice_info():
    try:
        result = subprocess.run(["dmidecode", "--type", "17"], capture_output=True, text=True, check=True)

        # Extracting relevant information
        array_handle_match = re.search(r"Array Handle:\s*(.+)", result.stdout)
        error_info_handle_match = re.search(r"Error Information Handle:\s*(.+)", result.stdout)
        total_width_match = re.search(r"Total Width:\s*(.+)", result.stdout)
        data_width_match = re.search(r"Data Width:\s*(.+)", result.stdout)
        size_match = re.search(r"Size:\s*(.+)", result.stdout)
        form_factor_match = re.search(r"Form Factor:\s*(.+)", result.stdout)
        set_match = re.search(r"Set:\s*(.+)", result.stdout)
        locator_match = re.search(r"Locator:\s*(.+)", result.stdout)
        bank_locator_match = re.search(r"Bank Locator:\s*(.+)", result.stdout)
        array_handle = array_handle_match.group(1).strip() if array_handle_match else "N/A"
        error_info_handle = error_info_handle_match.group(1).strip() if error_info_handle_match else "N/A"
        total_width = total_width_match.group(1).strip() if total_width_match else "N/A"
        data_width = data_width_match.group(1).strip() if data_width_match else "N/A"
        size = size_match.group(1).strip() if size_match else "N/A"
        form_factor = form_factor_match.group(1).strip() if form_factor_match else "N/A"
        set_value = set_match.group(1).strip() if set_match else "N/A"
        locator = locator_match.group(1).strip() if locator_match else "N/A"
        bank_locator = bank_locator_match.group(1).strip() if bank_locator_match else "N/A"


        return {
            "Array Handle": array_handle,
            "Error Information Handle": error_info_handle,
            "Total Width": total_width,
            "Data Width": data_width,
            "Size": size,
            "Form Factor": form_factor,
            "Set": set_value,
            "Locator": locator,
            "Bank Locator": bank_locator,
            # Include more parameter values as needed...
        }
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving memory information: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return {}

def format_system_info(info):
    formatted_info = ""
    for key, value in info.items():
        # ... (Your existing formatting logic)
        if key == "Memory Device":
            formatted_info += f"\n{key}\n"
            for mem_key, mem_value in value.items():
                formatted_info += f"    {mem_key}: {mem_value}\n"
def get_system_info():
    info = {
        "Hostname": socket.gethostname(),
        "Manufacturer": platform.system(),
        "Product Name": platform.node(),
        "Serial Number": platform.processor(),
        "BIOS Version": platform.architecture(),
        "System Version": platform.version(),
        "Baseboard Manufacture": platform.machine(),
        "Baseboard Product Name": platform.processor(),
        "Baseboard Version": platform.python_compiler(),
        "Baseboard Serial Number": platform.python_version(),
    }

    try:
        battery = psutil.sensors_battery()
        info["Battery Percent"] = battery.percent if battery else None

        info["CPU Cores"] = psutil.cpu_count(logical=False)

        cpu_info = platform.uname()
        info["CPU Information"] = cpu_info if cpu_info else None

        memory_info = psutil.virtual_memory()
        info["Total Memory"] = memory_info.total if memory_info else None

        disk_info = psutil.disk_usage('/')
        info["Total Disk Space"] = disk_info.total if disk_info else None
        info["Used Disk Space"] = disk_info.used if disk_info else None
        info["Available Disk Space"] = disk_info.free if disk_info else None
        info["Disk Space Usage Percentage"] = disk_info.percent if disk_info else None

        network_info = psutil.net_if_addrs()
        info["Network Configuration"] = network_info if network_info else None

        form_factor, locator = get_memory_info()
        info["Memory Device"] = {
            "Total Width": memory_info.width if memory_info else None,
            "Data Width": memory_info.bits if memory_info else None,
            "Size": memory_info.total if memory_info else None,
            "Form Factor": form_factor,
            "Locator": locator,
        }

        # Additional Information
        additional_info = {
            "Linux Version": platform.version(),
            "Linux Distribution": platform.system(),
            "Linux Release": platform.release(),
        }
        info["Additional Information"] = additional_info

    except Exception as e:
        print(f"Error retrieving additional information: {e}")

    return info

def format_system_info(info):
    formatted_info = ""
    for key, value in info.items():
        if key == "CPU Information":
            formatted_info += f"\n{key}:\n"
            for cpu_key, cpu_value in zip(value._fields, value):
                formatted_info += f"{cpu_key}: {cpu_value}\n"
        elif key == "Total Memory":
            formatted_info += f"\nMemory Information\n"
            formatted_info += f"{key}: {value} bytes\n"
        elif key == "Disk Space Usage Percentage":
            formatted_info += f"\nDisk Space\n"
            formatted_info += f"{key}: {value}%\n"
            formatted_info += "Filesystem      Size  Used Avail Use% Mounted on\n"
            partitions = psutil.disk_partitions()
            for partition in partitions:
                partition_info = psutil.disk_usage(partition.mountpoint)
                formatted_info += f"{partition.device}  {partition_info.total}  {partition_info.used}  {partition_info.free}  {partition_info.percent}\n"
        elif key == "Memory Device":
            formatted_info += f"\nMemory Device\n"
            for mem_key, mem_value in value.items():
                formatted_info += f"{mem_key}: {mem_value}\n"
        elif key == "Network Configuration":
            formatted_info += f"\n{key}:\n"
            for iface, addresses in value.items():
                formatted_info += f"  {iface}:\n"
                for address in addresses:
                    formatted_info += f"    {address.family.name} Address: {address.address}\n"
        elif key == "Additional Information":
            formatted_info += f"\n{key}:\n"
            for add_key, add_value in value.items():
                formatted_info += f"{add_key}: {add_value}\n"
        else:
            formatted_info += f"{key}: {value}\n"
    return formatted_info

def generate_report():
    system_info = get_system_info()
    report_text = format_system_info(system_info)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, report_text)
    download_button.config(state=tk.NORMAL)

def save_report():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if file_path:
        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            doc.addPageTemplates([PageTemplate(id='normal', frames=[Frame(doc.leftMargin, doc.bottomMargin,
             doc.width, doc.height, id='normal')])])
            elements = []

            styles = getSampleStyleSheet()

            # Header
            doc.build([Spacer(1, 1)])
            elements.append(Spacer(0.5, 0.2 * inch))
            elements.append(Header("Compliance Master System Report", styles['Heading1']))

            report_text = text_widget.get(1.0, tk.END)
            report_paragraphs = [Paragraph(line, styles["Normal"]) for line in report_text.split('\n')]
            elements.extend(report_paragraphs)
            elements.append(Header("Compliance Master System Report", styles['Heading1']))
            elements.append(Paragraph("\nDisk Space Usage:", styles["Heading2"]))
            disk_space_table = create_disk_space_table()
            elements.append(disk_space_table)

            doc.build(elements, onFirstPage=create_header, onLaterPages=create_header)
            status_label.config(text=f"Report saved to {file_path}")
        except Exception as e:
            print(f"Error saving PDF: {e}")
            status_label.config(text=f"Error saving PDF: {e}")

def create_disk_space_table():
    partitions = psutil.disk_partitions()
    data = [["Filesystem", "Size", "Used", "Avail", "Use%"]]
    for partition in partitions:
        partition_info = psutil.disk_usage(partition.mountpoint)
        data.append([
            partition.device, partition_info.total, partition_info.used,
            partition_info.free, partition_info.percent
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    return table

# Your UI setup
root = tk.Tk()
root.title("Compliance Master Report")

generate_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_button.pack(pady=10)

text_widget = tk.Text(root, height=40, width=80, fg="black", font=("Arial", 10))
text_widget.pack(padx=10, pady=10)

download_button = tk.Button(root, text="Save Report", command=save_report, state=tk.DISABLED)
download_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()



