using System;
using System.Collections.Generic;
using System.IO;

namespace Lab6
{
    class Program
    {
        
        static void Main(string[] args)
        {
            var FApath = "D:\\Projects\\AN 3\\SEM 1\\FLCD\\LABS\\LAB 6\\Lab6\\Lab6\\FA.in";
            var fa = new FA(FApath);
            fa.Run();
        }
    }
}
