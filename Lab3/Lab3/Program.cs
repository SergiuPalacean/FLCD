using Lab3.Model;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace Lab3
{
    class Program
    {
        static void Main(string[] args)
        {
            string filepathProgram = "D:\\Projects\\AN 3\\SEM 1\\FLCD\\LABS\\LAB 1\\p1error.txt";
            string[] lines = File.ReadAllLines(filepathProgram);
            string filepathToken = "D:\\Projects\\AN 3\\SEM 1\\FLCD\\LABS\\LAB 2\\Token.in";
            var tokensArray = File.ReadAllLines(filepathToken);
            var tokens = new List<string>(tokensArray);
            SymbolTable symbolTable = new SymbolTable();
            List<(string, int)> pif = new List<(string, int)>();
            Regex regIdentifier = new Regex(@"^[A-Za-z][A-Za-z0-9]*$");
            Regex regConstantNR = new Regex(@"^([0]{1}|(\+|\-)?[1-9]+)$");
            Regex regConstantCHAR = new Regex(@"^\""[a-zA-Z]\""$");
            Regex regConstantSTRING = new Regex(@"^\""[a-zA-Z0-9]*\""$");
            Regex regConstantCOMMENT = new Regex(@"^//");
            List<string> errors = new List<string>();
            int lineNr = 1;

            foreach (var line in lines)
            {
                var linetokens = line.Split(new char[] { ' '});
                foreach(var linetok1 in linetokens)
                {
                    var linetok = linetok1.Trim();
                    
                    if(tokens.Contains(linetok))
                    {
                        pif.Add((linetok, 0));
                    }
                    else if(regIdentifier.IsMatch(linetok) || regConstantNR.IsMatch(linetok) || regConstantCHAR.IsMatch(linetok) || regConstantSTRING.IsMatch(linetok))
                    {
                        pif.Add((linetok, symbolTable.Add(linetok)));
                    }
                    else if(regConstantCOMMENT.IsMatch(linetok))
                    {

                    }
                    else
                    {
                        if(!linetok.Equals(""))
                        {
                            string str = "Lexical error in line " + lineNr + " " + line + " token: " + linetok;
                            errors.Add(str);
                        }
                        
                    }
                }
                lineNr++;
            }
            if (errors.Count != 0)
            {
                Console.WriteLine("Lexically incorrect");
                foreach (var err in errors)
                    Console.WriteLine(err);
            }
            else
                Console.WriteLine("Lexically correct");
            foreach (var elem in pif)
            {
                Console.WriteLine(elem);
            }
            Console.WriteLine(symbolTable.typestring);
            symbolTable.TraverseInOrder();
        }
    }
}
