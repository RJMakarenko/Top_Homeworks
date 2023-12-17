from abc import ABC, abstractmethod


class SmartDevice(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def get_the_status(self):
        pass


class SmartLamp(SmartDevice):
    def __init__(self, name: str, status: bool = False, bright: int = 0):
        super().__init__(name)
        self.status = status
        self.bright = bright

    def turn_on(self) -> None:
        self.status = True
        print(f'Устройство {self.name} включена!')

    def turn_off(self) -> None:
        self.status = False
        print(f'Лампа {self.name} выключена')

    def get_the_status(self) -> None:
        if self.status:
            print(f'Лампа {self.name} включена! Яркость установлена на значении {self.bright}')
        else:
            print(f'Лампа {self.name} выключена!')

    def change_bright(self, value: int) -> None:
        self.bright = value


class SmartSmokeDetector(SmartDevice):
    def __init__(self, name: str, status: bool = False):
        super().__init__(name)
        self.status = status

    def turn_on(self) -> None:
        self.status = True
        print(f'Датчик {self.name} включен!')

    def turn_off(self) -> None:
        self.status = False
        print(f'Датчик {self.name} выключен!')

    def get_the_status(self) -> None:
        if self.status:
            print(f'Датчик {self.name} включен!')
        else:
            print(f'Датчик {self.name} выключен!')

    def check_smoke(self, value: int) -> None:
        self.bright = value


class SmartAirHumidifier(SmartDevice):
    def __init__(self, name: str, status: bool = False, humidity_level: int = 50):
        super().__init__(name)
        self.status = status
        self.humidity_level = humidity_level

    def turn_on(self) -> None:
        self.status = True
        print(f'Устройство "{self.name}" включено!')

    def turn_off(self) -> None:
        self.status = False
        print(f'Устройство "{self.name}" выключено')

    def get_the_status(self) -> None:
        if self.status:
            print(f'Устройство "{self.name}" работает! Уровень влажности установлен на значении {self.humidity_level}')
        else:
            print(f'Устройство "{self.name}" выключено!')

    def change_humidity_level(self, value: int) -> None:
        if self.status:
            self.humidity_level = value
        else:
            print('Сначала включите устройство!')


class UrgentNotification:
    def send_notification(self, message):
        print(message)


class WiFiConnect:
    ssid = ''
    password = ''

    def set_wifi_settings(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def get_wifi_settings(self):
        if self.ssid:
            print('Настройки сети wifi установлены.')
            print(f'Имя сети: {self.ssid}\nПароль: {self.password}\n')
        else:
            print(f'Устройство не подключено к wifi сети!')

    def wifi_connect(self, ssid):
        if self.ssid:
            print(f'Устройство успешно подключено к сети {ssid}')
        else:
            print('Настройки WiFi не заданы!')


class WorkSchedule:
    schedule = 'Не задано'

    def set_schedule(self, schedule):
        self.schedule = schedule
        print('Расписание работы успешно установлено!')

    def get_schedule(self):
        print(f'Текущий режим работы: {self.schedule}')


class AirHumidifierWifiSchedule(SmartAirHumidifier, WiFiConnect, WorkSchedule):
    """
    Умный увлажнитель воздуха с WiFi и расписанием работы
    """

    def __init__(self, name):
        super().__init__(name)


class SmartSmokeDetectorWiFiNotification(SmartSmokeDetector, WiFiConnect, UrgentNotification):
    """
    Умный детектор дыма с WiFi и отправкой срочных сообщений
    """

    def __init__(self, name):
        super().__init__(name)


class SmartLampWiFiSchedule(SmartLamp, WiFiConnect, WorkSchedule):
    """
    Умная лампа с WiFi и расписанием работы
    """
    def __init__(self, name):
        super().__init__(name)

# Проверяем работу увлажнителя
air_humidifier_1 = AirHumidifierWifiSchedule('Увлажнитель в спальне')
air_humidifier_1.turn_on()  # Включаем устройство
air_humidifier_1.change_humidity_level(40)  # Установим новый уровень влажности
air_humidifier_1.get_the_status()  # Получим статус устройства
air_humidifier_1.get_wifi_settings()  # Получим текущие настройки wifi
air_humidifier_1.set_wifi_settings('MyNet', '12345678')  # Установим настройки wifi
air_humidifier_1.wifi_connect('MyNet')  # Подключаем устройство к сети
air_humidifier_1.get_schedule()  # Получим текущее расписание
air_humidifier_1.set_schedule('08:00 - 14:00')  # Установим новое расписание
air_humidifier_1.get_schedule()  # Получим текущее расписание

# Проверяем работу датчика дыма
smoke_detector = SmartSmokeDetectorWiFiNotification('Датчик дыма в гостиной')
smoke_detector.turn_on()
smoke_detector.get_the_status()
smoke_detector.get_wifi_settings()
smoke_detector.set_wifi_settings('MyNet', '12345678')
smoke_detector.wifi_connect('MyNet')
smoke_detector.get_wifi_settings()
smoke_detector.send_notification('Обнаружен дым!!!')

# Проверяем работу умной лампы
smart_lamp = SmartLampWiFiSchedule('Лампа в детской')
smart_lamp.turn_on()  # Включаем устройство
smart_lamp.change_bright(80)  # Установим новый уровень яркости
smart_lamp.get_the_status()  # Получим статус устройства
smart_lamp.get_wifi_settings()  # Получим текущие настройки wifi
smart_lamp.set_wifi_settings('MyNet', '12345678')  # Установим настройки wifi
smart_lamp.wifi_connect('MyNet')  # Подключаем устройство к сети
smart_lamp.get_schedule()  # Получим текущее расписание
smart_lamp.set_schedule('18:00 - 21:00')  # Установим новое расписание
smart_lamp.get_schedule()  # Получим текущее расписание