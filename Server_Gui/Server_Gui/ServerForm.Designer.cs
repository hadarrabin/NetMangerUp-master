

namespace Server_Gui
{
    partial class ServerForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.UUIDbox = new System.Windows.Forms.TextBox();
            this.UserNameBox = new System.Windows.Forms.TextBox();
            this.OsBox = new System.Windows.Forms.TextBox();
            this.CPUBox = new System.Windows.Forms.TextBox();
            this.CpuNumBox = new System.Windows.Forms.TextBox();
            this.RAMBox = new System.Windows.Forms.TextBox();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.IPBox = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.Clients = new System.Windows.Forms.ListBox();
            this.processes = new System.Windows.Forms.DataGridView();
            this.AddClientB = new System.Windows.Forms.Button();
            this.TUsingBox = new System.Windows.Forms.TextBox();
           
            this.pIDDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.pnameDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.usingDataGridViewTextBoxColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.flowLayoutPanel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.processes)).BeginInit();
            
           
            this.SuspendLayout();
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(1, 342);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(425, 46);
            this.textBox1.TabIndex = 1;
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(1, 266);
            this.textBox2.Multiline = true;
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(425, 53);
            this.textBox2.TabIndex = 2;
            // 
            // UUIDbox
            // 
            this.UUIDbox.Location = new System.Drawing.Point(3, 29);
            this.UUIDbox.Name = "UUIDbox";
            this.UUIDbox.Size = new System.Drawing.Size(186, 20);
            this.UUIDbox.TabIndex = 3;
            this.UUIDbox.Text = "UUID: ";
            this.UUIDbox.TextChanged += new System.EventHandler(this.textBox3_TextChanged);
            // 
            // UserNameBox
            // 
            this.UserNameBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.UserNameBox.Location = new System.Drawing.Point(3, 55);
            this.UserNameBox.Name = "UserNameBox";
            this.UserNameBox.Size = new System.Drawing.Size(186, 23);
            this.UserNameBox.TabIndex = 4;
            this.UserNameBox.Text = "user name: ";
            // 
            // OsBox
            // 
            this.OsBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.OsBox.Location = new System.Drawing.Point(3, 166);
            this.OsBox.Name = "OsBox";
            this.OsBox.Size = new System.Drawing.Size(186, 22);
            this.OsBox.TabIndex = 5;
            this.OsBox.Text = "OS version: ";
            // 
            // CPUBox
            // 
            this.CPUBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.CPUBox.Location = new System.Drawing.Point(3, 138);
            this.CPUBox.Name = "CPUBox";
            this.CPUBox.Size = new System.Drawing.Size(186, 22);
            this.CPUBox.TabIndex = 6;
            this.CPUBox.Text = "processor: ";
            // 
            // CpuNumBox
            // 
            this.CpuNumBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.CpuNumBox.Location = new System.Drawing.Point(3, 111);
            this.CpuNumBox.Name = "CpuNumBox";
            this.CpuNumBox.Size = new System.Drawing.Size(186, 21);
            this.CpuNumBox.TabIndex = 7;
            this.CpuNumBox.Text = "CPU\'s: ";
            // 
            // RAMBox
            // 
            this.RAMBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.RAMBox.Location = new System.Drawing.Point(3, 84);
            this.RAMBox.Name = "RAMBox";
            this.RAMBox.Size = new System.Drawing.Size(186, 21);
            this.RAMBox.TabIndex = 8;
            this.RAMBox.Text = "RAM size: ";
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.Controls.Add(this.IPBox);
            this.flowLayoutPanel1.Controls.Add(this.UUIDbox);
            this.flowLayoutPanel1.Controls.Add(this.UserNameBox);
            this.flowLayoutPanel1.Controls.Add(this.RAMBox);
            this.flowLayoutPanel1.Controls.Add(this.CpuNumBox);
            this.flowLayoutPanel1.Controls.Add(this.CPUBox);
            this.flowLayoutPanel1.Controls.Add(this.OsBox);
            this.flowLayoutPanel1.Location = new System.Drawing.Point(12, 12);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(206, 194);
            this.flowLayoutPanel1.TabIndex = 9;
            // 
            // IPBox
            // 
            this.IPBox.Location = new System.Drawing.Point(3, 3);
            this.IPBox.Name = "IPBox";
            this.IPBox.Size = new System.Drawing.Size(186, 20);
            this.IPBox.TabIndex = 14;
            this.IPBox.Text = "IP:";
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.button1.Location = new System.Drawing.Point(12, 217);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(109, 43);
            this.button1.TabIndex = 10;
            this.button1.Text = "start server";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.button2.Location = new System.Drawing.Point(643, 256);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(112, 51);
            this.button2.TabIndex = 11;
            this.button2.Text = "Get processes for Ip";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Visible = false;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // Clients
            // 
            this.Clients.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.Clients.FormattingEnabled = true;
            this.Clients.HorizontalScrollbar = true;
            this.Clients.ItemHeight = 15;
            this.Clients.Location = new System.Drawing.Point(256, 25);
            this.Clients.Name = "Clients";
            this.Clients.ScrollAlwaysVisible = true;
            this.Clients.Size = new System.Drawing.Size(117, 94);
            this.Clients.TabIndex = 12;
            this.Clients.SelectedIndexChanged += new System.EventHandler(this.Clients_SelectedIndexChanged);
            // 
            // processes
            // 
            this.processes.AutoGenerateColumns = false;
            this.processes.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.processes.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.pIDDataGridViewTextBoxColumn,
            this.pnameDataGridViewTextBoxColumn,
            this.usingDataGridViewTextBoxColumn});

            this.processes.Location = new System.Drawing.Point(413, 13);
            this.processes.MultiSelect = false;
            this.processes.Name = "processes";
            this.processes.ReadOnly = true;
            this.processes.Size = new System.Drawing.Size(342, 221);
            this.processes.TabIndex = 13;
            // 
            // AddClientB
            // 
            this.AddClientB.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.AddClientB.Location = new System.Drawing.Point(12, 217);
            this.AddClientB.Name = "AddClientB";
            this.AddClientB.Size = new System.Drawing.Size(110, 43);
            this.AddClientB.TabIndex = 14;
            this.AddClientB.Text = "Add a Client";
            this.AddClientB.UseVisualStyleBackColor = true;
            this.AddClientB.Visible = false;
            this.AddClientB.Click += new System.EventHandler(this.AddClientB_Click);
            // 
            // TUsingBox
            // 
            this.TUsingBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.TUsingBox.Location = new System.Drawing.Point(471, 256);
            this.TUsingBox.Multiline = true;
            this.TUsingBox.Name = "TUsingBox";
            this.TUsingBox.Size = new System.Drawing.Size(92, 35);
            this.TUsingBox.TabIndex = 15;
            this.TUsingBox.Text = "Using:";
           
           
            // 
            // pIDDataGridViewTextBoxColumn
            // 
            this.pIDDataGridViewTextBoxColumn.DataPropertyName = "PID";
            this.pIDDataGridViewTextBoxColumn.HeaderText = "PID";
            this.pIDDataGridViewTextBoxColumn.Name = "pIDDataGridViewTextBoxColumn";
            this.pIDDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // pnameDataGridViewTextBoxColumn
            // 
            this.pnameDataGridViewTextBoxColumn.DataPropertyName = "Pname";
            this.pnameDataGridViewTextBoxColumn.HeaderText = "Pname";
            this.pnameDataGridViewTextBoxColumn.Name = "pnameDataGridViewTextBoxColumn";
            this.pnameDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // usingDataGridViewTextBoxColumn
            // 
            this.usingDataGridViewTextBoxColumn.DataPropertyName = "Using";
            this.usingDataGridViewTextBoxColumn.HeaderText = "Using";
            this.usingDataGridViewTextBoxColumn.Name = "usingDataGridViewTextBoxColumn";
            this.usingDataGridViewTextBoxColumn.ReadOnly = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(767, 420);
            this.Controls.Add(this.TUsingBox);
            this.Controls.Add(this.AddClientB);
            this.Controls.Add(this.processes);
            this.Controls.Add(this.Clients);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.textBox2);
            this.Controls.Add(this.textBox1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.flowLayoutPanel1.ResumeLayout(false);
            this.flowLayoutPanel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.processes)).EndInit();
           
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        public System.Windows.Forms.TextBox textBox1;
        public System.Windows.Forms.TextBox textBox2;
        public System.Windows.Forms.TextBox UUIDbox;
        public System.Windows.Forms.TextBox UserNameBox;
        public System.Windows.Forms.TextBox OsBox;
        public System.Windows.Forms.TextBox CPUBox;
        public System.Windows.Forms.TextBox CpuNumBox;
        public System.Windows.Forms.TextBox RAMBox;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        public System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        public System.Windows.Forms.ListBox Clients;
        public System.Windows.Forms.DataGridView processes;
        public System.Windows.Forms.TextBox IPBox;
        public System.Windows.Forms.Button AddClientB;
        public System.Windows.Forms.TextBox TUsingBox;
        private System.Windows.Forms.BindingSource table1BindingSource;
        private System.Windows.Forms.DataGridViewTextBoxColumn pIDDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn pnameDataGridViewTextBoxColumn;
        private System.Windows.Forms.DataGridViewTextBoxColumn usingDataGridViewTextBoxColumn;
    }
}

