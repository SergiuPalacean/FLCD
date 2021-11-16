﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab6
{
    public class FA
    {
        private string path;
        string[] lines;
        int index;
        List<string> states;
        List<string> initialStates;
        List<string> finalStates;
        List<string> alphabet;
        Dictionary<(string, string), string> transitions;
        public FA(string _path)
        {
            path = _path;
            lines = File.ReadAllLines(path);
            index = 0;
            states = new List<string>();
            initialStates = new List<string>();
            finalStates = new List<string>();
            alphabet = new List<string>();
            transitions = new Dictionary<(string, string), string>();
            PopulateFields();
        }

        private void DisplayMenu()
        {
            Console.WriteLine("1: Display all the states");
            Console.WriteLine("2: Display the initial state");
            Console.WriteLine("3: Display the final state");
            Console.WriteLine("4: Display the transitions");
            Console.WriteLine("5: Display the alphabet");
            Console.WriteLine("6: Check DFA");
            Console.WriteLine("0: Exit");
        }

        private void DisplayAllStates()
        {
            var allStates = "";
            foreach(var l in states)
            {
                allStates += l + " ";
            }
            Console.WriteLine(allStates);
        }

        private void DisplayInitialStates()
        {
            var states = "";
            foreach (var l in initialStates)
            {
                states += l + " ";
            }
            Console.WriteLine(states);
        }

        private void DisplayFinalStates()
        {
            var states = "";
            foreach (var l in finalStates)
            {
                states += l + " ";
            }
            Console.WriteLine(states);
        }

        private void DisplayTransitions()
        {
            foreach(var (k1, k2) in transitions.Keys)
            {
                Console.WriteLine(k1 + "->" + k2 + " trough " + transitions[(k1, k2)]);
            }
        }

        private void DisplayAlphabet()
        {
            var alp = "";
            foreach(var a in alphabet)
            {
                alp += a + " ";
            }
            Console.WriteLine(alp);
        }

        private void Check()
        {
            var sequence = Console.ReadLine();
            var splitSequence = sequence.Split(' ');
            var initState = "";
            var finState = "";
            var transition = "";
            var index = 1;
            var startState = "";
            var endState = "";
            var accepted = true;

            initState = splitSequence[0];
            finState = splitSequence[splitSequence.Length - 1];
            
            if(initialStates.Contains(initState) && finalStates.Contains(finState))
            {
                foreach (var seq in splitSequence)
                {
                    if (index % 3 == 1)
                    {
                        startState = seq;
                    }
                    else if(index % 3 == 2)
                    {
                        transition = seq;
                    }
                    else if(index % 3 == 0)
                    {
                        if(transitions.ContainsKey((startState, endState)))
                        {
                            if(!transitions[(startState, endState)].Contains(transition))
                            {
                                accepted = false;
                            }
                        }
                    }
                }
            }
            else
            {
                accepted = false;
            }
            if(accepted == true)
            {
                Console.WriteLine("DFA is accepted");
            }
            else
            {
                Console.WriteLine("DFA is not accepted");
            }
        }

        public void Run()
        {
            var cond = true;
            while (cond == true)
            {
                DisplayMenu();
                try
                {
                    var cmd = int.Parse(Console.ReadLine());
                    switch (cmd)
                    {
                        case 0:
                            cond = false;
                            break;
                        case 1:
                            DisplayAllStates();
                            break;
                        case 2:
                            DisplayInitialStates();
                            break;
                        case 3:
                            DisplayFinalStates();
                            break;
                        case 4:
                            DisplayTransitions();
                            break;
                        case 5:
                            DisplayAlphabet();
                            break;
                        case 6:
                            Check();
                            break;
                        default:
                            break;
                    }
                }
                catch (Exception)
                {

                }
            }
        }

        private void PopulateFields()
        {
            foreach (var line in lines)
            {
                switch (index)
                {
                    case 0:
                        var st = line.Split(',');
                        states = new List<string>(st);
                        break;
                    case 1:
                        initialStates.Add(line);
                        break;
                    case 2:
                        var fs = line.Split(',');
                        finalStates = new List<string>(fs);
                        break;
                    case 3:
                        alphabet = new List<string>(line.Split(','));
                        break;
                    case 4:
                        var al = line.Split(',');
                        foreach (var l in al)
                        {
                            alphabet.Add(l);
                        }
                        break;
                    case 5:
                        var al1 = line.Split(',');
                        foreach (var l in al1)
                        {
                            alphabet.Add(l);
                        }
                        break;
                    default:
                        var tr = line.Split(' ');
                        var k1 = tr[0];
                        var k2 = tr[2];
                        var val = tr[1];
                        transitions.Add((k1, k2), val);
                        break;
                }
                index++;
            }
        }
    }
}
