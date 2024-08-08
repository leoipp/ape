# Define two themes
light_theme = """
    QMainWindow {
        background-color: #FFFFFF;
    }
    QPushButton#main_button_home {
        background-image: url(:/svg/Style=bold (2).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#main_button_home:hover {
        background-image: url(:/svg/Style=bold (3).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_open_1,
    QPushButton#button_open_2,
    QPushButton#button_open_3,
    QPushButton#button_open_4,
    QPushButton#button_open_5,
    QPushButton#button_open_6,
    QPushButton#button_open_7,
    QPushButton#button_open_8,
    QPushButton#button_open_9,
    QPushButton#button_open_10,
    QPushButton#button_open_11,
    QPushButton#button_open_12,
    QPushButton#button_open_13,
    QPushButton#button_open_14,
    QPushButton#button_open_15,
    QPushButton#button_open_16 {
        background-image: url(:/svg/Style=bold.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_open_1:hover,
    QPushButton#button_open_2:hover,
    QPushButton#button_open_3:hover,
    QPushButton#button_open_4:hover,
    QPushButton#button_open_5:hover,
    QPushButton#button_open_6:hover,
    QPushButton#button_open_7:hover,
    QPushButton#button_open_8:hover,
    QPushButton#button_open_9:hover,
    QPushButton#button_open_10:hover,
    QPushButton#button_open_11:hover,
    QPushButton#button_open_12:hover,
    QPushButton#button_open_13:hover,
    QPushButton#button_open_14:hover,
    QPushButton#button_open_15:hover,
    QPushButton#button_open_16:hover {
        background-image: url(:/svg/Style=bold (1).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QFrame {
        background-color: #FFFFFF;
    }
    QFrame#frame_50,
    QFrame#frame_49,
    QFrame#frame_53,
    QFrame#frame_55,
    QFrame#frame_56{
        border-radius:10px;
    }
    QTableWidget::item {
        border-bottom: 1px solid #d3d3d3;
        border-top: 1px solid #d3d3d3;/* Show only bottom border for horizontal lines */
    }
    QTableWidget QHeaderView::section {
        border-bottom: 2px solid red;
    }
    QScrollBar:vertical {
        border: none;
        background: #f3f3f3;
        width: 8px;  /* Define a largura da barra de rolagem vertical */
        margin: 5px 0 5px 0;
    }
    QScrollBar::handle:vertical {
        background: #253d2c;
        min-height: 100px;
        border-radius: 7px;
        margin: 2px;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: #f3f3f3;
        height: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: #f3f3f3;
        height: 22px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        border: none;
        width: 0;
        height: 0;
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
"""

dark_theme = """
    QMainWindow {
        background-color: #121212
    }
    QPushButton {
        background-color: #5e5e5e;
        padding: 5px;
        font: 'Corbel', 12px;
        color: white;
    }
    QFrame {
        background-color: #5e5e5e;
    }
"""