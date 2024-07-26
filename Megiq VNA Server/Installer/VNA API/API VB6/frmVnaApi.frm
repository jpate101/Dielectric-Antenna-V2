VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.1#0"; "MSCOMCTL.OCX"
Begin VB.Form frmVnaApi 
   AutoRedraw      =   -1  'True
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "MegiQ VNA API"
   ClientHeight    =   13170
   ClientLeft      =   45
   ClientTop       =   435
   ClientWidth     =   12915
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   13170
   ScaleWidth      =   12915
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame1 
      Caption         =   "VNA Control"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000D&
      Height          =   3615
      Left            =   120
      TabIndex        =   0
      Top             =   0
      Width           =   6015
      Begin VB.PictureBox Picture1 
         BorderStyle     =   0  'None
         Height          =   3255
         Left            =   120
         ScaleHeight     =   3255
         ScaleWidth      =   5775
         TabIndex        =   1
         Top             =   240
         Width           =   5775
         Begin VB.TextBox txtConnectSerial 
            Height          =   285
            Left            =   3960
            TabIndex        =   66
            Top             =   120
            Width           =   855
         End
         Begin VB.CommandButton cmdLedState 
            Caption         =   "LED PG"
            Height          =   255
            Index           =   4
            Left            =   4920
            TabIndex        =   65
            Top             =   840
            Width           =   855
         End
         Begin VB.CommandButton cmdLedState 
            Caption         =   "LED P2"
            Height          =   255
            Index           =   2
            Left            =   4920
            TabIndex        =   64
            Top             =   480
            Width           =   855
         End
         Begin VB.CommandButton cmdLedState 
            Caption         =   "LED P1"
            Height          =   255
            Index           =   1
            Left            =   4920
            TabIndex        =   63
            Top             =   120
            Width           =   855
         End
         Begin VB.CommandButton cmdVNAInfo 
            Caption         =   "VNA Info"
            Height          =   375
            Left            =   3840
            TabIndex        =   62
            Top             =   480
            Width           =   975
         End
         Begin VB.CommandButton cmdCalibrate 
            Caption         =   "Calibrate"
            Height          =   495
            Left            =   2040
            TabIndex        =   36
            Top             =   1440
            Width           =   1095
         End
         Begin VB.CheckBox chkVNAShow 
            Caption         =   "Show Screen"
            Height          =   255
            Left            =   120
            TabIndex        =   7
            Top             =   720
            Value           =   1  'Checked
            Width           =   1575
         End
         Begin VB.CommandButton cmdConnect 
            Caption         =   "Connect"
            Height          =   375
            Left            =   2640
            TabIndex        =   6
            Top             =   480
            Width           =   1095
         End
         Begin VB.CommandButton cmdRunSweepOnce 
            Caption         =   "Sweep"
            Height          =   495
            Left            =   120
            TabIndex        =   5
            Top             =   1440
            Width           =   1095
         End
         Begin VB.CommandButton cmdRunSweepContinuously 
            Caption         =   "Run"
            Height          =   495
            Left            =   120
            TabIndex        =   4
            Top             =   2040
            Width           =   1095
         End
         Begin VB.CommandButton cmdStopSweep 
            Caption         =   "Stop"
            Height          =   495
            Left            =   120
            TabIndex        =   3
            Top             =   2640
            Width           =   1095
         End
         Begin MSComctlLib.ProgressBar pgbProgress 
            Height          =   135
            Left            =   120
            TabIndex        =   2
            Top             =   480
            Width           =   2295
            _ExtentX        =   4048
            _ExtentY        =   238
            _Version        =   393216
            BorderStyle     =   1
            Appearance      =   0
         End
         Begin MSComctlLib.ListView lvwCalibrations 
            Height          =   1695
            Left            =   3240
            TabIndex        =   35
            Top             =   1440
            Width           =   2415
            _ExtentX        =   4260
            _ExtentY        =   2990
            View            =   3
            LabelEdit       =   1
            LabelWrap       =   0   'False
            HideSelection   =   0   'False
            HideColumnHeaders=   -1  'True
            _Version        =   393217
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            Appearance      =   1
            NumItems        =   1
            BeginProperty ColumnHeader(1) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               Key             =   "Cal"
               Text            =   "Calibration"
               Object.Width           =   3528
            EndProperty
         End
         Begin VB.Label Label11 
            Alignment       =   2  'Center
            Caption         =   "Conn. to serial:"
            Height          =   255
            Left            =   2640
            TabIndex        =   67
            Top             =   120
            Width           =   1215
         End
         Begin VB.Label Label8 
            Caption         =   "Measure"
            BeginProperty Font 
               Name            =   "MS Sans Serif"
               Size            =   9.75
               Charset         =   0
               Weight          =   700
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            ForeColor       =   &H8000000D&
            Height          =   255
            Left            =   120
            TabIndex        =   39
            Top             =   1080
            Width           =   1095
         End
         Begin VB.Label Label7 
            Caption         =   "Calibrate"
            BeginProperty Font 
               Name            =   "MS Sans Serif"
               Size            =   9.75
               Charset         =   0
               Weight          =   700
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            ForeColor       =   &H8000000D&
            Height          =   255
            Left            =   2040
            TabIndex        =   38
            Top             =   1080
            Width           =   3495
         End
         Begin VB.Label Label2 
            Caption         =   "VNA status:"
            Height          =   255
            Left            =   120
            TabIndex        =   9
            Top             =   120
            Width           =   855
         End
         Begin VB.Label lblVNAStatus 
            Caption         =   "lblVNAStatus"
            Height          =   255
            Left            =   1080
            TabIndex        =   8
            Top             =   120
            Width           =   1335
         End
      End
   End
   Begin VB.Frame fraMeasurement 
      Caption         =   "Measurement"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000D&
      Height          =   9615
      Left            =   6240
      TabIndex        =   22
      Top             =   0
      Width           =   6495
      Begin VB.PictureBox Picture3 
         BorderStyle     =   0  'None
         Height          =   9255
         Left            =   120
         ScaleHeight     =   9255
         ScaleWidth      =   6255
         TabIndex        =   23
         Top             =   240
         Width           =   6255
         Begin VB.PictureBox picGenIdle 
            Height          =   975
            Left            =   720
            ScaleHeight     =   915
            ScaleWidth      =   1035
            TabIndex        =   57
            Top             =   1440
            Width           =   1095
            Begin VB.OptionButton optGenIdle 
               Caption         =   "Port Gen"
               Height          =   255
               Index           =   3
               Left            =   0
               TabIndex        =   61
               Top             =   720
               Width           =   975
            End
            Begin VB.OptionButton optGenIdle 
               Caption         =   "Off"
               Height          =   255
               Index           =   0
               Left            =   0
               TabIndex        =   60
               Top             =   0
               Width           =   975
            End
            Begin VB.OptionButton optGenIdle 
               Caption         =   "Port 1"
               Height          =   255
               Index           =   1
               Left            =   0
               TabIndex        =   59
               Top             =   240
               Width           =   975
            End
            Begin VB.OptionButton optGenIdle 
               Caption         =   "Port 2"
               Height          =   255
               Index           =   2
               Left            =   0
               TabIndex        =   58
               Top             =   480
               Width           =   975
            End
         End
         Begin VB.PictureBox picBias 
            Height          =   735
            Index           =   2
            Left            =   5040
            ScaleHeight     =   675
            ScaleWidth      =   1035
            TabIndex        =   52
            Top             =   1440
            Width           =   1095
            Begin VB.OptionButton optBias3 
               Caption         =   "PG On"
               Height          =   255
               Index           =   2
               Left            =   0
               TabIndex        =   55
               Top             =   480
               Width           =   975
            End
            Begin VB.OptionButton optBias3 
               Caption         =   "PG Gnd"
               Height          =   255
               Index           =   1
               Left            =   0
               TabIndex        =   54
               Top             =   240
               Width           =   975
            End
            Begin VB.OptionButton optBias3 
               Caption         =   "PG Off"
               Height          =   255
               Index           =   0
               Left            =   0
               TabIndex        =   53
               Top             =   0
               Width           =   975
            End
         End
         Begin VB.PictureBox picBias 
            Height          =   735
            Index           =   1
            Left            =   3840
            ScaleHeight     =   675
            ScaleWidth      =   1035
            TabIndex        =   48
            Top             =   1440
            Width           =   1095
            Begin VB.OptionButton optBias2 
               Caption         =   "P2 Off"
               Height          =   255
               Index           =   0
               Left            =   0
               TabIndex        =   51
               Top             =   0
               Width           =   975
            End
            Begin VB.OptionButton optBias2 
               Caption         =   "P2 Gnd"
               Height          =   255
               Index           =   1
               Left            =   0
               TabIndex        =   50
               Top             =   240
               Width           =   975
            End
            Begin VB.OptionButton optBias2 
               Caption         =   "P2 On"
               Height          =   255
               Index           =   2
               Left            =   0
               TabIndex        =   49
               Top             =   480
               Width           =   975
            End
         End
         Begin VB.PictureBox picBias 
            Height          =   735
            Index           =   0
            Left            =   2640
            ScaleHeight     =   675
            ScaleWidth      =   1035
            TabIndex        =   43
            Top             =   1440
            Width           =   1095
            Begin VB.OptionButton optBias1 
               Caption         =   "P1 On"
               Height          =   255
               Index           =   2
               Left            =   0
               TabIndex        =   46
               Top             =   480
               Width           =   975
            End
            Begin VB.OptionButton optBias1 
               Caption         =   "P1 Gnd"
               Height          =   255
               Index           =   1
               Left            =   0
               TabIndex        =   45
               Top             =   240
               Width           =   975
            End
            Begin VB.OptionButton optBias1 
               Caption         =   "P1 Off"
               Height          =   255
               Index           =   0
               Left            =   0
               TabIndex        =   44
               Top             =   0
               Width           =   975
            End
         End
         Begin VB.CommandButton cmdUpdateMeasurement 
            Caption         =   "Refresh"
            Height          =   495
            Left            =   5040
            TabIndex        =   37
            ToolTipText     =   "Update from the VNA measurement"
            Top             =   840
            Width           =   1095
         End
         Begin VB.CheckBox chkDualCalkit 
            Caption         =   "DualCalkit"
            Height          =   255
            Left            =   1200
            TabIndex        =   32
            Top             =   840
            Width           =   1335
         End
         Begin VB.CheckBox chkUseCalibration 
            Caption         =   "UseCalibration"
            Height          =   255
            Left            =   1200
            TabIndex        =   31
            Top             =   1080
            Width           =   1335
         End
         Begin VB.CommandButton cmdRenormalize 
            Caption         =   "Renormalize"
            Height          =   495
            Left            =   0
            TabIndex        =   30
            Top             =   840
            Width           =   1095
         End
         Begin VB.CommandButton cmdClearData 
            Caption         =   "Clear Data"
            Height          =   495
            Left            =   2640
            TabIndex        =   25
            Top             =   840
            Width           =   1095
         End
         Begin VB.CommandButton cmdClearCalibration 
            Caption         =   "Clear Cal."
            Height          =   495
            Left            =   3840
            TabIndex        =   24
            Top             =   840
            Width           =   1095
         End
         Begin MSComctlLib.TreeView tvwTraceSet 
            Height          =   4695
            Left            =   0
            TabIndex        =   33
            Top             =   4440
            Width           =   6255
            _ExtentX        =   11033
            _ExtentY        =   8281
            _Version        =   393217
            HideSelection   =   0   'False
            LabelEdit       =   1
            Style           =   7
            Appearance      =   1
         End
         Begin MSComctlLib.ListView lvwParameters 
            Height          =   1575
            Left            =   0
            TabIndex        =   40
            Top             =   2640
            Width           =   6255
            _ExtentX        =   11033
            _ExtentY        =   2778
            View            =   3
            LabelEdit       =   1
            LabelWrap       =   0   'False
            HideSelection   =   -1  'True
            FullRowSelect   =   -1  'True
            GridLines       =   -1  'True
            _Version        =   393217
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            Appearance      =   1
            BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
               Name            =   "MS Sans Serif"
               Size            =   8.25
               Charset         =   0
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            NumItems        =   7
            BeginProperty ColumnHeader(1) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               Key             =   "Name"
               Text            =   "Parameter"
               Object.Width           =   3105
            EndProperty
            BeginProperty ColumnHeader(2) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   1
               Key             =   "Min"
               Text            =   "Min"
               Object.Width           =   1323
            EndProperty
            BeginProperty ColumnHeader(3) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   2
               Key             =   "Max"
               Text            =   "Max"
               Object.Width           =   1323
            EndProperty
            BeginProperty ColumnHeader(4) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   3
               Key             =   "Start"
               Text            =   "Start"
               Object.Width           =   1323
            EndProperty
            BeginProperty ColumnHeader(5) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   4
               Key             =   "Stop"
               Text            =   "Stop"
               Object.Width           =   1323
            EndProperty
            BeginProperty ColumnHeader(6) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   5
               Key             =   "Steps"
               Text            =   "Steps"
               Object.Width           =   1323
            EndProperty
            BeginProperty ColumnHeader(7) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   6
               Key             =   "Dim"
               Text            =   "Dim"
               Object.Width           =   1058
            EndProperty
         End
         Begin VB.Label Label10 
            Caption         =   "Gen Idle:"
            Height          =   255
            Left            =   0
            TabIndex        =   56
            Top             =   1440
            Width           =   855
         End
         Begin VB.Label Label1 
            Caption         =   "Bias:"
            Height          =   255
            Left            =   2160
            TabIndex        =   47
            Top             =   1440
            Width           =   495
         End
         Begin VB.Label Label9 
            Caption         =   "Parameters"
            BeginProperty Font 
               Name            =   "MS Sans Serif"
               Size            =   9.75
               Charset         =   0
               Weight          =   700
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            ForeColor       =   &H8000000D&
            Height          =   255
            Left            =   0
            TabIndex        =   41
            Top             =   2400
            Width           =   1575
         End
         Begin VB.Label Label3 
            Caption         =   "Data"
            BeginProperty Font 
               Name            =   "MS Sans Serif"
               Size            =   9.75
               Charset         =   0
               Weight          =   700
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            ForeColor       =   &H8000000D&
            Height          =   255
            Left            =   0
            TabIndex        =   34
            Top             =   4200
            Width           =   1575
         End
         Begin VB.Label lblMeasurementDateTime 
            BorderStyle     =   1  'Fixed Single
            Caption         =   "Label7"
            Height          =   255
            Left            =   1200
            TabIndex        =   29
            Top             =   480
            Width           =   4935
         End
         Begin VB.Label Label6 
            Caption         =   "Date/Time:"
            Height          =   255
            Left            =   0
            TabIndex        =   28
            Top             =   480
            Width           =   855
         End
         Begin VB.Label lblMeasurementName 
            BorderStyle     =   1  'Fixed Single
            Caption         =   "Label6"
            Height          =   255
            Left            =   1200
            TabIndex        =   27
            Top             =   120
            Width           =   4935
         End
         Begin VB.Label Label5 
            Caption         =   "Name:"
            Height          =   255
            Left            =   0
            TabIndex        =   26
            Top             =   120
            Width           =   855
         End
      End
   End
   Begin VB.PictureBox picPlot 
      AutoRedraw      =   -1  'True
      BackColor       =   &H00000000&
      Height          =   3375
      Left            =   120
      ScaleHeight     =   3315
      ScaleWidth      =   12555
      TabIndex        =   21
      Top             =   9720
      Width           =   12615
   End
   Begin VB.Frame fraSession 
      Caption         =   "Session"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000D&
      Height          =   5895
      Left            =   120
      TabIndex        =   10
      Top             =   3720
      Width           =   6015
      Begin VB.PictureBox Picture2 
         BorderStyle     =   0  'None
         Height          =   5535
         Left            =   120
         ScaleHeight     =   5535
         ScaleWidth      =   5775
         TabIndex        =   11
         Top             =   240
         Width           =   5775
         Begin VB.CommandButton cmdGetPresetSession 
            Caption         =   "Presets"
            Height          =   255
            Left            =   4560
            TabIndex        =   42
            Top             =   480
            Width           =   975
         End
         Begin VB.CheckBox chkSaveData 
            Caption         =   "Save Data"
            Height          =   255
            Left            =   3960
            TabIndex        =   20
            Top             =   5160
            Value           =   1  'Checked
            Width           =   1455
         End
         Begin VB.CheckBox chkSaveCalibration 
            Caption         =   "Save Calibration"
            Height          =   255
            Left            =   3960
            TabIndex        =   19
            Top             =   4920
            Value           =   1  'Checked
            Width           =   1455
         End
         Begin VB.CommandButton cmdSaveSelectedItem 
            Caption         =   "Save Selected Item"
            Height          =   495
            Left            =   240
            TabIndex        =   18
            Top             =   4920
            Width           =   1215
         End
         Begin VB.CommandButton cmdSaveCurrentItem 
            Caption         =   "Save Current Item"
            Height          =   495
            Left            =   1560
            TabIndex        =   17
            Top             =   4920
            Width           =   1215
         End
         Begin VB.CommandButton cmdSaveSession 
            Caption         =   "Save Session"
            Height          =   495
            Left            =   2880
            TabIndex        =   16
            Top             =   4920
            Width           =   975
         End
         Begin MSComctlLib.ListView lvwMeasurements 
            Height          =   3855
            Left            =   240
            TabIndex        =   14
            Top             =   960
            Width           =   5295
            _ExtentX        =   9340
            _ExtentY        =   6800
            View            =   3
            LabelEdit       =   1
            LabelWrap       =   -1  'True
            HideSelection   =   -1  'True
            FullRowSelect   =   -1  'True
            GridLines       =   -1  'True
            _Version        =   393217
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            BorderStyle     =   1
            Appearance      =   1
            NumItems        =   4
            BeginProperty ColumnHeader(1) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               Text            =   "Name"
               Object.Width           =   3881
            EndProperty
            BeginProperty ColumnHeader(2) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   1
               Text            =   "Date"
               Object.Width           =   1764
            EndProperty
            BeginProperty ColumnHeader(3) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   2
               Text            =   "Time"
               Object.Width           =   1411
            EndProperty
            BeginProperty ColumnHeader(4) {BDD1F052-858B-11D1-B16A-00C0F0283628} 
               SubItemIndex    =   3
               Text            =   "Key"
               Object.Width           =   1411
            EndProperty
         End
         Begin VB.TextBox txtSessionFileName 
            Height          =   645
            Left            =   840
            MultiLine       =   -1  'True
            TabIndex        =   13
            Text            =   "frmVnaApi.frx":0000
            Top             =   120
            Width           =   3495
         End
         Begin VB.CommandButton cmdOpenSession 
            Caption         =   "Open"
            Height          =   285
            Left            =   4560
            TabIndex        =   12
            Top             =   120
            Width           =   975
         End
         Begin VB.Label Label4 
            Caption         =   "File:"
            Height          =   255
            Left            =   240
            TabIndex        =   15
            Top             =   120
            Width           =   615
         End
      End
   End
End
Attribute VB_Name = "frmVnaApi"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private WithEvents clsVNA As mvnaVNAMain
Attribute clsVNA.VB_VarHelpID = -1
Private WithEvents clsSession As mvnaSession
Attribute clsSession.VB_VarHelpID = -1
Private WithEvents clsMeasurement As mvnaMeasurement
Attribute clsMeasurement.VB_VarHelpID = -1

Private strPlotTraceSet As String
Private strPlotTrace As String
Private strPlotChannel As String
Private clsTempMeasurement As mvnaMeasurement

'---------------------------------
' Measurement Events
'---------------------------------
Private Sub clsMeasurement_evtCalibrationChange(ByVal CalibrationNr As Long, ByVal NrCalibrations As Long)
  Debug.Print ("Measurement_evtCalibrationChange()")
  On Error GoTo mError
  
  If (clsTempMeasurement Is Nothing) Then
    Call ShowCurrentCalibration
  Else
    Call ShowCurrentMeasurement     ' Update the whole measurement
  End If

  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtDataChange(ByVal TraceNr As Long, ByVal NrTraces As Long)
  Debug.Print ("Measurement_evtDataChange()")
  On Error GoTo mError
  
  If (TraceNr = 0) Then
    ' General data update
    If (clsTempMeasurement Is Nothing) Then
      Call ShowCurrentData
    Else
      Call ShowCurrentMeasurement     ' Update the whole measurement
    End If
  ElseIf (TraceNr = NrTraces) Then
    ' Last trace received
    If (clsTempMeasurement Is Nothing) Then
      Call ShowCurrentData
    Else
      Call ShowCurrentMeasurement     ' Update the whole measurement
    End If
  End If

  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtDirty(ByVal Flag As Boolean)
  ' Measurement is Dirty (has a change)
  Debug.Print ("Measurement_evtDirty()")
  On Error GoTo mError
  
  If (clsTempMeasurement Is Nothing) Then
    Call ShowCurrentSettings
  Else
    Call ShowCurrentMeasurement     ' Update the whole measurement
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtIdleSettingsChange()
  ' Idle settings (PortIdleGenerator) change
  Debug.Print ("Measurement_evtIdleSettingsChange()")
  On Error GoTo mError
  
  PortIdleGenerator = clsMeasurement.PortIdleGenerator
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtSettingsChange()
  Debug.Print ("Measurement_evtSettingsChange()")
  On Error GoTo mError
  
  If (clsTempMeasurement Is Nothing) Then
    Call ShowCurrentSettings
  Else
    Call ShowCurrentMeasurement     ' Update the whole measurement
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtSetupChange()
  Debug.Print ("Measurement_evtSetupChange()")
  On Error GoTo mError
  
  If (clsTempMeasurement Is Nothing) Then
    Call ShowCurrentSettings
  Else
    Call ShowCurrentMeasurement     ' Update the whole measurement
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsMeasurement_evtSweepProgress(ByVal PointsReceived As Long, ByVal PointsTotal As Long)
'  Debug.Print ("Measurement_evtSweepProgress()")
End Sub



'---------------------------------
' VNA Main events
'---------------------------------
Private Sub clsVNA_evtDataChange(ByVal TraceNr As Long, ByVal NrTraces As Long)
  Debug.Print ("VNA_evtDataChange()")
End Sub

Private Sub clsVNA_evtMeasurementChange()
  Debug.Print ("VNA_evtMeasurementChange()")
  ' Measurement has been replaced
  On Error GoTo mError
  
  Call ShowCurrentMeasurement

  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsVNA_evtSweepProgress(ByVal PointsReceived As Long, ByVal PointsTotal As Long)
'  Debug.Print ("VNA_evtSweepProgress()")
  On Error Resume Next
  If (PointsTotal > 0) Then
    pgbProgress.Max = PointsTotal
    pgbProgress.Value = PointsReceived
    pgbProgress.Visible = True
  Else
    pgbProgress.Visible = False
  End If
End Sub

Private Sub clsVNA_evtSystemStatus(ByVal Status As mvnaVNAStatus)
  Debug.Print ("VNA_evtSystemStatus()")
  Select Case Status
    Case mvnaVST_Disconnected
      lblVNAStatus.Caption = "Disconnected"
      cmdConnect.Caption = "Connect"
    Case mvnaVST_Initializing  ' Connecting and initializing
      lblVNAStatus.Caption = "Initializing"
      cmdConnect.Caption = "Disconnect"
    Case mvnaVST_Idle
      lblVNAStatus.Caption = "Idle"
      cmdConnect.Caption = "Disconnect"
    Case mvnaVST_Calibrating
      lblVNAStatus.Caption = "Calibrating"
      cmdConnect.Caption = "Disconnect"
    Case mvnaVST_Sweeping
      lblVNAStatus.Caption = "Measuring"
      cmdConnect.Caption = "Disconnect"
  End Select
  Call lblVNAStatus.Refresh
End Sub


'---------------------------------
' Session Events
'---------------------------------
Private Sub clsSession_evtDirty(ByVal Flag As Boolean)
  ' Session has changed
  On Error GoTo mError
  
  Call ShowSession(clsSession)
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub


'---------------------------------
' Form Control Events
'---------------------------------
Private Sub chkDualCalkit_Click()
  On Error GoTo mError
  
  If (chkDualCalkit.Enabled = False) Then Exit Sub
  clsVNA.Measurement.DualCalkit = IIf(chkDualCalkit.Value = vbChecked, True, False)
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub chkUseCalibration_Click()
  On Error GoTo mError
  
  If (chkUseCalibration.Enabled = False) Then Exit Sub
  clsVNA.Measurement.UseCalibration = IIf(chkUseCalibration.Value = vbChecked, True, False)
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub chkVNAShow_Click()
  On Error GoTo mError
  
  clsVNA.Application.ShowState = IIf(chkVNAShow.Value = vbChecked, mvnaWSS_Normal, mvnaWSS_Hidden)
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub clsVNA_evtTerminate()
  Unload Me
End Sub

Private Sub cmdCalibrate_Click()
  On Error GoTo mError
  
  If (Not lvwCalibrations.SelectedItem Is Nothing) Then
    Call clsVNA.RunCalibration(lvwCalibrations.SelectedItem.Index)
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdClearData_Click()
  On Error GoTo mError
  
  Call clsVNA.Measurement.ClearData
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdClearCalibration_Click()
  On Error GoTo mError
  
  Call clsVNA.Measurement.ClearCalibration
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdConnect_Click()
  ' Connect / Disconnect the VNA
  On Error GoTo mError
  
  If (cmdConnect.Caption = "Connect") Then
    Call clsVNA.ConnectSerial(txtConnectSerial.Text)
  Else
    Call clsVNA.Disconnect
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdGetPresetSession_Click()
  ' Get the Preset Session
  On Error GoTo mError
  
  Set Session = clsVNA.PresetSession
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdLedState_Click(Index As Integer)
  Static Led(4) As mvnaLedState
  Dim Port As mvnaVNAPort
  Dim Color As mvnaColor
  
  Led(Index) = Led(Index) + 1
  If (Led(Index) > mvnaLED_BlinkFast) Then Led(Index) = mvnaLED_Off
  
  Port = Index
  Call clsVNA.VNADevice.OverrideLedState(Port, mvnaCOL_Red, Led(Index))
'  Color = Index
'  Call clsVNA.VNADevice.OverrideLedState(mvnaVNP_Port1, Color, Led(Index))
End Sub

Private Sub cmdOpenSession_Click()
  ' Open a Session
  On Error GoTo mError
  
  Screen.MousePointer = vbHourglass
  Set Session = clsVNA.OpenSession(txtSessionFileName.Text)
  
  Screen.MousePointer = vbDefault
  Exit Sub
mError:
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdRenormalize_Click()
  ' Renormalize the VNA measurement
  On Error GoTo mError
  
  Call clsVNA.Measurement.Renormalize
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdSaveSession_Click()
  ' Save the Session to a new file
  Dim SaveOptions As mvnaVNADataOptions
  Dim FileName As String
  
  On Error GoTo mError
  
  If (clsSession Is Nothing) Then Exit Sub
  
  ' We could leave SaveOptions empty for saving all items
  If (chkSaveCalibration.Value = vbChecked) Then SaveOptions = SaveOptions Or mvnaVDO_CALIBRATION
  If (chkSaveData.Value = vbChecked) Then SaveOptions = SaveOptions Or mvnaVDO_DATA
  
  FileName = InputBox("Session file name:", , ReplaceFileName(clsSession.FileName, "TestSave.vns"))
  If (FileName = "") Then Exit Sub
  
  Screen.MousePointer = vbHourglass
  
  Call clsSession.SaveSession(FileName, False, SaveOptions)
  
  Screen.MousePointer = vbDefault
  Exit Sub
mError:
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdSaveCurrentItem_Click()
  ' Save the VNA Measurement as a new Measurement
  On Error GoTo mError
  
  If (clsSession Is Nothing) Then Exit Sub
  
  Screen.MousePointer = vbHourglass
  If (clsVNA.Measurement.Name = "[new]") Then
    Call clsSession.Measurements.AddItem(clsVNA.Measurement, clsVNA.Measurement.Name & "NEW ITEM", Now)
  Else
    Call clsSession.Measurements.AddItem(clsVNA.Measurement, clsVNA.Measurement.Name & "-NEW", Now)
  End If
  
  Screen.MousePointer = vbDefault
  Exit Sub
mError:
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdSaveSelectedItem_Click()
  ' Save the selected Session Measurement as a new Measurement
  Dim Li As ListItem
  Dim Mm As mvnaMeasurement
  
  On Error GoTo mError
  
  If (clsSession Is Nothing) Then Exit Sub
  
  Set Li = lvwMeasurements.SelectedItem
  If (Li Is Nothing) Then Exit Sub
  
  Screen.MousePointer = vbHourglass
  
  Set Mm = clsSession.Measurements.Item(Li.Key)
  Call clsSession.Measurements.AddItem(Mm, Mm.Name & "-NEW", Now)
  
  Screen.MousePointer = vbDefault
  Exit Sub
mError:
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdRunSweepContinuously_Click()
  On Error GoTo mError
  
  Call clsVNA.RunSweepContinuously
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdRunSweepOnce_Click()
  On Error GoTo mError
  
  Call clsVNA.RunSweepOnce
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdStopSweep_Click()
  On Error GoTo mError
  
  Call clsVNA.StopSweep
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdUpdateMeasurement_Click()
  ' Update the screen from the VNA measurement
  On Error GoTo mError
  
  Call ShowCurrentMeasurement

  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub cmdVNAInfo_Click()
  Dim S As String
  
  On Error GoTo mError
  
  S = clsVNA.VNADevice.VNAInfoString
  Call MsgBox(S, vbOKOnly Or vbInformation, "VNA Info")
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub optGenIdle_Click(Index As Integer)
  If (optGenIdle(Index).Enabled = False) Then Exit Sub
  Select Case Index
    Case 0
      clsVNA.Measurement.PortIdleGenerator = mvnaVNP_None
    Case 1
      clsVNA.Measurement.PortIdleGenerator = mvnaVNP_Port1
    Case 2
      clsVNA.Measurement.PortIdleGenerator = mvnaVNP_Port2
    Case 3
      clsVNA.Measurement.PortIdleGenerator = mvnaVNP_Port3
  End Select
End Sub

Private Sub optBias1_Click(Index As Integer)
  If (optBias1(Index).Enabled = False) Then Exit Sub
  clsVNA.Measurement.PortBias(mvnaVNP_Port1) = Index
End Sub

Private Sub optBias2_Click(Index As Integer)
  If (optBias2(Index).Enabled = False) Then Exit Sub
  clsVNA.Measurement.PortBias(mvnaVNP_Port2) = Index
End Sub

Private Sub optBias3_Click(Index As Integer)
  If (optBias3(Index).Enabled = False) Then Exit Sub
  clsVNA.Measurement.PortBias(mvnaVNP_Port3) = Index
End Sub

Private Sub lvwCalibrations_ItemClick(ByVal Item As MSComctlLib.ListItem)
  ' Fixes a List presentation error for Bold items
  If (Item.Bold) Then
    Item.Bold = False
    Item.Bold = True
  End If
End Sub

Private Sub lvwMeasurements_Click()
  ' Show the properties of the selected Measurement
  Dim Li As ListItem
  Dim Mm As mvnaMeasurement
  On Error GoTo mError
  
  If (clsSession Is Nothing) Then Exit Sub
  
  Set Li = lvwMeasurements.SelectedItem
  If (Li Is Nothing) Then Exit Sub
  
  Screen.MousePointer = vbHourglass
  
  Set clsTempMeasurement = clsSession.Measurements.Item(Li.Key)
  Call ShowMeasurement(clsTempMeasurement)
  
  Screen.MousePointer = vbDefault
  
  Exit Sub
mError:
'  Resume
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub lvwMeasurements_DblClick()
  ' Copy the selected Measurement to the VNA
  Dim Li As ListItem
  Dim Mm As mvnaMeasurement
  On Error GoTo mError
  
  If (clsSession Is Nothing) Then Exit Sub
  
  Set Li = lvwMeasurements.SelectedItem
  If (Li Is Nothing) Then Exit Sub
  
  Screen.MousePointer = vbHourglass
  
  Set Mm = clsSession.Measurements.Item(Li.Key)
  Set clsVNA.Measurement = Mm
  
  Screen.MousePointer = vbDefault
  
  Exit Sub
mError:
  Screen.MousePointer = vbDefault
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub lvwParameters_DblClick()
  ' Edit a Parameter
  Dim Li As ListItem
  Dim Par As mvnaParameter
  Dim S As String
  Dim A As Variant
  Dim i As Long
  Dim ValueList() As Double
  
  On Error GoTo mError
  
  If (Not clsTempMeasurement Is Nothing) Then
    Call Beep
    Exit Sub
  End If
  
  Set Li = lvwParameters.SelectedItem
  Set Par = clsMeasurement.Parameters(Li.Text)
  
  If (Par.IsSweep = True) Then
  
    If (Par.SweepType = mvnaSWT_List) Then
      ' For a parameter with a sweep list we create a string with the values separated with a ' '
      ValueList = Par.SweepValueList
      For i = 0 To UBound(ValueList)
        If (S <> "") Then S = S & " "
        S = S & Format(ValueList(i))
      Next i
      S = InputBox(Par.Name & " Value list:", , S)
    Else
      S = InputBox(Par.Name & " Start value:", , Format(Par.StartValue))
    End If
    
    If (S = "") Then Exit Sub
    
    ' Determine if the new 'startvalue' is a list or a single value
    A = Split(S, " ")
    If (UBound(A) = 0) Then
      ' Single startvalue: parameter is a linear sweep from start to stop
      Par.StartValue = CDbl(S)
      Par.SweepType = mvnaSWT_Lin
    Else
      ' Multiple values: parameter is a sweep list
      ReDim ValueList(UBound(A))
      For i = 0 To UBound(A)
        ValueList(i) = CDbl(A(i))
      Next i
      Par.SweepValueList = ValueList
      Par.SweepType = mvnaSWT_List
      Par.Steps = UBound(A)
    End If
    
    If (Par.SweepType <> mvnaSWT_List) Then
      S = InputBox(Par.Name & " Stop value:", , Format(Par.StopValue))
      If (S = "") Then Exit Sub
      Par.StopValue = CDbl(S)
      
      S = InputBox(Par.Name & " Steps:", , Format(Par.Steps))
      If (S = "") Then Exit Sub
      Par.Steps = CLng(S)
    End If
    
    Call Par.Update
  Else
    S = InputBox(Par.Name & " Current value:", , Format(Par.CurrentValue))
    If (S = "") Then Exit Sub
    Par.CurrentValue = CDbl(S)
    
    Call Par.Update
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub tvwTraceSet_NodeClick(ByVal Node As MSComctlLib.Node)
  ' Plot Data if we click on a Channel Node
  On Error GoTo mError
  
  If (InStr(Node.Text, "Channel ") <> 1) Then Exit Sub
  
  strPlotTraceSet = Node.Parent.Parent.Text
  strPlotTrace = Node.Parent.Text
  strPlotChannel = Node.Text
  
  If (clsTempMeasurement Is Nothing) Then
    Call PlotTraceChannel(clsMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel)
  Else
    Call PlotTraceChannel(clsTempMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel)
  End If
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

'---------------------------------
' Support functions
'---------------------------------
Private Property Get Session() As mvnaSession
  Set Session = clsSession
End Property

Private Property Set Session(Val As mvnaSession)
  Set clsSession = Val
  Call ShowSession(clsSession)
End Property


Private Property Get PortIdleGenerator() As mvnaVNAPort
  ' Set the IdleGen OptionButton
  Dim Opt As OptionButton
  
  For Each Opt In optGenIdle
    If (Opt.Value = True) Then
      Select Case Opt.Index
        Case 0
          PortIdleGenerator = mvnaVNP_None
        Case 1
          PortIdleGenerator = mvnaVNP_Port1
        Case 2
          PortIdleGenerator = mvnaVNP_Port2
        Case 3
          PortIdleGenerator = mvnaVNP_Port3
      End Select
      Exit For
    End If
  Next Opt
End Property

Private Property Let PortIdleGenerator(Val As mvnaVNAPort)
  Select Case Val
    Case mvnaVNP_None
      optGenIdle(0).Enabled = False
      optGenIdle(0).Value = True
      optGenIdle(0).Enabled = True
    Case mvnaVNP_Port1
      optGenIdle(1).Enabled = False
      optGenIdle(1).Value = True
      optGenIdle(1).Enabled = True
    Case mvnaVNP_Port2
      optGenIdle(2).Enabled = False
      optGenIdle(2).Value = True
      optGenIdle(2).Enabled = True
    Case mvnaVNP_Port3
      optGenIdle(3).Enabled = False
      optGenIdle(3).Value = True
      optGenIdle(3).Enabled = True
  End Select
End Property


Private Property Get PortBias(Port As mvnaVNAPort) As mvnaVNABiasControl
  ' Set the Bias OptionButton
  Dim Opt As OptionButton
  
  Select Case Port
    Case mvnaVNP_Port1
      For Each Opt In optBias1
        If (Opt.Value = True) Then PortBias = Opt.Index
      Next Opt
    Case mvnaVNP_Port2
      For Each Opt In optBias2
        If (Opt.Value = True) Then PortBias = Opt.Index
      Next Opt
    Case mvnaVNP_Port3
      For Each Opt In optBias3
        If (Opt.Value = True) Then PortBias = Opt.Index
      Next Opt
  End Select
End Property

Private Property Let PortBias(Port As mvnaVNAPort, Bias As mvnaVNABiasControl)
  ' Get the Bias OptionButton
  Select Case Port
    Case mvnaVNP_Port1
      optBias1(Bias).Enabled = False
      optBias1(Bias).Value = True
      optBias1(Bias).Enabled = True
    Case mvnaVNP_Port2
      optBias2(Bias).Enabled = False
      optBias2(Bias).Value = True
      optBias2(Bias).Enabled = True
    Case mvnaVNP_Port3
      optBias3(Bias).Enabled = False
      optBias3(Bias).Value = True
      optBias3(Bias).Enabled = True
  End Select
End Property


Private Sub ShowCurrentMeasurement()
  Set clsTempMeasurement = Nothing
  Call ShowMeasurement(clsMeasurement)
End Sub

Private Sub ShowCurrentSettings()
  Call ShowSettings(clsMeasurement)
End Sub

Private Sub ShowCurrentData()
  Call ShowData(clsVNA.Measurement)
End Sub

Private Sub ShowCurrentCalibration()
  Call ShowCalibration(clsMeasurement)
End Sub

Private Sub ShowMeasurement(Measurement As mvnaMeasurement)
  Call ShowSettings(Measurement)
  Call ShowData(Measurement)
  Call ShowCalibration(Measurement)
End Sub

Private Sub ShowSettings(Mm As mvnaMeasurement)
  If (Mm.Dirty = True) Then
    fraMeasurement.Caption = "Measurement *"
  Else
    fraMeasurement.Caption = "Measurement"
  End If
  
  Call ShowParameters(Mm)
  PortIdleGenerator = Mm.PortIdleGenerator
  PortBias(mvnaVNP_Port1) = Mm.PortBias(mvnaVNP_Port1)
  PortBias(mvnaVNP_Port2) = Mm.PortBias(mvnaVNP_Port2)
  PortBias(mvnaVNP_Port3) = Mm.PortBias(mvnaVNP_Port3)
  
  lblMeasurementName.Caption = Mm.Name
  lblMeasurementDateTime.Caption = Format(Mm.DateTime)
  
  chkUseCalibration.Enabled = False
  chkUseCalibration.Value = IIf(Mm.UseCalibration = True, vbChecked, vbUnchecked)
  chkUseCalibration.Enabled = True
  
  chkDualCalkit.Enabled = False
  chkDualCalkit.Value = IIf(Mm.DualCalkit = True, vbChecked, vbUnchecked)
  chkDualCalkit.Enabled = True
  
  DoEvents
End Sub

Private Sub ShowParameters(Mm As mvnaMeasurement)
  Dim Index As Integer
  Dim Par As mvnaParameter
  Dim Li As ListItem
  Dim ValueList() As Double
  Dim i As Long
  Dim S As String
  
  Index = 1
  On Error Resume Next
  Index = lvwParameters.SelectedItem.Index
  
  Call lvwParameters.ListItems.Clear
  For Each Par In Mm.Parameters
    Set Li = lvwParameters.ListItems.Add(, , Par.Name)
    If (InStr(Par.Name, "FREQUENCY") > 0) Then
      ' Normalize Frequencies to MHz
      Li.SubItems(1) = Format(Par.MinValue / 1000000)
      Li.SubItems(2) = Format(Par.MaxValue / 1000000)
      If (Par.IsSweep = True) Then
        If (Par.SweepType = mvnaSWT_List) Then
          ValueList = Par.SweepValueList
          For i = 0 To UBound(ValueList)
            If (S <> "") Then S = S & " "
            S = S & Format(ValueList(i) / 1000000)
          Next i
          Li.SubItems(3) = S
        Else
          Li.SubItems(3) = Format(Par.StartValue / 1000000)
          Li.SubItems(4) = Format(Par.StopValue / 1000000)
          Li.SubItems(5) = Format(Par.Steps)
        End If
      Else
        Li.SubItems(3) = Format(Par.CurrentValue / 1000000)
      End If
      Li.SubItems(6) = "M" & Par.Dimension
    Else
      Li.SubItems(1) = Format(Par.MinValue)
      Li.SubItems(2) = Format(Par.MaxValue)
      If (Par.IsSweep = True) Then
        If (Par.SweepType = mvnaSWT_List) Then
          ValueList = Par.SweepValueList
          For i = 0 To UBound(ValueList)
            If (S <> "") Then S = S & " "
            S = S & Format(ValueList(i))
          Next i
          Li.SubItems(3) = S
        Else
          Li.SubItems(3) = Format(Par.StartValue)
          Li.SubItems(4) = Format(Par.StopValue)
          Li.SubItems(5) = Format(Par.Steps)
        End If
      Else
        Li.SubItems(3) = Format(Par.CurrentValue)
      End If
      Li.SubItems(6) = Par.Dimension
    End If
  Next Par
  
  Set lvwParameters.SelectedItem = lvwParameters.ListItems(Index)
End Sub

Private Sub ShowData(Mm As mvnaMeasurement)
  Dim TraceSet As mvnaTraceSet
  
  Set TraceSet = Mm.TraceSet
  
  Call ViewTraceSet(tvwTraceSet, TraceSet, Mm.Name)

  If (strPlotChannel <> "") Then
    strPlotTraceSet = tvwTraceSet.Nodes(1).Text
    If (clsTempMeasurement Is Nothing) Then
      Call PlotTraceChannel(clsMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel)
    Else
      Call PlotTraceChannel(clsTempMeasurement, strPlotTraceSet, strPlotTrace, strPlotChannel)
    End If
  End If
End Sub

Private Sub ShowCalibration(Mm As mvnaMeasurement)
  Dim Cal As mvnaCalibration
  Dim Li As ListItem
  Dim Index As Integer
  
  On Error Resume Next
  Index = 1
  Index = lvwCalibrations.SelectedItem.Index
  
  Call lvwCalibrations.ListItems.Clear
  For Each Cal In Mm.Calibrations
    Set Li = lvwCalibrations.ListItems.Add(, Cal.Caption, Cal.Caption)
    If (Cal.Complete = True) Then Li.Bold = True
  Next Cal
  
  On Error Resume Next
  Set lvwCalibrations.SelectedItem = lvwCalibrations.ListItems(Index)
End Sub

Private Sub ShowSession(Session As mvnaSession)
  Dim Li As ListItem
  Dim Mm As mvnaMeasurement
  
  Call lvwMeasurements.ListItems.Clear
  
  If (Session Is Nothing) Then Exit Sub
  
  If (Session.Dirty = True) Then
    fraSession.Caption = "Session *"
  Else
    fraSession.Caption = "Session"
  End If
  
  For Each Mm In Session.Measurements
    Set Li = lvwMeasurements.ListItems.Add(, Mm.Key, Mm.Name)
    Li.SubItems(1) = Format(Mm.DateTime, "short date")
    Li.SubItems(2) = Format(Mm.DateTime, "short time")
    Li.SubItems(3) = Mm.Key
  Next Mm
End Sub

Private Sub PlotTraceChannel(Measurement As mvnaMeasurement, TraceSetName As String, TraceName As String, ChannelName As String)
  Dim TraceNr As Long
  Dim Caption As String
  Dim TraceSet As mvnaTraceSet
  Dim Trace As mvnaTrace
  Dim Channel As mvnaTraceChannel
  Dim Data As mvnaIQData
  Dim Values() As Double
  
  On Error GoTo mError
  
  If (Measurement Is Nothing) Then Exit Sub
  
  TraceNr = CLng(Right(TraceName, 2))
  Set TraceSet = Measurement.TraceSet
  Set Trace = TraceSet.Traces(TraceNr)
  
  If (InStr(ChannelName, "S11")) Then
    Set Channel = Trace.Channels("S11")
    Set Data = Channel.DataSet("Return")
    
  ElseIf (InStr(ChannelName, "S22")) Then
    Set Channel = Trace.Channels("S22")
    Set Data = Channel.DataSet("Return")
  
  ElseIf (InStr(ChannelName, "S12")) Then
    Set Channel = Trace.Channels("S12")
    Set Data = Channel.DataSet("Through")
  
  ElseIf (InStr(ChannelName, "S13")) Then
    Set Channel = Trace.Channels("S13")
    Set Data = Channel.DataSet("Through")
  
  ElseIf (InStr(ChannelName, "S21")) Then
    Set Channel = Trace.Channels("S21")
    Set Data = Channel.DataSet("Through")
  
  ElseIf (InStr(ChannelName, "S23")) Then
    Set Channel = Trace.Channels("S23")
    Set Data = Channel.DataSet("Through")
  
  Else
    Exit Sub
  End If
  
  Caption = TraceSetName & "\" & "Trace " & Format(TraceNr) & "\" & Channel & "\" & Data.Name & " data"
  
  Call Data.GetAmpValuesDb(Values)
  Call picPlot.Cls
  Call PlotData(picPlot, Values, Data.PValues, -50, 0, Caption)
  
  Exit Sub
mError:
  Call picPlot.Cls
End Sub

Private Function ReplaceFileName(InFile As String, FileName As String) As String
  Dim S As String
  Dim Ar() As String
  Dim i As Integer
  Dim OutFile As String
  
  ' Replace "C:\DIR1\DIR2\File.ext"
  ' By      "C:\DIR1\DIR2\FileName"
  
  If (InFile = "") Then
    ReplaceFileName = FileName
    Exit Function
  End If
  
  Ar = Split(InFile, "\")
  For i = 0 To UBound(Ar) - 1   ' Leave out "File.ext"
    OutFile = OutFile & Ar(i) & "\"
  Next i
  ReplaceFileName = OutFile & FileName
End Function

Private Sub ErrorHandler(ErrNunmer As Long, ErrDesc As String, ErrSource As String)
  Call MsgBox("Error: " & Format(Err.Number) & vbCrLf & vbCrLf & ErrDesc, vbOKOnly Or vbCritical)
End Sub

'---------------------------------
' Form Events
'---------------------------------
Private Sub Form_Load()
  On Error GoTo mError
  
  Debug.Print ("Starting VNA Application")
  
  Set clsVNA = New mvnaVNAMain
'  clsVNA.Application.ShowState = mvnaWSS_Hidden
  Set clsMeasurement = clsVNA.Measurement
  
  txtSessionFileName.Text = clsVNA.Application.Path & "\" & "VNA Data\VSB Measurements.vns"
  Call clsVNA_evtSystemStatus(clsVNA.SystemStatus)
  
  Call ShowCurrentSettings
  Call ShowCurrentCalibration
  Call ShowCurrentData
  
  Exit Sub
mError:
  Call ErrorHandler(Err.Number, Err.Description, Err.Source)
End Sub

Private Sub Form_Unload(Cancel As Integer)
  Set clsVNA = Nothing
  Set clsMeasurement = Nothing
  Set clsSession = Nothing
  Debug.Print ("VNA Application terminated")
End Sub

