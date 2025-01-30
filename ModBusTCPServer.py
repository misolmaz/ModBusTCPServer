import json
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

# Logger Ayarları
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


# JSON Yapılandırma Dosyası Yükleme
def load_config(config_file="datatypes.json"):
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


config = load_config()


# ASCII dönüştürücü
def convert_to_ascii(values):
    try:
        return ''.join(chr(v) for v in values if 32 <= v <= 126 or v == 0x20)
    except:
        return str(values)


# Gelen veriyi JSON yapılandırmasına göre anlamlı hale getiren fonksiyon
def parse_received_data(values, start_address):
    parsed_data = {}
    base_offset = start_address % 100  # Her 100'lük blok için kaydırma

    for field in config["fields"]:
        offset = field["offset"] + base_offset
        length = field["length"]
        data_type = field["type"]
        label = f"Bant {start_address // 100} - {field['name']}"

        if data_type == "CHAR" or data_type == "NCHAR":
            parsed_data[label] = ''.join(chr(v) for v in values[offset:offset + length]).rstrip()
        elif data_type == "DECIMAL":
            parsed_data[label] = values[offset] / 100 if length == 5.2 else values[offset]

    for key, value in parsed_data.items():
        log.info(f"{key}: '{value}'")

    return parsed_data


# Özel Modbus Slave Context
class CustomModbusSlaveContext(ModbusSlaveContext):
    def setValues(self, fx, address, values):
        if fx == 16:
            parsed_data = parse_received_data(values, address)
            log.info(f"Yazma İşlemi: Function={fx}, Address={address}")
        else:
            log.info(f"Yazma İşlemi: Function={fx}, Address={address}, Values={values}")
        super().setValues(fx, address, values)

    def getValues(self, fx, address, count=1):
        values = super().getValues(fx, address, count)
        if fx == 3:
            parsed_data = parse_received_data(values, address)
            log.info(f"Okuma İşlemi: Function={fx}, Address={address}")
        else:
            log.info(f"Okuma İşlemi: Function={fx}, Address={address}, Values={values}")
        return values


# Veri bloğu oluştur ve özel context ata
store = CustomModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 1000),
    co=ModbusSequentialDataBlock(0, [0] * 1000),
    hr=ModbusSequentialDataBlock(0, [0] * 1000),
    ir=ModbusSequentialDataBlock(0, [0] * 1000),
)
context = ModbusServerContext(slaves=store, single=True)

# Sunucuyu Başlat
if __name__ == "__main__":
    print("Modbus TCP Sunucusu Başladı...")
    StartTcpServer(context, address=("127.0.0.1", 502))
