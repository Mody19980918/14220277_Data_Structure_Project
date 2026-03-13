APP_STYLE = """
QWidget {
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 14px;
}

QMainWindow, QWidget#appRoot {
    background: #f6f8fb;
}

QFrame#card {
    background: white;
    border: 1px solid #dfe3eb;
    border-radius: 10px;
}

QLabel#title {
    font-size: 22px;
    font-weight: 600;
    color: #1f2937;
}

QLabel#dashboardTitle {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
    qproperty-alignment: AlignCenter;
}

QLabel#greeting {
    font-family: "Segoe UI Semibold", "Microsoft JhengHei UI", Arial, sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    qproperty-alignment: AlignCenter;
}

QLabel#dashboardSummary {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    qproperty-alignment: AlignCenter;
}

QLineEdit, QComboBox {
    border: 1px solid #cfd6e4;
    border-radius: 6px;
    padding: 6px 10px;
    background: #ffffff;
    color: #111827;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    placeholder-text-color: #6b7280;
}

QComboBox QAbstractItemView {
    background: #ffffff;
    color: #111827;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QPushButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 600;
}

/* nav buttons (admin/user panels) spacing */
QPushButton[nav="true"] {
    margin: 6px 0;
}

QPushButton:hover {
    background: #1d4ed8;
}

QPushButton[variant="ghost"] {
    background: transparent;
    color: #2563eb;
    border: 1px solid #2563eb;
}

QPushButton[size="small"] {
    padding: 2px 8px;
    min-height: 24px;
    border-radius: 4px;
    font-size: 12px;
}

QTableWidget {
    border: 1px solid #dfe3eb;
    border-radius: 8px;
    background: white;
    color: #111827;
    gridline-color: #e5e7eb;
}
"""
