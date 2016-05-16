using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.IO.Pipes;
using System.Windows.Forms;
using System.Diagnostics;

namespace Server_Gui
{
    class Communicator
    {
        //handles the communication between the Form and the python programm
        NamedPipeServerStream server;
        ServerForm Form_1;
        BinaryReader br;
        BinaryWriter bw;
        ComputersBasicDDataSet computersBasicDDataSet;

        public Communicator(ServerForm Form)
        {
            this.Form_1 = Form;
            this.computersBasicDDataSet = new ComputersBasicDDataSet();
            try
            {
                server = new NamedPipeServerStream("myPipee");
                this.Form_1.textBox1.AppendText("Waiting for Connection");
                this.Form_1.CreatePythonEngine();
                server.WaitForConnection();
                Debug.Print("Connected to python multi threding server");
                var bro = new BinaryReader(server);
                this.br = bro;
                var bwo = new BinaryWriter(server);
                this.bw = bwo;
              
            }
            catch (Exception e)
            {
                this.Form_1.textBox1.Text = e.ToString();
            }
        }
        public string Reead()
        {
            var lenn = (int)this.br.ReadUInt32();            // Read string length
            var str = new string(this.br.ReadChars(lenn));
            return str;
        }
        public void Wriite( string str)
        {
            this.bw.Write((uint)str.Length);
            this.bw.Write(str);
        }
        public void NewClient()
        {
            // need to connect and add IP to db and also to connect the combo box to the db
            // Create a new row. FROM (MSDN)
            // NorthwindDataSet.RegionRow newRegionRow;
            //newRegionRow = northwindDataSet.Region.NewRegionRow();
            //newRegionRow.RegionID = 5;
            //newRegionRow.RegionDescription = "NorthWestern";

            //// Add the row to the Region table
            //this.northwindDataSet.Region.Rows.Add(newRegionRow);

            //// Save the new row to the database
            //this.regionTableAdapter.Update(this.northwindDataSet.Region);
            ComputersBasicDDataSet.Basic_TableRow newTable1Row;
            newTable1Row = this.computersBasicDDataSet.Basic_Table.NewBasic_TableRow();
            string Ip = Reead();
            newTable1Row.IP = Ip;
            string UUId = Reead();
            newTable1Row.UUID = UUId;
            string username = Reead();
            newTable1Row.user_name = username;
            string Os = Reead();
            newTable1Row.OS_version = Os;
            string CPu = Reead();
            newTable1Row.Processor = CPu;
            string CPuNum = Reead();
            newTable1Row.CPUs = CPuNum;
            string RAm = Reead();
            newTable1Row.RAM_size = RAm;
            this.computersBasicDDataSet.Basic_Table.Rows.Add(newTable1Row);
            this.Form_1.Invoke(new MethodInvoker(delegate()
            {
                this.Form_1.Clients.BeginUpdate();
                this.Form_1.Clients.Items.Add(Ip);
                this.Form_1.Clients.SelectedItem = Ip;
                this.Form_1.Clients.Update();
                this.Form_1.Clients.EndUpdate();
                }));
            
        }
        public void UpdateBoxes(string Ip)
        {
            System.Data.DataRow copyingvaluesRow = this.computersBasicDDataSet.Basic_Table.Rows.Find(Ip);
            this.Form_1.Invoke(new MethodInvoker(delegate()
           {
               this.Form_1.Clients.BeginUpdate();
               this.Form_1.Clients.SelectedItem = Ip;
               this.Form_1.Clients.Update();
               this.Form_1.Clients.EndUpdate();
               this.Form_1.UUIDbox.Text = Convert.ToString(copyingvaluesRow["UUID"]);
               this.Form_1.UserNameBox.Text = Convert.ToString(copyingvaluesRow["user name"]);
               this.Form_1.RAMBox.Text = Convert.ToString(copyingvaluesRow["RAM size"]);
               this.Form_1.CpuNumBox.Text = Convert.ToString(copyingvaluesRow["CPUs"]);
               this.Form_1.CPUBox.Text = Convert.ToString(copyingvaluesRow["Processor"]);
               this.Form_1.OsBox.Text = Convert.ToString(copyingvaluesRow["OS version"]);
           }));
        }
        public void UpdateUsingB()
        {
            //the operation target is to update constantly the Using: box
            // its done by an infinite thread that requires the Ip from the server
            var Ipp = this.Form_1.Clients.SelectedItem;
            string Ip = Convert.ToString(Ipp);
            Timer t = new Timer();
            t.Interval = 30000;
            while (true)
            {
                t.Start();
                string info = this.Reead();
                if (info.Substring(0, Ip.Length).Equals(Ip))
                {
                    this.Form_1.TUsingBox.Text = "Using:" + info.Substring(Ip.Length);
                }
                else
                {
                    int Ipin = info.IndexOf(':');
                    string Ipn = info.Substring(0, Ipin);
                    System.Data.DataRow copyingvaluesRow = this.computersBasicDDataSet.Basic_Table.Rows.Find(Ipn);
                    string Datta = info.Substring(Ipin);
                    int Parami = info.IndexOf(':');
                    string Parmat = Datta.Substring(0, Parami);
                    copyingvaluesRow.BeginEdit();
                    copyingvaluesRow[Parmat] = Datta;
                }
                if (Convert.ToString(this.Form_1.Clients.SelectedItem) != Ip)
                    Ip = Convert.ToString(this.Form_1.Clients.SelectedItem);
            }
        }
        public void Execute(string st1)
        {
            if (st1 == "New client arrives")
            {
                this.NewClient();
            }
            // more tasks in future if needed
        }


    }
}
