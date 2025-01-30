from pymodbus.client import ModbusTcpClient
import json

# Konfigürasyonu yükle
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# Config'den IP ve Port bilgilerini al
config = load_config()
PLC_IP = config["PLC_IP"]
PLC_PORT = config["PLC_PORT"]

# Test verisi
test_veri = {
    "Veri 1": "Test123456789012",  # CHAR, 18 karakter
    "Veri 2": "DenemeVerisiTest12345678901234567890",  # CHAR, 40 karakter
    "Veri 3": "TR",  # CHAR, 2 karakter
    "Veri 4": 12,     # DEC, 2 basamaklı
    "Veri 5": 34,     # DEC, 2 basamaklı
    "Veri 6": "A123", # CHAR, 4 karakter
    "Veri 7": "XYZ1234" # CHAR, 7 karakter
}

def convert_char_to_ascii(value, length):
    """
    CHAR değerlerini ASCII kodlarına çevirir ve belirtilen uzunluğa göre doldurur.
    """
    ascii_values = [ord(char) for char in value]
    # Eksikse 0 ile doldur
    ascii_values.extend([0] * (length - len(ascii_values)))
    return ascii_values[:length]  # Fazlalık varsa kes

def prepare_data(test_veri):
    """
    Veriyi Modbus register'larına yazılabilir forma dönüştürür.
    """
    data = []

    # Veri 1 (CHAR, 18 karakter)
    data.extend(convert_char_to_ascii(test_veri["Veri 1"], 18))

    # Veri 2 (CHAR, 40 karakter)
    data.extend(convert_char_to_ascii(test_veri["Veri 2"], 40))

    # Veri 3 (CHAR, 2 karakter)
    data.extend(convert_char_to_ascii(test_veri["Veri 3"], 2))

    # Veri 4 (DEC, 2 basamaklı)
    data.append(test_veri["Veri 4"])

    # Veri 5 (DEC, 2 basamaklı)
    data.append(test_veri["Veri 5"])

    # Veri 6 (CHAR, 4 karakter)
    data.extend(convert_char_to_ascii(test_veri["Veri 6"], 4))

    # Veri 7 (CHAR, 7 karakter)
    data.extend(convert_char_to_ascii(test_veri["Veri 7"], 7))

    return data

def send_to_plc(data):
    """
    PLC'ye Modbus TCP üzerinden veriyi gönderir.
    """
    try:
        # PLC'ye bağlan
        client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
        client.connect()

        # Veriyi PLC'ye yaz
        start_address = 0  # Register başlangıç adresi
        client.write_registers(start_address, data)

        print("Veri başarıyla PLC'ye gönderildi:", data)
        client.close()
    except Exception as e:
        print("PLC bağlantı hatası:", e)

if __name__ == "__main__":
    # Veriyi hazırla
    prepared_data = prepare_data(test_veri)
    print("Hazırlanan veri:", prepared_data)

    # PLC'ye gönder
    send_to_plc(prepared_data)
