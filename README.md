# python-pylontech
Python lib to talk to pylontech lithium batteries (US2000, US3000, ...) using RS485

## What is this lib ?
This lib is meant to talk to Pylontech batteries using RS485. Sadly the protocol over RS485 is not some fancy thing like MODBUS but their own crappy protocol.

## How to use this lib ?
First of all, you need a USB to RS485 converter. They are many available online for some bucks.

Then, you simply need to import the lib and start asking values:
```python

>>> import pylontech
>>> p = pylontech.Pylontech()
>>> print(p.get_values())
Container: 
    CommandValue = 1
    NumberOfCells = 15
    CellVoltages = ListContainer: 
        3.325
        3.326
        3.325
        3.325
        3.325
        3.325
        3.325
        3.324
        3.324
        3.324
        3.326
        3.326
        3.326
        3.326
        3.326
    NumberOfTemperatures = 5
    AverageBMSTemperature = 30.01
    GroupedCellsTemperatures = ListContainer: 
        29.61
        29.61
        29.61
        29.61
    Current = 0
    Voltage = 49.878
    RemainingCapacity = 49.0
    TotalCapacity = 50.0
    CycleNumber = 0
>>> print(p.get_system_parameters())
Container: 
    CellHighVoltageLimit = 3.7
    CellLowVoltageLimit = 3.05
    CellUnderVoltageLimit = 2.9
    ChargeHighTemperatureLimit = 33.41
    ChargeLowTemperatureLimit = 26.21
    ChargeCurrentLimit = 10.2
    ModuleHighVoltageLimit = 54.0
    ModuleLowVoltageLimit = 46.0
    ModuleUnderVoltageLimit = 44.5
    DischargeHighTemperatureLimit = 33.41
    DischargeLowTemperatureLimit = 26.21
    DischargeCurrentLimit = -10.0
```

## Dependencies
This lib depends on `pyserial` and the awesome `construct` lib.