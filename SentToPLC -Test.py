from pymodbus.client import ModbusTcpClient
import json

# Konfigürasyonu yükle
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# Gönderilecek veriyi JSON dosyasından yükle
def load_test_data():
    with open("test_data.json", "r") as file:
        return json.load(file)

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

    try:
        # Veri 1 (CHAR, 18 karakter)
        data.extend(convert_char_to_ascii(str(test_veri["Veri1"]), 18))

        # Veri 2 (CHAR, 40 karakter)
        data.extend(convert_char_to_ascii(str(test_veri["Veri2"]), 40))

        # Veri 3 (CHAR, 2 karakter)
        data.extend(convert_char_to_ascii(str(test_veri["Veri3"]), 2))

        # Veri 4 (CHAR, 2 karakter)
        data.extend(convert_char_to_ascii(str(test_veri["Veri4"]), 2))

        # Veri 5 (DECIMAL, 5.2) -> Ölçekleme
        data.append(int(test_veri["Veri5"] * 100))  # 100.50 -> 10050

        # Veri 6 (DECIMAL, 5.2) -> Ölçekleme
        data.append(int(test_veri["Veri6"] * 100))  # 1.00 -> 100

        # Veri 7 (DECIMAL, 1.0)
        data.append(int(test_veri["Veri7"]))  # 0 -> 0

    except KeyError as e:
        print(f"Hata: Eksik veri anahtarı: {e}")
    except ValueError as e:
        print(f"Hata: Geçersiz değer türü: {e}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

    return data


def send_to_plc(data, plc_ip, plc_port):
    """
    PLC'ye Modbus TCP üzerinden veriyi gönderir.
    """
    try:
        # PLC'ye bağlan
        client = ModbusTcpClient(plc_ip, port=plc_port)
        client.connect()

        # Veriyi PLC'ye yaz
        start_address = 0  # Register başlangıç adresi
        client.write_registers(start_address, data)

        print("Veri başarıyla PLC'ye gönderildi:", data)
        client.close()
    except Exception as e:
        print("PLC bağlantı hatası:", e)

if __name__ == "__main__":
    print("SentToPLC başladı.")

    # Konfigürasyonu yükle
    try:
        config = load_config()
        PLC_IP = config["PLC_IP"]
        PLC_PORT = config["PLC_PORT"]
    except Exception as e:
        print("Config yüklenirken hata:", e)

    # Gönderilecek veriyi yükle
    try:
        test_veri = load_test_data()
    except Exception as e:
        print("Test verisi yüklenirken hata:", e)

    # Veriyi hazırla
    try:
        prepared_data = prepare_data(test_veri)
        print("Hazırlanan veri:", prepared_data)
    except Exception as e:
        print("Veri hazırlama sırasında hata:", e)

    # PLC'ye gönder
    try:
        send_to_plc(prepared_data, PLC_IP, PLC_PORT)
    except Exception as e:
        print("PLC'ye gönderim sırasında hata:", e)

