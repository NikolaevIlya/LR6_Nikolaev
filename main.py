import wmi
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('usb_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class USBMonitorWindows:
    def __init__(self, allowed_devices):
        """
        allowed_devices: список разрешенных идентификаторов (VID/PID или части DeviceID)
        """
        self.allowed_devices = set(allowed_devices)
        self.wmi_conn = wmi.WMI()
        self.known_devices = set()

    def get_normalized_id(self, device_id):
        """
        Нормализует DeviceID, удаляя динамическую часть
        Оставляет только VID/PID и постоянные идентификаторы
        """
        # Разделяем DeviceID по обратному слешу
        parts = device_id.split('\\')
        if len(parts) >= 2:
            # Берем первую часть (USB) и VID/PID
            # Например: USB\VID_09DA&PID_79A1
            return f"{parts[0]}\\{parts[1]}"
        return device_id

    def get_current_usb_devices(self):
        """
        Получение списка текущих USB устройств
        """
        devices = {}
        for usb in self.wmi_conn.Win32_USBHub():
            if usb.DeviceID and usb.Name:
                # Получаем нормализованный ID
                normalized_id = self.get_normalized_id(usb.DeviceID)

                devices[usb.DeviceID] = {
                    'name': usb.Name,
                    'device_id': usb.DeviceID,
                    'normalized_id': normalized_id,
                    'description': usb.Description or ''
                }
        return devices

    def is_allowed(self, device_id, normalized_id, device_name):
        """
        Проверка, разрешено ли устройство
        Сравниваем по нормализованному ID и имени
        """
        # Проверяем по нормализованному ID (VID/PID)
        if normalized_id in self.allowed_devices:
            return True, f"Device match by VID/PID: {normalized_id}"

        # Проверяем, содержится ли разрешенный ID в нормализованном
        for allowed in self.allowed_devices:
            if allowed in normalized_id:
                return True, f"Device match by partial VID/PID: {allowed}"

        # Проверяем по имени устройства
        device_name_lower = device_name.lower()
        for allowed in self.allowed_devices:
            if allowed.lower() in device_name_lower:
                return True, f"Name match: {allowed}"

        return False, None

    def start_monitoring(self):
        """
        Запуск мониторинга USB устройств
        """
        logging.info("=" * 50)
        logging.info("USB мониторинг запущен (Windows)")
        logging.info(f"Разрешенные устройства: {len(self.allowed_devices)} записей")
        logging.info("=" * 50)

        # Выводим разрешенные ID
        for i, dev in enumerate(list(self.allowed_devices)[:5]):
            logging.info(f"  Разрешено {i + 1}: {dev}")
        if len(self.allowed_devices) > 5:
            logging.info(f"  ... и еще {len(self.allowed_devices) - 5}")

        # Получаем начальный список устройств
        current_devices = self.get_current_usb_devices()
        self.known_devices = set(current_devices.keys())

        logging.info(f"Обнаружено {len(self.known_devices)} USB устройств")

        # Выводим текущие устройства для отладки
        for dev_id, dev_info in current_devices.items():
            logging.info(f"  Текущее: {dev_info['name']} -> {dev_info['normalized_id']}")

        try:
            while True:
                current_devices = self.get_current_usb_devices()
                current_ids = set(current_devices.keys())

                # Проверяем новые устройства
                new_devices = current_ids - self.known_devices

                for dev_id in new_devices:
                    device = current_devices[dev_id]
                    device_name = device['name']
                    normalized_id = device['normalized_id']

                    allowed, reason = self.is_allowed(dev_id, normalized_id, device_name)

                    if allowed:
                        logging.info(f"[+] РАЗРЕШЕНО: {device_name}")
                        logging.info(f"    DeviceID: {dev_id}")
                        logging.info(f"    Normalized ID: {normalized_id}")
                        logging.info(f"    Причина: {reason}")
                    else:
                        logging.warning(f"[!] НЕИЗВЕСТНОЕ УСТРОЙСТВО: {device_name}")
                        logging.warning(f"    DeviceID: {dev_id}")
                        logging.warning(f"    Normalized ID: {normalized_id}")

                        # Здесь можно добавить дополнительные действия
                        # Например, отправить уведомление или запустить скрипт блокировки

                # Проверяем отключенные устройства
                removed_devices = self.known_devices - current_ids
                for dev_id in removed_devices:
                    logging.info(f"[-] Устройство отключено: {dev_id}")

                self.known_devices = current_ids
                time.sleep(2)  # Проверяем каждые 2 секунды

        except KeyboardInterrupt:
            logging.info("Мониторинг остановлен пользователем")
        except Exception as e:
            logging.error(f"Ошибка: {e}", exc_info=True)


def main():
    # Список разрешенных устройств - используем только VID/PID часть
    allowed = [
        "USB\VID_09DA&PID_79A1",  # Постоянная часть DeviceID
        # Можно добавить другие устройства:
        # "USB\VID_046D&PID_C52B",  # Logitech
        # "USB\VID_0781&PID_5583",  # SanDisk
    ]

    monitor = USBMonitorWindows(allowed)
    monitor.start_monitoring()


if __name__ == "__main__":
    main()