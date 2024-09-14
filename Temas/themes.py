# Define two themes
light_theme = """
    QProgressBar {
        background-color: #F1F2F6;
        color: #808080;
        border-style: none;
        border-radius: 10px;
        }
    QLabel {
        font-family: 'Poppins';
    }
    QTabBar::tab:!first:!last {
        border: none;  /* Remove borders for the middle tabs */
        min-width: 80px;
        padding: 2 5px;
    }
    QTabBar::tab {
        min-width: 80px;
        bor
    }
    QTabBar::tab:hover {
        background: #878672; /* Hover background color */
    }
    QTabBar::tab:first {
        border-top-left-radius: 10px;  /* Round border for the first tab */
        border-bottom-left-radius: 10px;
    }
    QTabBar::tab:last {
        border-top-right-radius: 10px;  /* Round border for the last tab */
        border-bottom-right-radius: 10px;
    }
    QTabBar::tab:selected {
        background: #16271C; /* Selected tab background color */
        color: white; /* Selected tab text color */
    }
    QTabBar::tab:selected:hover {
        background: #16271C; /* Keep the selected tab color when hovered */
    }
    QProgressBar::chunk {
        border-radius: 10px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(253, 251, 212, 255), stop:1 rgba(22, 39, 28, 255));
    }
    QPushButton#toggle_button {
        background-image: url(:/svg/Style=outline (3).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QCheckBox {
                spacing: 0px;
            }
    QCheckBox::indicator {
                width: 26px;
                height: 24px;
            }
    QCheckBox::indicator:unchecked {
                background-image: url(:/svg/Style=bold (18).svg);
            }
    QCheckBox::indicator:hover {
                background-image: url(:/svg/Style=bold (28).svg);
            }
    QCheckBox::indicator:checked {
        background-image: url(:/svg/Style=bold (17).svg);
    }
    QMainWindow {
        background-color: #F1F2F6;
    }
    QTabWidget#tabWidget {  
        background-color: #FFFFFF;
    }    
    
    QComboBox {
        background-color: rgba(22, 39, 28, 0.2);
        border-radius: 10px;
        padding: 5px;
        font-family: 'Poppins';
        font-size: 10pt;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px; /* Adjust width of arrow button */
        border-left-width: 1px;
        border-left-color: rgba(22, 39, 28, 0.4); /* Match border color */
        border-left-style: solid; /* Solid border */
        border-top-right-radius: 10px; /* Match the corner radius */
        border-bottom-right-radius: 10px; /* Match the corner radius */
    }
    QComboBox::down-arrow {
        image: url(:/svg/Style=bold (12).svg); /* Customize the arrow icon if needed */
        width: 12px; /* Adjust the arrow size */
        height: 12px;
    }
    QFrame#Header,
    QFrame#frame_2,
    QFrame#Footer {
        background-color: #FFFFFF;
    }
    QTextEdit#query_text_edit {
        background-color: #FFFFFF;
    }
    QPushButton#menu {
        background-image: url(:/svg/firstline1.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#menu:hover {
        background-image: url(:/svg/firstline.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#menu_2:checked {
        background-image: url(:/svg/Style=linear (3).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#menu_2:checked:hover {
        background-image: url(:/svg/Style=linear (6).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#menu_2 {
        background-image: url(:/svg/Style=linear (4).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#menu_2:hover {
        background-image: url(:/svg/Style=linear (5).svg);
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
    QFrame#frame_52,
    QFrame#frame_44,
    QFrame#frame_27,
    QFrame#frame_61,
    QFrame#frame_3,
    QFrame#frame_6,
    QFrame#frame_76,
    QFrame#frame_16,
    QFrame#frame_11,
    QFrame#frame_18, 
    QFrame#frame_17,
    QFrame#frame_15,
    QFrame#frame_20 {
        background-color: #FFFFFF;
        border-radius:10px;
    }
    QPushButton#bt_close {
        background-image: url(:/svg/Style=outline (10).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#bt_close:hover {
        background-image: url(:/svg/Style=outline (10).svg);
        background-repeat: no-repeat;
        background-position: center;
        background-color: red;
    }
    QPushButton#bt_minimize {
        background-image: url(:/svg/Style=outline (9).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#bt_minimize:hover {
        background-image: url(:/svg/Style=outline (9).svg);
        background-repeat: no-repeat;
        background-position: center;
        background-color: #F1F2F6;
    }
    QPushButton#bt_maximize {
        background-image: url(:/svg/Style=outline (8).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#bt_maximize:hover {
        background-image: url(:/svg/Style=outline (8).svg);
        background-repeat: no-repeat;
        background-position: center;
        background-color: #F1F2F6;
    }
    QPushButton#button_manejo {
        background-image: url(:/svg/Style=bold (19).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px;
    }
    QPushButton#button_manejo:hover {
        background-image: url(:/svg/Style=bold (20).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px;
    }
    QPushButton#button_resultados {
        background-image: url(:/svg/Style=bold (21).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#button_resultados:hover {
        background-image: url(:/svg/Style=bold (22).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }    
    QPushButton#button_consistir {
        background-image: url(:/svg/Style=bold (13).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_consistir:hover {
        background-image: url(:/svg/Style=bold (14).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_consistencia {
        background-image: url(:/svg/Style=bold (23).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#button_consistencia:hover {
        background-image: url(:/svg/Style=bold (24).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }
    QPushButton#button_dados {
        background-image: url(:/svg/Style=bold (26).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#button_dados:hover {
        background-image: url(:/svg/Style=bold (27).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }
    QPushButton#button_inicio {
        background-image: url(:/svg/Style=bold (30).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#button_inicio:hover {
        background-image: url(:/svg/Style=bold (29).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }
    QPushButton#pushButton_12 {
        background-image: url(:/svg/Style=outline (5).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#pushButton_12:hover {
        background-image: url(:/svg/Style=outline (4).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }
    QPushButton#pushButton_10 {
        background-image: url(:/svg/Style=outline (6).svg);
        background-repeat: no-repeat;
        background-position: left;
        border: none;
        color: white;
        padding: 6px 5px; /* Apply padding consistently */
    }
    QPushButton#pushButton_10:hover {
        background-image: url(:/svg/Style=outline (7).svg);
        background-repeat: no-repeat;
        background-position: left;
        background-color: #F1F2F6;
        color: #16271C;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        padding: 5px;
    }
    QPushButton#button_reprocessar {
        background-image: url(:/svg/save-2.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_reprocessar:hover {
        background-image: url(:/svg/save-22.svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_limpar {
        background-image: url(:/svg/Style=outline (11).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_limpar:hover {
        background-image: url(:/svg/Style=outline (12).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_executar {
        background-image: url(:/svg/Style=outline (16).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_executar:hover {
        background-image: url(:/svg/Style=outline (15).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_exportar {
        background-image: url(:/svg/Style=bold (31).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#qry_exportar:hover {
        background-image: url(:/svg/Style=bold (32).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_exportar {
        background-image: url(:/svg/Style=bold (15).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#button_exportar:hover {
        background-image: url(:/svg/Style=bold (16).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#salvar_1,
    QPushButton#salvar_2,
    QPushButton#salvar_3,
    QPushButton#salvar_4,
    QPushButton#salvar_5,
    QPushButton#salvar_6,
    QPushButton#salvar_7{
        background-image: url(:/svg/Style=bold (7).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#salvar_1:hover,
    QPushButton#salvar_2:hover,
    QPushButton#salvar_3:hover,
    QPushButton#salvar_4:hover,
    QPushButton#salvar_5:hover,
    QPushButton#salvar_6:hover,
    QPushButton#salvar_7:hover{
        background-image: url(:/svg/Style=bold (4).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#r_1,
    QPushButton#r_2,
    QPushButton#r_3,
    QPushButton#r_4,
    QPushButton#r_5,
    QPushButton#r_6,
    QPushButton#r_7,
    QPushButton#r_8,
    QPushButton#r_9,
    QPushButton#r_10,
    QPushButton#button_deletar {
        background-image: url(:/svg/Style=bold (10).svg);
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    }
    QPushButton#r_1:hover,
    QPushButton#r_2:hover,
    QPushButton#r_3:hover,
    QPushButton#r_4:hover,
    QPushButton#r_5:hover,
    QPushButton#r_6:hover,
    QPushButton#r_7:hover,
    QPushButton#r_8:hover,
    QPushButton#r_9:hover,
    QPushButton#r_10:hover,
    QPushButton#button_deletar:hover {
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
    QPushButton#button_open_16,
    QPushButton#button_open_23 {
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
    QPushButton#button_open_16:hover,
    QPushButton#button_open_23:hover {
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
    QLineEdit#lineEdit_5,
    QLineEdit#lineEdit_7,
    QLineEdit#lineEdit_8,
    QLineEdit#lineEdit_9,
    QLineEdit#lineEdit_10,
    QLineEdit#est_bo_2,
    QLineEdit#est_ip_2,
    QLineEdit#est_co_2,
    QLineEdit#est_pi_2,
    QLineEdit#est_po_2,
    QLineEdit#est_sa_2,
    QLineEdit#est_sb_2,
    QLineEdit#est_vi_2,
    QLineEdit#e_bo,
    QLineEdit#e_ip,
    QLineEdit#e_po,
    QLineEdit#e_co,
    QLineEdit#e_pi,
    QLineEdit#e_sb,
    QLineEdit#e_sa,
    QLineEdit#e_vi,
    QLineEdit#gg,
    QLineEdit#mec_col,
    QLineEdit#pg,
    QLineEdit#r2,
    QLineEdit#rat,
    QLineEdit#rbt,
    QLineEdit#ra3,
    QLineEdit#ra2,
    QLineEdit#rb3,
    QLineEdit#rb2,
    QLineEdit#act,
    QLineEdit#jt,
    QLineEdit#fae,
    QLineEdit#i7_2,
    QLineEdit#i8_2,
    QLineEdit#i9_2,
    QLineEdit#i10_2,
    QLineEdit#i11_2,
    QLineEdit#i12_2,
    QLineEdit#i13_2,
    QLineEdit#i14_2,
    QLineEdit#ct_bo,
    QLineEdit#ct_ip,
    QLineEdit#ct_po,
    QLineEdit#ct_co,
    QLineEdit#ct_pi,
    QLineEdit#ct_sb,
    QLineEdit#ct_sa,
    QLineEdit#ct_vi{
        background-color: rgba(22, 39, 28, 0.2);
        border-radius: 10px;
    }
    QLineEdit#est_bo_2:focus,
    QLineEdit#est_ip_2:focus,
    QLineEdit#est_co_2:focus,
    QLineEdit#est_pi_2:focus,
    QLineEdit#est_po_2:focus,
    QLineEdit#est_sa_2:focus,
    QLineEdit#est_sb_2:focus,
    QLineEdit#est_vi_2:focus,
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
    QLineEdit#lineEdit_5:focus,
    QLineEdit#lineEdit_7:focus,
    QLineEdit#lineEdit_8:focus,
    QLineEdit#lineEdit_9:focus,
    QLineEdit#lineEdit_10:focus,
    QLineEdit#e_bo:focus,
    QLineEdit#e_ip:focus,
    QLineEdit#e_po:focus,
    QLineEdit#e_co:focus,
    QLineEdit#e_pi:focus,
    QLineEdit#e_sb:focus,
    QLineEdit#e_sa:focus,
    QLineEdit#e_vi:focus,
    QLineEdit#gg:focus,
    QLineEdit#mec_col:focus,
    QLineEdit#pg:focus,
    QLineEdit#r2:focus,
    QLineEdit#rat:focus,
    QLineEdit#rbt:focus,
    QLineEdit#ra3:focus,
    QLineEdit#ra2:focus,
    QLineEdit#rb3:focus,
    QLineEdit#rb2:focus,
    QLineEdit#act:focus,
    QLineEdit#jt:focus,
    QLineEdit#fae:focus,
    QLineEdit#i7_2:focus,
    QLineEdit#i8_2:focus,
    QLineEdit#i9_2:focus,
    QLineEdit#i10_2:focus,
    QLineEdit#i11_2:focus,
    QLineEdit#i12_2:focus,
    QLineEdit#i13_2:focus,
    QLineEdit#i14_2:focus,
    QLineEdit#ct_bo:focus,
    QLineEdit#ct_ip:focus,
    QLineEdit#ct_po:focus,
    QLineEdit#ct_co:focus,
    QLineEdit#ct_pi:focus,
    QLineEdit#ct_sb:focus,
    QLineEdit#ct_sa:focus,
    QLineEdit#ct_vi:focus {
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
    QLineEdit#search_10,
    QLineEdit#search_11{
        background-image: url(:/svg/Style=outline (1).svg);
        background-position: right center; /* Attempt to position image with padding */
        background-repeat: no-repeat;
        background-color: rgba(22, 39, 28, 0.2);
        border-radius: 10px;
        padding-right: 3px;
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
    QLineEdit#search_10:focus,
    QLineEdit#search_11:focus {
        background-image: url(:/svg/Style=outline (1).svg);
        background-color: rgb(22, 39, 28, .5); /* Keep the background color the same */
        border-radius: 10px;
        padding-right: 5px;
    }
    
    QFrame#side_bar {
        background-color: #16271C;
        border:none;
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
    QTableWidget::item:selected {
        background-color: rgba(22, 39, 28, 0.2); 
    }
    QHeaderView::section {
                border-bottom: 2px solid #16271C;
                border-left: none;       
                border-right: none;           
                border-top: none;    
                font-family: 'Poppins SemiBold';
                font-size: 8pt;  
                font-weight: bold;
                background: rgba(22, 39, 28, 0.2);  
                border-radius: 0px;
                margin: 0px;
                padding: 2px;
            }
    QHeaderView::section:first {
        border-top-left-radius: 10px;  /* Round the top-left corner */
    }
    
    QHeaderView::section:last {
        border-top-right-radius: 10px;  /* Round the top-right corner */
    }

    QScrollBar:vertical {
        border: none;
        background: #f3f3f3;
        width: 12px;  /* Define a largura da barra de rolagem vertical */
        margin: 5px 0 5px 0;
    }
    QScrollBar::handle:vertical {
        background: #16271C;
        min-height: 100px;
        border-radius: 3px;
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
    QScrollBar:horizontal {
    border: none;
    background: #f3f3f3;
    height: 12px;  /* Define the height of the horizontal scrollbar */
    margin: 0 5px 0 5px;
    }
    
    QScrollBar::handle:horizontal {
        background: #16271C;
        min-width: 100px;
        border-radius: 3px;
        margin: 2px;
    }
    
    QScrollBar::add-line:horizontal {
        border: none;
        background: #f3f3f3;
        width: 10px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    
    QScrollBar::sub-line:horizontal {
        border: none;
        background: #f3f3f3;
        width: 22px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
        border: none;
        width: 0;
        height: 0;
        background: none;
    }
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
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