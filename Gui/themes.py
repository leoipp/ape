# Define two themes
light_theme = """
    QPushButton#toggle_button {
        background-image: url(:/svg/Style=outline (3).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    
    QMainWindow {
        background-color: #F1F2F6;
    }
    QFrame#Header,
    QFrame#Footer {
        background-color: #FFFFFF;
    }
    QPushButton#menu {
        background-image: url(:/svg/Style=outline.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QFrame#frame_10,
    QFrame#frame_12,
    QFrame#frame_7,
    QFrame#frame_13,
    QFrame#frame_51,
    QFrame#frame_9,
    QFrame#frame_54,
    QFrame#frame_60,
    QFrame#frame_73,
    QFrame#frame_75,
    QFrame#frame_43,
    QFrame#frame_42,
    QFrame#frame_52 {
        background-color: #FFFFFF;
        border-radius:10px;
    }
    QPushButton#button_consistencia {
        background-image: url(:/svg/Style=linear (1).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    
    QPushButton#button_consistencia:hover {
        background-color: #D0D4D2; /* Change background color on hover */
    }
    QPushButton#button_inicio:hover,
    QPushButton#button_dados:hover,
    QPushButton#button_resultados:hover {
        background-color: rgba(22, 39, 28, 0.2);
    }
    QPushButton#salvar_1,
    QPushButton#salvar_2 {
        background-image: url(:/svg/Style=bold (7).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#salvar_1:hover,
    QPushButton#salvar_2:hover {
        background-image: url(:/svg/Style=bold (4).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#r_1 {
        background-image: url(:/svg/Style=bold (10).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#r_1:hover {
        background-image: url(:/svg/Style=bold (11).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#b1:hover,
    QPushButton#b2:hover,
    QPushButton#b3:hover,
    QPushButton#b4:hover,
    QPushButton#b5:hover,
    QPushButton#b6:hover,
    QPushButton#b7:hover,
    QPushButton#b8:hover,
    QPushButton#b9:hover,
    QPushButton#b10:hover,
    QPushButton#b11:hover {
        color: #16271C;
        border-top: none;       
        border-left: none;         
        border-right: none;         
        border-bottom: 3px solid #16271C;
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
    QLineEdit#cr,
    QLineEdit#pe,
    QLineEdit#sa,
    QLineEdit#ca,
    QLineEdit#ce,
    QLineEdit#al,
    QLineEdit#it,
    QLineEdit#pc,
    QLineEdit#sb,
    QLineEdit#pd,
    QLineEdit#po,
    QLineEdit#ma,
    QLineEdit#ba,
    QLineEdit#vi,
    QLineEdit#lineEdit_5{
        background-color: rgba(22, 39, 28, 0.2);
        border-radius: 10px;
    }
    QLineEdit#cr:focus,
    QLineEdit#pe:focus,
    QLineEdit#sa:focus,
    QLineEdit#ca:focus,
    QLineEdit#ce:focus,
    QLineEdit#al:focus,
    QLineEdit#it:focus,
    QLineEdit#pc:focus,
    QLineEdit#sb:focus,
    QLineEdit#pd:focus,
    QLineEdit#po:focus,
    QLineEdit#ma:focus,
    QLineEdit#ba:focus,
    QLineEdit#vi:focus,
    QLineEdit#lineEdit_5:focus {
        background-color: rgb(22, 39, 28, .5);
        border-radius: 10px;
    }
    
    QLineEdit#search_1,
    QLineEdit#search_2,
    QLineEdit#search_3,
    QLineEdit#search_4,
    QLineEdit#search_5,
    QLineEdit#search_6,
    QLineEdit#search_7,
    QLineEdit#search_8,
    QLineEdit#search_9,
    QLineEdit#search_10 {
        background-image: url(:/svg/Style=outline (1).svg);
        background-position: right; /* Attempt to position image with padding */
        background-repeat: no-repeat;
        background-color: rgba(22, 39, 28, 0.2);
        border-radius: 10px;
    }
    QLineEdit#search_1:focus,
    QLineEdit#search_2:focus,
    QLineEdit#search_3:focus,
    QLineEdit#search_4:focus,
    QLineEdit#search_5:focus,
    QLineEdit#search_6:focus,
    QLineEdit#search_7:focus,
    QLineEdit#search_8:focus,
    QLineEdit#search_9:focus,
    QLineEdit#search_10:focus {
        background-image: url(:/svg/Style=outline (1).svg);
        background-color: rgb(22, 39, 28, .5); /* Keep the background color the same */
        border-radius: 10px;
        padding-right: 5px;
    }
    
    QFrame#side_bar {
        background-color: #16271C;
    }
    QTableWidget {
        border: 2px solid #FFFFFF;
        border-radius: 10px;
        background-clip: border;
        background-color: #FFFFFF; 
    }
    QTableWidget QTableCornerButton::section {
        border-radius: 10px;
        background-color: transparent;
        border: none;
    }
    QTableWidget::item {
        border-bottom: 1px solid #d3d3d3;
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
        background: #16271C;
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
    QPushButton#toggle_button {
            background-image: url(:/svg/Style=outline (2).svg);
            background-repeat: no-repeat;
            background-position: center;
            border: none;
        }
    QPushButton {
        background-color: #5e5e5e;
        padding: 5px;
        font: 'Corbel', 12px;
        color: white;
    }
    QWidget#Main_Background {
        background-color: #131313;
    }
    QFrame#frame_10,
    QFrame#frame_12,
    QFrame#frame_7,
    QFrame#frame_13,
    QFrame#frame_51,
    QFrame#frame_9,
    QFrame#frame_54,
    QFrame#frame_60,
    QFrame#frame_73,
    QFrame#frame_75,
    QFrame#frame_43,
    QFrame#frame_42,
    QFrame#frame_52 {
        background-color: #000000;
        border-radius:10px;
    }
    
    QFrame#side_bar {
        background-color: #DDDED7;
    }
"""