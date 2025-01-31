# ModBusTCPServer

## 📖 Project Description
This project is a **Python-based Modbus TCP server** designed to facilitate **communication between a PLC (or any Modbus-compatible device) and a client application**.  
It processes incoming data **based on a JSON configuration file (`datatypes.json`)**, making it easy to parse and display structured Modbus messages.

## 🎯 **Features**
- **Starts a Modbus TCP server** and logs incoming/outgoing data.
- **Converts received data into human-readable ASCII and numeric formats.**
- **Uses a JSON-based configuration file** to dynamically interpret incoming data.
- **Provides flexibility for different Modbus test cases and PLC communication projects.**

---

## 🚀 **Installation & Usage**

### 1️⃣ **Requirements**
Ensure that the following dependencies are installed:
- **Python 3.8+**  
- **pymodbus** library  
- **Git (Optional, for cloning the repository)**  

### 2️⃣ **Installing Dependencies**
Before running the project, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 3️⃣ **Running the Modbus TCP Server**
Run the server using the following command:

```sh
python ModBusTCPServer.py
```

## 📝 Author

**👤 Mehmet Solmaz, PhD**  
📧 **Email:** mehmet@example.com  
🔗 **GitHub:** [misolmaz](https://github.com/misolmaz)  
🔗 **LinkedIn:** [linkedin.com/in/mehmetsolmaz](https://linkedin.com/in/mehmetsolmaz)  

---

## 🛡️ License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

### ✅ Fixes & Improvements in This Version
- **Fixed incorrect markdown formatting in the Author section.**
- **Closed missing markdown syntax issues.**
- **Properly formatted command blocks for better readability.**
- **Added a 'Running the Server' section for clarity.**
 