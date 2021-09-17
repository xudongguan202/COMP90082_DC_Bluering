import wx
import wx.xrc
import wx.grid as grid
import wx.grid as gridlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import csv
from csv import writer
import re
import pymysql


def Testr(path_Client, path_Lab):

    df_Client = pd.read_csv(path_Client, skiprows=22)
    df_Lab = pd.read_csv(path_Lab, skiprows=22)

    headLab = pd.read_csv(
        "Raw MEX measurement data 1Lab.csv", usecols=[2], nrows=17
    )
    headClient = pd.read_csv(
        "Raw MEX measurement data 1Client.csv", usecols=[2], nrows=17
    )
    # print(headClient)

    # 提取Client基本信息
    chamberID_Client = headClient.iat[2, 0]
    chamberID_Lab = headLab.iat[2, 0]
    clientName = headClient.iat[15, 0]
    clientAddress = headClient.iat[16, 0]

    measurement_Client = headClient.iat[6, 0]
    measurement_Client = headClient.iat[5, 0]
    measurement_Lab = headLab.iat[6, 0]
    background_Lab = headLab.iat[5, 0]
    xAxisList = df_Client["kV"].unique()
    filterName = df_Client["Filter"].unique()

    current1_Client = df_Client["Current1(pA)"]
    current2_Client = df_Client["Current2(pA)"]

    current1_Lab = df_Lab["Current1(pA)"]
    current2_Lab = df_Lab["Current2(pA)"]

    BgdIC1_Before_Client = current1_Client.iloc[0:89].mean(axis=0)
    BgdMC1_Before_Client = current2_Client.iloc[0:89].mean(axis=0)

    BgdIC2_Before_Lab = current1_Lab.iloc[0:89].mean(axis=0)
    BgdMC2_Before_Lab = current2_Lab.iloc[0:89].mean(axis=0)

    df_Client["R1"] = (
        (
            (df_Client["Current2(pA)"] - BgdIC2_Before_Lab)
            / (df_Client["Current1(pA)"] - BgdMC2_Before_Lab)
        )
        .groupby([df_Client["Filter"], df_Client["XraysOn"]])
        .transform("mean")
        .round(5)
    )
    df_Lab["R2"] = (
        (
            (df_Lab["Current2(pA)"] - BgdIC2_Before_Lab)
            / (df_Lab["Current1(pA)"] - BgdMC2_Before_Lab)
        )
        .groupby([df_Lab["Filter"], df_Lab["XraysOn"]])
        .transform("mean")
        .round(5)
    )

    # currentLab_Mean["H2"]=currentLab_Mean.apply(H2,axis=1)
    pd.set_option("display.max_rows", None)

    group_Client = df_Client.groupby(["Filter", "XraysOn"], as_index=False)
    df_Client_MEX = group_Client.agg(
        {
            "kV": "mean",
            "Current1(pA)": "mean",
            "Current2(pA)": "mean",
            "T(MC)": "mean",
            "T(Air)": "mean",
            "R1": "mean",
        }
    )

    group_Lab = df_Lab.groupby(["Filter", "XraysOn"], as_index=False)
    df_Lab_MEX = group_Lab.agg(
        {
            "kV": "mean",
            "Current1(pA)": "mean",
            "Current2(pA)": "mean",
            "T(MC)": "mean",
            "T(SC)": "mean",
            "H(%)": "mean",
            "R2": "mean",
        }
    )
    df_Client_MEX["R2"] = df_Lab_MEX["R2"]
    df_Lab_MEX["MC2"] = df_Lab_MEX[["Current1(pA)"]].apply(
        lambda x: x["Current1(pA)"] - BgdMC2_Before_Lab, axis=1
    )
    df_Lab_MEX["IC2"] = df_Lab_MEX[["Current2(pA)"]].apply(
        lambda x: x["Current2(pA)"] - BgdIC2_Before_Lab, axis=1
    )

    df_Client_MEX["MC1"] = df_Lab_MEX[["Current1(pA)"]].apply(
        lambda x: x["Current1(pA)"] - BgdMC1_Before_Client, axis=1
    )
    df_Client_MEX["IC1"] = df_Lab_MEX[["Current2(pA)"]].apply(
        lambda x: x["Current2(pA)"] - BgdIC1_Before_Client, axis=1
    )
    df_Client_MEX["MC2"] = df_Lab_MEX["MC2"]
    df_Client_MEX["IC2"] = df_Lab_MEX["IC2"]
    df_Client_MEX["TM2"] = df_Lab_MEX["T(MC)"]
    df_Client_MEX["TS2"] = df_Lab_MEX["T(SC)"]
    df_Client_MEX["H2"] = df_Lab_MEX["H(%)"]

    Ma = 6.18e-06
    WE = 33.97

    df_Client_MEX["NK"] = df_Lab_MEX[["Current2(pA)"]].apply(
        lambda x: x["Current2(pA)"] - BgdIC1_Before_Client, axis=1
    )
    # df_Client_MEX["k"]=

    # print(df_Client_MEX)

    product = pd.read_csv("KKMaWE.csv", skiprows=10)
    product = product[["Filter", "Product"]]

    df_merge_col = pd.merge(df_Client_MEX, product, on="Filter")
    df_merge_col["NK"] = df_merge_col[
        ["Product", "R1", "R2", "T(Air)", "H2", "T(MC)", "TS2", "TM2"]
    ].apply(
        lambda x: x["R2"]
        * WE
        * x["Product"]
        * ((273.15 + x["TS2"]) / (273.15 + x["TM2"]))
        * (0.995766667 + 0.000045 * x["H2"])
        / (Ma * x["R1"] * (273.15 + x["T(Air)"]) / (273.15 + x["T(MC)"]))
        / 1000000,
        axis=1,
    )

    df_merge_col = df_merge_col.drop(df_merge_col[df_merge_col.XraysOn == False].index)

    KeV = df_merge_col["kV"].values.tolist()
    Beam = df_merge_col["Filter"].values.tolist()
    NK = df_merge_col["NK"].values.tolist()

    # print(df_merge_col)
    return KeV, Beam, NK


class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        frame = MainFrame()
        # frame = GraphFrame()
        frame.Show()


# This class is the main interface class
class MainFrame(wx.Frame):
    def __init__(
        self,
        title="App",
        pos=wx.DefaultPosition,
        size=wx.Size(1100, 700),
        style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
    ):
        # super().__init__(None, title = title)
        super().__init__(
            None,
            id=wx.ID_ANY,
            title=u"Digital Calibration Generator",
            pos=wx.DefaultPosition,
            size=wx.Size(1100, 700),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )
        self.InitFrame()

    def InitFrame(self):

        # global var #

        self.confirmed = False  # chech if confirm is clicked
        self.readed = False

        ##############

        self.SetSizeHints(wx.Size(1100, 700), wx.Size(1100, 700))

        bSizer_main = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_left = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(700, -1), wx.TAB_TRAVERSAL
        )
        self.m_panel_left.SetMinSize(wx.Size(700, -1))
        self.m_panel_left.SetMaxSize(wx.Size(700, -1))

        bSizer_left = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_show_run = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 40),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_show_run.SetMinSize(wx.Size(-1, 40))
        self.m_panel_show_run.SetMaxSize(wx.Size(-1, 40))

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel28 = wx.Panel(
            self.m_panel_show_run,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_total_run = wx.StaticText(
            self.m_panel28,
            wx.ID_ANY,
            u"Total Runs",
            wx.Point(-1, -1),
            wx.DefaultSize,
            0,
        )
        self.m_staticText_total_run.Wrap(-1)

        bSizer15.Add(self.m_staticText_total_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_total_run = wx.TextCtrl(
            self.m_panel28,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY,
        )
        self.m_textCtrl_total_run.SetValue("0")
        bSizer15.Add(self.m_textCtrl_total_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel28.SetSizer(bSizer15)
        self.m_panel28.Layout()
        bSizer15.Fit(self.m_panel28)
        bSizer14.Add(self.m_panel28, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel281 = wx.Panel(
            self.m_panel_show_run,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_selected_run = wx.StaticText(
            self.m_panel281,
            wx.ID_ANY,
            u"Selected Runs",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText_selected_run.Wrap(-1)

        bSizer16.Add(self.m_staticText_selected_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_selected_run = wx.TextCtrl(
            self.m_panel281,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY,
        )
        self.m_textCtrl_selected_run.SetValue("0")
        bSizer16.Add(self.m_textCtrl_selected_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel281.SetSizer(bSizer16)
        self.m_panel281.Layout()
        bSizer16.Fit(self.m_panel281)
        bSizer14.Add(self.m_panel281, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel282 = wx.Panel(
            self.m_panel_show_run,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button_confirm = wx.Button(
            self.m_panel282,
            wx.ID_ANY,
            u"Confirm",
            wx.DefaultPosition,
            wx.Size(100, 30),
            0,
        )
        self.m_button_confirm.SetMinSize(wx.Size(100, 30))
        self.m_button_confirm.SetMaxSize(wx.Size(100, 30))

        bSizer17.Add(self.m_button_confirm, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.confirm, self.m_button_confirm)

        self.m_button_compare = wx.Button(
            self.m_panel282,
            wx.ID_ANY,
            u"Compare",
            wx.DefaultPosition,
            wx.Size(100, 30),
            0,
        )
        self.m_button_compare.SetMinSize(wx.Size(100, 30))
        self.m_button_compare.SetMaxSize(wx.Size(100, 30))

        bSizer17.Add(self.m_button_compare, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.compare, self.m_button_compare)

        self.m_panel282.SetSizer(bSizer17)
        self.m_panel282.Layout()
        bSizer17.Fit(self.m_panel282)
        bSizer14.Add(self.m_panel282, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_show_run.SetSizer(bSizer14)
        self.m_panel_show_run.Layout()
        bSizer_left.Add(self.m_panel_show_run, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_pbar = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 30),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_pbar.SetMinSize(wx.Size(-1, 30))
        self.m_panel_pbar.SetMaxSize(wx.Size(-1, 30))

        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        MainFrame.m_progress_bar = wx.Gauge(
            self.m_panel_pbar,
            wx.ID_ANY,
            100,
            wx.DefaultPosition,
            wx.Size(500, -1),
            wx.GA_HORIZONTAL,
        )
        MainFrame.m_progress_bar.SetValue(0)
        bSizer18.Add(MainFrame.m_progress_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.m_panel_pbar.SetSizer(bSizer18)
        self.m_panel_pbar.Layout()
        bSizer_left.Add(self.m_panel_pbar, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_upload1 = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer_run1 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_upload1, wx.ID_ANY, u"Run 1"), wx.VERTICAL
        )

        bSizer_run1_inside = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file = wx.Panel(
            sbSizer_run1.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel39 = wx.Panel(
            self.m_panel_run1_file,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer27 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run11 = wx.FilePickerCtrl(
            self.m_panel39,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run11.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run11.SetMaxSize(wx.Size(600, -1))

        bSizer27.Add(self.m_filePicker_run11, 0, wx.ALL, 1)

        self.m_panel39.SetSizer(bSizer27)
        self.m_panel39.Layout()
        bSizer27.Fit(self.m_panel39)
        bSizer24.Add(self.m_panel39, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel40 = wx.Panel(
            self.m_panel_run1_file,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer271 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run12 = wx.FilePickerCtrl(
            self.m_panel40,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run12.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run12.SetMaxSize(wx.Size(600, -1))

        bSizer271.Add(self.m_filePicker_run12, 0, wx.ALL, 1)

        self.m_panel40.SetSizer(bSizer271)
        self.m_panel40.Layout()
        bSizer271.Fit(self.m_panel40)
        bSizer24.Add(self.m_panel40, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file.SetSizer(bSizer24)
        self.m_panel_run1_file.Layout()
        bSizer24.Fit(self.m_panel_run1_file)
        bSizer_run1_inside.Add(self.m_panel_run1_file, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check = wx.Panel(
            sbSizer_run1.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            wx.TAB_TRAVERSAL,
        )
        bSizer_run1_check = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run1 = wx.CheckBox(
            self.m_panel_run1_check,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        bSizer_run1_check.Add(self.m_checkBox_run1, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check.SetSizer(bSizer_run1_check)
        self.m_panel_run1_check.Layout()
        bSizer_run1_check.Fit(self.m_panel_run1_check)
        bSizer_run1_inside.Add(self.m_panel_run1_check, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run1.Add(bSizer_run1_inside, 1, wx.EXPAND, 1)

        self.m_panel_upload1.SetSizer(sbSizer_run1)
        self.m_panel_upload1.Layout()
        sbSizer_run1.Fit(self.m_panel_upload1)
        bSizer_left.Add(self.m_panel_upload1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload2 = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer_run11 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_upload2, wx.ID_ANY, u"Run 2"), wx.VERTICAL
        )

        bSizer_run1_inside1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file1 = wx.Panel(
            sbSizer_run11.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer241 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel391 = wx.Panel(
            self.m_panel_run1_file1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer272 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run21 = wx.FilePickerCtrl(
            self.m_panel391,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run21.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run21.SetMaxSize(wx.Size(600, -1))

        bSizer272.Add(self.m_filePicker_run21, 0, wx.ALL, 1)

        self.m_panel391.SetSizer(bSizer272)
        self.m_panel391.Layout()
        bSizer272.Fit(self.m_panel391)
        bSizer241.Add(self.m_panel391, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel401 = wx.Panel(
            self.m_panel_run1_file1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer2711 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run22 = wx.FilePickerCtrl(
            self.m_panel401,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run22.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run22.SetMaxSize(wx.Size(600, -1))

        bSizer2711.Add(self.m_filePicker_run22, 0, wx.ALL, 1)

        self.m_panel401.SetSizer(bSizer2711)
        self.m_panel401.Layout()
        bSizer2711.Fit(self.m_panel401)
        bSizer241.Add(self.m_panel401, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file1.SetSizer(bSizer241)
        self.m_panel_run1_file1.Layout()
        bSizer241.Fit(self.m_panel_run1_file1)
        bSizer_run1_inside1.Add(self.m_panel_run1_file1, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check1 = wx.Panel(
            sbSizer_run11.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(70, -1),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_run1_check1.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check1.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run2 = wx.CheckBox(
            self.m_panel_run1_check1,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        bSizer_run1_check1.Add(self.m_checkBox_run2, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check1.SetSizer(bSizer_run1_check1)
        self.m_panel_run1_check1.Layout()
        bSizer_run1_inside1.Add(self.m_panel_run1_check1, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run11.Add(bSizer_run1_inside1, 1, wx.EXPAND, 1)

        self.m_panel_upload2.SetSizer(sbSizer_run11)
        self.m_panel_upload2.Layout()
        sbSizer_run11.Fit(self.m_panel_upload2)
        bSizer_left.Add(self.m_panel_upload2, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload3 = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer_run12 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_upload3, wx.ID_ANY, u"Run 3"), wx.VERTICAL
        )

        bSizer_run1_inside2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file2 = wx.Panel(
            sbSizer_run12.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer242 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel392 = wx.Panel(
            self.m_panel_run1_file2,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer273 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run31 = wx.FilePickerCtrl(
            self.m_panel392,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run31.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run31.SetMaxSize(wx.Size(600, -1))

        bSizer273.Add(self.m_filePicker_run31, 0, wx.ALL, 1)

        self.m_panel392.SetSizer(bSizer273)
        self.m_panel392.Layout()
        bSizer273.Fit(self.m_panel392)
        bSizer242.Add(self.m_panel392, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel402 = wx.Panel(
            self.m_panel_run1_file2,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer2712 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run32 = wx.FilePickerCtrl(
            self.m_panel402,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run32.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run32.SetMaxSize(wx.Size(600, -1))

        bSizer2712.Add(self.m_filePicker_run32, 0, wx.ALL, 1)

        self.m_panel402.SetSizer(bSizer2712)
        self.m_panel402.Layout()
        bSizer2712.Fit(self.m_panel402)
        bSizer242.Add(self.m_panel402, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file2.SetSizer(bSizer242)
        self.m_panel_run1_file2.Layout()
        bSizer242.Fit(self.m_panel_run1_file2)
        bSizer_run1_inside2.Add(self.m_panel_run1_file2, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check2 = wx.Panel(
            sbSizer_run12.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(70, -1),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_run1_check2.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check2.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run3 = wx.CheckBox(
            self.m_panel_run1_check2,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        bSizer_run1_check2.Add(self.m_checkBox_run3, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check2.SetSizer(bSizer_run1_check2)
        self.m_panel_run1_check2.Layout()
        bSizer_run1_inside2.Add(self.m_panel_run1_check2, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run12.Add(bSizer_run1_inside2, 1, wx.EXPAND, 1)

        self.m_panel_upload3.SetSizer(sbSizer_run12)
        self.m_panel_upload3.Layout()
        sbSizer_run12.Fit(self.m_panel_upload3)
        bSizer_left.Add(self.m_panel_upload3, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload4 = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer_run13 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_upload4, wx.ID_ANY, u"Run 4"), wx.VERTICAL
        )

        bSizer_run1_inside3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file3 = wx.Panel(
            sbSizer_run13.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer243 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel393 = wx.Panel(
            self.m_panel_run1_file3,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer274 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run41 = wx.FilePickerCtrl(
            self.m_panel393,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run41.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run41.SetMaxSize(wx.Size(600, -1))

        bSizer274.Add(self.m_filePicker_run41, 0, wx.ALL, 1)

        self.m_panel393.SetSizer(bSizer274)
        self.m_panel393.Layout()
        bSizer274.Fit(self.m_panel393)
        bSizer243.Add(self.m_panel393, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel403 = wx.Panel(
            self.m_panel_run1_file3,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer2713 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run42 = wx.FilePickerCtrl(
            self.m_panel403,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run42.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run42.SetMaxSize(wx.Size(600, -1))

        bSizer2713.Add(self.m_filePicker_run42, 0, wx.ALL, 1)

        self.m_panel403.SetSizer(bSizer2713)
        self.m_panel403.Layout()
        bSizer2713.Fit(self.m_panel403)
        bSizer243.Add(self.m_panel403, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file3.SetSizer(bSizer243)
        self.m_panel_run1_file3.Layout()
        bSizer243.Fit(self.m_panel_run1_file3)
        bSizer_run1_inside3.Add(self.m_panel_run1_file3, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check3 = wx.Panel(
            sbSizer_run13.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(70, -1),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_run1_check3.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check3.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run4 = wx.CheckBox(
            self.m_panel_run1_check3,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        bSizer_run1_check3.Add(self.m_checkBox_run4, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check3.SetSizer(bSizer_run1_check3)
        self.m_panel_run1_check3.Layout()
        bSizer_run1_inside3.Add(self.m_panel_run1_check3, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run13.Add(bSizer_run1_inside3, 1, wx.EXPAND, 1)

        self.m_panel_upload4.SetSizer(sbSizer_run13)
        self.m_panel_upload4.Layout()
        sbSizer_run13.Fit(self.m_panel_upload4)
        bSizer_left.Add(self.m_panel_upload4, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload5 = wx.Panel(
            self.m_panel_left,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer_run14 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_upload5, wx.ID_ANY, u"Run 5"), wx.VERTICAL
        )

        bSizer_run1_inside4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file4 = wx.Panel(
            sbSizer_run14.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer244 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel394 = wx.Panel(
            self.m_panel_run1_file4,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer275 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run51 = wx.FilePickerCtrl(
            self.m_panel394,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run51.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run51.SetMaxSize(wx.Size(600, -1))

        bSizer275.Add(self.m_filePicker_run51, 0, wx.ALL, 1)

        self.m_panel394.SetSizer(bSizer275)
        self.m_panel394.Layout()
        bSizer275.Fit(self.m_panel394)
        bSizer244.Add(self.m_panel394, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel404 = wx.Panel(
            self.m_panel_run1_file4,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer2714 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run52 = wx.FilePickerCtrl(
            self.m_panel404,
            wx.ID_ANY,
            wx.EmptyString,
            u"Select a file",
            u"*.csv",
            wx.DefaultPosition,
            wx.Size(600, -1),
            wx.FLP_DEFAULT_STYLE,
        )
        self.m_filePicker_run52.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run52.SetMaxSize(wx.Size(600, -1))

        bSizer2714.Add(self.m_filePicker_run52, 0, wx.ALL, 1)

        self.m_panel404.SetSizer(bSizer2714)
        self.m_panel404.Layout()
        bSizer2714.Fit(self.m_panel404)
        bSizer244.Add(self.m_panel404, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file4.SetSizer(bSizer244)
        self.m_panel_run1_file4.Layout()
        bSizer244.Fit(self.m_panel_run1_file4)
        bSizer_run1_inside4.Add(self.m_panel_run1_file4, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check4 = wx.Panel(
            sbSizer_run14.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(70, -1),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_run1_check4.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check4.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run5 = wx.CheckBox(
            self.m_panel_run1_check4,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        bSizer_run1_check4.Add(self.m_checkBox_run5, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check4.SetSizer(bSizer_run1_check4)
        self.m_panel_run1_check4.Layout()
        bSizer_run1_inside4.Add(self.m_panel_run1_check4, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run14.Add(bSizer_run1_inside4, 1, wx.EXPAND, 1)

        self.m_panel_upload5.SetSizer(sbSizer_run14)
        self.m_panel_upload5.Layout()
        sbSizer_run14.Fit(self.m_panel_upload5)
        bSizer_left.Add(self.m_panel_upload5, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_left.SetSizer(bSizer_left)
        self.m_panel_left.Layout()
        bSizer_main.Add(self.m_panel_left, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_right = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, -1), wx.TAB_TRAVERSAL
        )
        self.m_panel_right.SetMinSize(wx.Size(400, -1))
        self.m_panel_right.SetMaxSize(wx.Size(400, -1))

        bSizer_right = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_job_no = wx.Panel(
            self.m_panel_right,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 40),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_job_no.SetMinSize(wx.Size(-1, 40))
        self.m_panel_job_no.SetMaxSize(wx.Size(-1, 40))

        bSizer57 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_job_no = wx.StaticText(
            self.m_panel_job_no,
            wx.ID_ANY,
            u"  Job number",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText_job_no.Wrap(-1)

        bSizer57.Add(self.m_staticText_job_no, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.m_textCtrl_job_no = wx.TextCtrl(
            self.m_panel_job_no,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(200, -1),
        )
        self.m_textCtrl_job_no.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_job_no.SetMaxSize(wx.Size(200, -1))

        bSizer57.Add(self.m_textCtrl_job_no, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.m_button_job = wx.Button(
            self.m_panel_job_no,
            wx.ID_ANY,
            u"Generate",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer57.Add(self.m_button_job, 0, wx.ALL, 5)

        self.m_panel_job_no.SetSizer(bSizer57)
        self.m_panel_job_no.Layout()
        bSizer_right.Add(self.m_panel_job_no, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_equip_info = wx.Panel(
            self.m_panel_right,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 210),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_equip_info.SetMinSize(wx.Size(-1, 210))
        self.m_panel_equip_info.SetMaxSize(wx.Size(-1, 210))

        sbSizer11 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_equip_info, wx.ID_ANY, u"Equipment Information"),
            wx.VERTICAL,
        )

        self.m_panel65 = wx.Panel(
            sbSizer11.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer58 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(
            self.m_panel65,
            wx.ID_ANY,
            u"Chamber 1",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText6.Wrap(-1)

        bSizer58.Add(self.m_staticText6, 0, wx.ALL, 1)

        self.m_panel68 = wx.Panel(
            self.m_panel65,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer59 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(
            self.m_panel68,
            wx.ID_ANY,
            u"       Model",
            wx.DefaultPosition,
            wx.Size(100, -1),
            0,
        )
        self.m_staticText7.Wrap(-1)

        self.m_staticText7.SetMinSize(wx.Size(100, -1))
        self.m_staticText7.SetMaxSize(wx.Size(100, -1))

        bSizer59.Add(self.m_staticText7, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_model1 = wx.TextCtrl(
            self.m_panel68,
            wx.ID_ANY,
            wx.EmptyString,
            wx.Point(-1, -1),
            wx.Size(200, -1),
            wx.TE_READONLY,
        )
        self.m_textCtrl_model1.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_model1.SetMaxSize(wx.Size(200, -1))

        bSizer59.Add(self.m_textCtrl_model1, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel68.SetSizer(bSizer59)
        self.m_panel68.Layout()
        bSizer59.Fit(self.m_panel68)
        bSizer58.Add(self.m_panel68, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel69 = wx.Panel(
            self.m_panel65,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer591 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText71 = wx.StaticText(
            self.m_panel69,
            wx.ID_ANY,
            u"       Serial  ",
            wx.DefaultPosition,
            wx.Size(100, -1),
            0,
        )
        self.m_staticText71.Wrap(-1)

        self.m_staticText71.SetMinSize(wx.Size(100, -1))
        self.m_staticText71.SetMaxSize(wx.Size(100, -1))

        bSizer591.Add(self.m_staticText71, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_serial1 = wx.TextCtrl(
            self.m_panel69,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(200, -1),
            wx.TE_READONLY,
        )
        self.m_textCtrl_serial1.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_serial1.SetMaxSize(wx.Size(200, -1))

        bSizer591.Add(self.m_textCtrl_serial1, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_panel69.SetSizer(bSizer591)
        self.m_panel69.Layout()
        bSizer591.Fit(self.m_panel69)
        bSizer58.Add(self.m_panel69, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel65.SetSizer(bSizer58)
        self.m_panel65.Layout()
        bSizer58.Fit(self.m_panel65)
        sbSizer11.Add(self.m_panel65, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel66 = wx.Panel(
            sbSizer11.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer581 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText61 = wx.StaticText(
            self.m_panel66,
            wx.ID_ANY,
            u"Chamber 2",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText61.Wrap(-1)

        bSizer581.Add(self.m_staticText61, 0, wx.ALL, 1)

        self.m_panel681 = wx.Panel(
            self.m_panel66,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer592 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText72 = wx.StaticText(
            self.m_panel681,
            wx.ID_ANY,
            u"       Model",
            wx.DefaultPosition,
            wx.Size(100, -1),
            0,
        )
        self.m_staticText72.Wrap(-1)

        self.m_staticText72.SetMinSize(wx.Size(100, -1))
        self.m_staticText72.SetMaxSize(wx.Size(100, -1))

        bSizer592.Add(self.m_staticText72, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_model2 = wx.TextCtrl(
            self.m_panel681,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(200, -1),
            wx.TE_READONLY,
        )
        self.m_textCtrl_model2.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_model2.SetMaxSize(wx.Size(200, -1))

        bSizer592.Add(self.m_textCtrl_model2, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel681.SetSizer(bSizer592)
        self.m_panel681.Layout()
        bSizer592.Fit(self.m_panel681)
        bSizer581.Add(self.m_panel681, 1, wx.EXPAND | wx.ALL, 2)

        self.m_panel66.SetSizer(bSizer581)
        self.m_panel66.Layout()
        bSizer581.Fit(self.m_panel66)
        sbSizer11.Add(self.m_panel66, 1, wx.EXPAND | wx.ALL, 5)

        self.m_button_read = wx.Button(
            sbSizer11.GetStaticBox(),
            wx.ID_ANY,
            u"Read Information",
            wx.DefaultPosition,
            wx.Size(300, 25),
            0,
        )
        self.m_button_read.SetMinSize(wx.Size(300, 25))
        self.m_button_read.SetMaxSize(wx.Size(300, 25))

        sbSizer11.Add(self.m_button_read, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.read, self.m_button_read)

        self.m_panel_equip_info.SetSizer(sbSizer11)
        self.m_panel_equip_info.Layout()
        sbSizer11.Fit(self.m_panel_equip_info)
        bSizer_right.Add(self.m_panel_equip_info, 1, wx.EXPAND | wx.ALL, 10)

        self.m_panel_client_info = wx.Panel(
            self.m_panel_right,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 200),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel_client_info.SetMinSize(wx.Size(-1, 200))
        self.m_panel_client_info.SetMaxSize(wx.Size(-1, 200))

        sbSizer12 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel_client_info, wx.ID_ANY, u"Client Information"),
            wx.VERTICAL,
        )

        bSizer44 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel74 = wx.Panel(
            sbSizer12.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 50),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel74.SetMinSize(wx.Size(-1, 50))
        self.m_panel74.SetMaxSize(wx.Size(-1, 50))

        bSizer71 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText21 = wx.StaticText(
            self.m_panel74,
            wx.ID_ANY,
            u"Client Name",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText21.Wrap(-1)

        bSizer71.Add(self.m_staticText21, 0, wx.ALL, 2)

        self.m_textCtrl_client_name = wx.TextCtrl(
            self.m_panel74,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(170, -1),
            0,
        )
        self.m_textCtrl_client_name.SetMinSize(wx.Size(170, -1))
        self.m_textCtrl_client_name.SetMaxSize(wx.Size(170, -1))

        bSizer71.Add(self.m_textCtrl_client_name, 0, wx.ALL, 2)

        self.m_panel74.SetSizer(bSizer71)
        self.m_panel74.Layout()
        bSizer44.Add(self.m_panel74, 1, wx.ALL, 1)

        self.m_panel741 = wx.Panel(
            sbSizer12.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 50),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel741.SetMinSize(wx.Size(-1, 50))
        self.m_panel741.SetMaxSize(wx.Size(-1, 50))

        bSizer712 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText212 = wx.StaticText(
            self.m_panel741,
            wx.ID_ANY,
            u"Operator",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText212.Wrap(-1)

        bSizer712.Add(self.m_staticText212, 0, wx.ALL, 2)

        self.m_textCtrl_operator = wx.TextCtrl(
            self.m_panel741,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(170, -1),
            0,
        )
        self.m_textCtrl_operator.SetMinSize(wx.Size(170, -1))
        self.m_textCtrl_operator.SetMaxSize(wx.Size(170, -1))

        bSizer712.Add(self.m_textCtrl_operator, 0, wx.ALL, 2)

        self.m_panel741.SetSizer(bSizer712)
        self.m_panel741.Layout()
        bSizer44.Add(self.m_panel741, 1, wx.ALL, 1)

        sbSizer12.Add(bSizer44, 1, wx.EXPAND, 0)

        self.m_panel75 = wx.Panel(
            sbSizer12.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 100),
            wx.TAB_TRAVERSAL,
        )
        self.m_panel75.SetMinSize(wx.Size(-1, 100))
        self.m_panel75.SetMaxSize(wx.Size(-1, 100))

        bSizer711 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText211 = wx.StaticText(
            self.m_panel75,
            wx.ID_ANY,
            u"Client Address",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText211.Wrap(-1)

        bSizer711.Add(self.m_staticText211, 0, wx.ALL, 1)

        self.m_textCtrl_client_address1 = wx.TextCtrl(
            self.m_panel75,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(350, -1),
            0,
        )
        self.m_textCtrl_client_address1.SetMinSize(wx.Size(350, -1))
        self.m_textCtrl_client_address1.SetMaxSize(wx.Size(350, -1))

        bSizer711.Add(self.m_textCtrl_client_address1, 0, wx.ALL, 2)

        self.m_textCtrl_client_address2 = wx.TextCtrl(
            self.m_panel75,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(350, -1),
            0,
        )
        self.m_textCtrl_client_address2.SetMinSize(wx.Size(350, -1))
        self.m_textCtrl_client_address2.SetMaxSize(wx.Size(350, -1))

        bSizer711.Add(self.m_textCtrl_client_address2, 0, wx.ALL, 2)

        self.m_panel75.SetSizer(bSizer711)
        self.m_panel75.Layout()
        sbSizer12.Add(self.m_panel75, 1, wx.EXPAND | wx.ALL, 2)

        self.m_button_update = wx.Button(
            sbSizer12.GetStaticBox(),
            wx.ID_ANY,
            u"Update Information",
            wx.DefaultPosition,
            wx.Size(300, 25),
            0,
        )
        self.m_button_update.SetMinSize(wx.Size(300, 25))
        self.m_button_update.SetMaxSize(wx.Size(300, 25))

        sbSizer12.Add(self.m_button_update, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.update_info, self.m_button_update)

        self.m_panel_client_info.SetSizer(sbSizer12)
        self.m_panel_client_info.Layout()
        bSizer_right.Add(self.m_panel_client_info, 1, wx.EXPAND | wx.ALL, 10)

        self.m_panel_pdf_dcc = wx.Panel(
            self.m_panel_right,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            wx.TAB_TRAVERSAL,
        )
        bSizer81 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_upload = wx.Button(
            self.m_panel_pdf_dcc,
            wx.ID_ANY,
            u"Upload Data",
            wx.DefaultPosition,
            wx.Size(200, 30),
            0,
        )
        self.m_button_upload.SetMinSize(wx.Size(200, 30))
        self.m_button_upload.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_upload, 0, wx.ALIGN_CENTER | wx.ALL, 4)
        self.Bind(wx.EVT_BUTTON, self.upload_csv, self.m_button_upload)

        self.m_button_download = wx.Button(
            self.m_panel_pdf_dcc,
            wx.ID_ANY,
            u"Download Data",
            wx.DefaultPosition,
            wx.Size(200, 30),
            0,
        )
        self.m_button_download.SetMinSize(wx.Size(200, 30))
        self.m_button_download.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_download, 0, wx.ALIGN_CENTER | wx.ALL, 4)
        self.Bind(wx.EVT_BUTTON, self.download_csv, self.m_button_download)

        self.m_button_pdf = wx.Button(
            self.m_panel_pdf_dcc,
            wx.ID_ANY,
            u"Generate PDF",
            wx.DefaultPosition,
            wx.Size(200, 30),
            0,
        )
        self.m_button_pdf.SetMinSize(wx.Size(200, 30))
        self.m_button_pdf.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_pdf, 0, wx.ALIGN_CENTER | wx.ALL, 4)

        self.m_button_dcc = wx.Button(
            self.m_panel_pdf_dcc,
            wx.ID_ANY,
            u"Generate DCC",
            wx.DefaultPosition,
            wx.Size(200, 30),
            0,
        )
        self.m_button_dcc.SetMinSize(wx.Size(200, 30))
        self.m_button_dcc.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_dcc, 0, wx.ALIGN_CENTER | wx.ALL, 4)

        self.m_panel_pdf_dcc.SetSizer(bSizer81)
        self.m_panel_pdf_dcc.Layout()
        bSizer81.Fit(self.m_panel_pdf_dcc)
        bSizer_right.Add(self.m_panel_pdf_dcc, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_right.SetSizer(bSizer_right)
        self.m_panel_right.Layout()
        bSizer_main.Add(self.m_panel_right, 1, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # reset confirm bind
        self.m_filePicker_run11.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run11
        )
        self.m_filePicker_run12.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run12
        )
        self.m_filePicker_run21.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run21
        )
        self.m_filePicker_run22.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run22
        )
        self.m_filePicker_run31.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run31
        )
        self.m_filePicker_run32.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run32
        )
        self.m_filePicker_run41.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run41
        )
        self.m_filePicker_run42.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run42
        )
        self.m_filePicker_run51.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run51
        )
        self.m_filePicker_run52.Bind(
            wx.EVT_FILEPICKER_CHANGED, self.resetConfirm, self.m_filePicker_run52
        )

    def compare(self, event):
        MainFrame.m_progress_bar.SetValue(0)
        # set global value for analysis file path
        global pathClient
        global pathLab
        global selected_run

        pathClient = []
        pathLab = []
        selected_run = self.m_textCtrl_selected_run.GetValue()
        client_info = True

        for file_path in total_file_path_list:
            file = open(file_path)
            with file as f:
                reader = csv.reader(f)
                result = list(reader)
                if result[16][0] == "[DATA]":
                    client_info = False
                    break

        if self.confirmed:
            if client_info == True:
                MainFrame.m_progress_bar.SetValue(10)

                if self.m_checkBox_run1.GetValue() == True:
                    pathClient.append(self.m_filePicker_run11.GetPath())
                    pathLab.append(self.m_filePicker_run12.GetPath())
                if self.m_checkBox_run2.GetValue() == True:
                    pathClient.append(self.m_filePicker_run21.GetPath())
                    pathLab.append(self.m_filePicker_run22.GetPath())
                if self.m_checkBox_run3.GetValue() == True:
                    pathClient.append(self.m_filePicker_run31.GetPath())
                    pathLab.append(self.m_filePicker_run32.GetPath())
                if self.m_checkBox_run4.GetValue() == True:
                    pathClient.append(self.m_filePicker_run41.GetPath())
                    pathLab.append(self.m_filePicker_run42.GetPath())
                if self.m_checkBox_run5.GetValue() == True:
                    pathClient.append(self.m_filePicker_run51.GetPath())
                    pathLab.append(self.m_filePicker_run52.GetPath())

                MainFrame.m_progress_bar.SetValue(20)
                frame = GraphFrame()
                frame.Show()

                MainFrame.m_progress_bar.SetValue(100)
            else:
                dlg = wx.MessageDialog(
                    None,
                    u"Please complete the client information in all files!",
                    u"Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()

        else:
            dlg = wx.MessageDialog(
                None,
                u"Please confirm your data files!",
                u"Not confirmed",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()

    def confirm(self, event):

        self.resetConfirm(event)
        MainFrame.m_progress_bar.SetValue(0)
        self.m_textCtrl_selected_run.SetValue("0")
        self.m_textCtrl_total_run.SetValue("0")

        global total_file_path_list

        selected_run_num = 0
        total_run_num = 0
        total_file_path_list = []
        client_file_path_list = []
        lab_file_path_list = []
        client_chamber = []
        lab_chamber = []
        client_name = []
        address_1 = []
        address_2 = []
        operator = []
        CAL_Number = []
        chamber_flag = True
        client_info_flag = True

        # check if user selects a box
        if (
            self.m_checkBox_run1.GetValue()
            == self.m_checkBox_run2.GetValue()
            == self.m_checkBox_run3.GetValue()
            == self.m_checkBox_run4.GetValue()
            == self.m_checkBox_run5.GetValue()
            == False
        ):
            dlg = wx.MessageDialog(
                None,
                u"Please select the checkbox you need!",
                u"No selected checkbox",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return

        # if pair of path not empty -> total run + 1
        # + if check box -> selected run + 1
        if self.m_checkBox_run1.GetValue():
            selected_run_num += 1
        if (
            self.m_filePicker_run11.GetPath() != ""
            or self.m_filePicker_run12.GetPath() != ""
        ):
            total_run_num += 1
        # if there is a file is empty, alert
        if self.m_checkBox_run1.GetValue():
            if (
                self.m_filePicker_run11.GetPath() == ""
                or self.m_filePicker_run12.GetPath() == ""
            ):
                dlg = wx.MessageDialog(
                    None,
                    u"Please select the file of Run 1!",
                    u"File Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()
                return
            else:
                client_file_path_list.append(self.m_filePicker_run11.GetPath())
                lab_file_path_list.append(self.m_filePicker_run12.GetPath())

        if self.m_checkBox_run2.GetValue():
            selected_run_num += 1
        if (
            self.m_filePicker_run21.GetPath() != ""
            or self.m_filePicker_run22.GetPath() != ""
        ):
            total_run_num += 1
        if self.m_checkBox_run2.GetValue():
            if (
                self.m_filePicker_run21.GetPath() == ""
                or self.m_filePicker_run22.GetPath() == ""
            ):
                dlg = wx.MessageDialog(
                    None,
                    u"Please select the file of Run 2!",
                    u"File Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()
                return
            else:
                client_file_path_list.append(self.m_filePicker_run21.GetPath())
                lab_file_path_list.append(self.m_filePicker_run22.GetPath())

        if self.m_checkBox_run3.GetValue():
            selected_run_num += 1
        if (
            self.m_filePicker_run31.GetPath() != ""
            or self.m_filePicker_run32.GetPath() != ""
        ):
            total_run_num += 1
        if self.m_checkBox_run3.GetValue():
            if (
                self.m_filePicker_run31.GetPath() == ""
                or self.m_filePicker_run32.GetPath() == ""
            ):
                dlg = wx.MessageDialog(
                    None,
                    u"Please select the file of Run 3!",
                    u"File Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()
                return
            else:
                client_file_path_list.append(self.m_filePicker_run31.GetPath())
                lab_file_path_list.append(self.m_filePicker_run32.GetPath())

        if self.m_checkBox_run4.GetValue():
            selected_run_num += 1
        if (
            self.m_filePicker_run41.GetPath() != ""
            or self.m_filePicker_run42.GetPath() != ""
        ):
            total_run_num += 1
        if self.m_checkBox_run4.GetValue():
            if (
                self.m_filePicker_run41.GetPath() == ""
                or self.m_filePicker_run42.GetPath() == ""
            ):
                dlg = wx.MessageDialog(
                    None,
                    u"Please select the file of Run 4!",
                    u"File Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()
                return
            else:
                client_file_path_list.append(self.m_filePicker_run41.GetPath())
                lab_file_path_list.append(self.m_filePicker_run42.GetPath())

        if self.m_checkBox_run5.GetValue():
            selected_run_num += 1
        if (
            self.m_filePicker_run51.GetPath() != ""
            or self.m_filePicker_run52.GetPath() != ""
        ):
            total_run_num += 1
        if self.m_checkBox_run5.GetValue():
            if (
                self.m_filePicker_run51.GetPath() == ""
                or self.m_filePicker_run52.GetPath() == ""
            ):
                dlg = wx.MessageDialog(
                    None,
                    u"Please select the file of Run 5!",
                    u"File Incomplete",
                    wx.YES_DEFAULT | wx.ICON_WARNING,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    dlg.Destroy()
                return
            else:
                client_file_path_list.append(self.m_filePicker_run51.GetPath())
                lab_file_path_list.append(self.m_filePicker_run52.GetPath())

        # check data structure
        total_file_path_list = client_file_path_list + lab_file_path_list
        for file_path in total_file_path_list:
            file = open(file_path)
            with file as f:
                reader = csv.reader(f)
                result = list(reader)
                label_row1 = result[17]  # get line 18
                label_row2 = result[22]  # get line 23
                header = result[:16]  # get first 16 lines
                label_column = []
                # validate row
                standard_row = [
                    "kV",
                    "mA",
                    "BarCode",
                    "XraysOn",
                    "HVLFilter(mm)",
                    "Filter",
                    "FilterReady",
                    "HVLReady",
                    "N",
                    "Current1(pA)",
                    "Current2(pA)",
                    "P(kPa)",
                    "T(MC)",
                    "T(Air)",
                    "T(SC)",
                    "H(%)",
                    "Comment",
                ]

                # validate column
                standard_column = [
                    "[COMET X-RAY MEASUREMENT]",
                    "Filename",
                    "Date",
                    "Chamber",
                    "Description",
                    "Software",
                    "Backgrounds",
                    "Measurements",
                    "Trolley (mm)",
                    "SCD (mm)",
                    "Aperture wheel",
                    "Comment",
                    "Monitor electrometer range",
                    "Monitor HV",
                    "MEFAC-IC electrometer range",
                    "IC HV",
                ]
                for i in header:
                    label_column.append(i[0])

                if (
                    standard_row != label_row1 and standard_row != label_row2
                ) or standard_column != label_column:
                    dlg = wx.MessageDialog(
                        None,
                        u"The file: " + file_path + " data structure is not valid!",
                        u"File Error",
                        wx.YES_DEFAULT | wx.ICON_WARNING,
                    )
                    if dlg.ShowModal() == wx.ID_YES:
                        dlg.Destroy()
                    return
            file.close()

        # check whether client information and chamber ID are same in all files
        for file_path in client_file_path_list:
            file = open(file_path)
            with file as f:
                reader = csv.reader(f)
                result = list(reader)
                Chamber_row = result[3]  # get line 4
                client_chamber.append(Chamber_row[2].replace(" ", ""))
                if result[21][0] == "[DATA]":
                    client_name_row = result[16]  # get line 17
                    client_name.append(client_name_row[2])
                    address_1_row = result[17]
                    address_1.append(address_1_row[2])
                    address_2_row = result[18]
                    address_2.append(address_2_row[2])
                    operator_row = result[19]
                    operator.append(operator_row[2])
                    CAL_Number_row = result[20]
                    CAL_Number.append(CAL_Number_row[2])

        for file_path in lab_file_path_list:
            file = open(file_path)
            with file as f:
                reader = csv.reader(f)
                result = list(reader)
                Chamber_row = result[3]  # get line 4
                lab_chamber.append(Chamber_row[2].replace(" ", ""))
                if result[21][0] == "[DATA]":
                    client_name_row = result[16]  # get line 17
                    client_name.append(client_name_row[2])
                    address_1_row = result[17]
                    address_1.append(address_1_row[2])
                    address_2_row = result[18]
                    address_2.append(address_2_row[2])
                    operator_row = result[19]
                    operator.append(operator_row[2])
                    CAL_Number_row = result[20]
                    CAL_Number.append(CAL_Number_row[2])

        for i in range(len(client_chamber)):
            if i == len(client_chamber) - 1:
                break
            if client_chamber[i] == client_chamber[i + 1]:
                continue
            else:
                chamber_flag = False
                break

        for i in range(len(lab_chamber)):
            if i == len(lab_chamber):
                break
            if lab_chamber[i] == "MEFAC":
                continue
            else:
                chamber_flag = False

        for i in range(len(client_name)):
            if len(client_name) == 0:
                break
            if i == len(client_name) - 1:
                break
            if client_name[i] == client_name[i + 1]:
                continue
            else:
                client_info_flag = False

        for i in range(len(address_1)):
            if len(address_1) == 0:
                break
            if i == len(address_1) - 1:
                break
            if address_1[i] == address_1[i + 1]:
                continue
            else:
                client_info_flag = False

        for i in range(len(address_2)):
            if len(address_2) == 0:
                break
            if i == len(address_2) - 1:
                break
            if address_2[i] == address_2[i + 1]:
                continue
            else:
                client_info_flag = False

        for i in range(len(operator)):
            if len(operator) == 0:
                break
            if i == len(operator) - 1:
                break
            if operator[i] == operator[i + 1]:
                continue
            else:
                client_info_flag = False

        for i in range(len(CAL_Number)):
            if len(CAL_Number) == 0:
                break
            if i == len(CAL_Number) - 1:
                break
            if CAL_Number[i] == CAL_Number[i + 1]:
                continue
            else:
                client_info_flag = False

        if not client_info_flag:
            dlg = wx.MessageDialog(
                None,
                u"Client information is not the same!",
                u"Client Information Error",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return

        if not chamber_flag:
            dlg = wx.MessageDialog(
                None,
                u"Chamber ID is not valid! "
                u"\nPlease check the chamber information and put file_CLIENT in field 1 and file_LAB in field 2.",
                u"Chamber ID Error",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return

        self.m_textCtrl_selected_run.SetValue(str(selected_run_num))
        self.m_textCtrl_total_run.SetValue(str(total_run_num))
        if selected_run_num > 0:
            self.confirmed = True

    def read(self, event):

        if self.confirmed:

            # reset empty
            self.m_textCtrl_job_no.SetValue("")
            self.m_textCtrl_model1.SetValue("")
            self.m_textCtrl_serial1.SetValue("")
            self.m_textCtrl_model2.SetValue("")
            self.m_textCtrl_client_name.SetValue("")
            self.m_textCtrl_operator.SetValue("")
            self.m_textCtrl_client_address1.SetValue("")
            self.m_textCtrl_client_address2.SetValue("")

            path_11 = self.m_filePicker_run11.GetPath()  # run1 client
            path_12 = self.m_filePicker_run12.GetPath()  # run1 lab
            if path_11 != "" and path_12 != "" and self.confirmed:

                # set hint
                self.m_textCtrl_job_no.SetHint("Please generate job number")
                self.m_textCtrl_client_name.SetHint("Enter client name")
                self.m_textCtrl_operator.SetHint("Enter operator name")
                self.m_textCtrl_client_address1.SetHint("Enter address line 1")
                self.m_textCtrl_client_address2.SetHint("Enter address line 2")

                # read client chamber information
                client_chamber_info_df = pd.read_csv(
                    path_11, skiprows=3, nrows=1, header=None
                )  # row 4
                client_chamber_info = client_chamber_info_df[2][0]
                tmp_list = client_chamber_info.split(" ")
                # last element is serial, rest is model
                serial_info = tmp_list[-1]
                model_info = ""
                for i in range(len(tmp_list) - 1):
                    model_info += " "
                    model_info += tmp_list[i]
                self.m_textCtrl_model1.SetValue(model_info[1:])
                self.m_textCtrl_serial1.SetValue(serial_info)

                # read lab chamber info
                lab_chamber_info_df = pd.read_csv(
                    path_12, skiprows=3, nrows=1, header=None
                )
                lab_chamber_info = lab_chamber_info_df[2][0]
                self.m_textCtrl_model2.SetValue(lab_chamber_info)

                # check where is [DATA]
                check_df = pd.read_csv(
                    path_11, skiprows=21, nrows=1, header=None
                )  # row 22
                if check_df[0][0] == "[DATA]":
                    client_info_df = pd.read_csv(
                        path_11, skiprows=16, nrows=5, header=None
                    )  # row 17-21
                    # read job number
                    job_no = client_info_df[2][4]  # col3 row5
                    job_no = re.sub("[^0-9]", "", str(job_no))
                    self.m_textCtrl_job_no.SetValue(job_no)

                    # read client info
                    client_name = client_info_df[2][0]
                    client_address1 = client_info_df[2][1]
                    client_address2 = client_info_df[2][2]
                    operator_name = client_info_df[2][3]
                    self.m_textCtrl_client_name.SetValue(client_name)
                    self.m_textCtrl_operator.SetValue(operator_name)
                    self.m_textCtrl_client_address1.SetValue(client_address1)
                    self.m_textCtrl_client_address2.SetValue(client_address2)

                self.readed = True
        else:
            dlg = wx.MessageDialog(
                None,
                u"Please confirm your data files!",
                u"Not confirmed",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()

    def update_info(self, event):

        if self.confirmed and self.readed:

            path_client_lst = []
            path_lab_lst = []
            path_client_lst.append(self.m_filePicker_run11.GetPath())
            path_client_lst.append(self.m_filePicker_run21.GetPath())
            path_client_lst.append(self.m_filePicker_run31.GetPath())
            path_client_lst.append(self.m_filePicker_run41.GetPath())
            path_client_lst.append(self.m_filePicker_run51.GetPath())
            path_lab_lst.append(self.m_filePicker_run12.GetPath())
            path_lab_lst.append(self.m_filePicker_run22.GetPath())
            path_lab_lst.append(self.m_filePicker_run32.GetPath())
            path_lab_lst.append(self.m_filePicker_run42.GetPath())
            path_lab_lst.append(self.m_filePicker_run52.GetPath())

            updated_client_name = self.m_textCtrl_client_name.GetValue()
            updated_operator_name = self.m_textCtrl_operator.GetValue()
            updated_address1 = self.m_textCtrl_client_address1.GetValue()
            updated_address2 = self.m_textCtrl_client_address2.GetValue()
            client_name = ["Client name", "", updated_client_name]
            address1 = ["Address 1", "", updated_address1]
            address2 = ["Address 2", "", updated_address2]
            oper = ["Operator", "", updated_operator_name]
            CAL = ["CAL Number", "", ""]

            for i in range(len(path_client_lst)):
                path_client = path_client_lst[i]
                path_lab = path_lab_lst[i]
                if path_client != "" and path_lab != "":
                    check_df = pd.read_csv(
                        path_client, skiprows=16, nrows=1, header=None
                    )  # row 17
                    # there is no client information, add new rows for client information
                    if check_df[0][0] == "[DATA]":
                        line = []
                        # reading the csv file
                        with open(path_client, "rt") as f:
                            data = csv.reader(f)
                            for row in data:
                                line.append(row)

                        # rewrite rows
                        with open(path_client, "w", newline="") as f:
                            writer = csv.writer(f)
                            i = 0
                            for row in line:
                                if i == 16:
                                    writer.writerow(client_name)
                                    writer.writerow(address1)
                                    writer.writerow(address2)
                                    writer.writerow(oper)
                                    writer.writerow(CAL)
                                    i = i + 5
                                writer.writerow(row)
                                i += 1
                            f.close()
                    # there already client information exist, change data
                    if check_df[0][0] != "[DATA]":
                        line = []
                        # reading the csv file
                        with open(path_client, "rt") as f:
                            data = csv.reader(f)
                            for row in data:
                                line.append(row)

                        # updating the column value/data
                        line[16][2] = updated_client_name
                        line[17][2] = updated_address1
                        line[18][2] = updated_address2
                        line[19][2] = updated_operator_name

                        # writing into the file
                        with open(path_client, "w", newline="") as f:
                            writer = csv.writer(f)
                            for row in line:
                                writer.writerow(row)

                    check_df = pd.read_csv(
                        path_lab, skiprows=16, nrows=1, header=None
                    )  # row 17
                    # there is no client information, add new rows for client information
                    if check_df[0][0] == "[DATA]":
                        line = []
                        # reading the csv file
                        with open(path_lab, "rt") as f:
                            data = csv.reader(f)
                            for row in data:
                                line.append(row)

                        # rewrite rows
                        with open(path_lab, "w", newline="") as f:
                            writer = csv.writer(f)
                            i = 0
                            for row in line:
                                if i == 16:
                                    writer.writerow(client_name)
                                    writer.writerow(address1)
                                    writer.writerow(address2)
                                    writer.writerow(oper)
                                    writer.writerow(CAL)
                                    i = i + 5
                                writer.writerow(row)
                                i += 1
                            f.close()
                    # there already client information exist, change data
                    if check_df[0][0] != "[DATA]":
                        line = []
                        # reading the csv file
                        with open(path_lab, "rt") as f:
                            data = csv.reader(f)
                            for row in data:
                                line.append(row)

                        # updating the column value/data
                        line[16][2] = updated_client_name
                        line[17][2] = updated_address1
                        line[18][2] = updated_address2
                        line[19][2] = updated_operator_name

                        # writing into the file
                        with open(path_lab, "w", newline="") as f:
                            writer = csv.writer(f)
                            for row in line:
                                writer.writerow(row)
            dlg = wx.MessageDialog(
                None,
                u"Successfully updated client information!",
                u"Successfully updated",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
        elif not self.confirmed:
            dlg = wx.MessageDialog(
                None,
                u"Please confirm your data files!",
                u"Not confirmed",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return
        elif not self.readed:
            dlg = wx.MessageDialog(
                None,
                u"Please read your data files!",
                u"Not read",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return

    def resetConfirm(self, event):
        self.confirmed = False
        self.readed = False

    def upload_csv(self, event):
        global pathClient
        global pathLab
        progress = 0
        MainFrame.m_progress_bar.SetValue(progress)
        pathClient = []
        pathLab = []

        # key in your DataBase password
        db = pymysql.connect(
            host="localhost", user="root", password="password", database="bluering"
        )

        cursor = db.cursor()
        if self.confirmed and self.readed:
            # path_11 = self.m_filePicker_run11.GetPath()  # run1 client
            # path_12 = self.m_filePicker_run12.GetPath()  # run1 lab

            if self.m_checkBox_run1.GetValue():
                pathClient.append(self.m_filePicker_run11.GetPath())
                pathLab.append(self.m_filePicker_run12.GetPath())
            if self.m_checkBox_run2.GetValue():
                pathClient.append(self.m_filePicker_run21.GetPath())
                pathLab.append(self.m_filePicker_run22.GetPath())
            if self.m_checkBox_run3.GetValue():
                pathClient.append(self.m_filePicker_run31.GetPath())
                pathLab.append(self.m_filePicker_run32.GetPath())
            if self.m_checkBox_run4.GetValue():
                pathClient.append(self.m_filePicker_run41.GetPath())
                pathLab.append(self.m_filePicker_run42.GetPath())
            if self.m_checkBox_run5.GetValue():
                pathClient.append(self.m_filePicker_run51.GetPath())
                pathLab.append(self.m_filePicker_run52.GetPath())

            for pathClient1, pathLab1 in zip(pathClient, pathLab):
                # store run11(Client) file
                csv_file_name = pathClient1
                df = pd.read_csv(csv_file_name, encoding="raw_unicode_escape")

                chamber = df.iloc[2][2]

                sql = "SELECT chamber FROM header WHERE chamber = '%s'" % (chamber)

                cursor.execute(sql)
                results = cursor.fetchall()

                if results != ():
                    # print("This chamber have been already stored in database!")
                    dlg = wx.MessageDialog(
                        None,
                        u"The chamber ID has been already exist in database",
                        u"repeat chamber ID",
                        wx.YES_DEFAULT | wx.ICON_WARNING,
                    )
                    if dlg.ShowModal() == wx.ID_YES:
                        dlg.Destroy()
                elif df.iloc[15][0] == "[DATA]":
                    filename = df.iloc[0][2]
                    date = df.iloc[1][2]
                    chamber = df.iloc[2][2]
                    chamber2 = chamber.split()
                    model = " "
                    model = model.join(chamber2[:-1])
                    serial = chamber2[-1]
                    description = df.iloc[3][2]
                    software = df.iloc[4][2]
                    backgrounds = df.iloc[5][2]
                    measurements = df.iloc[6][2]
                    trolley = df.iloc[7][2]
                    sCD = df.iloc[8][2]
                    aperture_wheel = df.iloc[9][2]
                    comment = df.iloc[10][2]
                    monitorelectrometerrange = df.iloc[11][2]
                    monitor_hv = df.iloc[12][2]
                    mEFAC_ICElectrometerRange = df.iloc[13][2]
                    ic_hv = df.iloc[14][2]
                    sql = (
                        "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                        % (
                            filename,
                            date,
                            chamber,
                            model,
                            serial,
                            description,
                            software,
                            backgrounds,
                            measurements,
                            trolley,
                            sCD,
                            aperture_wheel,
                            comment,
                            monitorelectrometerrange,
                            monitor_hv,
                            mEFAC_ICElectrometerRange,
                            ic_hv
                        )
                    )
                    # excute sql
                    cursor.execute(sql)
                    # commit to database
                    db.commit()

                    df2 = pd.read_csv(
                        csv_file_name, encoding="raw_unicode_escape", skiprows=17
                    )
                    for i in range(len(df2)):
                        kV = df2.iloc[i]["kV"]
                        mA = df2.iloc[i]["mA"]
                        barCode = df2.iloc[i]["BarCode"]
                        xraysOn = df2.iloc[i]["XraysOn"]
                        hVLFilter = df2.iloc[i]["HVLFilter(mm)"]
                        filter = df2.iloc[i]["Filter"]
                        filter_Ready = df2.iloc[i]["FilterReady"]
                        hVLReady = df2.iloc[i]["HVLReady"]
                        n = df2.iloc[i]["N"]
                        current1 = df2.iloc[i]["Current1(pA)"]
                        current2 = df2.iloc[i]["Current2(pA)"]
                        p = df2.iloc[i]["P(kPa)"]
                        t_MC = df2.iloc[i]["T(MC)"]
                        t_Air = df2.iloc[i]["T(Air)"]
                        t_SC = df2.iloc[i]["T(SC)"]
                        h = df2.iloc[i]["H(%)"]
                        sql = (
                            "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                            % (
                                filename,
                                chamber,
                                kV,
                                mA,
                                barCode,
                                xraysOn,
                                hVLFilter,
                                filter,
                                filter_Ready,
                                hVLReady,
                                n,
                                current1,
                                current2,
                                p,
                                t_MC,
                                t_Air,
                                t_SC,
                                h
                            )
                        )
                        try:
                            # excute sql
                            cursor.execute(sql)
                            # commit to database
                            db.commit()
                            print("processing...")
                        except:
                            # if fail rollback
                            db.rollback()
                            print("fail")

                elif df.iloc[20][0] == "[DATA]":
                    #print("elif")
                    filename = df.iloc[0][2]
                    date = df.iloc[1][2]
                    chamber = df.iloc[2][2]
                    chamber2 = chamber.split()
                    model = " "
                    model = model.join(chamber2[:-1])
                    serial = chamber2[-1]
                    description = df.iloc[3][2]
                    software = df.iloc[4][2]
                    backgrounds = df.iloc[5][2]
                    measurements = df.iloc[6][2]
                    trolley = int(df.iloc[7][2])
                    sCD = int(df.iloc[8][2])
                    aperture_wheel = df.iloc[9][2]
                    comment = df.iloc[10][2]
                    monitorelectrometerrange = df.iloc[11][2]
                    monitor_hv = df.iloc[12][2]
                    mEFAC_ICElectrometerRange = df.iloc[13][2]
                    ic_hv = df.iloc[14][2]
                    client_name = df.iloc[15][2]
                    address1 = df.iloc[16][2]
                    address2 = df.iloc[17][2]
                    operator = df.iloc[18][2]
                    calnumber = df.iloc[19][2]
                    sql = (
                        "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv,clientname,address1,address2,operator,calnumber) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                        % (
                            filename,
                            date,
                            chamber,
                            model,
                            serial,
                            description,
                            software,
                            backgrounds,
                            measurements,
                            trolley,
                            sCD,
                            aperture_wheel,
                            comment,
                            monitorelectrometerrange,
                            monitor_hv,
                            mEFAC_ICElectrometerRange,
                            ic_hv,
                            client_name,
                            address1,
                            address2,
                            operator,
                            calnumber
                        )
                    )
                    try:
                        # excute sql
                        cursor.execute(sql)
                        # commit to database
                        db.commit()
                    except:
                        # if fail rollback
                        db.rollback()
                        print("fail")
                    df2 = pd.read_csv(
                        csv_file_name, encoding="raw_unicode_escape", skiprows=22
                    )

                    for i in range(len(df2)):
                        kV = int(df2.iloc[i]["kV"])
                        mA = int(df2.iloc[i]["mA"])
                        barCode = df2.iloc[i]["BarCode"]
                        xraysOn = df2.iloc[i]["XraysOn"]
                        hLFilter = df2.iloc[i]["HVLFilter(mm)"]
                        filter = df2.iloc[i]["Filter"]
                        filterReady = df2.iloc[i]["FilterReady"]
                        hVLReady = df2.iloc[i]["HVLReady"]
                        n = df2.iloc[i]["N"]
                        current1 = float(df2.iloc[i]["Current1(pA)"])
                        current2 = float(df2.iloc[i]["Current2(pA)"])
                        p = float(df2.iloc[i]["P(kPa)"])
                        t_MC = float(df2.iloc[i]["T(MC)"])
                        t_Air = float(df2.iloc[i]["T(Air)"])
                        t_SC = float(df2.iloc[i]["T(SC)"])
                        h = float(df2.iloc[i]["H(%)"])
                        sql = (
                            "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                            % (
                                filename,
                                chamber,
                                kV,
                                mA,
                                barCode,
                                xraysOn,
                                hVLFilter,
                                filter,
                                filterReady,
                                hVLReady,
                                n,
                                current1,
                                current2,
                                p,
                                t_MC,
                                t_Air,
                                t_SC,
                                h
                            )
                        )
                        try:
                            # excute sql
                            cursor.execute(sql)
                            # commit to database
                            db.commit()
                            print("processing...")
                        except:
                            # if fail rollback
                            db.rollback()
                            print("fail")

                # store run12(Lab) file
                csv_file_name = pathLab1
                df = pd.read_csv(csv_file_name, encoding="raw_unicode_escape")

                chamber = df.iloc[2][2]

                sql = "SELECT chamber FROM header WHERE chamber = '%s'" % (chamber)

                cursor.execute(sql)
                results = cursor.fetchall()

                if results != ():
                    # print("This chamber have been already stored in database!")
                    dlg = wx.MessageDialog(
                        None,
                        u"The chamber ID has been already exist in database",
                        u"repeat chamber ID",
                        wx.YES_DEFAULT | wx.ICON_WARNING,
                    )
                    if dlg.ShowModal() == wx.ID_YES:
                        dlg.Destroy()
                elif df.iloc[15][0] == "[DATA]":
                    filename = df.iloc[0][2]
                    date = df.iloc[1][2]
                    chamber = df.iloc[2][2]
                    chamber2 = chamber.split()
                    model = " "
                    model = model.join(chamber2[:-1])
                    serial = chamber2[-1]
                    description = df.iloc[3][2]
                    software = df.iloc[4][2]
                    backgrounds = df.iloc[5][2]
                    measurements = df.iloc[6][2]
                    trolley = df.iloc[7][2]
                    sCD = df.iloc[8][2]
                    aperture_wheel = df.iloc[9][2]
                    comment = df.iloc[10][2]
                    monitorelectrometerrange = df.iloc[11][2]
                    monitor_hv = df.iloc[12][2]
                    mEFAC_ICElectrometerRange = df.iloc[13][2]
                    ic_hv = df.iloc[14][2]
                    sql = (
                            "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                            % (
                                filename,
                                date,
                                chamber,
                                model,
                                serial,
                                description,
                                software,
                                backgrounds,
                                measurements,
                                trolley,
                                sCD,
                                aperture_wheel,
                                comment,
                                monitorelectrometerrange,
                                monitor_hv,
                                mEFAC_ICElectrometerRange,
                                ic_hv
                            )
                    )
                    # excute sql
                    cursor.execute(sql)
                    # commit to database
                    db.commit()

                    df2 = pd.read_csv(
                        csv_file_name, encoding="raw_unicode_escape", skiprows=17
                    )
                    for i in range(len(df2)):
                        kV = df2.iloc[i]["kV"]
                        mA = df2.iloc[i]["mA"]
                        barCode = df2.iloc[i]["BarCode"]
                        xraysOn = df2.iloc[i]["XraysOn"]
                        hVLFilter = df2.iloc[i]["HVLFilter(mm)"]
                        filter = df2.iloc[i]["Filter"]
                        filter_Ready = df2.iloc[i]["FilterReady"]
                        hVLReady = df2.iloc[i]["HVLReady"]
                        n = df2.iloc[i]["N"]
                        current1 = df2.iloc[i]["Current1(pA)"]
                        current2 = df2.iloc[i]["Current2(pA)"]
                        p = df2.iloc[i]["P(kPa)"]
                        t_MC = df2.iloc[i]["T(MC)"]
                        t_Air = df2.iloc[i]["T(Air)"]
                        t_SC = df2.iloc[i]["T(SC)"]
                        h = df2.iloc[i]["H(%)"]
                        sql = (
                                "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                                % (
                                    filename,
                                    chamber,
                                    kV,
                                    mA,
                                    barCode,
                                    xraysOn,
                                    hVLFilter,
                                    filter,
                                    filter_Ready,
                                    hVLReady,
                                    n,
                                    current1,
                                    current2,
                                    p,
                                    t_MC,
                                    t_Air,
                                    t_SC,
                                    h
                                )
                        )
                        try:
                            # excute sql
                            cursor.execute(sql)
                            # commit to database
                            db.commit()
                            print("processing...")
                        except:
                            # if fail rollback
                            db.rollback()
                            print("fail")

                elif df.iloc[20][0] == "[DATA]":
                    # print("elif")
                    filename = df.iloc[0][2]
                    date = df.iloc[1][2]
                    chamber = df.iloc[2][2]
                    chamber2 = chamber.split()
                    model = " "
                    model = model.join(chamber2[:-1])
                    serial = chamber2[-1]
                    description = df.iloc[3][2]
                    software = df.iloc[4][2]
                    backgrounds = df.iloc[5][2]
                    measurements = df.iloc[6][2]
                    trolley = int(df.iloc[7][2])
                    sCD = int(df.iloc[8][2])
                    aperture_wheel = df.iloc[9][2]
                    comment = df.iloc[10][2]
                    monitorelectrometerrange = df.iloc[11][2]
                    monitor_hv = df.iloc[12][2]
                    mEFAC_ICElectrometerRange = df.iloc[13][2]
                    ic_hv = df.iloc[14][2]
                    client_name = df.iloc[15][2]
                    address1 = df.iloc[16][2]
                    address2 = df.iloc[17][2]
                    operator = df.iloc[18][2]
                    calnumber = df.iloc[19][2]
                    sql = (
                            "INSERT INTO header(filename,Date,chamber,model,serial,description,software,backgrounds,measurements,Trolley,SCD,aperturewheel,Comment,monitorelectrometerrange,monitorhv,MEFAC_ICElectrometerRange,ic_hv,clientname,address1,address2,operator,calnumber) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                            % (
                                filename,
                                date,
                                chamber,
                                model,
                                serial,
                                description,
                                software,
                                backgrounds,
                                measurements,
                                trolley,
                                sCD,
                                aperture_wheel,
                                comment,
                                monitorelectrometerrange,
                                monitor_hv,
                                mEFAC_ICElectrometerRange,
                                ic_hv,
                                client_name,
                                address1,
                                address2,
                                operator,
                                calnumber
                            )
                    )
                    try:
                        # excute sql
                        cursor.execute(sql)
                        # commit to database
                        db.commit()
                    except:
                        # if fail rollback
                        db.rollback()
                        print("fail")
                    df2 = pd.read_csv(
                        csv_file_name, encoding="raw_unicode_escape", skiprows=22
                    )

                    for i in range(len(df2)):
                        kV = int(df2.iloc[i]["kV"])
                        mA = int(df2.iloc[i]["mA"])
                        barCode = df2.iloc[i]["BarCode"]
                        xraysOn = df2.iloc[i]["XraysOn"]
                        hLFilter = df2.iloc[i]["HVLFilter(mm)"]
                        filter = df2.iloc[i]["Filter"]
                        filterReady = df2.iloc[i]["FilterReady"]
                        hVLReady = df2.iloc[i]["HVLReady"]
                        n = df2.iloc[i]["N"]
                        current1 = float(df2.iloc[i]["Current1(pA)"])
                        current2 = float(df2.iloc[i]["Current2(pA)"])
                        p = float(df2.iloc[i]["P(kPa)"])
                        t_MC = float(df2.iloc[i]["T(MC)"])
                        t_Air = float(df2.iloc[i]["T(Air)"])
                        t_SC = float(df2.iloc[i]["T(SC)"])
                        h = float(df2.iloc[i]["H(%)"])
                        sql = (
                                "INSERT INTO body(filename,chamber,kv,ma,barcode,xrayson,HVLFilter,filter,filterready,hvlready,n,Current1,Current2,P,T_MC,T_Air,T_SC,H) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                                % (
                                    filename,
                                    chamber,
                                    kV,
                                    mA,
                                    barCode,
                                    xraysOn,
                                    hVLFilter,
                                    filter,
                                    filterReady,
                                    hVLReady,
                                    n,
                                    current1,
                                    current2,
                                    p,
                                    t_MC,
                                    t_Air,
                                    t_SC,
                                    h
                                )
                        )
                        try:
                            # excute sql
                            cursor.execute(sql)
                            # commit to database
                            db.commit()
                            print("processing...")
                        except:
                            # if fail rollback
                            db.rollback()
                            print("fail")
                progress = progress + 10
                MainFrame.m_progress_bar.SetValue(progress)

            MainFrame.m_progress_bar.SetValue(100)
            # close connection
            db.close()
            # print("Success!")
            dlg = wx.MessageDialog(
                None,
                u"You have already store all the data to database",
                u"successful stored",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            return
        elif not self.confirmed:
            dlg = wx.MessageDialog(
                None,
                u"Please confirm your data files!",
                u"Not confirmed",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
        elif not self.readed:
            dlg = wx.MessageDialog(
                None,
                u"Please read your data files!",
                u"Not readed",
                wx.YES_DEFAULT | wx.ICON_WARNING,
            )
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()

    def download_csv(self, event):
        frame = DatabaseFrame()
        frame.Show()


# This class is for scatter plot
class LeftPanelGraph(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.axes.set_ylabel("NK mGy / nC")
        self.axes.set_xlabel("E_eff / keV ")

    def draw(self):
        for i in range(len(pathClient)):
            KeV, Beam, NK = Testr(pathClient[i], pathLab[i])
            x = KeV
            y = NK
            self.axes.scatter(x, y, label="Run" + str(i + 1))
            self.axes.set_xlim(xmin=0)
        self.axes.legend(loc="upper center", fancybox=True, shadow=True, ncol=5)


# This class is for Table
class RightPanelGrid(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.mygrid = grid.Grid(self)
        tmpKeV, tmpBeam, tmpNK = Testr(pathClient[0], pathLab[0])
        rowSize = len(tmpBeam)
        colSize = 2 + 1 + len(pathClient) * 2
        self.mygrid.CreateGrid(rowSize, colSize)

        # get the cell attribute for the top left row
        for i in range(rowSize):
            attr = gridlib.GridCellAttr()
            attr.SetReadOnly(True)
            self.mygrid.SetRowAttr(i, attr)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mygrid, 0, wx.EXPAND, 0)
        self.sizer.SetSizeHints(self)
        # self.SetSizer(self.sizer)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        ### update real-time data
        self.mygrid.SetColLabelValue(0, "Beam")
        self.mygrid.SetColLabelValue(1, "E_eff")

        for i in range(len(pathClient)):
            self.mygrid.SetColLabelValue(i + 2, "Run" + str(i + 1) + "_NK")
        self.mygrid.SetColLabelValue(2 + len(pathClient), "Average")
        for i in range(len(pathClient)):
            self.mygrid.SetColLabelValue(
                3 + len(pathClient) + i, "Run" + str(i + 1) + "/Avg"
            )

        # put data for Beam and KEV_eff
        for i in range(len(tmpBeam)):
            self.mygrid.SetCellValue(i, 0, str(tmpBeam[i]))
            self.mygrid.SetCellValue(i, 1, str(tmpKeV[i]))

        # put data for average
        average_NK = []
        for i in range(rowSize):
            tmp = 0
            for j in range(len(pathClient)):
                KeV, Beam, NK = Testr(pathClient[j], pathLab[j])
                tmp += NK[i]
            average_NK.append(tmp / len(pathClient))

        MainFrame.m_progress_bar.SetValue(40)

        for i in range(len(average_NK)):
            self.mygrid.SetCellValue(
                i, 2 + len(pathClient), str(round(average_NK[i], 4))
            )

        # put data for Run1/2/3/4 NK, Run/Average
        for i in range(len(pathClient)):
            KeV, Beam, NK = Testr(pathClient[i], pathLab[i])
            for j in range(rowSize):
                self.mygrid.SetCellValue(j, i + 2, str(round(NK[j], 4)))
                self.mygrid.SetCellValue(
                    j, i + 3 + len(pathClient), str(round(NK[j] / average_NK[j], 4))
                )

        MainFrame.m_progress_bar.SetValue(60)


class GraphFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, parent=None, title=u"Graphs Demonstration", size=wx.Size(1200, 600)
        )
        self.SetMinSize(wx.Size(1200, 600))
        self.SetMaxSize(wx.Size(1500, 600))

        spliter = wx.SplitterWindow(self)
        leftgraph = LeftPanelGraph(spliter)
        rightgrid = RightPanelGrid(spliter)
        spliter.SplitVertically(leftgraph, rightgrid)
        spliter.SetMinimumPaneSize(600)

        leftgraph.draw()
        MainFrame.m_progress_bar.SetValue(80)


class DatabaseFrame(wx.Frame):
    def __init__(
        self,
    ):
        wx.Frame.__init__(
            self,
            parent=None,
            id=wx.ID_ANY,
            title=u"Database Management",
            pos=wx.DefaultPosition,
            size=wx.Size(700, 500),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.Size(700, 500), wx.Size(700, 500))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 50), wx.TAB_TRAVERSAL
        )
        self.m_panel1.SetMinSize(wx.Size(-1, 50))
        self.m_panel1.SetMaxSize(wx.Size(-1, 50))

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel2 = wx.Panel(
            self.m_panel1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(
            self.m_panel2, wx.ID_ANY, u"Job ID", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText1.Wrap(-1)

        bSizer3.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_job = wx.TextCtrl(
            self.m_panel2,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        self.m_textCtrl_job.SetHint("Enter job ID")
        bSizer3.Add(self.m_textCtrl_job, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel2.SetSizer(bSizer3)
        self.m_panel2.Layout()
        bSizer3.Fit(self.m_panel2)
        bSizer2.Add(self.m_panel2, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel3 = wx.Panel(
            self.m_panel1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer31 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11 = wx.StaticText(
            self.m_panel3,
            wx.ID_ANY,
            u"Client Name",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText11.Wrap(-1)

        bSizer31.Add(self.m_staticText11, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_client = wx.TextCtrl(
            self.m_panel3,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        self.m_textCtrl_client.SetHint("Enter client name")
        bSizer31.Add(self.m_textCtrl_client, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel3.SetSizer(bSizer31)
        self.m_panel3.Layout()
        bSizer31.Fit(self.m_panel3)
        bSizer2.Add(self.m_panel3, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel4 = wx.Panel(
            self.m_panel1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer32 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(
            self.m_panel4,
            wx.ID_ANY,
            u"Chamber ID",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText12.Wrap(-1)

        bSizer32.Add(self.m_staticText12, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_chamber = wx.TextCtrl(
            self.m_panel4,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            0,
        )
        self.m_textCtrl_chamber.SetHint("Enter chamber ID")
        bSizer32.Add(self.m_textCtrl_chamber, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel4.SetSizer(bSizer32)
        self.m_panel4.Layout()
        bSizer32.Fit(self.m_panel4)
        bSizer2.Add(self.m_panel4, 1, wx.EXPAND | wx.ALL, 5)

        self.m_button_search = wx.Button(
            self.m_panel1, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.Size(70, -1), 0
        )
        self.m_button_search.SetMinSize(wx.Size(70, -1))
        self.m_button_search.SetMaxSize(wx.Size(70, -1))

        bSizer2.Add(self.m_button_search, 0, wx.ALIGN_CENTER | wx.ALL, 8)
        self.Bind(wx.EVT_BUTTON, self.search, self.m_button_search)

        self.m_panel1.SetSizer(bSizer2)
        self.m_panel1.Layout()
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 0)

        self.m_panel5 = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 420), wx.TAB_TRAVERSAL
        )
        self.m_panel5.SetMinSize(wx.Size(-1, 420))
        self.m_panel5.SetMaxSize(wx.Size(-1, 420))

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_treeCtrl = wx.TreeCtrl(
            self.m_panel5,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, 350),
            wx.TR_DEFAULT_STYLE | wx.TR_MULTIPLE | wx.TR_TWIST_BUTTONS,
        )
        self.m_treeCtrl.SetMinSize(wx.Size(-1, 350))
        self.m_treeCtrl.SetMaxSize(wx.Size(-1, 350))

        bSizer9.Add(self.m_treeCtrl, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button_db_download = wx.Button(
            self.m_panel5,
            wx.ID_ANY,
            u"Download CSV",
            wx.DefaultPosition,
            wx.Size(200, 30),
            0,
        )
        self.m_button_db_download.SetMinSize(wx.Size(200, 30))
        self.m_button_db_download.SetMaxSize(wx.Size(200, 30))
        bSizer9.Add(self.m_button_db_download, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.download_db, self.m_button_db_download)

        self.m_panel5.SetSizer(bSizer9)
        self.m_panel5.Layout()
        bSizer1.Add(self.m_panel5, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def search(self, event):
        self.root = self.m_treeCtrl.AddRoot("Something goes here")
        self.m_treeCtrl.SetItemData(self.root, ("key", "value"))
        os = self.m_treeCtrl.AppendItem(self.root, "Operating Systems")
        self.m_treeCtrl.Expand(self.root)
        return

    def download_db(self, event):
        return


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
