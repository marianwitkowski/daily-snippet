using System;
using System.Diagnostics;

namespace ConsoleAppReverseString 
{
    class Program
    {
        private static String ReverseXor(String str)
        {
            char[] strArr = str.ToCharArray();
            int length = str.Length - 1;
            for (int i = 0; i < length; i++, length--)
            {
                strArr[i] ^= strArr[length];
                strArr[length] ^= strArr[i];
                strArr[i] ^= strArr[length];
            }
            return new string(strArr);
        }

        private static String ReverseArr(String str)
        {
            char[] charArray = str.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }


        public static String ReverseSwap(string str)
        {
            char[] chars = str.ToCharArray();
            for (int i = 0, j = str.Length - 1; i < j; i++, j--)
            {
                chars[i] = str[j];
                chars[j] = str[i];
            }
            return new string(chars);
        }

        const int LOOP = 100000;

        static void Main(string[] args)
        {

            String s = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent efficitur euismod ante vel euismod.";

            Stopwatch sw = Stopwatch.StartNew();
            for (int i = 0; i < LOOP; i++)
            {
                String res = ReverseArr(s);
            }
            sw.Stop();
            Console.WriteLine("Time taken for ReverseArr: {0}ms", sw.Elapsed.TotalMilliseconds);


            sw = Stopwatch.StartNew();
            for (int i = 0; i < LOOP; i++)
            {
                String res = ReverseXor(s);
            }
            sw.Stop();
            Console.WriteLine("Time taken for ReverseXor: {0}ms", sw.Elapsed.TotalMilliseconds);

            sw = Stopwatch.StartNew();
            for (int i = 0; i < LOOP; i++)
            {
                String res = ReverseSwap(s);
            }
            sw.Stop();
            Console.WriteLine("Time taken for ReverseSwap: {0}ms", sw.Elapsed.TotalMilliseconds);

            /*
                  Time taken for ReverseArr: 45,9626ms
                  Time taken for ReverseXor: 86,2541ms
                  Time taken for ReverseSwap: 67,6877ms
            */

            Console.ReadLine();
        }
    }
}
