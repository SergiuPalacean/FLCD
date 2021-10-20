using System;
using System.Collections.Generic;
using System.Text;

namespace Lab3.Model
{
    class Node
    {
        public string Data { get; set; }
        public int Index { get; set; }
        public Node Left { get; set; }
        public Node Right { get; set; }

        public Node(string data)
        {
            Data = data;
            Left = Right = null;
        }
    }
}
