using System;
using System.Collections.Generic;
using System.Text;

namespace Lab3.Model
{
    class SymbolTable
    {
        private Node root;
        private int index;

        public SymbolTable()
        {
            root = null;
            index = 0;
        }

        public int Add(string id)
        {
            Node node = new Node(id);
            if(root is null)
            {
                root = node;
                root.Index = index;
                index++;
                return root.Index;
            }
            else
            {
                Node aux = root;
                while(!aux.Data.Equals(id))
                {
                    if(id.CompareTo(aux.Data)<0)
                    {
                        if(aux.Left!=null)
                        {
                            aux = aux.Left;
                        }
                        else
                        {
                            aux.Left = node;
                            aux.Left.Index = index;
                            index++;
                        }
                    }
                    else
                    {
                        if (aux.Right != null)
                        {
                            aux = aux.Right;
                        }
                        else
                        {
                            aux.Right = node;
                            aux.Right.Index = index;
                            index++;
                        }
                    }
                }
                return aux.Index;
            }
        }
    }
}
