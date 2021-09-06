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
    NumberOfModules = 3
    Module = ListContainer:
        Container:
            NumberOfCells = 15
            CellVoltages = ListContainer:
                3.306
                3.307
                3.305
                3.305
                3.306
                3.305
                3.304
                3.305
                3.306
                3.306
                3.307
                3.307
                3.308
                3.307
                3.306
            NumberOfTemperatures = 5
            AverageBMSTemperature = 29.81
            GroupedCellsTemperatures = ListContainer:
                29.61
                29.61
                29.61
                29.61
            Current = -3.5
            Voltage = 49.59
            Power = -173.565
            RemainingCapacity = 39.5
            TotalCapacity = 50.0
            CycleNumber = 5
    -->8-- SNIP -->8--
    TotalPower = -525.8022
    StateOfCharge = 0.79

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
