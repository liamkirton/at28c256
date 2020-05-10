constexpr uint32_t PIN_SER = 2;
constexpr uint32_t PIN_SRCLK = 3;
constexpr uint32_t PIN_RCLK = 4;
constexpr uint32_t PIN_WE = 13;

constexpr uint32_t PIN_D0 = 5;

void write_address(uint16_t address, bool write) {
    address = (address & 0x7fff) | ((write ? 1 : 0) << 15);

    for (int8_t i = 15; i >= 0; --i) {
        bool bit = address & (1 << i);
        digitalWrite(PIN_SER, bit ? HIGH : LOW);
        digitalWrite(PIN_SRCLK, HIGH);
        delayMicroseconds(100);
        digitalWrite(PIN_SRCLK, LOW);
    }

    digitalWrite(PIN_RCLK, HIGH);
    delayMicroseconds(100);
    digitalWrite(PIN_RCLK, LOW);
}

uint8_t read_value(uint16_t address) {
    write_address(address, false);

    uint8_t v = 0;
    for (uint8_t i = 0; i < 8; ++i) {
        v |= (digitalRead(PIN_D0 + i) ? 1 : 0) << i;
    }

    return v;
}

uint16_t write_value(uint16_t address, uint8_t v) {
    for (uint8_t retry = 0; retry < 3; ++retry) {
        write_address(address, true);
    
        for (uint8_t i = 0; i < 8; ++i) {
            pinMode(PIN_D0 + i, OUTPUT);
            digitalWrite(PIN_D0 + i, ((v & (1 << i)) != 0) ? HIGH : LOW);
        }
    
        digitalWrite(PIN_WE, LOW);
        delayMicroseconds(1);
        digitalWrite(PIN_WE, HIGH);
    
        for (uint8_t i = 0; i < 8; ++i) {
            pinMode(PIN_D0 + i, INPUT);
        }
    
        write_address(address, false);
    
        for (uint16_t wait = 0; wait < 0xffff; ++wait) {
            if ((digitalRead(PIN_D0 + 7) == HIGH) == ((v & (1 << 7)) != 0)) {
                return wait;
            }
        }
    }

    return 0xffff;
}

void setup() {
    pinMode(PIN_SER, OUTPUT);
    pinMode(PIN_SRCLK, OUTPUT);
    pinMode(PIN_RCLK, OUTPUT);
    pinMode(PIN_WE, OUTPUT);

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);

    for (uint8_t i = 0; i < 8; ++i) {
        pinMode(PIN_D0 + i, INPUT);
    }

    digitalWrite(PIN_SER, LOW);
    digitalWrite(PIN_SRCLK, LOW);
    digitalWrite(PIN_RCLK, LOW);
    digitalWrite(PIN_WE, HIGH);
    delay(100);

    Serial.begin(115200);
    Serial.println("Arduino AT28C256");
}

void loop() {
    if (Serial.available() > 0) {
        auto cmd = Serial.read();

        uint16_t address{ 0 };
        uint8_t value{ 0 };

        switch(cmd) {
            case 0x1:
                Serial.readBytes(reinterpret_cast<char *>(&address), sizeof(address));
                value = read_value(address);
                Serial.write(value);
                break;

            case 0x2:
                Serial.readBytes(reinterpret_cast<char *>(&address), sizeof(address));
                Serial.readBytes(reinterpret_cast<char *>(&value), sizeof(value));
                write_value(address, value);
                Serial.write(0);
                break;
        }
    }
}
