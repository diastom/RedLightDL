[Setup]
; Basic Application Information
AppName=RedLight DL
AppVersion=2.1.1
AppPublisher=RedLight Team
DefaultDirName={autopf}\RedLightDL
DefaultGroupName=RedLight DL
OutputBaseFilename=RedLightSetup
OutputDir=Output
Compression=lzma2/max
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
; Icon settings
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
; Dark Mode Support for Installer
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Source everything from the FinalBuild folder (which contains both C# host and Python backend)
Source: "FinalBuild\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RedLight DL"; Filename: "{app}\RedLightGUI.exe"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\RedLight DL"; Filename: "{app}\RedLightGUI.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\RedLightGUI.exe"; Description: "{cm:LaunchProgram,RedLight DL}"; Flags: nowait postinstall skipifsilent
