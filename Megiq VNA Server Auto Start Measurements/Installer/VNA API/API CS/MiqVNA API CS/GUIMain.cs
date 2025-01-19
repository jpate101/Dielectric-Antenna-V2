using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

using System.Media;
using Microsoft.Win32;
using System.Diagnostics;
using System.Runtime.InteropServices;
using MiQVNA;
using System.IO;
using System.Drawing.Imaging;
using Microsoft.VisualBasic; // ^_^ InputBox


namespace MiQVNAAPI
{
    public partial class GUIMain : Form
    {
        #region PROPERTIES //------------------------------------------------------------------------------------------------

        private mvnaVNAMain myVNA;
        private mvnaSession mySession;
        private mvnaMeasurement myMeasurement;
        private mvnaLedState myLEDP1, myLEDP2, myLEDPG;
        private mvnaMeasurement tempMeasurement;

        private String strPlotTraceSet = "";
        private String strPlotTrace = "";
        private String strPlotChannel = "";

        #endregion

        #region FORM //------------------------------------------------------------------------------------------------------

        public GUIMain()
        {
            InitializeComponent();
        }

        private void GUIMain_Load(object sender, EventArgs e)
        {
            try
            {
                myVNA = new mvnaVNAMain();
                myVNA.evtDataChange += new __mvnaVNAMain_evtDataChangeEventHandler(myVNA_evtDataChange);
                myVNA.evtSweepProgress += new __mvnaVNAMain_evtSweepProgressEventHandler(myVNA_evtSweepProgress);
                myVNA.evtSystemStatus += new __mvnaVNAMain_evtSystemStatusEventHandler(myVNA_evtSystemStatus);
                myVNA.evtMeasurementChange += new __mvnaVNAMain_evtMeasurementChangeEventHandler(myVNA_evtMeasurementChange);
                myMeasurement = myVNA.get_Measurement();
                myMeasurement.evtCalibrationChange += new __mvnaMeasurement_evtCalibrationChangeEventHandler(myMeasurement_evtCalibrationChange);
                myMeasurement.evtDataChange += new __mvnaMeasurement_evtDataChangeEventHandler(myMeasurement_evtDataChange);
                myMeasurement.evtDirty += new __mvnaMeasurement_evtDirtyEventHandler(myMeasurement_evtDirty);
                myMeasurement.evtIdleSettingsChange += new __mvnaMeasurement_evtIdleSettingsChangeEventHandler(myMeasurement_evtIdleSettingsChange);
                myMeasurement.evtSettingsChange += new __mvnaMeasurement_evtSettingsChangeEventHandler(myMeasurement_evtSettingsChange);
                myMeasurement.evtSetupChange += new __mvnaMeasurement_evtSetupChangeEventHandler(myMeasurement_evtSetupChange);
                myMeasurement.evtSweepProgress += new __mvnaMeasurement_evtSweepProgressEventHandler(myMeasurement_evtSweepProgress);

                mySession = myVNA.PresetSession;
                mySession.evtDirty += new __mvnaSession_evtDirtyEventHandler(mySession_evtDirty);

                StatusReport(myVNA.SystemStatus);
                ShowCurrentSettings();
                ShowCurrentCalibration();
                ShowCurrentData();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void GUIMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            myMeasurement = null;
            tempMeasurement = null;
        }

        #endregion

        #region GUI EVENTS //------------------------------------------------------------------------------------------------

        private void buttonConnect_Click(object sender, EventArgs e)
        {
            try
            {
                if (myVNA.SystemStatus == mvnaVNAStatus.mvnaVST_Disconnected)
                {
                    myVNA.Connect();
                }
                else
                {
                    myVNA.Disconnect();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonSweep_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.RunSweepOnce();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonRun_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.RunSweepContinuously();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.StopSweep();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonOpenVNS_Click(object sender, EventArgs e)
        {
            try
            {
                OpenFileDialog OpenSetDialog = new OpenFileDialog();

                // Set filter options and filter index.
                OpenSetDialog.Filter = "Session Files|*.vns|All Files|*.*";
                OpenSetDialog.FilterIndex = 1;
                OpenSetDialog.Multiselect = false;
                OpenSetDialog.InitialDirectory = myVNA.Application.Path + "\\VNA Data";
                DialogResult res = OpenSetDialog.ShowDialog();
                if (res == DialogResult.OK)
                {

                    Cursor = Cursors.WaitCursor;
                    string VNSfile = OpenSetDialog.FileName;
                    mySession = myVNA.OpenSession(ref VNSfile);
                    textBoxFile.Text = VNSfile;
                    ShowSession(mySession);
                    Cursor = Cursors.Default;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonPresetsVNS_Click(object sender, EventArgs e)
        {
            try
            {
                mySession = myVNA.PresetSession;
                ShowSession(mySession);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void ShowSession(mvnaSession Session)
        {
            try
            {
                listViewMeasurements.Items.Clear();
                if (Session == null)
                    return;
                if (Session.Dirty)
                    groupBoxSession.Text = "Session *";
                else
                    groupBoxSession.Text = "Session";
                foreach (mvnaMeasurement msi in mySession.Measurements)
                {
                    ListViewItem lvi = listViewMeasurements.Items.Add(msi.get_Name());
                    lvi.SubItems.Add(msi.DateTime.ToShortDateString());
                    lvi.SubItems.Add(msi.DateTime.ToShortTimeString());
                    lvi.SubItems.Add(msi.Key);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void checkBoxShowScreen_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                myVNA.Application.ShowState = ((CheckBox)sender).Checked ? mvnaWindowShowState.mvnaWSS_Normal : mvnaWindowShowState.mvnaWSS_Hidden;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonLEDP1_Click(object sender, EventArgs e)
        {
            try
            {
                myLEDP1++;
                if (myLEDP1 > mvnaLedState.mvnaLED_BlinkFast) myLEDP1 = mvnaLedState.mvnaLED_Off;
                myVNA.VNADevice.OverrideLedState((mvnaVNAPort)1, mvnaColor.mvnaCOL_Red, myLEDP1);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonLEDP2_Click(object sender, EventArgs e)
        {
            try
            {
                myLEDP2++;
                if (myLEDP2 > mvnaLedState.mvnaLED_BlinkFast) myLEDP2 = mvnaLedState.mvnaLED_Off;
                myVNA.VNADevice.OverrideLedState((mvnaVNAPort)2, mvnaColor.mvnaCOL_Green, myLEDP2);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonLEDPG_Click(object sender, EventArgs e)
        {
            try
            {
                myLEDPG++;
                if (myLEDPG > mvnaLedState.mvnaLED_BlinkFast) myLEDPG = mvnaLedState.mvnaLED_Off;
                myVNA.VNADevice.OverrideLedState((mvnaVNAPort)4, mvnaColor.mvnaCOL_Blue, myLEDPG);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonVNAInfo_Click(object sender, EventArgs e)
        {
            try
            {
                MessageBox.Show(myVNA.VNADevice.VNAInfoString, "VNA Info");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void listViewMeasurements_SelectedIndexChanged(object sender, EventArgs e)
        {
            try
            {
                if (listViewMeasurements.SelectedItems.Count == 0)
                    return;
                ListViewItem lvi = listViewMeasurements.SelectedItems[0];
                String Key = lvi.SubItems[3].Text;
                tempMeasurement = mySession.Measurements.get_Item(Key);
                ShowMeasurement(tempMeasurement);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonCalibrate_Click(object sender, EventArgs e)
        { // Also used for doubleclick in list!
            try
            {
                myVNA.RunCalibration(listViewCalibrations.SelectedIndices[0] + 1);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonClearCal_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.get_Measurement().ClearCalibration();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonClearData_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.get_Measurement().ClearData();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void checkBoxDualCalKit_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                myVNA.get_Measurement().DualCalkit = checkBoxDualCalKit.Checked;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void checkBoxUseCalibration_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                myVNA.get_Measurement().UseCalibration = checkBoxUseCalibration.Checked;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void radioButtonGenIdle_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                if ((RadioButton)sender == radioButtonGenOff) myVNA.get_Measurement().PortIdleGenerator = mvnaVNAPort.mvnaVNP_None;
                if ((RadioButton)sender == radioButtonGenP1) myVNA.get_Measurement().PortIdleGenerator = mvnaVNAPort.mvnaVNP_Port1;
                if ((RadioButton)sender == radioButtonGenP2) myVNA.get_Measurement().PortIdleGenerator = mvnaVNAPort.mvnaVNP_Port2;
                if ((RadioButton)sender == radioButtonGenPGen) myVNA.get_Measurement().PortIdleGenerator = mvnaVNAPort.mvnaVNP_Port3;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonRenormalize_Click(object sender, EventArgs e)
        {
            try
            {
                myVNA.get_Measurement().Renormalize();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void radioButtonBias_CheckedChanged(object sender, EventArgs e)
        {
            try
            {
                if ((RadioButton)sender == radioButtonBiasP1Gnd) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port1, mvnaVNABiasControl.mvnaVBC_Ground);
                if ((RadioButton)sender == radioButtonBiasP1Off) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port1, mvnaVNABiasControl.mvnaVBC_Off);
                if ((RadioButton)sender == radioButtonBiasP1On) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port1, mvnaVNABiasControl.mvnaVBC_On);
                if ((RadioButton)sender == radioButtonBiasP2Gnd) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port2, mvnaVNABiasControl.mvnaVBC_Ground);
                if ((RadioButton)sender == radioButtonBiasP2Off) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port2, mvnaVNABiasControl.mvnaVBC_Off);
                if ((RadioButton)sender == radioButtonBiasP2On) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port2, mvnaVNABiasControl.mvnaVBC_On);
                if ((RadioButton)sender == radioButtonBiasPGGnd) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port3, mvnaVNABiasControl.mvnaVBC_Ground);
                if ((RadioButton)sender == radioButtonBiasPGOff) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port3, mvnaVNABiasControl.mvnaVBC_Off);
                if ((RadioButton)sender == radioButtonBiasPGOn) myVNA.get_Measurement().set_PortBias(mvnaVNAPort.mvnaVNP_Port3, mvnaVNABiasControl.mvnaVBC_On);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonRefresh_Click(object sender, EventArgs e)
        {
            try
            {
                if (myMeasurement == null) return;
                ShowCurrentMeasurement();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void listViewMeasurements_DoubleClick(object sender, EventArgs e)
        {
            try
            {
                if (listViewMeasurements.SelectedItems.Count == 0)
                    return;
                Cursor = Cursors.WaitCursor;
                ListViewItem lvi = listViewMeasurements.SelectedItems[0];
                String Key = lvi.SubItems[3].Text;
                tempMeasurement = mySession.Measurements.get_Item(Key);
                ShowMeasurement(tempMeasurement);
                myVNA.set_Measurement(tempMeasurement);
                Cursor = Cursors.Default;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void treeViewData_NodeMouseClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            try
            {
                if (e.Node.Text.Contains("Channel"))
                {
                    strPlotTraceSet = e.Node.Parent.Parent.Text;
                    strPlotTrace = e.Node.Parent.Text;
                    strPlotChannel = e.Node.Text;
                    if (tempMeasurement == null)
                        PlotTraceChannel(myMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel);
                    else
                        PlotTraceChannel(tempMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void listViewParameters_DoubleClick(object sender, EventArgs e)
        {
            try
            {
                if (tempMeasurement != null)
                {
                    SystemSounds.Beep.Play();
                    return;
                }
                String S = "";
                Array ValueList;
                mvnaParameter Par = myMeasurement.Parameters[listViewParameters.SelectedItems[0].Text];
                if (Par.IsSweep)
                {
                    if (Par.get_SweepType() == mvnaSweepType.mvnaSWT_List)
                    {
                        ValueList = Par.get_SweepValueList();
                        for (int i = 0; i <= ValueList.GetUpperBound(0); i++)
                        {
                            if (S != "") S = S + " ";
                            S = S + ValueList.GetValue(i).ToString();
                        }
                        S = Interaction.InputBox(Par.Name + " Value list:", Application.ProductName, S);
                    }
                    else
                    {
                        S = Interaction.InputBox(Par.Name + " Start Value", Application.ProductName, Par.StartValue.ToString());
                    }

                    if (S == "") return;

                    String delim = " ";
                    String[] ValsA = S.Split(delim.ToCharArray());
                    if (ValsA.GetUpperBound(0) == 0)
                    {
                        Par.StartValue = Convert.ToDouble(S);
                        Par.set_SweepType(mvnaSweepType.mvnaSWT_Lin);
                    }
                    else
                    {
                        List<double> SetList = new List<double> { };
                        for (int i = 0; i <= ValsA.GetUpperBound(0); i++)
                        {
                            SetList.Add(Convert.ToDouble(ValsA[i]));
                        }
                        Par.set_SweepValueList(SetList.ToArray());
                        Par.set_SweepType(mvnaSweepType.mvnaSWT_List);
                        Par.Steps = SetList.Count - 1;
                    }

                    if (Par.get_SweepType() != mvnaSweepType.mvnaSWT_List)
                    {
                        S = Interaction.InputBox(Par.Name + " Stop value:", Application.ProductName, Par.StopValue.ToString());
                        if (S == "") return;
                        Par.StopValue = Convert.ToDouble(S);
                        S = Interaction.InputBox(Par.Name + " Steps:", Application.ProductName, Par.Steps.ToString());
                        if (S == "") return;
                        Par.CurrentValue = Convert.ToInt32(S);
                    }
                }
                else
                {
                    S = Interaction.InputBox(Par.Name + " current value:", Application.ProductName, Par.CurrentValue.ToString());
                    if (S == "") return;
                    Par.CurrentValue = Convert.ToDouble(S);
                }
                Par.Update();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonSaveSession_Click(object sender, EventArgs e)
        {
            try
            {
                if (mySession == null)
                    return;
                mvnaVNADataOptions SaveOptions = new mvnaVNADataOptions();
                if (checkBoxSaveCal.Checked) SaveOptions |= mvnaVNADataOptions.mvnaVDO_CALIBRATION;
                if (checkBoxSaveData.Checked) SaveOptions |= mvnaVNADataOptions.mvnaVDO_DATA;

                SaveFileDialog SaveSessionDialog = new SaveFileDialog();
                SaveSessionDialog.Filter = "VNA Session Files|*.vns|All Files|*.*";
                DialogResult res = SaveSessionDialog.ShowDialog();
                if (res == DialogResult.OK)
                {
                    Cursor = Cursors.WaitCursor;
                    mySession.SaveSession(SaveSessionDialog.FileName, false, SaveOptions);
                    Cursor = Cursors.Default;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonSaveSelectedItem_Click(object sender, EventArgs e)
        {
            try
            {
                if (mySession == null)
                    return;
                if (listViewMeasurements.SelectedItems.Count == 0)
                    return;
                Cursor = Cursors.WaitCursor;
                String Key = listViewMeasurements.SelectedItems[0].SubItems[3].Text;
                mvnaMeasurement Mm = mySession.Measurements.Item[Key];
                mySession.Measurements.AddItem(Mm, Mm.get_Name() + "-NEW", DateTime.Now);
                Cursor = Cursors.Default;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        private void buttonSaveCurrentItem_Click(object sender, EventArgs e)
        {
            try
            {
                if (mySession == null)
                    return;
                Cursor = Cursors.WaitCursor;
                if (myVNA.get_Measurement().get_Name() == "[new]")
                    mySession.Measurements.AddItem(myVNA.get_Measurement(), myVNA.get_Measurement().get_Name() + "NEW ITEM", DateTime.Now);
                else
                    mySession.Measurements.AddItem(myVNA.get_Measurement(), myVNA.get_Measurement().get_Name() + "-NEW", DateTime.Now);
                Cursor = Cursors.Default;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }
        }

        #endregion

        #region VNA EVENTS //------------------------------------------------------------------------------------------------

        void myVNA_evtMeasurementChange()
        {
            ShowCurrentMeasurement();
        }

        void myVNA_evtSystemStatus(mvnaVNAStatus Status)
        {
            StatusReport(Status);
        }

        void myVNA_evtSweepProgress(int PointsReceived, int PointsTotal)
        {
            SweepBar(PointsReceived, PointsTotal);
        }

        void myVNA_evtDataChange(int TraceNr, int NrTraces)
        {
            // Nothing here
        }

        void myMeasurement_evtSweepProgress(int PointsReceived, int PointsTotal)
        {
            // throw new NotImplementedException();
            // Sweep Progress is handled by myVNA_evtSweepProgress
        }

        void myMeasurement_evtSetupChange()
        {
            if (tempMeasurement == null)
                ShowCurrentSettings();
            else
                ShowCurrentMeasurement();
        }

        void myMeasurement_evtSettingsChange()
        {
            if (tempMeasurement == null)
                ShowCurrentSettings();
            else
                ShowCurrentMeasurement();
        }

        void myMeasurement_evtIdleSettingsChange()
        {
            ShowGenerator();
        }

        void myMeasurement_evtDirty(bool Flag)
        {
            if (tempMeasurement == null)
                ShowCurrentSettings();
            else
                ShowCurrentMeasurement();
        }

        void myMeasurement_evtDataChange(int TraceNr, int NrTraces)
        {
            if (TraceNr == 0)
            {
                if (tempMeasurement == null)
                    ShowCurrentData();
                else
                    ShowCurrentMeasurement();
            }
            else if (TraceNr == NrTraces)
            {
                if (tempMeasurement == null)
                    ShowCurrentData();
                else
                    ShowCurrentMeasurement();
            }
        }

        void myMeasurement_evtCalibrationChange(int CalibrationNr, int NrCalibrations)
        {
            if (tempMeasurement == null)
                ShowCurrentCalibration();
            else
                ShowCurrentMeasurement();
        }

        void mySession_evtDirty(bool Flag)
        {
            throw new NotImplementedException();
        }

        #endregion

        #region THREADED GUI UPDATE //---------------------------------------------------------------------------------------

        private void StatusReport(mvnaVNAStatus Stat)
        {
            if (labelStatus.InvokeRequired)
            {
                labelStatus.BeginInvoke(new MethodInvoker(delegate()
                {
                    StatusReport(Stat);
                }));
            }
            else
            {
                switch (Stat)
                {
                    case mvnaVNAStatus.mvnaVST_Disconnected:
                        labelStatus.Text = "VNA status: Disconnected";
                        break;
                    case mvnaVNAStatus.mvnaVST_Initializing:
                        labelStatus.Text = "VNA status: Initializing";
                        break;
                    case mvnaVNAStatus.mvnaVST_Idle:
                        labelStatus.Text = "VNA status: Idle";
                        break;
                    case mvnaVNAStatus.mvnaVST_Calibrating:
                        labelStatus.Text = "VNA status: Calibrating";
                        break;
                    case mvnaVNAStatus.mvnaVST_Sweeping:
                        labelStatus.Text = "VNA status: Sweeping";
                        break;
                }
                if (myVNA.SystemStatus == mvnaVNAStatus.mvnaVST_Disconnected)
                {
                    buttonConnect.Text = "Connect";
                }
                else
                {
                    buttonConnect.Text = "Disconnect";
                }
            }
        }

        private void SweepBar(int PointsReceived, int PointsTotal)
        {
            if (progressBarSweep.InvokeRequired)
            {
                progressBarSweep.BeginInvoke(new MethodInvoker(delegate()
                {
                    SweepBar(PointsReceived, PointsTotal);
                }));
            }
            else
            {
                progressBarSweep.Maximum = PointsTotal;
                progressBarSweep.Value = PointsReceived;
            }
        }

        private void ShowDataTree(int TraceNr, int NrTraces)
        {
            if (treeViewData.InvokeRequired)
            {
                treeViewData.BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowDataTree(TraceNr, NrTraces);
                }));
            }
            else
            {
                try
                {
                    ShowTraceSet(myVNA.TraceSet);
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }
        }

        private void ShowMeasurement(mvnaMeasurement Measurement)
        {
            if (((Control)this).InvokeRequired)
                ((Control)this).BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowMeasurement(Measurement);
                }));
            else
            {
                Cursor = Cursors.WaitCursor;
                ShowSettings(Measurement);
                ShowData(Measurement);
                ShowCalibration(Measurement);
                Cursor = Cursors.Default;
            }
        }

        private void ShowSettings(mvnaMeasurement Measurement)
        {
            if (Measurement == null)
                return;
            if (groupBoxMeasurement.InvokeRequired)
                groupBoxMeasurement.BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowSettings(Measurement);
                }));
            else
            {
                if (Measurement.Dirty)
                    groupBoxMeasurement.Text = "Measurement *";
                else
                    groupBoxMeasurement.Text = "Measurement";

                ShowParameters(Measurement);

                mvnaVNAPort PortIdleGen = Measurement.PortIdleGenerator;
                switch (PortIdleGen)
                {
                    case mvnaVNAPort.mvnaVNP_None:
                        radioButtonGenOff.Checked = true;
                        break;
                    case mvnaVNAPort.mvnaVNP_Port1:
                        radioButtonGenP1.Checked = true;
                        break;
                    case mvnaVNAPort.mvnaVNP_Port2:
                        radioButtonGenP2.Checked = true;
                        break;
                    case mvnaVNAPort.mvnaVNP_Port3:
                        radioButtonGenPGen.Checked = true;
                        break;
                }

                mvnaVNABiasControl BC;
                BC = Measurement.get_PortBias(mvnaVNAPort.mvnaVNP_Port1);
                switch (BC)
                {
                    case mvnaVNABiasControl.mvnaVBC_Ground:
                        radioButtonBiasP1Gnd.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_Off:
                        radioButtonBiasP1Off.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_On:
                        radioButtonBiasP1On.Checked = true;
                        break;
                }
                BC = Measurement.get_PortBias(mvnaVNAPort.mvnaVNP_Port2);
                switch (BC)
                {
                    case mvnaVNABiasControl.mvnaVBC_Ground:
                        radioButtonBiasP2Gnd.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_Off:
                        radioButtonBiasP2Off.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_On:
                        radioButtonBiasP2On.Checked = true;
                        break;
                }
                BC = Measurement.get_PortBias(mvnaVNAPort.mvnaVNP_Port3);
                switch (BC)
                {
                    case mvnaVNABiasControl.mvnaVBC_Ground:
                        radioButtonBiasPGGnd.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_Off:
                        radioButtonBiasPGOff.Checked = true;
                        break;
                    case mvnaVNABiasControl.mvnaVBC_On:
                        radioButtonBiasPGOn.Checked = true;
                        break;
                }

                textBoxMeasurementName.Text = Measurement.get_Name();
                textBoxMeasurementDate.Text = Measurement.DateTime.ToString();
                checkBoxUseCalibration.Checked = Measurement.UseCalibration;
                checkBoxDualCalKit.Checked = Measurement.DualCalkit;
            }
        }

        private void ShowParameters(mvnaMeasurement Measurement)
        {
            if (listViewParameters.InvokeRequired)
                listViewParameters.BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowParameters(Measurement);
                }));
            else
            {
                listViewParameters.Items.Clear();
                foreach (mvnaParameter par in Measurement.Parameters)
                {
                    ListViewItem lvi = new ListViewItem(par.Name);
                    if (par.Name.Contains("FREQUENCY"))
                    {
                        lvi.SubItems.Add((par.MinValue / 1000000).ToString());
                        lvi.SubItems.Add((par.MaxValue / 1000000).ToString());
                        if (par.IsSweep)
                        {
                            if (par.get_SweepType() == mvnaSweepType.mvnaSWT_List)
                            {
                                String S = "";
                                Array ValueList = par.get_SweepValueList();
                                for (int i = 0; i <= ValueList.GetUpperBound(0); i++)
                                {
                                    if (S != "") S = S + " ";
                                    S = S + (Convert.ToDouble(ValueList.GetValue(i)) / 1000000).ToString();
                                }
                                lvi.SubItems.Add(S);
                                lvi.SubItems.Add("");
                                lvi.SubItems.Add("");
                            }
                            else
                            {
                                lvi.SubItems.Add((par.StartValue / 1000000).ToString());
                                lvi.SubItems.Add((par.StopValue / 1000000).ToString());
                                lvi.SubItems.Add(par.Steps.ToString());
                            }
                        }
                        else
                        {
                            lvi.SubItems.Add((par.CurrentValue / 1000000).ToString());
                            lvi.SubItems.Add("");
                            lvi.SubItems.Add("");
                        }
                        lvi.SubItems.Add("M" + par.Dimension.ToString());
                    }
                    else
                    {
                        lvi.SubItems.Add(par.MinValue.ToString());
                        lvi.SubItems.Add(par.MaxValue.ToString());
                        if (par.IsSweep)
                        {
                            if (par.get_SweepType() == mvnaSweepType.mvnaSWT_List)
                            {
                                String S = "";
                                Array ValueList = par.get_SweepValueList();
                                for (int i = 0; i <= ValueList.GetUpperBound(0); i++)
                                {
                                    if (S != "") S = S + " ";
                                    S = S + ValueList.GetValue(i).ToString();
                                }
                                lvi.SubItems.Add(S);
                                lvi.SubItems.Add("");
                                lvi.SubItems.Add("");
                            }
                            else
                            {
                                lvi.SubItems.Add(par.StartValue.ToString());
                                lvi.SubItems.Add(par.StopValue.ToString());
                                lvi.SubItems.Add(par.Steps.ToString());
                            }
                        }
                        else
                        {
                            lvi.SubItems.Add(par.CurrentValue.ToString());
                            lvi.SubItems.Add("");
                            lvi.SubItems.Add("");
                        }
                        lvi.SubItems.Add(par.Dimension.ToString());
                    }
                    listViewParameters.Items.Add(lvi);
                }
            }
        }

        private void ShowData(mvnaMeasurement Measurement)
        {
            if (strPlotChannel.Length != 0)
            {
                if (tempMeasurement == null)
                    PlotTraceChannel(myMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel);
                else
                    PlotTraceChannel(tempMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel);
            }
            ShowTraceSet(Measurement.TraceSet);
        }

        private void ShowCalibration(mvnaMeasurement Measurement)
        {
            if (listViewCalibrations.InvokeRequired)
                listViewCalibrations.BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowCalibration(Measurement);
                }));
            else
            {
                listViewCalibrations.Items.Clear();
                foreach (mvnaCalibration Cal in Measurement.Calibrations)
                {
                    ListViewItem lvi = new ListViewItem(Cal.Caption.ToString());
                    if (Cal.Complete)
                    {
                        lvi.Font = new Font(lvi.Font, lvi.Font.Style | FontStyle.Bold);
                    }
                    listViewCalibrations.Items.Add(lvi);
                }
            }
        }

        private void ShowTraceSet(mvnaTraceSet TraceSet)
        {
            if (treeViewData.InvokeRequired)
                treeViewData.BeginInvoke(new MethodInvoker(delegate()
                {
                    ShowTraceSet(TraceSet);
                }));
            else
            {
                treeViewData.Nodes.Clear();
                TreeNode rootnode = new TreeNode("TraceSet");
                foreach (mvnaParameter par in TraceSet.Parameters)
                {
                    if (par.Name.Contains("FREQUENCY"))
                    {
                        if (!par.IsSweep)
                        {
                            TreeNode traceinfo = new TreeNode(par.Name + " " +
                                (par.CurrentValue / 1000000).ToString() + " " +
                                "M" + par.Dimension);
                            rootnode.Nodes.Add(traceinfo);
                        }
                        else
                        {
                            TreeNode traceinfo = new TreeNode(par.Name + " " +
                                (par.StartValue / 1000000).ToString() + " to " +
                                (par.StopValue / 1000000).ToString() + " " +
                                "M" + par.Dimension);
                            rootnode.Nodes.Add(traceinfo);

                        }
                    }
                    else
                    {
                        if (!par.IsSweep)
                        {
                            TreeNode traceinfo = new TreeNode(par.Name + " " +
                                par.CurrentValue.ToString() + " " +
                                par.Dimension);
                            rootnode.Nodes.Add(traceinfo);
                        }
                        else
                        {
                            TreeNode traceinfo = new TreeNode(par.Name + " " +
                                par.StartValue.ToString() + " to " +
                                par.StopValue.ToString() + " " +
                                par.Dimension);
                            rootnode.Nodes.Add(traceinfo);

                        }
                    }
                }
                foreach (mvnaTrace Trace in TraceSet.Traces)
                {
                    TreeNode mynode = new TreeNode("Trace " + Trace.TraceNumber.ToString());

                    foreach (mvnaParameter par in Trace.Parameters)
                    {
                        if (par.Name.Contains("FREQUENCY"))
                        {
                            if (!par.IsSweep)
                            {
                                TreeNode traceinfo = new TreeNode(par.Name + " " +
                                    (par.CurrentValue / 1000000).ToString() + " " +
                                    "M" + par.Dimension);
                                mynode.Nodes.Add(traceinfo);
                            }
                            else
                            {
                                TreeNode traceinfo = new TreeNode(par.Name + " " +
                                    (par.StartValue / 1000000).ToString() + " to " +
                                    (par.StopValue / 1000000).ToString() + " " +
                                    "M" + par.Dimension);
                                mynode.Nodes.Add(traceinfo);

                            }

                        }
                        else
                        {
                            if (!par.IsSweep)
                            {
                                TreeNode traceinfo = new TreeNode(par.Name + " " +
                                    par.CurrentValue.ToString() + " " +
                                    par.Dimension);
                                mynode.Nodes.Add(traceinfo);
                            }
                            else
                            {
                                TreeNode traceinfo = new TreeNode(par.Name + " " +
                                    par.StartValue.ToString() + " to " +
                                    par.StopValue.ToString() + " " +
                                    par.Dimension);
                                mynode.Nodes.Add(traceinfo);

                            }
                        }

                    }
                    foreach (mvnaTraceChannel chan in Trace.Channels)
                    {
                        TreeNode channode = new TreeNode("Channel " + chan.Name);
                        foreach (mvnaIQData data in chan.DataSet)
                        {
                            TreeNode pointsnode = new TreeNode("Contains " +
                                data.Size.ToString()
                                + " " +
                                data.get_Name()
                                + " data points.");
                            channode.Nodes.Add(pointsnode);
                        }
                        mynode.Nodes.Add(channode);
                    }
                    rootnode.Nodes.Add(mynode);
                }
                treeViewData.Nodes.Add(rootnode);
                treeViewData.ExpandAll();
                rootnode.EnsureVisible();
            }
        }

        private void ShowGenerator()
        {
            if (radioButtonGenOff.InvokeRequired)
            {
                radioButtonGenOff.BeginInvoke(new MethodInvoker(delegate()
                {
                    myMeasurement_evtIdleSettingsChange();
                }));
            }
            else
            {
                if (myMeasurement.PortIdleGenerator == mvnaVNAPort.mvnaVNP_None) radioButtonGenOff.Checked = true;
                if (myMeasurement.PortIdleGenerator == mvnaVNAPort.mvnaVNP_Port1) radioButtonGenP1.Checked = true;
                if (myMeasurement.PortIdleGenerator == mvnaVNAPort.mvnaVNP_Port2) radioButtonGenP2.Checked = true;
                if (myMeasurement.PortIdleGenerator == mvnaVNAPort.mvnaVNP_Port3) radioButtonGenPGen.Checked = true;
            }
        }

        private void ShowCurrentMeasurement()
        {
            tempMeasurement = null;
            ShowMeasurement(myMeasurement);
        }

        private void ShowCurrentCalibration()
        {
            ShowCalibration(myMeasurement);
        }

        private void ShowCurrentData()
        {
            ShowData(myMeasurement);
        }

        private void ShowCurrentSettings()
        {
            ShowSettings(myMeasurement);
        }

        private void PlotTraceChannel(mvnaMeasurement Measurement, String TraceSetName, String TraceName, String ChannelName)
        {
            UInt32 TraceNumber;
            String Caption;
            mvnaTraceSet TraceSet;
            mvnaTrace Trace;
            mvnaTraceChannel Channel;
            mvnaIQData Data;
            Array Values;

            try
            {

                if (Measurement == null)
                    return;
                TraceNumber = Convert.ToUInt32(TraceName.Substring(TraceName.Length - 2, 2));
                TraceSet = Measurement.TraceSet;
                Trace = TraceSet.Traces[TraceNumber];

                if (ChannelName.Contains("S11"))
                {
                    Channel = Trace.Channels["S11"];
                    Data = Channel.DataSet["Return"];
                }
                else if (ChannelName.Contains("S22"))
                {
                    Channel = Trace.Channels["S22"];
                    Data = Channel.DataSet["Return"];
                }
                else if (ChannelName.Contains("S12"))
                {
                    Channel = Trace.Channels["S12"];
                    Data = Channel.DataSet["Through"];
                }
                else if (ChannelName.Contains("S13"))
                {
                    Channel = Trace.Channels["S13"];
                    Data = Channel.DataSet["Through"];
                }
                else if (ChannelName.Contains("S21"))
                {
                    Channel = Trace.Channels["S21"];
                    Data = Channel.DataSet["Through"];
                }
                else if (ChannelName.Contains("S23"))
                {
                    Channel = Trace.Channels["S23"];
                    Data = Channel.DataSet["Through"];
                }
                else
                {
                    return;
                }
                Caption = TraceSetName + "\\" + "Trace " + TraceNumber.ToString() + "\\" + Channel.Name + "\\" +
                    Data.get_Name() + "data";
                Values = Array.CreateInstance(typeof(double), Data.Values.Length);
                Data.GetAmpValuesDb(ref Values);
                PlotData(pictureBoxGraph, (double[])Values, (double[])(Data.PValues), -50, 0, Caption);
            }
            catch (Exception e)
            {
                String msg = e.ToString(); // Do not print. This is expected.
                pictureBoxGraph.Image = null;
            }
        }

        private void PlotData(PictureBox Pic, Double[] Data, Double[] PData, Double ScaleMin, Double ScaleMax, String Caption = "")
        {
            Int32 i;
            Int32 NrSamples;
            Double X;
            Double XLast;
            Double XStep;
            Double Y;
            Double YLast;
            Double YStep;
            Double YScale;
            Bitmap Bump = new Bitmap(Pic.Width, Pic.Height);
            Graphics Fig = Graphics.FromImage(Bump);
            Font myFont = buttonCalibrate.Font; // Use same font as on buttons.

            NrSamples = PData.Length;
            if (NrSamples <= 1) return;

            // Put Gridlines
            X = 0;
            XStep = (double)(Pic.Width) / 10.0; //Basic: ScaleWidth

            for (i = 0; i <= 10; i++)
            {
                Fig.DrawLine(new Pen(Color.FromArgb(0x80, 0x80, 0x80), 1), new Point((int)X, 0), new Point((int)X, Pic.Width));
                X += XStep;
            }
            Y = 0;
            YStep = (double)(Pic.Height) / 5.0;
            for (i = 0; i <= 5; i++)
            {
                Fig.DrawLine(new Pen(Color.FromArgb(0x80, 0x80, 0x80), 1), new Point(0, (int)Y), new Point(Pic.Width, (int)Y));
                Y += YStep;
            }

            // Put Scale
            Fig.DrawString(ScaleMax.ToString() + " dB",
                   myFont,
                   new SolidBrush(Color.White),
                   new Point(0, 0));

            Fig.DrawString(ScaleMin.ToString() + " dB",
                               myFont,
                               new SolidBrush(Color.White),
                               new Point(0, Pic.Height - (int)(Fig.MeasureString("A", myFont).Height)));

            // We assume that the X-axis contains frequency data.
            // This is only correct for frequency sweeps.
            Fig.DrawString((PData[0] / 1000000).ToString() + " MHz",
                               myFont,
                               new SolidBrush(Color.White),
                               new Point(0, (Pic.Height - (int)(Fig.MeasureString("A", myFont).Height)) / 2));

            Fig.DrawString((PData[NrSamples - 1] / 1000000).ToString() + " MHz",
                               myFont,
                               new SolidBrush(Color.White),
                               new Point(Pic.Width - (int)(Fig.MeasureString((PData[NrSamples - 1] / 1000000).ToString() + " MHz", myFont).Width),
                                   (Pic.Height - (int)(Fig.MeasureString("A", myFont).Height)) / 2));

            // Put Caption
            if (Caption.Length > 0)
                Fig.DrawString(Caption,
                    myFont,
                    new SolidBrush(Color.White),
                    new Point(Pic.Width - (int)(Fig.MeasureString(Caption, myFont).Width), 0));

            // Plot Data
            X = 0;
            XLast = X;
            XStep = (double)(Pic.Width) / (NrSamples - 1.0);
            YScale = (double)(Pic.Height) / (ScaleMax - ScaleMin);
            YLast = (double)(Pic.Height) - (Data[0] - ScaleMin) * YScale;

            for (i = 0; i < NrSamples; i++)
            {
                Y = Pic.Height - (Data[i] - ScaleMin) * YScale;
                Fig.DrawLine(new Pen(Color.Yellow, 1), new Point((int)XLast, (int)YLast), new Point((int)X, (int)Y));
                if (NrSamples <= 20)
                {
                    int radius = 6;
                    Rectangle Circle = new Rectangle((int)X - radius, (int)Y - radius, 2 * radius, 2 * radius);
                    Fig.DrawEllipse(new Pen(Color.Yellow, 1), Circle);
                }
                XLast = X;
                YLast = Y;
                X += XStep;
            }

            Pic.Image = Bump;
            Pic.Invalidate();
        }

        #endregion
    }
}
