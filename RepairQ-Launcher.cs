using System;
using System.IO;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;

public class RepairQLauncher
{
    [STAThread]
    public static void Main(string[] args)
    {
        try
        {
            // Get the directory where this EXE is located
            string appDir = Path.GetDirectoryName(Application.ExecutablePath);
            string batPath = Path.Combine(appDir, "RepairQ-Run.bat");
            string jreCheck = Path.Combine(appDir, "jre", "bin", "java.exe");
            string jarFile = Path.Combine(appDir, "RepairQ-0.0.1-SNAPSHOT.jar");

            // Verify all required files exist
            if (!File.Exists(batPath))
            {
                MessageBox.Show(
                    "Error: RepairQ launcher not found.\n\nPlease ensure the distribution files are intact.",
                    "RepairQ - Installation Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                return;
            }

            if (!File.Exists(jreCheck))
            {
                MessageBox.Show(
                    "Error: Java runtime not found.\n\nPlease re-extract the RepairQ distribution.",
                    "RepairQ - Installation Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                return;
            }

            if (!File.Exists(jarFile))
            {
                MessageBox.Show(
                    "Error: RepairQ application not found.\n\nPlease re-extract the RepairQ distribution.",
                    "RepairQ - Installation Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                return;
            }

            // Launch the batch file
            ProcessStartInfo psi = new ProcessStartInfo
            {
                FileName = batPath,
                UseShellExecute = false,
                CreateNoWindow = true,
                WorkingDirectory = appDir
            };

            Process process = Process.Start(psi);
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                "Error starting RepairQ:\n\n" + ex.Message,
                "RepairQ - Startup Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
        }
    }
}
