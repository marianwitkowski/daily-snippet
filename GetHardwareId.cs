using System;
using System.Management;
using System.Text;

namespace GetHardwareIdApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(GetHardwareId());
            Console.ReadKey();
        }

        private static String GetHardwareId()
        {
            StringBuilder sb = new StringBuilder(100);

            /*
             Watch out! BIOS version could change after firmware upgrade. Important for tablets with Win10
            */
            ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT * FROM Win32_BIOS");
            foreach (ManagementObject queryObj in searcher.Get())
            {
                sb.Append(queryObj["Version"].ToString().Substring(0, 4));
                break;
            }

            searcher = new ManagementObjectSearcher("SELECT * FROM Win32_Processor");
            foreach (ManagementObject queryObj in searcher.Get())
            {
                sb.Append(queryObj["ProcessorId"].ToString());
                break;
            }

            searcher = new ManagementObjectSearcher("SELECT * FROM Win32_DiskDrive");
            foreach (ManagementObject queryObj in searcher.Get())
            {
                sb.Append(queryObj["Signature"].ToString());
                break;
            }

            byte[] bytes = Encoding.UTF8.GetBytes(sb.ToString());
            String res = Convert.ToBase64String(System.Security.Cryptography.SHA256.Create().ComputeHash(bytes));
            return res;
        }

    }
}
