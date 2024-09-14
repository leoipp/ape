from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QTableWidget, QHeaderView, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt

from Database.Database import Database
from Dialogs.Open import SheetSelectionDialog, HeaderSelectionDialog
from Temas.themes import light_theme, dark_theme
from Database.Consistencia import Consist

import sqlite3

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as mcolors
import pandas as pd


class UtilityFunctions:
    def __init__(self, main_window):
        """
        Provide utility functions for theming, image processing, and visual effects.
        """
        self.main_window = main_window
        self.tab_counter = 0

    def set_theme(self, theme_name):
        """
        Apply the selected theme to the application.
        """
        self.main_window.setStyleSheet(light_theme if theme_name == 'light' else dark_theme)

    def switch_theme(self):
        """
        Toggle between light and dark themes.
        """
        self.set_theme('dark' if self.main_window.styleSheet() == light_theme else 'light')

    def update_all_labels(self):
        """
        Update all labels based on the current text inputs.
        """
        labels = [
            self.main_window.label_38, self.main_window.label_39, self.main_window.label_40, self.main_window.label_41,
            self.main_window.label_42, self.main_window.label_43, self.main_window.label_44, self.main_window.label_45,
            self.main_window.label_46, self.main_window.label_47, self.main_window.label_48, self.main_window.label_49,
            self.main_window.label_50, self.main_window.label_51
        ]
        edits = [
            self.main_window.cr, self.main_window.pe, self.main_window.sa, self.main_window.ca, self.main_window.ce,
            self.main_window.al, self.main_window.it, self.main_window.pc, self.main_window.sb,
            self.main_window.pd, self.main_window.po, self.main_window.ma, self.main_window.ba, self.main_window.vi
        ]
        for edit, label in zip(edits, labels):
            label.setText(self.prod_min(edit.text(), self.main_window.lineEdit_5.text()))

    def openFileDialog(self, table_name, table_widget, hder, label_shape):
        filePath = SheetSelectionDialog.openFileDialog(self.main_window)
        if filePath:
            df = SheetSelectionDialog.loadExcel(filePath, self.main_window)
            if df is not None:
                headers = df.columns.tolist()
                names, selected_headers = HeaderSelectionDialog.openDialog(headers, hder, self.main_window)
                if names and selected_headers:
                    df_selected = df[selected_headers]
                    df_selected.columns = names
                    db = Database(self.main_window.label_base.text())
                    db.create_table_from_dataframe(df_selected, table_name, parent=self.main_window)
                    self.populate_table_from_db(db, table_name, table_widget, label_shape)

    def consist_bt(self, consist=2):
        try:
            db = Consist(self.main_window.label_base.text())

            if consist == 1:  # Only proceed if there are changes
                self.main_window.data_processing.salvar_ajuste()
                df = db.ajuste_base()
            elif consist == 2:
                df = db.pipeline()
            elif consist == 3:
                db.delete_selected_rows('apex_base_1', self.main_window.tab_consist, 'id')
                df = db.ajuste_base()
            else:
                pass
            self.populateTableWidget(df, self.main_window.tab_consist)
            self.main_window.label_25.setText(str(df.shape))

            vals = db.print_ajuste_base('apex_base_1')
            labs = [
                self.main_window.label_131,
                self.main_window.label_132,
                self.main_window.label_133,
                self.main_window.label_134,
                self.main_window.label_138,
                self.main_window.label_136,
                self.main_window.label_137,
                self.main_window.label_139,
                self.main_window.label_135,
                self.main_window.label_141
            ]
            for label, val in zip(labs, vals):
                label.setText(str(val))

        except sqlite3.OperationalError as op:
            print(f"SQLite error occurred: {op}")

    def drop_table_and_clear_widget(self, table_name):
        """
        Drops a table from the database and clears the corresponding QTableWidget.

        Parameters:
        ----------
        table_name : str
            The name of the table to drop from the database.
        """
        # Drop the table
        Database(self.main_window.label_base.text()).drop_table(table_name)

        # Clear the associated QTableWidget
        widget_mapping = {
            'IFC': self.main_window.tab_1,
            'CurvaProdutividade': self.main_window.tab_3,
            'RTMaterialGenetico': self.main_window.tab_4,
            'Orcamento': self.main_window.tab_5,
            'ClassesInclinacao': self.main_window.tab_6,
            'CadastroFlorestal': self.main_window.tab_7,
            'CustosSilvicultura_REF_REG': self.main_window.tab_22,
            'CustosColheitaPI': self.main_window.tab_8,
            'CustosColheitaPO': self.main_window.tab_9,
            'CustosColheitaCO': self.main_window.tab_10,
            'CustosColheitaGN': self.main_window.tab_11,
            'CustosColheitaBO': self.main_window.tab_12,
            'CustosColheitaSB': self.main_window.tab_13,
            'CustosTransRod': self.main_window.tab_14,
            'OutrosCustos': self.main_window.tab_15,
            'IFPC': self.main_window.tab_2
        }

        if table_name in widget_mapping:
            self.clear_table_widget(widget_mapping[table_name])

    def database_vacumm(self):
        try:
            Consist(self.main_window.label_base.text()).vacuum_database()
        except Exception as e:
            print(e)

    @staticmethod
    def populateTableWidget(df, table_widget):
        table_widget.setRowCount(0)
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for row_number, row_data in enumerate(df.values):
            table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row_number, column_number, item)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setSelectionBehavior(QTableWidget.SelectRows)

    def populate_table_from_db(self, db, table_name, table_widget, label_shape=None):
        df = db.fetch_all(table_name, parent=self.main_window)
        if label_shape:
            label_shape.setText(str(df.shape))
        self.populateTableWidget(df, table_widget)

    def on_sel_apex_1(self, event):
        sel_item = self.main_window.apex_comp_1.currentText()
        if sel_item != '':
            db = Consist(self.main_window.label_base.text())

            # Define the update mappings
            _update = {
                self.main_window.gn_r: ('GN', 'Reforma', 1),
                self.main_window.ne_r: ('NE', 'Reforma', 1),
                self.main_window.rd_r: ('RD', 'Reforma', 1),
                self.main_window.gn_g: ('GN', 'Regeneração', 1),
                self.main_window.ne_g: ('NE', 'Regeneração', 1),
                self.main_window.rd_g: ('RD', 'Regeneração', 1),
                self.main_window.sa_t_r: ('SA', 'Reforma', 3),
                self.main_window.co_t_r: ('CO', 'Reforma', 3),
                self.main_window.pi_t_r: ('PI', 'Reforma', 3),
                self.main_window.ip_t_r: ('IP', 'Reforma', 3),
                self.main_window.sa_t_g: ('SA', 'Regeneração', 3),
                self.main_window.co_t_g: ('CO', 'Regeneração', 3),
                self.main_window.pi_t_g: ('PI', 'Regeneração', 3),
                self.main_window.ip_t_g: ('IP', 'Regeneração', 3),
                self.main_window.cr_r: ('CR', 'Reforma', 5),
                self.main_window.sa_r: ('SA', 'Reforma', 5),
                self.main_window.pe_r: ('PE', 'Reforma', 5),
                self.main_window.vi_r: ('VI', 'Reforma', 5),
                self.main_window.ca_r: ('CA', 'Reforma', 5),
                self.main_window.ce_r: ('CE', 'Reforma', 5),
                self.main_window.al_r: ('AL', 'Reforma', 5),
                self.main_window.it_r: ('IT', 'Reforma', 5),
                self.main_window.pc_r: ('PC', 'Reforma', 5),
                self.main_window.sb_r: ('SB', 'Reforma', 5),
                self.main_window.ba_r: ('BA', 'Reforma', 5),
                self.main_window.ma_r: ('MA', 'Reforma', 5),
                self.main_window.pd_r: ('PD', 'Reforma', 5),
                self.main_window.po_r: ('PO', 'Reforma', 5),
                self.main_window.cr_g: ('CR', 'Regeneração', 5),
                self.main_window.sa_g: ('SA', 'Regeneração', 5),
                self.main_window.pe_g: ('PE', 'Regeneração', 5),
                self.main_window.vi_g: ('VI', 'Regeneração', 5),
                self.main_window.ca_g: ('CA', 'Regeneração', 5),
                self.main_window.ce_g: ('CE', 'Regeneração', 5),
                self.main_window.al_g: ('AL', 'Regeneração', 5),
                self.main_window.it_g: ('IT', 'Regeneração', 5),
                self.main_window.pc_g: ('PC', 'Regeneração', 5),
                self.main_window.sb_g: ('SB', 'Regeneração', 5),
                self.main_window.ba_g: ('BA', 'Regeneração', 5),
                self.main_window.ma_g: ('MA', 'Regeneração', 5),
                self.main_window.pd_g: ('PD', 'Regeneração', 5),
                self.main_window.po_g: ('PO', 'Regeneração', 5),
                self.main_window.apex_1: ('CR', 'Regeneração', 5),
                self.main_window.apex_2: ('SA', 'Regeneração', 5),
                self.main_window.apex_3: ('PE', 'Regeneração', 5),
                self.main_window.apex_5: ('VI', 'Regeneração', 5),
                self.main_window.apex_7: ('CA', 'Regeneração', 5),
                self.main_window.apex_8: ('CE', 'Regeneração', 5),
                self.main_window.apex_10: ('AL', 'Regeneração', 5),
                self.main_window.apex_11: ('IT', 'Regeneração', 5),
                self.main_window.apex_12: ('PC', 'Regeneração', 5),
                self.main_window.apex_14: ('SB', 'Regeneração', 5),
                self.main_window.apex_16: ('BA', 'Regeneração', 5),
                self.main_window.apex_17: ('MA', 'Regeneração', 5),
                self.main_window.apex_18: ('PD', 'Regeneração', 5),
                self.main_window.apex_20: ('PO', 'Regeneração', 5),
                self.main_window.apex_4: ('SA', 'Regeneração', 3),
                self.main_window.apex_6: ('GN', 'Regeneração', 1),
                self.main_window.apex_9: ('CO', 'Regeneração', 3),
                self.main_window.apex_13: ('PI', 'Regeneração', 3),
                self.main_window.apex_15: ('NE', 'Regeneração', 1),
                self.main_window.apex_19: ('IP', 'Regeneração', 3),
                self.main_window.apex_21: ('RD', 'Regeneração', 1)
            }

            for k, v in _update.items():
                val = db.regional_resumo(sel_item, v[1], v[0], v[2])
                if val is None:
                    val = 0  # Default to 0 if the value is None
                k.setText(f"{val:,.0f}".replace(',', '.'))

            # Update total labels
            total_updates = {
                self.main_window.total_r: (self.main_window.gn_r, self.main_window.ne_r, self.main_window.rd_r),
                self.main_window.total_g: (self.main_window.gn_g, self.main_window.ne_g, self.main_window.rd_g),
                self.main_window.apex_total_1: (self.main_window.apex_21, self.main_window.apex_15, self.main_window.apex_6)
            }
            for total_label, components in total_updates.items():
                total_val = sum(float(comp.text().replace('.', '')) for comp in components)
                total_label.setText(f"{total_val:,.0f}".replace(',', '.'))

            # Update the final totals
            update_totals = {
                self.main_window.gn_n: (self.main_window.gn_r, self.main_window.gn_g),
                self.main_window.ne_n: (self.main_window.ne_r, self.main_window.ne_g),
                self.main_window.rd_n: (self.main_window.rd_r, self.main_window.rd_g),
                self.main_window.sa_t_n: (self.main_window.sa_t_r, self.main_window.sa_t_g),
                self.main_window.co_t_n: (self.main_window.co_t_r, self.main_window.co_t_g),
                self.main_window.pi_t_n: (self.main_window.pi_t_r, self.main_window.pi_t_g),
                self.main_window.ip_t_n: (self.main_window.ip_t_r, self.main_window.ip_t_g),
                self.main_window.cr_n: (self.main_window.cr_r, self.main_window.cr_g),
                self.main_window.sa_n: (self.main_window.sa_r, self.main_window.sa_g),
                self.main_window.pe_n: (self.main_window.pe_r, self.main_window.pe_g),
                self.main_window.vi_n: (self.main_window.vi_r, self.main_window.vi_g),
                self.main_window.ca_n: (self.main_window.ca_r, self.main_window.ca_g),
                self.main_window.ce_n: (self.main_window.ce_r, self.main_window.ce_g),
                self.main_window.al_n: (self.main_window.al_r, self.main_window.al_g),
                self.main_window.it_n: (self.main_window.it_r, self.main_window.it_g),
                self.main_window.pc_n: (self.main_window.pc_r, self.main_window.pc_g),
                self.main_window.sb_n: (self.main_window.sb_r, self.main_window.sb_g),
                self.main_window.ba_n: (self.main_window.ba_r, self.main_window.ba_g),
                self.main_window.ma_n: (self.main_window.ma_r, self.main_window.ma_g),
                self.main_window.pd_n: (self.main_window.pd_r, self.main_window.pd_g),
                self.main_window.po_n: (self.main_window.po_r, self.main_window.po_g),
                self.main_window.total_n: (self.main_window.total_r, self.main_window.total_g)
            }
            for total_label, (label1, label2) in update_totals.items():
                total_val = float(label1.text().replace('.', '')) + float(label2.text().replace('.', ''))
                total_label.setText(f"{total_val:,.0f}".replace(',', '.'))

            # Update percentages
            percentage_updates = {
                self.main_window.gn_x: (self.main_window.gn_g, self.main_window.gn_n),
                self.main_window.ne_x: (self.main_window.ne_g, self.main_window.ne_n),
                self.main_window.rd_x: (self.main_window.rd_g, self.main_window.rd_n),
                self.main_window.sa_t_x: (self.main_window.sa_t_g, self.main_window.sa_t_n),
                self.main_window.co_t_x: (self.main_window.co_t_g, self.main_window.co_t_n),
                self.main_window.pi_t_x: (self.main_window.pi_t_g, self.main_window.pi_t_n),
                self.main_window.ip_t_x: (self.main_window.ip_t_g, self.main_window.ip_t_n),
                self.main_window.cr_x: (self.main_window.cr_g, self.main_window.cr_n),
                self.main_window.sa_x: (self.main_window.sa_g, self.main_window.sa_n),
                self.main_window.pe_x: (self.main_window.pe_g, self.main_window.pe_n),
                self.main_window.vi_x: (self.main_window.vi_g, self.main_window.vi_n),
                self.main_window.ca_x: (self.main_window.ca_g, self.main_window.ca_n),
                self.main_window.ce_x: (self.main_window.ce_g, self.main_window.ce_n),
                self.main_window.al_x: (self.main_window.al_g, self.main_window.al_n),
                self.main_window.it_x: (self.main_window.it_g, self.main_window.it_n),
                self.main_window.pc_x: (self.main_window.pc_g, self.main_window.pc_n),
                self.main_window.sb_x: (self.main_window.sb_g, self.main_window.sb_n),
                self.main_window.ba_x: (self.main_window.ba_g, self.main_window.ba_n),
                self.main_window.ma_x: (self.main_window.ma_g, self.main_window.ma_n),
                self.main_window.pd_x: (self.main_window.pd_g, self.main_window.pd_n),
                self.main_window.po_x: (self.main_window.po_g, self.main_window.po_n),
                self.main_window.total_x: (self.main_window.total_g, self.main_window.total_n)
            }
            for percentage_label, (label1, label2) in percentage_updates.items():
                val1 = float(label1.text().replace('.', ''))
                val2 = float(label2.text().replace('.', ''))
                try:
                    percentage = (val1 / val2) * 100 if val2 != 0 else 0
                except ZeroDivisionError:
                    percentage = 0
                percentage_label.setText(f"{percentage:.0f}".replace('.', ','))

            vals = db.fetch_row_by_rowid('ParametrosHistorico', int(sel_item.split('_')[-1]))
            vals = list(vals.values())
            parameters = {
                self.main_window.p1: vals[4],
                self.main_window.p2: vals[5],
                self.main_window.p3: vals[1],
                self.main_window.p4: vals[2],
                self.main_window.p5: vals[3],
                self.main_window.p6: vals[13],
                self.main_window.p7: vals[10],
                self.main_window.p8: vals[11],
                self.main_window.p9: vals[12],
                self.main_window.p10: vals[8],
                self.main_window.p11: vals[6],
                self.main_window.p12: vals[9],
                self.main_window.p13: vals[7],
            }
            for k, v in parameters.items():
                k.setText(v.replace('.', 'x').replace(',', '.').replace('x', ','))

                # A-B
                a_b = {
                    self.main_window._apex_1: (self.main_window.apex_1, self.main_window.apex_1_),
                    self.main_window._apex_2: (self.main_window.apex_2, self.main_window.apex_2_),
                    self.main_window._apex_3: (self.main_window.apex_3, self.main_window.apex_3_),
                    self.main_window._apex_5: (self.main_window.apex_5, self.main_window.apex_5_),
                    self.main_window._apex_7: (self.main_window.apex_7, self.main_window.apex_7_),
                    self.main_window._apex_8: (self.main_window.apex_8, self.main_window.apex_8_),
                    self.main_window._apex_10: (self.main_window.apex_10, self.main_window.apex_10_),
                    self.main_window._apex_11: (self.main_window.apex_11, self.main_window.apex_11_),
                    self.main_window._apex_12: (self.main_window.apex_12, self.main_window.apex_12_),
                    self.main_window._apex_14: (self.main_window.apex_14, self.main_window.apex_14_),
                    self.main_window._apex_16: (self.main_window.apex_16, self.main_window.apex_16_),
                    self.main_window._apex_17: (self.main_window.apex_17, self.main_window.apex_17_),
                    self.main_window._apex_18: (self.main_window.apex_18, self.main_window.apex_18_),
                    self.main_window._apex_20: (self.main_window.apex_20, self.main_window.apex_20_),
                    self.main_window._apex_4: (self.main_window.apex_4, self.main_window.apex_4_),
                    self.main_window._apex_6: (self.main_window.apex_6, self.main_window.apex_6_),
                    self.main_window._apex_9: (self.main_window.apex_9, self.main_window.apex_9_),
                    self.main_window._apex_13: (self.main_window.apex_13, self.main_window.apex_13_),
                    self.main_window._apex_15: (self.main_window.apex_15, self.main_window.apex_15_),
                    self.main_window._apex_19: (self.main_window.apex_19, self.main_window.apex_19_),
                    self.main_window._apex_21: (self.main_window.apex_21, self.main_window.apex_21_),
                    self.main_window.apex_total_1_2: (self.main_window.apex_total_1, self.main_window.apex_total_2)
                }
                for k, v in a_b.items():
                    try:
                        v1, v2 = float(v[0].text().replace('.', '')), float(v[1].text().replace('.', ''))
                    except ValueError:
                        v1, v2 = 0, 0
                    val = v1 - v2
                    k.setText(f"{val:.0f}".replace('.', ','))

            sizes = np.array(
                [
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'GN', 1),
                        db.regional_resumo(sel_item, 'Regeneração', 'GN', 1)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'NE', 1),
                        db.regional_resumo(sel_item, 'Regeneração', 'NE', 1)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'RD', 1),
                        db.regional_resumo(sel_item, 'Regeneração', 'RD', 1)
                    ]
                ]
            )
            main_labels = ['Guanhães', 'Nova Era', 'Rio Doce']
            sub_labels = ['Alto Fuste', 'Talhadia']
            somas = np.array(
                [
                    [db.regional_resumo(sel_item, 'Reforma', 'GN', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'GN', 1)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'GN', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'GN', 1)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'NE', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'NE', 1)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'NE', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'NE', 1)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'RD', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'RD', 1)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'RD', 1) +
                     db.regional_resumo(sel_item, 'Regeneração', 'RD', 1)
                     ]
                ]
            )
            self.plot_grouped_bar_chart(self.main_window.plotRegional, main_labels, sub_labels, sizes, sel_item, somas)

            sizes = np.array(
                [
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'SA', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'SA', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'VI', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'VI', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'CO', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'CO', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'PI', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'PI', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'SB', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'SB', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'IP', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'IP', 3)
                    ],
                    [
                        db.regional_resumo(sel_item, 'Reforma', 'PO', 3),
                        db.regional_resumo(sel_item, 'Regeneração', 'PO', 3)
                    ]
                ]
            )
            main_labels = ['Sabinópolis', 'Virginópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Ipaba', 'Pompéu']
            sub_labels = ['Alto Fuste', 'Talhadia']
            somas = np.array(
                [
                    [db.regional_resumo(sel_item, 'Reforma', 'SA', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'SA', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'SA', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'SA', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'VI', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'VI', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'VI', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'VI', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'CO', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'CO', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'CO', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'CO', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'PI', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'PI', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'PI', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'PI', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'SB', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'SB', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'SB', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'SB', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'IP', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'IP', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'IP', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'IP', 3)
                     ],
                    [db.regional_resumo(sel_item, 'Reforma', 'PO', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'PO', 3)
                        ,
                     db.regional_resumo(sel_item, 'Reforma', 'PO', 3) +
                     db.regional_resumo(sel_item, 'Regeneração', 'PO', 3)
                     ]
                ]
            )
            self.plot_grouped_bar_chart(self.main_window.plotRegiao, main_labels, sub_labels, sizes, sel_item, somas)

        else:
            pass

    def on_sel_apex_2(self, event):
        sel_item = self.main_window.apex_comp_2.currentText()
        if sel_item != '':
            db = Consist(self.main_window.label_base.text())

            # Define the update mappings
            _update = {
                self.main_window.apex_1_: ('CR', 'Regeneração', 5),
                self.main_window.apex_2_: ('SA', 'Regeneração', 5),
                self.main_window.apex_3_: ('PE', 'Regeneração', 5),
                self.main_window.apex_5_: ('VI', 'Regeneração', 5),
                self.main_window.apex_7_: ('CA', 'Regeneração', 5),
                self.main_window.apex_8_: ('CE', 'Regeneração', 5),
                self.main_window.apex_10_: ('AL', 'Regeneração', 5),
                self.main_window.apex_11_: ('IT', 'Regeneração', 5),
                self.main_window.apex_12_: ('PC', 'Regeneração', 5),
                self.main_window.apex_14_: ('SB', 'Regeneração', 5),
                self.main_window.apex_16_: ('BA', 'Regeneração', 5),
                self.main_window.apex_17_: ('MA', 'Regeneração', 5),
                self.main_window.apex_18_: ('PD', 'Regeneração', 5),
                self.main_window.apex_20_: ('PO', 'Regeneração', 5),
                self.main_window.apex_4_: ('SA', 'Regeneração', 3),
                self.main_window.apex_6_: ('GN', 'Regeneração', 1),
                self.main_window.apex_9_: ('CO', 'Regeneração', 3),
                self.main_window.apex_13_: ('PI', 'Regeneração', 3),
                self.main_window.apex_15_: ('NE', 'Regeneração', 1),
                self.main_window.apex_19_: ('IP', 'Regeneração', 3),
                self.main_window.apex_21_: ('RD', 'Regeneração', 1)
            }
            for k, v in _update.items():
                val = db.regional_resumo(sel_item, v[1], v[0], v[2])
                if val is None:
                    val = 0  # Default to 0 if the value is None
                k.setText(f"{val:,.0f}".replace(',', '.'))

            # Update total labels
            total_updates = {
                self.main_window.apex_total_2: (
                    self.main_window.apex_21_, self.main_window.apex_15_, self.main_window.apex_6_)
            }
            for total_label, components in total_updates.items():
                total_val = sum(float(comp.text().replace('.', '')) for comp in components)
                total_label.setText(f"{total_val:,.0f}".replace(',', '.'))

            # A-B
            a_b = {
                self.main_window._apex_1: (self.main_window.apex_1, self.main_window.apex_1_),
                self.main_window._apex_2: (self.main_window.apex_2, self.main_window.apex_2_),
                self.main_window._apex_3: (self.main_window.apex_3, self.main_window.apex_3_),
                self.main_window._apex_5: (self.main_window.apex_5, self.main_window.apex_5_),
                self.main_window._apex_7: (self.main_window.apex_7, self.main_window.apex_7_),
                self.main_window._apex_8: (self.main_window.apex_8, self.main_window.apex_8_),
                self.main_window._apex_10: (self.main_window.apex_10, self.main_window.apex_10_),
                self.main_window._apex_11: (self.main_window.apex_11, self.main_window.apex_11_),
                self.main_window._apex_12: (self.main_window.apex_12, self.main_window.apex_12_),
                self.main_window._apex_14: (self.main_window.apex_14, self.main_window.apex_14_),
                self.main_window._apex_16: (self.main_window.apex_16, self.main_window.apex_16_),
                self.main_window._apex_17: (self.main_window.apex_17, self.main_window.apex_17_),
                self.main_window._apex_18: (self.main_window.apex_18, self.main_window.apex_18_),
                self.main_window._apex_20: (self.main_window.apex_20, self.main_window.apex_20_),
                self.main_window._apex_4: (self.main_window.apex_4, self.main_window.apex_4_),
                self.main_window._apex_6: (self.main_window.apex_6, self.main_window.apex_6_),
                self.main_window._apex_9: (self.main_window.apex_9, self.main_window.apex_9_),
                self.main_window._apex_13: (self.main_window.apex_13, self.main_window.apex_13_),
                self.main_window._apex_15: (self.main_window.apex_15, self.main_window.apex_15_),
                self.main_window._apex_19: (self.main_window.apex_19, self.main_window.apex_19_),
                self.main_window._apex_21: (self.main_window.apex_21, self.main_window.apex_21_),
                self.main_window.apex_total_1_2: (self.main_window.apex_total_1, self.main_window.apex_total_2)
            }
            for k, v in a_b.items():
                v1, v2 = float(v[0].text().replace('.', '')), float(v[1].text().replace('.', ''))
                val = v1 - v2
                k.setText(f"{val:.0f}".replace('.', ','))

            vals = db.fetch_row_by_rowid('ParametrosHistorico', int(sel_item.split('_')[-1]))
            vals = list(vals.values())
            parameters = {
                self.main_window.p1_: vals[4],
                self.main_window.p2_: vals[5],
                self.main_window.p3_: vals[1],
                self.main_window.p4_: vals[2],
                self.main_window.p5_: vals[3],
                self.main_window.p6_: vals[13],
                self.main_window.p7_: vals[10],
                self.main_window.p8_: vals[11],
                self.main_window.p9_: vals[12],
                self.main_window.p10_: vals[8],
                self.main_window.p11_: vals[6],
                self.main_window.p12_: vals[9],
                self.main_window.p13_: vals[7],
            }
            for k, v in parameters.items():
                k.setText(v.replace('.', 'x').replace(',', '.').replace('x', ','))

        else:
            pass

    def add_new_tab(self, table_name=None):
        # Create a new tab widget and layout
        new_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(new_tab)

        # Create a QTableWidget and set it up
        table_widget = QtWidgets.QTableWidget(new_tab)
        table_widget.verticalHeader().setVisible(False)  # Hide the vertical header
        table_widget.horizontalHeader().setDefaultSectionSize(150)
        table_widget.horizontalHeader().setMinimumSectionSize(150)# Set default size for horizontal headers
        table_widget.verticalHeader().setDefaultSectionSize(80)  # Set default size for vertical headers
        table_widget.verticalHeader().setMinimumSectionSize(40)
        table_widget.setShowGrid(True)  # Show the grid lines
        table_widget.setGridStyle(Qt.NoPen) # Set minimum size for vertical headers

        # Add the table widget to the layout
        layout.addWidget(table_widget)

        # If a table name is provided, populate the table from the database
        if table_name and self.main_window.label_base.text() != '':
            db = Database(self.main_window.label_base.text())
            self.populate_table_from_db(db, table_name, table_widget, None)
            db.populate_tree_with_tables_and_columns(tree_widget=self.main_window.treeWidget)
        # Add the new tab to the tab widget
        self.main_window.table_holder.addTab(new_tab, f"Manejo {self.tab_counter + 1}")
        self.tab_counter += 1

        self.main_window.table_holder.tabBar().setStyleSheet("""
                QTabBar::tab {
                    font-family: 'Poppins';
                    font-size: 8pt;
                    min-width: 80px;
                }
            """)

    def execute_query(self):
        query_text = self.main_window.query_text_edit.toPlainText()
        try:
            if self.main_window.label_base.text() != '':
                db = Database(self.main_window.label_base.text())
                headers, rows = db.execute_query_db(query_text)
                db.populate_tree_with_tables_and_columns(tree_widget=self.main_window.treeWidget)

                self.main_window.result_table.verticalHeader().setVisible(False)  # Hide the vertical header
                self.main_window.result_table.horizontalHeader().setDefaultSectionSize(150)
                self.main_window.result_table.horizontalHeader().setMinimumSectionSize(150)  # Set default size for horizontal headers
                self.main_window.result_table.verticalHeader().setDefaultSectionSize(80)  # Set default size for vertical headers
                self.main_window.result_table.verticalHeader().setMinimumSectionSize(40)
                self.main_window.result_table.setShowGrid(True)  # Show the grid lines
                self.main_window.result_table.setGridStyle(Qt.NoPen)  # Set minimum size for vertical headers

                if headers and rows:
                    self.main_window.result_table.setColumnCount(len(headers))
                    self.main_window.result_table.setHorizontalHeaderLabels(headers)
                    self.main_window.result_table.setRowCount(len(rows))

                    for row_idx, row_data in enumerate(rows):
                        for col_idx, col_data in enumerate(row_data):
                            item = QtWidgets.QTableWidgetItem(str(col_data))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.main_window.result_table.setItem(row_idx, col_idx, item)

                    self.main_window.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.main_window.result_table.setSelectionBehavior(QTableWidget.SelectRows)

                    self.main_window.headers = headers
                    self.main_window.rows = rows
                else:
                    self.main_window.result_table.clear()
                    self.main_window.result_table.setRowCount(0)
                    self.main_window.result_table.setColumnCount(0)
        except Exception as e:
            pass

    def export_result_table_to_file(self, result_table):
        """
        Exports the data from a QTableWidget (result_table) to a CSV or Excel file, with a file dialog to choose the location and file type.

        :param result_table: The QTableWidget containing the data to export.
        """
        try:
            # Open a file dialog to select the file location, name, and type
            options = QFileDialog.Options()
            file_filter = "CSV Files (*.csv);;Excel Files (*.xlsx)"  # Allow both CSV and Excel file types
            file_path, selected_filter = QFileDialog.getSaveFileName(None, "Save File", "", file_filter,
                                                                     options=options)

            # If the user cancels the dialog, return early
            if not file_path:
                return

            # Determine the file type based on the selected filter
            if "csv" in selected_filter.lower():
                file_type = "csv"
                if not file_path.endswith(".csv"):
                    file_path += ".csv"  # Ensure CSV extension
            elif "xlsx" in selected_filter.lower():
                file_type = "excel"
                if not file_path.endswith(".xlsx"):
                    file_path += ".xlsx"  # Ensure Excel extension
            else:
                raise ValueError("Unsupported file type selected.")

            # Get the number of rows and columns in the result table
            rows = self.main_window.result_table.rowCount()
            columns = self.main_window.result_table.columnCount()

            # Extract headers from the result table
            headers = [self.main_window.result_table.horizontalHeaderItem(col).text() for col in range(columns)]

            # Extract data from the result table
            data = []
            for row in range(rows):
                row_data = []
                for col in range(columns):
                    item = self.main_window.result_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # Create a pandas DataFrame with the extracted data
            df = pd.DataFrame(data, columns=headers)

            # Export to the selected file type
            if file_type == "csv":
                df.to_csv(file_path, index=False, sep=';')  # Export as CSV with ';' as delimiter
            elif file_type == "excel":
                df.to_excel(file_path, index=False)  # Export as Excel file

            print(f"Data exported successfully to {file_path}")

        except Exception as e:
            print(f"An error occurred while exporting: {e}")

    @staticmethod
    def clear_table_widget(table_widget):
        """
        Clears all data from the specified QTableWidget.

        Parameters:
        ----------
        table_widget : QTableWidget
            The table widget to clear.
        """
        table_widget.clearContents()
        table_widget.setRowCount(0)

    @staticmethod
    def show_menu(button, menu):
        """
        Display the menu below the button.
        """
        button_rect = button.rect()
        menu_width = button.width()  # Set the menu width to the button width
        global_pos = button.mapToGlobal(button_rect.bottomLeft())
        menu.setFixedWidth(menu_width)  # Set the menu width to the button width
        menu.exec_(global_pos)

    @staticmethod
    def prod_min(prod, perda_percentual):
        """
        Calculate the minimum production value considering a percentage loss.
        """
        try:
            prod_value, perda_value = float(prod), float(perda_percentual)
            return "{:.2f}".format(prod_value * (1 - perda_value / 100))
        except ValueError:
            return "-"

    @staticmethod
    def apply_drop_shadow(widget):
        """
        Apply a drop shadow effect to a widget.
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def set_circular_image(label, pixmap):
        """
        Set a circular image on a QLabel.
        """
        size = min(label.width(), label.height())
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        label.setPixmap(circular_pixmap)
        label.setFixedSize(size, size)

    @staticmethod
    def search_in_table(search_text, tabela):
        search_text = search_text.lower()
        for row in range(tabela.rowCount()):
            row_hidden = True
            for col in range(tabela.columnCount()):
                item = tabela.item(row, col)
                if item and search_text in item.text().lower():
                    row_hidden = False
                    break
            tabela.setRowHidden(row, row_hidden)

    @staticmethod
    def nova_canvas(layout, fig, ax, tb=True):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        canvas = FigureCanvas(fig)
        if tb:
            toolbar = NavigationToolbar(canvas, None)
            layout.addWidget(toolbar)
        layout.addWidget(canvas)
        ax.clear()
        canvas.draw()

    @staticmethod
    def clear_layout(layout):
        """
        Clear all widgets from the given layout.

        :param layout: The layout to clear.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def plot_grouped_bar_chart(self, layout, main_labels, sub_labels, values, title, sum):
        try:
            self.clear_layout(layout)

            fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure without toolbar

            # Set up the canvas and toolbar
            self.nova_canvas(layout, fig, ax, tb=False)

            # Number of main labels and sub-labels
            n_main_labels = len(main_labels)
            n_sub_labels = len(sub_labels)

            # Bar positions
            bar_width = 0.35
            bar_spacing = 0.1  # Space between groups
            explode_effect = 0.05  # Space between bars within each group
            index = np.arange(n_main_labels) * (bar_width * n_sub_labels + bar_spacing)

            # Define two distinct colors
            color_set = ['#16271C', '#878672']  # Define start and end colors

            # Plot bars for each sub-label with explode effect
            for i, (label, color) in enumerate(zip(sub_labels, color_set)):
                bars = ax.bar(index + i * (bar_width + explode_effect), values[:, i], bar_width, label=label,
                              color=color, zorder=2)

                # Customize the text properties
                for bar, value in zip(bars, sum[:, i]):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                            f'{int(height):,}'.replace(',', '.'), ha='center', va='center', color='white', fontsize=8,
                            fontweight='bold')
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{(int(height) / value) * 100:,.0f}%',
                            ha='center', va='bottom', fontsize=8)

            # Set the title
            ax.set_title(title, color='black')

            # Set labels
            ax.set_xticks(index + (bar_width + explode_effect) * (n_sub_labels - 1) / 2)
            ax.set_xticklabels(main_labels)

            formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
            ax.yaxis.set_major_formatter(formatter)

            ax.legend()

            # Remove the frame lines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Draw the canvas to render the plot
            fig.canvas.draw()
        except Exception as e:
            print(f"An error occurred in bar graph: {e}")

    def plot_bar_chart(self, layout, labels, values, title, sum):
        try:
            self.clear_layout(layout)

            fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure without toolbar

            # Set up the canvas and toolbar
            self.nova_canvas(layout, fig, ax, tb=False)

            # Number of labels
            n_labels = len(labels)

            # Bar positions
            bar_width = 0.6
            index = np.arange(n_labels)

            # Define the color for the bars
            color = '#16271C'

            # Plot bars
            bars = ax.bar(index, values, bar_width, color=color, zorder=2)

            # Customize the text properties
            for bar, value in zip(bars, sum):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                        f'{int(height):,}'.replace(',', '.'), ha='center', va='center', color='white', fontsize=8,
                        fontweight='bold')
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f'{(int(height) / value) * 100:,.0f}%', ha='center', va='bottom', fontsize=8)

            # Set the title
            ax.set_title(title, color='black')

            # Set labels
            ax.set_xticks(index)
            ax.set_xticklabels(labels)

            # Format the y-axis with commas
            formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', '.'))
            ax.yaxis.set_major_formatter(formatter)

            # Remove the frame lines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Draw the canvas to render the plot
            fig.canvas.draw()
        except Exception as e:
            print(f"An error occurred in bar graph: {e}")

    @staticmethod
    def generate_color_palette(colors, num_colors):
        """
        Generate a color palette by interpolating between multiple colors.

        :param colors: A list of colors in hex format to interpolate between (e.g., ['#16271C', '#26427F', '#627368', '#878672']).
        :param num_colors: The total number of colors to generate.
        :return: A list of colors in hex format.
        """
        # Convert hex colors to RGB
        rgb_colors = [np.array(mcolors.hex2color(color)) for color in colors]

        # Number of intervals
        num_intervals = len(colors) - 1

        # Number of colors per interval
        colors_per_interval = np.linspace(0, 1, num_colors // num_intervals + 1)

        # Generate the color palette
        palette = []
        for i in range(num_intervals):
            start_rgb = rgb_colors[i]
            end_rgb = rgb_colors[i + 1]
            for t in colors_per_interval:
                interpolated_color = start_rgb + (end_rgb - start_rgb) * t
                palette.append(mcolors.rgb2hex(interpolated_color))

        # Ensure the final color is included
        palette = palette[:num_colors]  # Trim any excess colors if the division isn't perfect
        return palette

    def plot_radar_chart(self, layout, categories, values_list, title, labels=None):
        """
        Create a radar chart and add it to the specified layout.

        :param layout: The layout where the radar chart should be added.
        :param categories: List of categories (labels) for each axis of the radar chart.
        :param values_list: List of lists, where each list contains values corresponding to the categories.
        :param title: Title of the radar chart.
        :param labels: List of labels for each set of values. Defaults to None.
        """
        try:
            self.clear_layout(layout)
            # Number of variables we're plotting.
            num_vars = len(categories)

            # Compute angle for each category
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1]  # Complete the loop

            # Create a figure and a polar subplot
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            # Set up the canvas using nova_canvas
            self.nova_canvas(layout, fig, ax, tb=False)

            # Generate a color palette from the start to end color
            palette = self.generate_color_palette(['#16271C', '#24382A', '#304D38', '#3C6246', '#487754', '#627368', '#7F8A78', '#9CA088', '#B9B698','#E9D8E3'], len(values_list))

            # Plot each set of values
            for i, values in enumerate(values_list):
                values += values[:1]  # Complete the loop for values
                label = labels[i] if labels else f"Set {i + 1}"
                color = palette[i]  # Get a color from the generated palette

                # Plot data
                ax.fill(angles, values, color=color, alpha=0.25)
                ax.plot(angles, values, color=color, linewidth=2, label=label)

            # Add category labels to the chart
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)

            # Set the title of the chart
            ax.set_title(title, size=12, color='black', pad=20)

            # Add a legend in the best possible location
            if labels:
                ax.legend(loc='best', bbox_to_anchor=(1.1, 1.1))

            # Draw the canvas to render the radar chart
            fig.canvas.draw()
        except Exception as e:
            print(f"An error occurred in radar chart: {e}")

    def plot_horizontal_bar_chart(self, layout, labels, values_1, values_2, title):
        """
        Create a horizontal bar chart with values from two different selections,
        with bars facing each other on the same label, and y-axis labels aligned to the center vertical line.

        :param layout: The layout where the bar chart should be added.
        :param labels: List of labels for the bar chart.
        :param values_1: List of values corresponding to the labels from on_sel_apex_1.
        :param values_2: List of values corresponding to the labels from on_sel_apex_2.
        :param title: Title of the bar chart.
        """
        try:
            self.clear_layout(layout)
            # Set up the figure and axis
            fig, ax = plt.subplots(figsize=(10, 6))

            # Set up the canvas using nova_canvas
            self.nova_canvas(layout, fig, ax, tb=False)

            # Define the positions and bar width
            y_pos = np.arange(len(labels))
            bar_width = 0.55

            # Plot the bars for both sets of values, with values_1 on the left and values_2 on the right
            bars2 = ax.barh(y_pos, values_1, bar_width, label='APEX 02', color='#16271C', align='center')
            bars1 = ax.barh(y_pos, -np.array(values_2), bar_width, label='APEX 01', color='#878672', align='center')

            # Hide all axes
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            # Hide x-axis labels and ticks
            ax.set_xticks([])

            # Hide the y-axis tick labels
            ax.set_yticks([])

            # Add a vertical line at the center for separation
           #ax.axvline(0, color='black', linewidth=0.5)

            # Add the y-axis labels (categories) on the vertical line
            for i, label in enumerate(labels):
                ax.text(0, y_pos[i] - bar_width / 2, label, ha='center', va='top', fontsize=10, color='black')

            # Add value labels inside the bars
            for bar in bars2:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:,.0f}'.replace(',', '.'), ha='right',
                        va='center', color='white', fontsize=8, fontweight='bold')

            for bar in bars1:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height() / 2, f'{(width * -1):,.0f}'.replace(',', '.'), ha='left',
                        va='center', color='white', fontsize=8, fontweight='bold')

            # Add a legend
            ax.legend()

            ax.set_title(title, size=12, color='black', pad=20)
            # Draw the canvas to render the plot
            fig.canvas.draw()
        except Exception as e:
            print(f"An error occurred in horizontal bar chart: {e}")

    def combox_changes(self):
        try:
            db = Consist(self.main_window.label_base.text())
            sel_item = self.main_window.apex_comp_1.currentText()
            sel_item2 = self.main_window.apex_comp_2.currentText()
            labels = ['Sabinópolis', 'Virginópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Ipaba', 'Pompéu']
            vals_item2 = [
                db.regional_resumo(sel_item, 'Regeneração', 'SA', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'VI', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'CO', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'PI', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'SB', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'IP', 3),
                db.regional_resumo(sel_item, 'Regeneração', 'PO', 3)

            ]
            vals_item1 = [
                db.regional_resumo(sel_item2, 'Regeneração', 'SA', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'VI', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'CO', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'PI', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'SB', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'IP', 3),
                db.regional_resumo(sel_item2, 'Regeneração', 'PO', 3)

            ]
            self.plot_horizontal_bar_chart(self.main_window.plotHorizontalGraph, labels, vals_item1, vals_item2, 'Comparativo de Talhadia (ha)')
        except sqlite3.OperationalError as sqe:
            print(f'Error: {sqe}')
            pass

    def checkboxes_av_eco(self):
        db = Consist(self.main_window.label_base.text())
        sel_item = self.main_window.apex_comp_1.currentText()
        sel_tab = self.main_window.comb1.currentText()
        # Define the mapping of ComboBox selections to columns/labels
        tab_mapping = {
            'Custo Posto-Fábrica': 'CustosPostoFabrica',
            'Custo de Colheita': 'CustosColheitaTotal',
            'Custo de Silvicultura': 'CustoMADPE',
            'Custos Taxas ADM': 'CustosTAXAADM'
        }

        # Get the mapped value based on ComboBox selection
        selected_column = tab_mapping.get(sel_tab, 'CustosPostoFabrica')
        group_1 = [(self.main_window.checkBox_7.isChecked(), 1), (self.main_window.checkBox_6.isChecked(), 3)]
        group_2 = [(self.main_window.checkBox_9.isChecked(), 'False'), (self.main_window.checkBox_10.isChecked(), 'True')]

        # Function to find the checked checkbox index in a group if exactly one is checked
        def get_checked_index(group):
            checked_items = [index for checked, index in group if checked]
            return checked_items[0] if len(checked_items) == 1 else None

        # Get the checked index for each group
        checked_group_1 = get_checked_index(group_1)
        checked_group_2 = get_checked_index(group_2)

        # If all groups have exactly one checkbox checked, return the indices
        if checked_group_1 and checked_group_2:
            if checked_group_1 == 1:
                sizes = np.array(
                    [
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'GN', checked_group_1, selected_column+'_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'GN', checked_group_1, selected_column+'_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'NE', checked_group_1, selected_column+'_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'NE', checked_group_1, selected_column+'_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'RD', checked_group_1, selected_column+'_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'RD', checked_group_1, selected_column+'_REF_REG', checked_group_2)
                        ]
                    ]
                )
                main_labels = ['Guanhães', 'Nova Era', 'Rio Doce']
                sub_labels = ['Alto Fuste', 'Talhadia']
                somas = np.array(
                    [
                        [db.regional_resumo_av(sel_item, 'Reforma', 'GN', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'GN', checked_group_1, selected_column+'_REF_REG', 'True')
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'GN', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'GN', checked_group_1, selected_column+'_REF_REG', 'True')
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'NE', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'NE', checked_group_1, selected_column+'_REF_REG', 'True')
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'NE', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'NE', checked_group_1, selected_column+'_REF_REG', 'True')
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'RD', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'RD', checked_group_1, selected_column+'_REF_REG', 'True')
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'RD', checked_group_1, selected_column+'_REF_REF', 'True') +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'RD', checked_group_1, selected_column+'_REF_REG', 'True')
                         ]
                    ]
                )
                self.plot_grouped_bar_chart(self.main_window.plotAv_1, main_labels, sub_labels, sizes, sel_tab+" R$: "+sel_item, somas)
                return
            if checked_group_1 == 3:
                sizes = np.array(
                    [
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'SA', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'SA', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'VI', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'VI', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'CO', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'CO', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'PI', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'PI', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'SB', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'SB', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'IP', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'IP', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ],
                        [
                            db.regional_resumo_av(sel_item, 'Reforma', 'PO', checked_group_1,
                                                  selected_column + '_REF_REF', checked_group_2),
                            db.regional_resumo_av(sel_item, 'Regeneração', 'PO', checked_group_1,
                                                  selected_column + '_REF_REG', checked_group_2)
                        ]
                    ]
                )
                main_labels = ['Sabinópolis', 'Virginópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Ipaba', 'Pompéu']
                sub_labels = ['Alto Fuste', 'Talhadia']
                somas = np.array(
                    [
                        [db.regional_resumo_av(sel_item, 'Reforma', 'SA', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'SA', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'SA', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'SA', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'VI', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'VI', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'VI', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'VI', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'CO', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'CO', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'CO', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'CO', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'PI', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'PI', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'PI', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'PI', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'SB', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'SB', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'SB', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'SB', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'IP', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'IP', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'IP', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'IP', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ],
                        [db.regional_resumo_av(sel_item, 'Reforma', 'PO', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'PO', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                            ,
                         db.regional_resumo_av(sel_item, 'Reforma', 'PO', checked_group_1, selected_column + '_REF_REF',
                                               checked_group_2) +
                         db.regional_resumo_av(sel_item, 'Regeneração', 'PO', checked_group_1,
                                               selected_column + '_REF_REG', checked_group_2)
                         ]
                    ]
                )
                self.plot_grouped_bar_chart(self.main_window.plotAv_1, main_labels, sub_labels, sizes,
                                            sel_tab + " R$: " + sel_item, somas)
                return
        else:
            # Return None if more than one or no checkbox is checked in any group
            return None
