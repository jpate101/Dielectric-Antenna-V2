namespace MiQVNAAPI
{
    partial class GUIMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(GUIMain));
            this.progressBarSweep = new System.Windows.Forms.ProgressBar();
            this.buttonConnect = new System.Windows.Forms.Button();
            this.buttonRun = new System.Windows.Forms.Button();
            this.buttonSweep = new System.Windows.Forms.Button();
            this.buttonStop = new System.Windows.Forms.Button();
            this.buttonOpenVNS = new System.Windows.Forms.Button();
            this.treeViewData = new System.Windows.Forms.TreeView();
            this.groupBoxVNAControl = new System.Windows.Forms.GroupBox();
            this.buttonLEDPG = new System.Windows.Forms.Button();
            this.buttonLEDP2 = new System.Windows.Forms.Button();
            this.buttonLEDP1 = new System.Windows.Forms.Button();
            this.labelCalibrate = new System.Windows.Forms.Label();
            this.labelMeasure = new System.Windows.Forms.Label();
            this.checkBoxShowScreen = new System.Windows.Forms.CheckBox();
            this.listViewCalibrations = new System.Windows.Forms.ListView();
            this.buttonCalibrate = new System.Windows.Forms.Button();
            this.buttonVNAInfo = new System.Windows.Forms.Button();
            this.labelStatus = new System.Windows.Forms.Label();
            this.listViewParameters = new System.Windows.Forms.ListView();
            this.columnParameter = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderMin = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderMax = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderStart = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderStop = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderSteps = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderDim = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.listViewMeasurements = new System.Windows.Forms.ListView();
            this.columnHeaderName = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderDate = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderTime = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeaderKey = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.buttonPresetsVNS = new System.Windows.Forms.Button();
            this.buttonSaveSelectedItem = new System.Windows.Forms.Button();
            this.buttonSaveCurrentItem = new System.Windows.Forms.Button();
            this.buttonSaveSession = new System.Windows.Forms.Button();
            this.labelParameters = new System.Windows.Forms.Label();
            this.labelData = new System.Windows.Forms.Label();
            this.labelName = new System.Windows.Forms.Label();
            this.labelDate = new System.Windows.Forms.Label();
            this.groupBoxSession = new System.Windows.Forms.GroupBox();
            this.checkBoxSaveData = new System.Windows.Forms.CheckBox();
            this.checkBoxSaveCal = new System.Windows.Forms.CheckBox();
            this.textBoxFile = new System.Windows.Forms.TextBox();
            this.labelFile = new System.Windows.Forms.Label();
            this.groupBoxMeasurement = new System.Windows.Forms.GroupBox();
            this.groupBoxBiasPGen = new System.Windows.Forms.GroupBox();
            this.radioButtonBiasPGOn = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasPGGnd = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasPGOff = new System.Windows.Forms.RadioButton();
            this.groupBoxBiasP2 = new System.Windows.Forms.GroupBox();
            this.radioButtonBiasP2On = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasP2Gnd = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasP2Off = new System.Windows.Forms.RadioButton();
            this.labelBias = new System.Windows.Forms.Label();
            this.labelGenIdle = new System.Windows.Forms.Label();
            this.groupBoxBiasP1 = new System.Windows.Forms.GroupBox();
            this.radioButtonBiasP1On = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasP1Gnd = new System.Windows.Forms.RadioButton();
            this.radioButtonBiasP1Off = new System.Windows.Forms.RadioButton();
            this.groupBoxGenIdle = new System.Windows.Forms.GroupBox();
            this.radioButtonGenPGen = new System.Windows.Forms.RadioButton();
            this.radioButtonGenP2 = new System.Windows.Forms.RadioButton();
            this.radioButtonGenP1 = new System.Windows.Forms.RadioButton();
            this.radioButtonGenOff = new System.Windows.Forms.RadioButton();
            this.buttonRefresh = new System.Windows.Forms.Button();
            this.buttonClearCal = new System.Windows.Forms.Button();
            this.checkBoxUseCalibration = new System.Windows.Forms.CheckBox();
            this.checkBoxDualCalKit = new System.Windows.Forms.CheckBox();
            this.textBoxMeasurementDate = new System.Windows.Forms.TextBox();
            this.textBoxMeasurementName = new System.Windows.Forms.TextBox();
            this.buttonClearData = new System.Windows.Forms.Button();
            this.buttonRenormalize = new System.Windows.Forms.Button();
            this.pictureBoxGraph = new System.Windows.Forms.PictureBox();
            this.groupBoxVNAControl.SuspendLayout();
            this.groupBoxSession.SuspendLayout();
            this.groupBoxMeasurement.SuspendLayout();
            this.groupBoxBiasPGen.SuspendLayout();
            this.groupBoxBiasP2.SuspendLayout();
            this.groupBoxBiasP1.SuspendLayout();
            this.groupBoxGenIdle.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxGraph)).BeginInit();
            this.SuspendLayout();
            // 
            // progressBarSweep
            // 
            this.progressBarSweep.Location = new System.Drawing.Point(9, 37);
            this.progressBarSweep.Name = "progressBarSweep";
            this.progressBarSweep.Size = new System.Drawing.Size(159, 10);
            this.progressBarSweep.TabIndex = 4;
            // 
            // buttonConnect
            // 
            this.buttonConnect.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonConnect.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonConnect.Location = new System.Drawing.Point(186, 16);
            this.buttonConnect.Name = "buttonConnect";
            this.buttonConnect.Size = new System.Drawing.Size(75, 23);
            this.buttonConnect.TabIndex = 5;
            this.buttonConnect.Text = "Disconnect";
            this.buttonConnect.UseVisualStyleBackColor = true;
            this.buttonConnect.Click += new System.EventHandler(this.buttonConnect_Click);
            // 
            // buttonRun
            // 
            this.buttonRun.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonRun.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonRun.Location = new System.Drawing.Point(9, 157);
            this.buttonRun.Name = "buttonRun";
            this.buttonRun.Size = new System.Drawing.Size(75, 23);
            this.buttonRun.TabIndex = 7;
            this.buttonRun.Text = "Run";
            this.buttonRun.UseVisualStyleBackColor = true;
            this.buttonRun.Click += new System.EventHandler(this.buttonRun_Click);
            // 
            // buttonSweep
            // 
            this.buttonSweep.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSweep.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonSweep.Location = new System.Drawing.Point(9, 129);
            this.buttonSweep.Name = "buttonSweep";
            this.buttonSweep.Size = new System.Drawing.Size(75, 23);
            this.buttonSweep.TabIndex = 8;
            this.buttonSweep.Text = "Sweep";
            this.buttonSweep.UseVisualStyleBackColor = true;
            this.buttonSweep.Click += new System.EventHandler(this.buttonSweep_Click);
            // 
            // buttonStop
            // 
            this.buttonStop.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonStop.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonStop.Location = new System.Drawing.Point(9, 185);
            this.buttonStop.Name = "buttonStop";
            this.buttonStop.Size = new System.Drawing.Size(75, 23);
            this.buttonStop.TabIndex = 9;
            this.buttonStop.Text = "Stop";
            this.buttonStop.UseVisualStyleBackColor = true;
            this.buttonStop.Click += new System.EventHandler(this.buttonStop_Click);
            // 
            // buttonOpenVNS
            // 
            this.buttonOpenVNS.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonOpenVNS.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonOpenVNS.Location = new System.Drawing.Point(315, 17);
            this.buttonOpenVNS.Name = "buttonOpenVNS";
            this.buttonOpenVNS.Size = new System.Drawing.Size(75, 23);
            this.buttonOpenVNS.TabIndex = 11;
            this.buttonOpenVNS.Text = "Open";
            this.buttonOpenVNS.UseVisualStyleBackColor = true;
            this.buttonOpenVNS.Click += new System.EventHandler(this.buttonOpenVNS_Click);
            // 
            // treeViewData
            // 
            this.treeViewData.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.treeViewData.ForeColor = System.Drawing.SystemColors.ControlText;
            this.treeViewData.Location = new System.Drawing.Point(9, 413);
            this.treeViewData.Name = "treeViewData";
            this.treeViewData.Size = new System.Drawing.Size(472, 215);
            this.treeViewData.TabIndex = 12;
            this.treeViewData.NodeMouseClick += new System.Windows.Forms.TreeNodeMouseClickEventHandler(this.treeViewData_NodeMouseClick);
            // 
            // groupBoxVNAControl
            // 
            this.groupBoxVNAControl.Controls.Add(this.buttonLEDPG);
            this.groupBoxVNAControl.Controls.Add(this.buttonLEDP2);
            this.groupBoxVNAControl.Controls.Add(this.buttonLEDP1);
            this.groupBoxVNAControl.Controls.Add(this.labelCalibrate);
            this.groupBoxVNAControl.Controls.Add(this.labelMeasure);
            this.groupBoxVNAControl.Controls.Add(this.checkBoxShowScreen);
            this.groupBoxVNAControl.Controls.Add(this.listViewCalibrations);
            this.groupBoxVNAControl.Controls.Add(this.buttonCalibrate);
            this.groupBoxVNAControl.Controls.Add(this.buttonVNAInfo);
            this.groupBoxVNAControl.Controls.Add(this.labelStatus);
            this.groupBoxVNAControl.Controls.Add(this.buttonSweep);
            this.groupBoxVNAControl.Controls.Add(this.buttonRun);
            this.groupBoxVNAControl.Controls.Add(this.buttonConnect);
            this.groupBoxVNAControl.Controls.Add(this.progressBarSweep);
            this.groupBoxVNAControl.Controls.Add(this.buttonStop);
            this.groupBoxVNAControl.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBoxVNAControl.ForeColor = System.Drawing.Color.DodgerBlue;
            this.groupBoxVNAControl.Location = new System.Drawing.Point(12, 12);
            this.groupBoxVNAControl.Name = "groupBoxVNAControl";
            this.groupBoxVNAControl.Size = new System.Drawing.Size(396, 278);
            this.groupBoxVNAControl.TabIndex = 15;
            this.groupBoxVNAControl.TabStop = false;
            this.groupBoxVNAControl.Text = "VNA Control";
            // 
            // buttonLEDPG
            // 
            this.buttonLEDPG.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonLEDPG.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonLEDPG.Location = new System.Drawing.Point(287, 74);
            this.buttonLEDPG.Name = "buttonLEDPG";
            this.buttonLEDPG.Size = new System.Drawing.Size(75, 23);
            this.buttonLEDPG.TabIndex = 24;
            this.buttonLEDPG.Text = "LED PG";
            this.buttonLEDPG.UseVisualStyleBackColor = true;
            this.buttonLEDPG.Click += new System.EventHandler(this.buttonLEDPG_Click);
            // 
            // buttonLEDP2
            // 
            this.buttonLEDP2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonLEDP2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonLEDP2.Location = new System.Drawing.Point(287, 45);
            this.buttonLEDP2.Name = "buttonLEDP2";
            this.buttonLEDP2.Size = new System.Drawing.Size(75, 23);
            this.buttonLEDP2.TabIndex = 23;
            this.buttonLEDP2.Text = "LED P2";
            this.buttonLEDP2.UseVisualStyleBackColor = true;
            this.buttonLEDP2.Click += new System.EventHandler(this.buttonLEDP2_Click);
            // 
            // buttonLEDP1
            // 
            this.buttonLEDP1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonLEDP1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonLEDP1.Location = new System.Drawing.Point(287, 16);
            this.buttonLEDP1.Name = "buttonLEDP1";
            this.buttonLEDP1.Size = new System.Drawing.Size(75, 23);
            this.buttonLEDP1.TabIndex = 22;
            this.buttonLEDP1.Text = "LED P1";
            this.buttonLEDP1.UseVisualStyleBackColor = true;
            this.buttonLEDP1.Click += new System.EventHandler(this.buttonLEDP1_Click);
            // 
            // labelCalibrate
            // 
            this.labelCalibrate.AutoSize = true;
            this.labelCalibrate.Location = new System.Drawing.Point(130, 110);
            this.labelCalibrate.Name = "labelCalibrate";
            this.labelCalibrate.Size = new System.Drawing.Size(71, 16);
            this.labelCalibrate.TabIndex = 21;
            this.labelCalibrate.Text = "Calibrate";
            // 
            // labelMeasure
            // 
            this.labelMeasure.AutoSize = true;
            this.labelMeasure.Location = new System.Drawing.Point(6, 110);
            this.labelMeasure.Name = "labelMeasure";
            this.labelMeasure.Size = new System.Drawing.Size(68, 16);
            this.labelMeasure.TabIndex = 20;
            this.labelMeasure.Text = "Measure";
            // 
            // checkBoxShowScreen
            // 
            this.checkBoxShowScreen.AutoSize = true;
            this.checkBoxShowScreen.Checked = true;
            this.checkBoxShowScreen.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxShowScreen.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxShowScreen.ForeColor = System.Drawing.SystemColors.ControlText;
            this.checkBoxShowScreen.Location = new System.Drawing.Point(9, 51);
            this.checkBoxShowScreen.Name = "checkBoxShowScreen";
            this.checkBoxShowScreen.Size = new System.Drawing.Size(90, 17);
            this.checkBoxShowScreen.TabIndex = 19;
            this.checkBoxShowScreen.Text = "Show Screen";
            this.checkBoxShowScreen.UseVisualStyleBackColor = true;
            this.checkBoxShowScreen.CheckedChanged += new System.EventHandler(this.checkBoxShowScreen_CheckedChanged);
            // 
            // listViewCalibrations
            // 
            this.listViewCalibrations.Location = new System.Drawing.Point(226, 129);
            this.listViewCalibrations.Name = "listViewCalibrations";
            this.listViewCalibrations.Size = new System.Drawing.Size(164, 142);
            this.listViewCalibrations.TabIndex = 18;
            this.listViewCalibrations.UseCompatibleStateImageBehavior = false;
            this.listViewCalibrations.View = System.Windows.Forms.View.List;
            this.listViewCalibrations.DoubleClick += new System.EventHandler(this.buttonCalibrate_Click);
            // 
            // buttonCalibrate
            // 
            this.buttonCalibrate.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonCalibrate.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonCalibrate.Location = new System.Drawing.Point(133, 129);
            this.buttonCalibrate.Name = "buttonCalibrate";
            this.buttonCalibrate.Size = new System.Drawing.Size(75, 23);
            this.buttonCalibrate.TabIndex = 16;
            this.buttonCalibrate.Text = "Calibrate";
            this.buttonCalibrate.UseVisualStyleBackColor = true;
            this.buttonCalibrate.Click += new System.EventHandler(this.buttonCalibrate_Click);
            // 
            // buttonVNAInfo
            // 
            this.buttonVNAInfo.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonVNAInfo.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonVNAInfo.Location = new System.Drawing.Point(186, 55);
            this.buttonVNAInfo.Name = "buttonVNAInfo";
            this.buttonVNAInfo.Size = new System.Drawing.Size(75, 23);
            this.buttonVNAInfo.TabIndex = 17;
            this.buttonVNAInfo.Text = "VNA Info";
            this.buttonVNAInfo.UseVisualStyleBackColor = true;
            this.buttonVNAInfo.Click += new System.EventHandler(this.buttonVNAInfo_Click);
            // 
            // labelStatus
            // 
            this.labelStatus.AutoSize = true;
            this.labelStatus.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelStatus.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelStatus.Location = new System.Drawing.Point(6, 21);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(63, 13);
            this.labelStatus.TabIndex = 16;
            this.labelStatus.Text = "VNA status:";
            // 
            // listViewParameters
            // 
            this.listViewParameters.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnParameter,
            this.columnHeaderMin,
            this.columnHeaderMax,
            this.columnHeaderStart,
            this.columnHeaderStop,
            this.columnHeaderSteps,
            this.columnHeaderDim});
            this.listViewParameters.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listViewParameters.ForeColor = System.Drawing.SystemColors.ControlText;
            this.listViewParameters.Location = new System.Drawing.Point(9, 256);
            this.listViewParameters.Name = "listViewParameters";
            this.listViewParameters.Size = new System.Drawing.Size(472, 138);
            this.listViewParameters.TabIndex = 16;
            this.listViewParameters.UseCompatibleStateImageBehavior = false;
            this.listViewParameters.View = System.Windows.Forms.View.Details;
            this.listViewParameters.DoubleClick += new System.EventHandler(this.listViewParameters_DoubleClick);
            // 
            // columnParameter
            // 
            this.columnParameter.Text = "Parameter";
            this.columnParameter.Width = 104;
            // 
            // columnHeaderMin
            // 
            this.columnHeaderMin.Text = "Min";
            // 
            // columnHeaderMax
            // 
            this.columnHeaderMax.Text = "Max";
            // 
            // columnHeaderStart
            // 
            this.columnHeaderStart.Text = "Start";
            // 
            // columnHeaderStop
            // 
            this.columnHeaderStop.Text = "Stop";
            // 
            // columnHeaderSteps
            // 
            this.columnHeaderSteps.Text = "Steps";
            // 
            // columnHeaderDim
            // 
            this.columnHeaderDim.Text = "Dim";
            // 
            // listViewMeasurements
            // 
            this.listViewMeasurements.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeaderName,
            this.columnHeaderDate,
            this.columnHeaderTime,
            this.columnHeaderKey});
            this.listViewMeasurements.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listViewMeasurements.ForeColor = System.Drawing.SystemColors.ControlText;
            this.listViewMeasurements.Location = new System.Drawing.Point(9, 75);
            this.listViewMeasurements.MultiSelect = false;
            this.listViewMeasurements.Name = "listViewMeasurements";
            this.listViewMeasurements.Size = new System.Drawing.Size(381, 220);
            this.listViewMeasurements.TabIndex = 17;
            this.listViewMeasurements.UseCompatibleStateImageBehavior = false;
            this.listViewMeasurements.View = System.Windows.Forms.View.Details;
            this.listViewMeasurements.SelectedIndexChanged += new System.EventHandler(this.listViewMeasurements_SelectedIndexChanged);
            this.listViewMeasurements.DoubleClick += new System.EventHandler(this.listViewMeasurements_DoubleClick);
            // 
            // columnHeaderName
            // 
            this.columnHeaderName.Text = "Name";
            this.columnHeaderName.Width = 178;
            // 
            // columnHeaderDate
            // 
            this.columnHeaderDate.Text = "Date";
            this.columnHeaderDate.Width = 67;
            // 
            // columnHeaderTime
            // 
            this.columnHeaderTime.Text = "Time";
            // 
            // columnHeaderKey
            // 
            this.columnHeaderKey.Text = "Key";
            this.columnHeaderKey.Width = 71;
            // 
            // buttonPresetsVNS
            // 
            this.buttonPresetsVNS.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonPresetsVNS.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonPresetsVNS.Location = new System.Drawing.Point(315, 45);
            this.buttonPresetsVNS.Name = "buttonPresetsVNS";
            this.buttonPresetsVNS.Size = new System.Drawing.Size(75, 23);
            this.buttonPresetsVNS.TabIndex = 18;
            this.buttonPresetsVNS.Text = "Presets";
            this.buttonPresetsVNS.UseVisualStyleBackColor = true;
            this.buttonPresetsVNS.Click += new System.EventHandler(this.buttonPresetsVNS_Click);
            // 
            // buttonSaveSelectedItem
            // 
            this.buttonSaveSelectedItem.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSaveSelectedItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonSaveSelectedItem.Location = new System.Drawing.Point(9, 301);
            this.buttonSaveSelectedItem.Name = "buttonSaveSelectedItem";
            this.buttonSaveSelectedItem.Size = new System.Drawing.Size(86, 43);
            this.buttonSaveSelectedItem.TabIndex = 19;
            this.buttonSaveSelectedItem.Text = "Save Selected Item";
            this.buttonSaveSelectedItem.UseVisualStyleBackColor = true;
            this.buttonSaveSelectedItem.Click += new System.EventHandler(this.buttonSaveSelectedItem_Click);
            // 
            // buttonSaveCurrentItem
            // 
            this.buttonSaveCurrentItem.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSaveCurrentItem.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonSaveCurrentItem.Location = new System.Drawing.Point(101, 301);
            this.buttonSaveCurrentItem.Name = "buttonSaveCurrentItem";
            this.buttonSaveCurrentItem.Size = new System.Drawing.Size(86, 43);
            this.buttonSaveCurrentItem.TabIndex = 20;
            this.buttonSaveCurrentItem.Text = "Save Current Item";
            this.buttonSaveCurrentItem.UseVisualStyleBackColor = true;
            this.buttonSaveCurrentItem.Click += new System.EventHandler(this.buttonSaveCurrentItem_Click);
            // 
            // buttonSaveSession
            // 
            this.buttonSaveSession.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSaveSession.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonSaveSession.Location = new System.Drawing.Point(193, 301);
            this.buttonSaveSession.Name = "buttonSaveSession";
            this.buttonSaveSession.Size = new System.Drawing.Size(75, 43);
            this.buttonSaveSession.TabIndex = 21;
            this.buttonSaveSession.Text = "Save Session";
            this.buttonSaveSession.UseVisualStyleBackColor = true;
            this.buttonSaveSession.Click += new System.EventHandler(this.buttonSaveSession_Click);
            // 
            // labelParameters
            // 
            this.labelParameters.AutoSize = true;
            this.labelParameters.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelParameters.Location = new System.Drawing.Point(13, 240);
            this.labelParameters.Name = "labelParameters";
            this.labelParameters.Size = new System.Drawing.Size(88, 16);
            this.labelParameters.TabIndex = 22;
            this.labelParameters.Text = "Parameters";
            // 
            // labelData
            // 
            this.labelData.AutoSize = true;
            this.labelData.Location = new System.Drawing.Point(13, 397);
            this.labelData.Name = "labelData";
            this.labelData.Size = new System.Drawing.Size(41, 16);
            this.labelData.TabIndex = 23;
            this.labelData.Text = "Data";
            // 
            // labelName
            // 
            this.labelName.AutoSize = true;
            this.labelName.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelName.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelName.Location = new System.Drawing.Point(6, 21);
            this.labelName.Name = "labelName";
            this.labelName.Size = new System.Drawing.Size(38, 13);
            this.labelName.TabIndex = 25;
            this.labelName.Text = "Name:";
            // 
            // labelDate
            // 
            this.labelDate.AutoSize = true;
            this.labelDate.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelDate.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelDate.Location = new System.Drawing.Point(6, 47);
            this.labelDate.Name = "labelDate";
            this.labelDate.Size = new System.Drawing.Size(61, 13);
            this.labelDate.TabIndex = 26;
            this.labelDate.Text = "Date/Time:";
            // 
            // groupBoxSession
            // 
            this.groupBoxSession.Controls.Add(this.checkBoxSaveData);
            this.groupBoxSession.Controls.Add(this.checkBoxSaveCal);
            this.groupBoxSession.Controls.Add(this.textBoxFile);
            this.groupBoxSession.Controls.Add(this.labelFile);
            this.groupBoxSession.Controls.Add(this.buttonSaveSession);
            this.groupBoxSession.Controls.Add(this.buttonSaveCurrentItem);
            this.groupBoxSession.Controls.Add(this.buttonSaveSelectedItem);
            this.groupBoxSession.Controls.Add(this.buttonPresetsVNS);
            this.groupBoxSession.Controls.Add(this.listViewMeasurements);
            this.groupBoxSession.Controls.Add(this.buttonOpenVNS);
            this.groupBoxSession.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBoxSession.ForeColor = System.Drawing.Color.DodgerBlue;
            this.groupBoxSession.Location = new System.Drawing.Point(12, 296);
            this.groupBoxSession.Name = "groupBoxSession";
            this.groupBoxSession.Size = new System.Drawing.Size(396, 350);
            this.groupBoxSession.TabIndex = 27;
            this.groupBoxSession.TabStop = false;
            this.groupBoxSession.Text = "Session";
            // 
            // checkBoxSaveData
            // 
            this.checkBoxSaveData.AutoSize = true;
            this.checkBoxSaveData.Checked = true;
            this.checkBoxSaveData.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxSaveData.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxSaveData.ForeColor = System.Drawing.SystemColors.ControlText;
            this.checkBoxSaveData.Location = new System.Drawing.Point(293, 324);
            this.checkBoxSaveData.Name = "checkBoxSaveData";
            this.checkBoxSaveData.Size = new System.Drawing.Size(77, 17);
            this.checkBoxSaveData.TabIndex = 25;
            this.checkBoxSaveData.Text = "Save Data";
            this.checkBoxSaveData.UseVisualStyleBackColor = true;
            // 
            // checkBoxSaveCal
            // 
            this.checkBoxSaveCal.AutoSize = true;
            this.checkBoxSaveCal.Checked = true;
            this.checkBoxSaveCal.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxSaveCal.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxSaveCal.ForeColor = System.Drawing.SystemColors.ControlText;
            this.checkBoxSaveCal.Location = new System.Drawing.Point(293, 301);
            this.checkBoxSaveCal.Name = "checkBoxSaveCal";
            this.checkBoxSaveCal.Size = new System.Drawing.Size(103, 17);
            this.checkBoxSaveCal.TabIndex = 24;
            this.checkBoxSaveCal.Text = "Save Calibration";
            this.checkBoxSaveCal.UseVisualStyleBackColor = true;
            // 
            // textBoxFile
            // 
            this.textBoxFile.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxFile.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBoxFile.Location = new System.Drawing.Point(38, 17);
            this.textBoxFile.Multiline = true;
            this.textBoxFile.Name = "textBoxFile";
            this.textBoxFile.Size = new System.Drawing.Size(261, 51);
            this.textBoxFile.TabIndex = 23;
            // 
            // labelFile
            // 
            this.labelFile.AutoSize = true;
            this.labelFile.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFile.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelFile.Location = new System.Drawing.Point(6, 24);
            this.labelFile.Name = "labelFile";
            this.labelFile.Size = new System.Drawing.Size(26, 13);
            this.labelFile.TabIndex = 22;
            this.labelFile.Text = "File:";
            // 
            // groupBoxMeasurement
            // 
            this.groupBoxMeasurement.Controls.Add(this.groupBoxBiasPGen);
            this.groupBoxMeasurement.Controls.Add(this.groupBoxBiasP2);
            this.groupBoxMeasurement.Controls.Add(this.labelBias);
            this.groupBoxMeasurement.Controls.Add(this.labelGenIdle);
            this.groupBoxMeasurement.Controls.Add(this.groupBoxBiasP1);
            this.groupBoxMeasurement.Controls.Add(this.groupBoxGenIdle);
            this.groupBoxMeasurement.Controls.Add(this.buttonRefresh);
            this.groupBoxMeasurement.Controls.Add(this.buttonClearCal);
            this.groupBoxMeasurement.Controls.Add(this.checkBoxUseCalibration);
            this.groupBoxMeasurement.Controls.Add(this.checkBoxDualCalKit);
            this.groupBoxMeasurement.Controls.Add(this.textBoxMeasurementDate);
            this.groupBoxMeasurement.Controls.Add(this.textBoxMeasurementName);
            this.groupBoxMeasurement.Controls.Add(this.buttonClearData);
            this.groupBoxMeasurement.Controls.Add(this.buttonRenormalize);
            this.groupBoxMeasurement.Controls.Add(this.labelDate);
            this.groupBoxMeasurement.Controls.Add(this.labelName);
            this.groupBoxMeasurement.Controls.Add(this.labelData);
            this.groupBoxMeasurement.Controls.Add(this.labelParameters);
            this.groupBoxMeasurement.Controls.Add(this.listViewParameters);
            this.groupBoxMeasurement.Controls.Add(this.treeViewData);
            this.groupBoxMeasurement.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.groupBoxMeasurement.ForeColor = System.Drawing.Color.DodgerBlue;
            this.groupBoxMeasurement.Location = new System.Drawing.Point(414, 12);
            this.groupBoxMeasurement.Name = "groupBoxMeasurement";
            this.groupBoxMeasurement.Size = new System.Drawing.Size(489, 634);
            this.groupBoxMeasurement.TabIndex = 28;
            this.groupBoxMeasurement.TabStop = false;
            this.groupBoxMeasurement.Text = "Measurement";
            // 
            // groupBoxBiasPGen
            // 
            this.groupBoxBiasPGen.Controls.Add(this.radioButtonBiasPGOn);
            this.groupBoxBiasPGen.Controls.Add(this.radioButtonBiasPGGnd);
            this.groupBoxBiasPGen.Controls.Add(this.radioButtonBiasPGOff);
            this.groupBoxBiasPGen.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.groupBoxBiasPGen.Location = new System.Drawing.Point(406, 125);
            this.groupBoxBiasPGen.Name = "groupBoxBiasPGen";
            this.groupBoxBiasPGen.Size = new System.Drawing.Size(77, 94);
            this.groupBoxBiasPGen.TabIndex = 31;
            this.groupBoxBiasPGen.TabStop = false;
            // 
            // radioButtonBiasPGOn
            // 
            this.radioButtonBiasPGOn.AutoSize = true;
            this.radioButtonBiasPGOn.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasPGOn.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasPGOn.Location = new System.Drawing.Point(6, 67);
            this.radioButtonBiasPGOn.Name = "radioButtonBiasPGOn";
            this.radioButtonBiasPGOn.Size = new System.Drawing.Size(57, 17);
            this.radioButtonBiasPGOn.TabIndex = 2;
            this.radioButtonBiasPGOn.Text = "PG On";
            this.radioButtonBiasPGOn.UseVisualStyleBackColor = true;
            this.radioButtonBiasPGOn.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasPGGnd
            // 
            this.radioButtonBiasPGGnd.AutoSize = true;
            this.radioButtonBiasPGGnd.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasPGGnd.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasPGGnd.Location = new System.Drawing.Point(7, 44);
            this.radioButtonBiasPGGnd.Name = "radioButtonBiasPGGnd";
            this.radioButtonBiasPGGnd.Size = new System.Drawing.Size(63, 17);
            this.radioButtonBiasPGGnd.TabIndex = 1;
            this.radioButtonBiasPGGnd.Text = "PG Gnd";
            this.radioButtonBiasPGGnd.UseVisualStyleBackColor = true;
            this.radioButtonBiasPGGnd.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasPGOff
            // 
            this.radioButtonBiasPGOff.AutoSize = true;
            this.radioButtonBiasPGOff.Checked = true;
            this.radioButtonBiasPGOff.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasPGOff.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasPGOff.Location = new System.Drawing.Point(7, 20);
            this.radioButtonBiasPGOff.Name = "radioButtonBiasPGOff";
            this.radioButtonBiasPGOff.Size = new System.Drawing.Size(57, 17);
            this.radioButtonBiasPGOff.TabIndex = 0;
            this.radioButtonBiasPGOff.TabStop = true;
            this.radioButtonBiasPGOff.Text = "PG Off";
            this.radioButtonBiasPGOff.UseVisualStyleBackColor = true;
            this.radioButtonBiasPGOff.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // groupBoxBiasP2
            // 
            this.groupBoxBiasP2.Controls.Add(this.radioButtonBiasP2On);
            this.groupBoxBiasP2.Controls.Add(this.radioButtonBiasP2Gnd);
            this.groupBoxBiasP2.Controls.Add(this.radioButtonBiasP2Off);
            this.groupBoxBiasP2.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.groupBoxBiasP2.Location = new System.Drawing.Point(322, 125);
            this.groupBoxBiasP2.Name = "groupBoxBiasP2";
            this.groupBoxBiasP2.Size = new System.Drawing.Size(77, 94);
            this.groupBoxBiasP2.TabIndex = 31;
            this.groupBoxBiasP2.TabStop = false;
            // 
            // radioButtonBiasP2On
            // 
            this.radioButtonBiasP2On.AutoSize = true;
            this.radioButtonBiasP2On.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP2On.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP2On.Location = new System.Drawing.Point(6, 67);
            this.radioButtonBiasP2On.Name = "radioButtonBiasP2On";
            this.radioButtonBiasP2On.Size = new System.Drawing.Size(55, 17);
            this.radioButtonBiasP2On.TabIndex = 2;
            this.radioButtonBiasP2On.Text = "P2 On";
            this.radioButtonBiasP2On.UseVisualStyleBackColor = true;
            this.radioButtonBiasP2On.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasP2Gnd
            // 
            this.radioButtonBiasP2Gnd.AutoSize = true;
            this.radioButtonBiasP2Gnd.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP2Gnd.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP2Gnd.Location = new System.Drawing.Point(7, 44);
            this.radioButtonBiasP2Gnd.Name = "radioButtonBiasP2Gnd";
            this.radioButtonBiasP2Gnd.Size = new System.Drawing.Size(61, 17);
            this.radioButtonBiasP2Gnd.TabIndex = 1;
            this.radioButtonBiasP2Gnd.Text = "P2 Gnd";
            this.radioButtonBiasP2Gnd.UseVisualStyleBackColor = true;
            this.radioButtonBiasP2Gnd.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasP2Off
            // 
            this.radioButtonBiasP2Off.AutoSize = true;
            this.radioButtonBiasP2Off.Checked = true;
            this.radioButtonBiasP2Off.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP2Off.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP2Off.Location = new System.Drawing.Point(7, 20);
            this.radioButtonBiasP2Off.Name = "radioButtonBiasP2Off";
            this.radioButtonBiasP2Off.Size = new System.Drawing.Size(55, 17);
            this.radioButtonBiasP2Off.TabIndex = 0;
            this.radioButtonBiasP2Off.TabStop = true;
            this.radioButtonBiasP2Off.Text = "P2 Off";
            this.radioButtonBiasP2Off.UseVisualStyleBackColor = true;
            this.radioButtonBiasP2Off.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // labelBias
            // 
            this.labelBias.AutoSize = true;
            this.labelBias.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelBias.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelBias.Location = new System.Drawing.Point(202, 147);
            this.labelBias.Name = "labelBias";
            this.labelBias.Size = new System.Drawing.Size(30, 13);
            this.labelBias.TabIndex = 36;
            this.labelBias.Text = "Bias:";
            // 
            // labelGenIdle
            // 
            this.labelGenIdle.AutoSize = true;
            this.labelGenIdle.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelGenIdle.ForeColor = System.Drawing.SystemColors.ControlText;
            this.labelGenIdle.Location = new System.Drawing.Point(9, 147);
            this.labelGenIdle.Name = "labelGenIdle";
            this.labelGenIdle.Size = new System.Drawing.Size(50, 13);
            this.labelGenIdle.TabIndex = 35;
            this.labelGenIdle.Text = "Gen Idle:";
            // 
            // groupBoxBiasP1
            // 
            this.groupBoxBiasP1.Controls.Add(this.radioButtonBiasP1On);
            this.groupBoxBiasP1.Controls.Add(this.radioButtonBiasP1Gnd);
            this.groupBoxBiasP1.Controls.Add(this.radioButtonBiasP1Off);
            this.groupBoxBiasP1.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.groupBoxBiasP1.Location = new System.Drawing.Point(238, 125);
            this.groupBoxBiasP1.Name = "groupBoxBiasP1";
            this.groupBoxBiasP1.Size = new System.Drawing.Size(77, 94);
            this.groupBoxBiasP1.TabIndex = 30;
            this.groupBoxBiasP1.TabStop = false;
            // 
            // radioButtonBiasP1On
            // 
            this.radioButtonBiasP1On.AutoSize = true;
            this.radioButtonBiasP1On.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP1On.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP1On.Location = new System.Drawing.Point(6, 67);
            this.radioButtonBiasP1On.Name = "radioButtonBiasP1On";
            this.radioButtonBiasP1On.Size = new System.Drawing.Size(55, 17);
            this.radioButtonBiasP1On.TabIndex = 2;
            this.radioButtonBiasP1On.Text = "P1 On";
            this.radioButtonBiasP1On.UseVisualStyleBackColor = true;
            this.radioButtonBiasP1On.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasP1Gnd
            // 
            this.radioButtonBiasP1Gnd.AutoSize = true;
            this.radioButtonBiasP1Gnd.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP1Gnd.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP1Gnd.Location = new System.Drawing.Point(7, 44);
            this.radioButtonBiasP1Gnd.Name = "radioButtonBiasP1Gnd";
            this.radioButtonBiasP1Gnd.Size = new System.Drawing.Size(61, 17);
            this.radioButtonBiasP1Gnd.TabIndex = 1;
            this.radioButtonBiasP1Gnd.Text = "P1 Gnd";
            this.radioButtonBiasP1Gnd.UseVisualStyleBackColor = true;
            this.radioButtonBiasP1Gnd.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // radioButtonBiasP1Off
            // 
            this.radioButtonBiasP1Off.AutoSize = true;
            this.radioButtonBiasP1Off.Checked = true;
            this.radioButtonBiasP1Off.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonBiasP1Off.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonBiasP1Off.Location = new System.Drawing.Point(7, 20);
            this.radioButtonBiasP1Off.Name = "radioButtonBiasP1Off";
            this.radioButtonBiasP1Off.Size = new System.Drawing.Size(55, 17);
            this.radioButtonBiasP1Off.TabIndex = 0;
            this.radioButtonBiasP1Off.TabStop = true;
            this.radioButtonBiasP1Off.Text = "P1 Off";
            this.radioButtonBiasP1Off.UseVisualStyleBackColor = true;
            this.radioButtonBiasP1Off.CheckedChanged += new System.EventHandler(this.radioButtonBias_CheckedChanged);
            // 
            // groupBoxGenIdle
            // 
            this.groupBoxGenIdle.Controls.Add(this.radioButtonGenPGen);
            this.groupBoxGenIdle.Controls.Add(this.radioButtonGenP2);
            this.groupBoxGenIdle.Controls.Add(this.radioButtonGenP1);
            this.groupBoxGenIdle.Controls.Add(this.radioButtonGenOff);
            this.groupBoxGenIdle.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.groupBoxGenIdle.Location = new System.Drawing.Point(65, 125);
            this.groupBoxGenIdle.Name = "groupBoxGenIdle";
            this.groupBoxGenIdle.Size = new System.Drawing.Size(81, 112);
            this.groupBoxGenIdle.TabIndex = 29;
            this.groupBoxGenIdle.TabStop = false;
            // 
            // radioButtonGenPGen
            // 
            this.radioButtonGenPGen.AutoSize = true;
            this.radioButtonGenPGen.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonGenPGen.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonGenPGen.Location = new System.Drawing.Point(7, 90);
            this.radioButtonGenPGen.Name = "radioButtonGenPGen";
            this.radioButtonGenPGen.Size = new System.Drawing.Size(67, 17);
            this.radioButtonGenPGen.TabIndex = 3;
            this.radioButtonGenPGen.Text = "Port Gen";
            this.radioButtonGenPGen.UseVisualStyleBackColor = true;
            this.radioButtonGenPGen.CheckedChanged += new System.EventHandler(this.radioButtonGenIdle_CheckedChanged);
            // 
            // radioButtonGenP2
            // 
            this.radioButtonGenP2.AutoSize = true;
            this.radioButtonGenP2.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonGenP2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonGenP2.Location = new System.Drawing.Point(6, 67);
            this.radioButtonGenP2.Name = "radioButtonGenP2";
            this.radioButtonGenP2.Size = new System.Drawing.Size(53, 17);
            this.radioButtonGenP2.TabIndex = 2;
            this.radioButtonGenP2.Text = "Port 2";
            this.radioButtonGenP2.UseVisualStyleBackColor = true;
            this.radioButtonGenP2.CheckedChanged += new System.EventHandler(this.radioButtonGenIdle_CheckedChanged);
            // 
            // radioButtonGenP1
            // 
            this.radioButtonGenP1.AutoSize = true;
            this.radioButtonGenP1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonGenP1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonGenP1.Location = new System.Drawing.Point(7, 44);
            this.radioButtonGenP1.Name = "radioButtonGenP1";
            this.radioButtonGenP1.Size = new System.Drawing.Size(53, 17);
            this.radioButtonGenP1.TabIndex = 1;
            this.radioButtonGenP1.Text = "Port 1";
            this.radioButtonGenP1.UseVisualStyleBackColor = true;
            this.radioButtonGenP1.CheckedChanged += new System.EventHandler(this.radioButtonGenIdle_CheckedChanged);
            // 
            // radioButtonGenOff
            // 
            this.radioButtonGenOff.AutoSize = true;
            this.radioButtonGenOff.Checked = true;
            this.radioButtonGenOff.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.radioButtonGenOff.ForeColor = System.Drawing.SystemColors.ControlText;
            this.radioButtonGenOff.Location = new System.Drawing.Point(7, 20);
            this.radioButtonGenOff.Name = "radioButtonGenOff";
            this.radioButtonGenOff.Size = new System.Drawing.Size(39, 17);
            this.radioButtonGenOff.TabIndex = 0;
            this.radioButtonGenOff.TabStop = true;
            this.radioButtonGenOff.Text = "Off";
            this.radioButtonGenOff.UseVisualStyleBackColor = true;
            this.radioButtonGenOff.CheckedChanged += new System.EventHandler(this.radioButtonGenIdle_CheckedChanged);
            // 
            // buttonRefresh
            // 
            this.buttonRefresh.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonRefresh.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonRefresh.Location = new System.Drawing.Point(406, 84);
            this.buttonRefresh.Name = "buttonRefresh";
            this.buttonRefresh.Size = new System.Drawing.Size(75, 23);
            this.buttonRefresh.TabIndex = 34;
            this.buttonRefresh.Text = "Refresh";
            this.buttonRefresh.UseVisualStyleBackColor = true;
            this.buttonRefresh.Click += new System.EventHandler(this.buttonRefresh_Click);
            // 
            // buttonClearCal
            // 
            this.buttonClearCal.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonClearCal.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonClearCal.Location = new System.Drawing.Point(325, 85);
            this.buttonClearCal.Name = "buttonClearCal";
            this.buttonClearCal.Size = new System.Drawing.Size(75, 23);
            this.buttonClearCal.TabIndex = 33;
            this.buttonClearCal.Text = "ClearCal";
            this.buttonClearCal.UseVisualStyleBackColor = true;
            this.buttonClearCal.Click += new System.EventHandler(this.buttonClearCal_Click);
            // 
            // checkBoxUseCalibration
            // 
            this.checkBoxUseCalibration.AutoSize = true;
            this.checkBoxUseCalibration.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxUseCalibration.ForeColor = System.Drawing.SystemColors.ControlText;
            this.checkBoxUseCalibration.Location = new System.Drawing.Point(143, 111);
            this.checkBoxUseCalibration.Name = "checkBoxUseCalibration";
            this.checkBoxUseCalibration.Size = new System.Drawing.Size(94, 17);
            this.checkBoxUseCalibration.TabIndex = 32;
            this.checkBoxUseCalibration.Text = "UseCalibration";
            this.checkBoxUseCalibration.UseVisualStyleBackColor = true;
            this.checkBoxUseCalibration.CheckedChanged += new System.EventHandler(this.checkBoxUseCalibration_CheckedChanged);
            // 
            // checkBoxDualCalKit
            // 
            this.checkBoxDualCalKit.AutoSize = true;
            this.checkBoxDualCalKit.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxDualCalKit.ForeColor = System.Drawing.SystemColors.ControlText;
            this.checkBoxDualCalKit.Location = new System.Drawing.Point(143, 88);
            this.checkBoxDualCalKit.Name = "checkBoxDualCalKit";
            this.checkBoxDualCalKit.Size = new System.Drawing.Size(75, 17);
            this.checkBoxDualCalKit.TabIndex = 31;
            this.checkBoxDualCalKit.Text = "DualCalKit";
            this.checkBoxDualCalKit.UseVisualStyleBackColor = true;
            this.checkBoxDualCalKit.CheckedChanged += new System.EventHandler(this.checkBoxDualCalKit_CheckedChanged);
            // 
            // textBoxMeasurementDate
            // 
            this.textBoxMeasurementDate.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxMeasurementDate.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBoxMeasurementDate.Location = new System.Drawing.Point(85, 44);
            this.textBoxMeasurementDate.Name = "textBoxMeasurementDate";
            this.textBoxMeasurementDate.ReadOnly = true;
            this.textBoxMeasurementDate.Size = new System.Drawing.Size(396, 20);
            this.textBoxMeasurementDate.TabIndex = 30;
            // 
            // textBoxMeasurementName
            // 
            this.textBoxMeasurementName.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxMeasurementName.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBoxMeasurementName.Location = new System.Drawing.Point(85, 18);
            this.textBoxMeasurementName.Name = "textBoxMeasurementName";
            this.textBoxMeasurementName.ReadOnly = true;
            this.textBoxMeasurementName.Size = new System.Drawing.Size(396, 20);
            this.textBoxMeasurementName.TabIndex = 29;
            // 
            // buttonClearData
            // 
            this.buttonClearData.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonClearData.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonClearData.Location = new System.Drawing.Point(244, 85);
            this.buttonClearData.Name = "buttonClearData";
            this.buttonClearData.Size = new System.Drawing.Size(75, 23);
            this.buttonClearData.TabIndex = 28;
            this.buttonClearData.Text = "Clear Data";
            this.buttonClearData.UseVisualStyleBackColor = true;
            this.buttonClearData.Click += new System.EventHandler(this.buttonClearData_Click);
            // 
            // buttonRenormalize
            // 
            this.buttonRenormalize.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonRenormalize.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonRenormalize.Location = new System.Drawing.Point(16, 85);
            this.buttonRenormalize.Name = "buttonRenormalize";
            this.buttonRenormalize.Size = new System.Drawing.Size(75, 23);
            this.buttonRenormalize.TabIndex = 27;
            this.buttonRenormalize.Text = "Renormalize";
            this.buttonRenormalize.UseVisualStyleBackColor = true;
            this.buttonRenormalize.Click += new System.EventHandler(this.buttonRenormalize_Click);
            // 
            // pictureBoxGraph
            // 
            this.pictureBoxGraph.BackColor = System.Drawing.Color.Black;
            this.pictureBoxGraph.Location = new System.Drawing.Point(12, 652);
            this.pictureBoxGraph.Name = "pictureBoxGraph";
            this.pictureBoxGraph.Size = new System.Drawing.Size(891, 207);
            this.pictureBoxGraph.TabIndex = 29;
            this.pictureBoxGraph.TabStop = false;
            // 
            // GUIMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(918, 871);
            this.Controls.Add(this.pictureBoxGraph);
            this.Controls.Add(this.groupBoxMeasurement);
            this.Controls.Add(this.groupBoxSession);
            this.Controls.Add(this.groupBoxVNAControl);
            this.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.SystemColors.ControlText;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "GUIMain";
            this.Text = "MegiQ VNA API";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.GUIMain_FormClosing);
            this.Load += new System.EventHandler(this.GUIMain_Load);
            this.groupBoxVNAControl.ResumeLayout(false);
            this.groupBoxVNAControl.PerformLayout();
            this.groupBoxSession.ResumeLayout(false);
            this.groupBoxSession.PerformLayout();
            this.groupBoxMeasurement.ResumeLayout(false);
            this.groupBoxMeasurement.PerformLayout();
            this.groupBoxBiasPGen.ResumeLayout(false);
            this.groupBoxBiasPGen.PerformLayout();
            this.groupBoxBiasP2.ResumeLayout(false);
            this.groupBoxBiasP2.PerformLayout();
            this.groupBoxBiasP1.ResumeLayout(false);
            this.groupBoxBiasP1.PerformLayout();
            this.groupBoxGenIdle.ResumeLayout(false);
            this.groupBoxGenIdle.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxGraph)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ProgressBar progressBarSweep;
        private System.Windows.Forms.Button buttonConnect;
        private System.Windows.Forms.Button buttonRun;
        private System.Windows.Forms.Button buttonSweep;
        private System.Windows.Forms.Button buttonStop;
        private System.Windows.Forms.Button buttonOpenVNS;
        private System.Windows.Forms.TreeView treeViewData;
        private System.Windows.Forms.GroupBox groupBoxVNAControl;
        private System.Windows.Forms.Label labelStatus;
        private System.Windows.Forms.Button buttonVNAInfo;
        private System.Windows.Forms.Button buttonCalibrate;
        private System.Windows.Forms.ListView listViewCalibrations;
        private System.Windows.Forms.ListView listViewParameters;
        private System.Windows.Forms.Label labelCalibrate;
        private System.Windows.Forms.Label labelMeasure;
        private System.Windows.Forms.CheckBox checkBoxShowScreen;
        private System.Windows.Forms.ColumnHeader columnParameter;
        private System.Windows.Forms.ColumnHeader columnHeaderMin;
        private System.Windows.Forms.ColumnHeader columnHeaderMax;
        private System.Windows.Forms.ColumnHeader columnHeaderStart;
        private System.Windows.Forms.ColumnHeader columnHeaderStop;
        private System.Windows.Forms.ColumnHeader columnHeaderSteps;
        private System.Windows.Forms.ColumnHeader columnHeaderDim;
        private System.Windows.Forms.ListView listViewMeasurements;
        private System.Windows.Forms.ColumnHeader columnHeaderName;
        private System.Windows.Forms.ColumnHeader columnHeaderDate;
        private System.Windows.Forms.ColumnHeader columnHeaderTime;
        private System.Windows.Forms.ColumnHeader columnHeaderKey;
        private System.Windows.Forms.Button buttonPresetsVNS;
        private System.Windows.Forms.Button buttonSaveSelectedItem;
        private System.Windows.Forms.Button buttonSaveCurrentItem;
        private System.Windows.Forms.Button buttonSaveSession;
        private System.Windows.Forms.Label labelParameters;
        private System.Windows.Forms.Label labelData;
        private System.Windows.Forms.Label labelName;
        private System.Windows.Forms.Label labelDate;
        private System.Windows.Forms.GroupBox groupBoxSession;
        private System.Windows.Forms.GroupBox groupBoxMeasurement;
        private System.Windows.Forms.Button buttonClearData;
        private System.Windows.Forms.Button buttonRenormalize;
        private System.Windows.Forms.Button buttonRefresh;
        private System.Windows.Forms.Button buttonClearCal;
        private System.Windows.Forms.CheckBox checkBoxUseCalibration;
        private System.Windows.Forms.CheckBox checkBoxDualCalKit;
        private System.Windows.Forms.TextBox textBoxMeasurementDate;
        private System.Windows.Forms.TextBox textBoxMeasurementName;
        private System.Windows.Forms.GroupBox groupBoxGenIdle;
        private System.Windows.Forms.RadioButton radioButtonGenPGen;
        private System.Windows.Forms.RadioButton radioButtonGenP2;
        private System.Windows.Forms.RadioButton radioButtonGenP1;
        private System.Windows.Forms.RadioButton radioButtonGenOff;
        private System.Windows.Forms.GroupBox groupBoxBiasPGen;
        private System.Windows.Forms.RadioButton radioButtonBiasPGOn;
        private System.Windows.Forms.RadioButton radioButtonBiasPGGnd;
        private System.Windows.Forms.RadioButton radioButtonBiasPGOff;
        private System.Windows.Forms.GroupBox groupBoxBiasP2;
        private System.Windows.Forms.RadioButton radioButtonBiasP2On;
        private System.Windows.Forms.RadioButton radioButtonBiasP2Gnd;
        private System.Windows.Forms.RadioButton radioButtonBiasP2Off;
        private System.Windows.Forms.Label labelBias;
        private System.Windows.Forms.Label labelGenIdle;
        private System.Windows.Forms.GroupBox groupBoxBiasP1;
        private System.Windows.Forms.RadioButton radioButtonBiasP1On;
        private System.Windows.Forms.RadioButton radioButtonBiasP1Gnd;
        private System.Windows.Forms.RadioButton radioButtonBiasP1Off;
        private System.Windows.Forms.Button buttonLEDPG;
        private System.Windows.Forms.Button buttonLEDP2;
        private System.Windows.Forms.Button buttonLEDP1;
        private System.Windows.Forms.TextBox textBoxFile;
        private System.Windows.Forms.Label labelFile;
        private System.Windows.Forms.CheckBox checkBoxSaveData;
        private System.Windows.Forms.CheckBox checkBoxSaveCal;
        private System.Windows.Forms.PictureBox pictureBoxGraph;
    }
}

