# Installing San On Windows

 To download and use San into your own system, use the following methods, corresponding to your operating system.

 ### Windows
 - First install git into your computer:
 ```bash
 winget install --id Git.Git -e --source winget
 ```
 - Install Python
 ```bash
winget install Python.Python
 ```

 - Clone the GitHub repository:
 ```bash
git clone https://anubhav-1207/san
 ```
 - Enter San directory
 ```bash
 cd san
 ```

 > Now, while inside the `san` directory, you can use python to run your own `.san` files:
 
 ###### Usage: Remove the '<>' while actually running San.
 ```bash
python main.py <file.san>
 ```
