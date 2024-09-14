import os
from functools import partial
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidgetAction, QPushButton
from PyQt5 import QtCore

from Database.Consistencia import Consist
from Database.Database import Database
from Recursos.custom_widget import CustomMenu, CustomMenuItem
from Threads.Worker import APEX


class UiSetup:
    __version__ = "Versão: 1.0.1"

    def __init__(self, main_window):
        """
        Initialize UI elements and connect signals.
        """
        self.main_window = main_window
        uic.loadUi('Gui/MainUI.ui', main_window)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up UI elements and connect signals.
        """
        self.main_window.main_button_projeto.setText(os.getlogin())
        self.main_window.label_2.setText(UiSetup.__version__)
        self.main_window.side_bar.hide()
        self.main_window.utility_functions.set_theme('light')  # Correctly call set_theme through utility_functions
        self.main_window.utility_functions.apply_drop_shadow(self.main_window.side_bar)
        self.setup_comboboxes()
        self.setup_tabs()
        self.setup_buttons()
        self.setup_menu()
        self.setup_signals()
        self.setup_db_buttons()
        self.setup_drop_buttons()
        self.main_window.worker = None  # Thread setup
        self.main_window.thread = None
        self.main_window.bt_close.clicked.connect(self.main_window.close)
        self.main_window.bt_minimize.clicked.connect(self.minimize_window)
        self.main_window.bt_maximize.clicked.connect(self.maximize_window)

    def setup_comboboxes(self):
        """
        Initialize combo boxes with predefined items.
        """
        combo_boxes = [self.main_window.bo, self.main_window.ip, self.main_window.vi_2, self.main_window.sa_2,
                       self.main_window.sb_2, self.main_window.pi, self.main_window.co, self.main_window.po_2]
        for combo in combo_boxes:
            combo.addItems(['Região Alta', 'Região Baixa'])

        self.main_window.comb1.addItems(['Custo Posto-Fábrica', 'Custo de Colheita', 'Custo de Silvicultura', 'Custos Taxas ADM'])

    def setup_tabs(self):
        """
        Disable grid lines for specific tabs.
        """
        tabs = [self.main_window.tab_1, self.main_window.tab_2, self.main_window.tab_3, self.main_window.tab_4,
                self.main_window.tab_5, self.main_window.tab_6, self.main_window.tab_7, self.main_window.tab_8,
                self.main_window.tab_9, self.main_window.tab_10, self.main_window.tab_11, self.main_window.tab_12,
                self.main_window.tab_13, self.main_window.tab_14, self.main_window.tab_15, self.main_window.tab_22,
                self.main_window.tab_consist]
        for tab in tabs:
            tab.setShowGrid(False)

    def setup_buttons(self):
        """
        Connect buttons to their corresponding actions.
        """
        buttons = [
            (self.main_window.b1, 0), (self.main_window.b2, 1), (self.main_window.b3, 2), (self.main_window.b4, 3),
            (self.main_window.b5, 4), (self.main_window.b6, 5), (self.main_window.b7, 6), (self.main_window.b8, 7),
            (self.main_window.b9, 8), (self.main_window.b10, 10), (self.main_window.b11, 9)
        ]
        for button, index in buttons:
            button.clicked.connect(lambda _, index=index: self.main_window.stackedWidget.setCurrentIndex(index))

        self.main_window.button_dados.clicked.connect(lambda: self.main_window.stackedWidget_2.setCurrentIndex(0))
        self.main_window.button_consistencia.clicked.connect(lambda: self.main_window.stackedWidget_2.setCurrentIndex(1))
        self.main_window.button_resultados.clicked.connect(lambda: self.main_window.stackedWidget_2.setCurrentIndex(2))
        self.main_window.button_inicio.clicked.connect(lambda: self.main_window.stackedWidget_2.setCurrentIndex(3))

    def setup_drop_buttons(self):
        _ = {
            self.main_window.r_1: 'CurvaProdutividade',
            self.main_window.r_2: 'ClassesInclinacao',
            self.main_window.r_3: 'IFC',
            self.main_window.r_4: 'IFPC',
            self.main_window.r_5: 'OutrosCustos',
            self.main_window.r_6: 'CustosSilvicultura_REF_REG',
            self.main_window.r_7: 'CustosTransRod',
            self.main_window.r_8: 'CadastroFlorestal',
            self.main_window.r_9: 'RTMaterialGenetico',
            self.main_window.r_10: 'Orcamento',
        }
        for button, table_name in _.items():
            button.clicked.connect(lambda _, table=table_name: self.main_window.utility_functions.drop_table_and_clear_widget(table))

    def setup_db_buttons(self):
        # Define the button mappings
        button_names = {
            'button_open_1': ('IFC', self.main_window.tab_1, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area'],
                              self.main_window.label_4),
            'button_open_2': ('CurvaProdutividade', self.main_window.tab_3,
                              ['Idade', 'Sabinopolis', 'Cocais', 'Piracicaba', 'SantaBarbara', 'BeloOriente', 'Ipaba',
                               'Pompeu', 'Virginopolis'], self.main_window.label_5),
            'button_open_3': ('RTMaterialGenetico', self.main_window.tab_4,
                              ['DCR_MatGen', 'RegAlta', 'RegBaixaEncosta', 'RegBaixaBaixada'],
                              self.main_window.label_10),
            'button_open_4': ('Orcamento', self.main_window.tab_5, ['TalhaoAtual', 'TalhaoReferencia'], self.main_window.label_9),
            'button_open_5': ('ClassesInclinacao', self.main_window.tab_6,
                              ['Regiao', 'Area', 'HA0_28', 'HA29_38', 'HA38_MAIS', 'PCT0_28', 'PCT29_38', 'PCT38_MAIS'],
                              self.main_window.label_8),
            'button_open_6': ('CadastroFlorestal', self.main_window.tab_7,
                              ['Talhao', 'DCR_Projeto', 'DT_Plantio', 'ESP', 'DCR_MatGen', 'Area', 'DIST_LP',
                               'DIST_PFRod', 'DIST_PFFer', 'DIST_LFRod', 'DIST_Total'], self.main_window.label_11),
            'button_open_23': ('CustosSilvicultura_REF_REG', self.main_window.tab_22,
                               ['Fase', 'ANO', 'BO', 'IP', 'PO', 'CO', 'PI', 'SB', 'SA', 'VI'],
                               self.main_window.label_13),
            'button_open_8': ('CustosColheitaPI', self.main_window.tab_8, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_19),
            'button_open_9': ('CustosColheitaPO', self.main_window.tab_9, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_20),
            'button_open_10': ('CustosColheitaCO', self.main_window.tab_10, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_21),
            'button_open_11': ('CustosColheitaGN', self.main_window.tab_11, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_22),
            'button_open_12': ('CustosColheitaBO', self.main_window.tab_12, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_18),
            'button_open_13': ('CustosColheitaSB', self.main_window.tab_13, ['PROD', 'VMI', 'PD', 'GW'], self.main_window.label_23),
            'button_open_14': ('CustosTransRod', self.main_window.tab_14,
                               ['Distancia', 'Sabinopolis', 'Cocais', 'Piracicaba', 'SantaBarbara', 'BeloOriente',
                                'Ipaba', 'Pompeu', 'Virginopolis'], self.main_window.label_12),
            'button_open_15': ('OutrosCustos', self.main_window.tab_15,
                               ['Regiao', 'ApoioColheita', 'EstInterna', 'EstExterna', 'MovPatio', 'ADM', 'Taxas'],
                               self.main_window.label_15),
            'button_open_16': ('IFPC', self.main_window.tab_2, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area'],
                               self.main_window.label_3)
        }

        # Connect each button's clicked signal to the openFileDialog method
        for button_name, v in button_names.items():
            button = self.main_window.findChild(QPushButton, button_name)
            if button:
                button.clicked.connect(lambda _, v=v: self.main_window.utility_functions.openFileDialog(v[0], v[1], v[2], v[3]))

    def setup_menu(self):
        """
        Initialize the custom menu.
        """
        self.main_window.menu_projeto = CustomMenu(self.main_window)
        # Menu initialization logic
        self.add_custom_menu_item('Novo', self.main_window.create_db.criar_base, self.main_window.menu_projeto)
        self.add_custom_menu_item('Abrir', self.main_window.open_db.open_base, self.main_window.menu_projeto)
        self.add_custom_menu_item('Compactar', lambda: self.main_window.utility_functions.database_vacumm(), self.main_window.menu_projeto)
        self.main_window.main_button_projeto.clicked.connect(
            lambda: self.main_window.utility_functions.show_menu(self.main_window.main_button_projeto, self.main_window.menu_projeto)
        )

    def add_custom_menu_item(self, text, callback, menu):
        action = QWidgetAction(menu)
        custom_widget = CustomMenuItem(text, self.main_window)
        action.setDefaultWidget(custom_widget)
        menu.addAction(action)
        custom_widget.mousePressEvent = lambda _: callback()

    def setup_signals(self):
        """
        Connect signals for various widgets.
        """
        # Call switch_theme via utility_functions instance
        self.main_window.toggle_button.clicked.connect(self.main_window.utility_functions.switch_theme)
        self.main_window.button_reprocessar.clicked.connect(lambda: self.main_window.utility_functions.consist_bt(1))
        self.main_window.button_consistir.clicked.connect(lambda: self.main_window.utility_functions.consist_bt(2))
        self.main_window.button_deletar.clicked.connect(lambda: self.main_window.utility_functions.consist_bt(3))
        self.main_window.label_base.textChanged.connect(self.main_window.data_processing.atualizar_modelos)
        self.main_window.lineEdit_5.textChanged.connect(self.main_window.utility_functions.update_all_labels)
        self.main_window.qry_executar.clicked.connect(self.main_window.utility_functions.execute_query)
        self.main_window.qry_limpar.clicked.connect(lambda: self.main_window.query_text_edit.clear())
        self.main_window.qry_exportar.clicked.connect(self.main_window.utility_functions.export_result_table_to_file)
        self.setup_search_signals()
        self.setup_text_signals()
        self.setup_save_buttons()
        self.main_window.apex_comp_1.currentIndexChanged.connect(self.main_window.utility_functions.on_sel_apex_1)
        self.main_window.apex_comp_1.currentIndexChanged.connect(self.main_window.utility_functions.checkboxes_av_eco)
        self.main_window.apex_comp_2.currentIndexChanged.connect(self.main_window.utility_functions.on_sel_apex_2)
        self.main_window.apex_comp_1.currentIndexChanged.connect(lambda: self.main_window.utility_functions.combox_changes())
        self.main_window.apex_comp_2.currentIndexChanged.connect(lambda: self.main_window.utility_functions.combox_changes())
        self.main_window.checkBox.stateChanged.connect(lambda: self.on_checkbox_state_changed(0))
        self.main_window.checkBox_2.stateChanged.connect(lambda: self.on_checkbox_state_changed(1))
        self.main_window.checkBox_7.clicked.connect(lambda: self.change_checkbox([self.main_window.checkBox_7, self.main_window.checkBox_6]))
        self.main_window.checkBox_6.clicked.connect(lambda: self.change_checkbox([self.main_window.checkBox_7, self.main_window.checkBox_6]))
        self.main_window.checkBox_9.clicked.connect(lambda: self.change_checkbox([self.main_window.checkBox_9, self.main_window.checkBox_10]))
        self.main_window.checkBox_10.clicked.connect(lambda: self.change_checkbox([self.main_window.checkBox_9, self.main_window.checkBox_10]))
        self.main_window.checkBox_7.clicked.connect(lambda: self.main_window.utility_functions.checkboxes_av_eco())
        self.main_window.checkBox_6.clicked.connect(lambda: self.main_window.utility_functions.checkboxes_av_eco())
        self.main_window.checkBox_9.clicked.connect(lambda: self.main_window.utility_functions.checkboxes_av_eco())
        self.main_window.checkBox_10.clicked.connect(lambda: self.main_window.utility_functions.checkboxes_av_eco())
        self.main_window.comb1.currentIndexChanged.connect(lambda: self.main_window.utility_functions.checkboxes_av_eco())

    def setup_search_signals(self):
        """
        Connect search fields to their respective tables.
        """
        search_fields = [
            (self.main_window.search_1, self.main_window.tab_2), (self.main_window.search_2, self.main_window.tab_1),
            (self.main_window.search_3, self.main_window.tab_3), (self.main_window.search_4, self.main_window.tab_6),
            (self.main_window.search_5, self.main_window.tab_5), (self.main_window.search_6, self.main_window.tab_4),
            (self.main_window.search_7, self.main_window.tab_7), (self.main_window.search_8, self.main_window.tab_14),
            (self.main_window.search_9, self.main_window.tab_22), (self.main_window.search_10, self.main_window.tab_15),
            (self.main_window.search_11, self.main_window.tab_consist)
        ]
        for search_field, tab in search_fields:
            search_field.textChanged.connect(lambda text, tab=tab: self.main_window.utility_functions.search_in_table(text, tab))

    def setup_text_signals(self):
        """
        Connect text fields to their respective labels for real-time updates.
        """
        label_pairs = [
            (self.main_window.cr, self.main_window.label_38), (self.main_window.pe, self.main_window.label_39),
            (self.main_window.sa, self.main_window.label_40), (self.main_window.ca, self.main_window.label_41),
            (self.main_window.ce, self.main_window.label_42), (self.main_window.al, self.main_window.label_43),
            (self.main_window.it, self.main_window.label_44), (self.main_window.pc, self.main_window.label_45),
            (self.main_window.sb, self.main_window.label_46), (self.main_window.pd, self.main_window.label_47),
            (self.main_window.po, self.main_window.label_48), (self.main_window.ma, self.main_window.label_49),
            (self.main_window.ba, self.main_window.label_50), (self.main_window.vi, self.main_window.label_51)
        ]
        for edit, label in label_pairs:
            edit.textChanged.connect(lambda text, label=label: label.setText(self.main_window.utility_functions.prod_min(text, self.main_window.lineEdit_5.text())))

    def setup_save_buttons(self):
        """
        Connect save buttons to the corresponding calculations and database operations.
        """
        tabs_texto = {
            self.main_window.salvar_1: (['Regiao', 'ProdMin'],
                            [['CR', self.main_window.label_38], ['PE', self.main_window.label_39],
                             ['SA', self.main_window.label_40], ['CA', self.main_window.label_41],
                             ['CE', self.main_window.label_42], ['AL', self.main_window.label_43],
                             ['IT', self.main_window.label_44], ['PC', self.main_window.label_45],
                             ['SB', self.main_window.label_46], ['PD', self.main_window.label_47],
                             ['PO', self.main_window.label_48], ['MA', self.main_window.label_49],
                             ['BA', self.main_window.label_50], ['VI', self.main_window.label_51]],
                            'ProdMin'),
            self.main_window.salvar_2: (['Regiao', 'Elev'],
                            [
                                ['BO', self.main_window.bo],
                                ['IP', self.main_window.ip],
                                ['VI', self.main_window.vi_2],
                                ['SA', self.main_window.sa_2],
                                ['SB', self.main_window.sb_2],
                                ['PI', self.main_window.pi],
                                ['CO', self.main_window.co],
                                ['PO', self.main_window.po_2]
                            ], 'Elevacao'),
            self.main_window.salvar_3: (
                ['Regiao', 'Custo'],
                [
                    ['SB', self.main_window.lineEdit_8],
                    ['PI', self.main_window.lineEdit_7]
                ], 'CustoFerr'
            ),
            self.main_window.salvar_4: (
                ['Regiao', 'Custo'],
                [
                    ['SB', self.main_window.lineEdit_10],
                    ['PI', self.main_window.lineEdit_9]
                ], 'CustoMovPatio'
            ),
            self.main_window.salvar_5: (
                ['Regiao', 'Custo'],
                [
                    ['BO', self.main_window.est_bo_2],
                    ['IP', self.main_window.est_ip_2],
                    ['VI', self.main_window.est_vi_2],
                    ['SA', self.main_window.est_sa_2],
                    ['SB', self.main_window.est_sb_2],
                    ['PI', self.main_window.est_pi_2],
                    ['CO', self.main_window.est_co_2],
                    ['PO', self.main_window.est_po_2]
                ], 'CustoEstExterna'
            ),
            self.main_window.salvar_6: (
                ['Regiao', 'Custo'],
                [
                    ['BO', self.main_window.e_bo],
                    ['IP', self.main_window.e_ip],
                    ['PO', self.main_window.e_po],
                    ['CO', self.main_window.e_co],
                    ['PI', self.main_window.e_pi],
                    ['SB', self.main_window.e_sb],
                    ['SA', self.main_window.e_sa],
                    ['VI', self.main_window.e_vi]
                ], 'CustoTerra'
            ),
            self.main_window.salvar_7: (
                ['Idade', 'Perda'],
                [
                    ['7', self.main_window.i7_2],
                    ['8', self.main_window.i8_2],
                    ['9', self.main_window.i9_2],
                    ['10', self.main_window.i10_2],
                    ['11', self.main_window.i11_2],
                    ['12', self.main_window.i12_2],
                    ['13', self.main_window.i13_2],
                    ['14', self.main_window.i14_2]
                ], 'IndiceBrotacao'
            )

        }
        self.connect_buttons(tabs_texto, 1)
        _params = {
            self.main_window.button_manejo: (
                ['GanhoGenetico', 'PerdaGenetica', 'R2', 'TalhadiaRA', 'TalhadiaRB', 'RA3', 'RB3', 'RA2', 'RB2',
                 'AcrescimoColheitaTalhadia', 'Juros', 'AvaliacaoEco', 'MecColheita'],
                [[self.main_window.gg, self.main_window.pg, self.main_window.r2, self.main_window.rat,
                  self.main_window.rbt, self.main_window.ra3, self.main_window.rb3, self.main_window.ra2,
                  self.main_window.rb2, self.main_window.act, self.main_window.jt, self.main_window.fae, self.main_window.mec_col]],
                'Parametros'
            )
        }

        self.connect_buttons(_params, 2)

    def connect_buttons(self, config, mode):
        """
        Connect buttons to the `prod_calc_click` method with the appropriate parameters.
        """
        if mode == 1:
            for button, (headers, labels, table) in config.items():
                button.clicked.connect(partial(self.main_window.data_processing.prod_calc_click, headers, labels, table))
        if mode == 2:
            for button, (headers, labels_list, table_name) in config.items():
                button.clicked.connect(lambda _, h=headers, l=labels_list, t=table_name: self.handle_mode_2_click(h, l, t))

    def handle_mode_2_click(self, headers, labels_list, table_name):
        """
        Handle the button click in mode 2 by executing the necessary actions and starting the thread.
        """
        # Execute the handle_params_click method
        self.main_window.data_processing.handle_params_click(headers, labels_list, table_name)

        # Start the thread after handling the parameters click
        self.start_thread()

    def start_thread(self):
        if self.main_window.thread and self.main_window.thread.isRunning():
            self.main_window.thread.quit()
            self.main_window.thread.wait()
        self.main_window.progressBar.setValue(0)

        self.main_window.thread = QtCore.QThread()
        self.main_window.worker = APEX(self.main_window.progressBar, self.main_window.label_base.text(), self.main_window.t700.isChecked())
        self.main_window.worker.moveToThread(self.main_window.thread)
        self.main_window.thread.started.connect(self.main_window.worker.run)
        self.main_window.worker.barra_att.connect(self.update_progress)
        self.main_window.worker.bar_max.connect(self.set_progress_bar_max)
        self.main_window.worker.fim.connect(self.finalizado_simulacao_manejo)
        self.main_window.thread.start()

    def update_progress(self, value):
        self.main_window.progressBar.setValue(value)

    def set_progress_bar_max(self, max_value):
        self.main_window.progressBar.setMaximum(max_value)

    def finalizado_simulacao_manejo(self):
        self.main_window.progressBar.setValue(0)
        db = Database(self.main_window.label_base.text())
        n = [x for x in db.list_tables() if x.startswith('Apex_Manejo')]
        goal = n[-1]
        self.main_window.utility_functions.add_new_tab(goal)
        self.main_window.apex_comp_1.clear()
        self.main_window.apex_comp_2.clear()
        self.main_window.apex_comp_1.addItems(n)
        self.main_window.apex_comp_2.addItems(n)
        if len(n) > 0:
            db = Consist(self.main_window.label_base.text())
            values = []
            for t in n:
                values.append([
                    db.regional_resumo(t, 'Regeneração', 'SA', 3)/(db.regional_resumo(t, 'Regeneração', 'SA', 3)+db.regional_resumo(t, 'Reforma', 'SA', 3)),
                    db.regional_resumo(t, 'Regeneração', 'VI', 3)/(db.regional_resumo(t, 'Regeneração', 'VI', 3)+db.regional_resumo(t, 'Reforma', 'VI', 3)),
                    db.regional_resumo(t, 'Regeneração', 'CO', 3)/(db.regional_resumo(t, 'Regeneração', 'CO', 3)+db.regional_resumo(t, 'Reforma', 'CO', 3)),
                    db.regional_resumo(t, 'Regeneração', 'PI', 3)/(db.regional_resumo(t, 'Regeneração', 'PI', 3)+db.regional_resumo(t, 'Reforma', 'PI', 3)),
                    db.regional_resumo(t, 'Regeneração', 'SB', 3)/(db.regional_resumo(t, 'Regeneração', 'SB', 3)+db.regional_resumo(t, 'Reforma', 'SB', 3)),
                    db.regional_resumo(t, 'Regeneração', 'IP', 3)/(db.regional_resumo(t, 'Regeneração', 'IP', 3)+db.regional_resumo(t, 'Reforma', 'IP', 3)),
                    db.regional_resumo(t, 'Regeneração', 'PO', 3)/(db.regional_resumo(t, 'Regeneração', 'PO', 3)+db.regional_resumo(t, 'Reforma', 'PO', 3))])

            categories = ['Sabinópolis', 'Virginópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Ipaba', 'Pompéu']
            self.main_window.utility_functions.plot_radar_chart(self.main_window.plotRadarChart, categories, values, 'Percentual de Talhadia (%)', n)

        msg = QtWidgets.QMessageBox()
        msg.setText("Manejo avaliado com sucesso!")
        msg.setWindowTitle("APEX")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def on_checkbox_state_changed(self, page_index):
        sender = self.main_window.sender()

        # Uncheck other checkboxes if the sender is checked and change the page
        if sender.isChecked():
            self.main_window.plots_resumo.setCurrentIndex(page_index)
            for checkbox in [self.main_window.checkBox, self.main_window.checkBox_2]:
                if checkbox != sender:
                    checkbox.setChecked(False)
        else:
            any_checked = any(cb.isChecked() for cb in
                              [self.main_window.checkBox, self.main_window.checkBox_2])
            if not any_checked:
                self.main_window.plots_resumo.setCurrentIndex(2)

    def change_checkbox(self, checks):
        sender = self.main_window.sender()

        # Uncheck all other checkboxes
        for checkbox in checks:
            if checkbox != sender:
                checkbox.setChecked(False)

        # Ensure the sender remains checked
        sender.setChecked(True)

    def minimize_window(self):
        self.main_window.showMinimized()

    def maximize_window(self):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            self.main_window.showMaximized()
