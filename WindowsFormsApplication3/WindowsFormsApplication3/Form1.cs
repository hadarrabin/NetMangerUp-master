using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using System.Threading;

namespace WindowsFormsApplication3
{
    public partial class Form1 : Form
    {
        #region  GLOBAL VARIBALES
        // If C# and python are connectd
        bool python_con = false;
        // if the updater thread isnt working
        bool Uth = true;
        // Creating a PythonSession object
        Communicator com;
        #endregion
        public Form1()
        {
            InitializeComponent();
        }
        private void Form_HandleCreated(object sender, EventArgs e)
        {
            this.com = new Communicator(this);
            // Handle enter keypress to send the command to the python client.
        }
        private void button1_Click(object sender, EventArgs e)
        {
            #region Connection checking
            if (!python_con)
            {

                try
                {
                    //try to create python server if there isnt one exists
                    CreatePythonEngine();
                    python_con = true;
                    com = new Communicator(this);
                }
                catch
                {
                    MessageBox.Show("Houston we have a problem....");
                    Environment.Exit(1);
                }
            }
            #endregion
            if (python_con)
            {
                this.textBox1.AppendText("Connection is good");
            }
            this.button1.Visible = false;
            this.AddClientB.Visible = true;
        }
        public void CreatePythonEngine()
        {
            Process pythonProcess = new Process();
            pythonProcess.StartInfo.FileName = "C:\\codeing\\Python27\\python.exe";
            pythonProcess.StartInfo.Arguments = "C:\\Users\\Hadar\\Documents\\GitHub\\NetMangerUp\\NetMM\\Server";
            pythonProcess.StartInfo.WorkingDirectory = Application.StartupPath;
            pythonProcess.Start();
        }
        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            
        }

        private void Clients_SelectedIndexChanged(object sender, EventArgs e)
        {
            var Currentt = this.Clients.SelectedItem;
            string Current = Convert.ToString(Currentt);
            // changes the values by DB
            this.com.UpdateBoxes(Current);
            if (Uth == true)
            {
                // starts an ifinite thread with description in communicator class
                ThreadStart S = new ThreadStart(com.UpdateUsingB);
                Thread Up = new Thread(S);
                Up.Start();
            }
        }

        private void AddClientB_Click(object sender, EventArgs e)
        {
            
            string necl = this.com.Reead();
            this.com.Execute(necl);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // TODO: This line of code loads data into the 'database21DataSet.Table1' table. You can move, or remove it, as needed.
            this.table1TableAdapter.Fill(this.database21DataSet.Table1);

        }



        
    }
}
