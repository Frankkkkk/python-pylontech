import sys
from typing import List
from pytest import approx

sys.path.extend("..")

import pylontech
from pylontech.pylontech import ToVolt, ToAmp, ToCelsius, DivideBy1000
import construct


class MockSerial(object):
    def __init__(self, responses: List[bytes]):
        self.responses = responses

    def readline(self) -> bytes:
        assert len(self.responses) > 0
        reply = self.responses[0]
        self.responses = self.responses[1:]
        return reply

    def write(self, data: bytes):
        print(f"write: {data}")


class Pylontech(pylontech.Pylontech):
    def __init__(self, responses):
        self.s = MockSerial(responses)


def test_us2000_3modules_info_parsing_1():

    p = Pylontech(
        [
            b"~20024600914211030F0CE70CE80CE60CE70CE80CE80CE80CE60CE50CE60CE80CE70CEA0CE50CE6050B910B870B870B870B87FFE6C18982DC02C350001F0F0CE20CE60CE60CE10CE50CE70CE60CE30CE20CE50CE30CE90CE70CE90CE9050B910B870B870B870B87FFE7C17082DC02C350001F0F0CE20CE50CE50CE20CE30CE30CE40CE50CE60CE60CE30CE40CE40CE60CE6050B910B7D0B7D0B7D0B7DFFE5C16082DC02C350001FB476\r"
        ]
    )

    d = p.get_values()

    assert d.NumberOfModules == 3
    m = d.Module[0]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.303,
            3.304,
            3.302,
            3.303,
            3.304,
            3.304,
            3.304,
            3.302,
            3.301,
            3.302,
            3.304,
            3.303,
            3.306,
            3.301,
            3.302,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([22.0, 22.0, 22.0, 22.0])
    assert m.Current == approx(-2.6)
    assert m.Voltage == approx(49.545)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 31
    assert m.AverageBMSTemperature == approx(23.0)
    assert m.RemainingCapacity == approx(33.5)
    assert m.TotalCapacity == approx(50)

    m = d.Module[1]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.298,
            3.302,
            3.302,
            3.297,
            3.301,
            3.303,
            3.302,
            3.299,
            3.298,
            3.301,
            3.299,
            3.305,
            3.303,
            3.305,
            3.305,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([22.0, 22.0, 22.0, 22.0])
    assert m.Current == approx(-2.5)
    assert m.Voltage == approx(49.52)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 31
    assert m.AverageBMSTemperature == approx(23.0)
    assert m.RemainingCapacity == approx(33.5)
    assert m.TotalCapacity == approx(50)

    m = d.Module[2]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.298,
            3.301,
            3.301,
            3.298,
            3.299,
            3.299,
            3.3,
            3.301,
            3.302,
            3.302,
            3.299,
            3.3,
            3.3,
            3.302,
            3.302,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([21.0, 21.0, 21.0, 21.0])
    assert m.Current == approx(-2.7)
    assert m.Voltage == approx(49.504)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 31
    assert m.AverageBMSTemperature == approx(23.0)
    assert m.RemainingCapacity == approx(33.5)
    assert m.TotalCapacity == approx(50)

    assert d.TotalPower == approx(-386.2778)
    assert d.StateOfCharge == approx(0.67)


def test_us3000_4modules_info_parsing_1():

    p = Pylontech(
        [
            b"~2002460061DC11040F0CFD0CFC0CFC0CFB0CFC0CFB0CFD0CFC0CFC0CFB0CFA0CFD0CFB0CFE0CFA050BE10BCD0BCD0BCD0BCD0000C2C1FFFF04FFFF002F00EFEC0121100F0CEB0CEB0CEB0CEA0CEA0CEC0CEB0CEB0CE90CE80CE60CE90CE90CEA0CE8050BE10BCD0BCD0BCD0BCDFFBCC1B2FFFF04FFFF002800F2D00121100F0CE80CE90CEA0CEA0CEA0CE90CEA0CEA0CEB0CEC0CEB0CEB0CEB0CEA0CEA050BE10BC30BC30BC30BC3FFB7C1B8FFFF04FFFF007100E7400121100F0CE90CEC0CEB0CEA0CEA0CEB0CE90CE80CEA0CEA0CEA0CEB0CEC0CEA0CEA050BD70BC30BC30BC30BB9FFBBC1B9FFFF04FFFF006B00ED080121108D63\r"
        ]
    )

    d = p.get_values()
    print(d)

    assert d.NumberOfModules == 4
    m = d.Module[0]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.325,
            3.324,
            3.324,
            3.323,
            3.324,
            3.323,
            3.325,
            3.324,
            3.324,
            3.323,
            3.322,
            3.325,
            3.323,
            3.326,
            3.322,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([29.0, 29.0, 29.0, 29.0])
    assert m.Current == approx(0)  # really??
    assert m.Voltage == approx(49.857)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 47
    assert m.AverageBMSTemperature == approx(31.0)
    assert m.RemainingCapacity == approx(61.42)
    assert m.TotalCapacity == approx(74)

    m = d.Module[1]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.307,
            3.307,
            3.307,
            3.306,
            3.306,
            3.308,
            3.307,
            3.307,
            3.305,
            3.304,
            3.302,
            3.305,
            3.305,
            3.306,
            3.304,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([29.0, 29.0, 29.0, 29.0])
    assert m.Current == approx(-6.8)
    assert m.Voltage == approx(49.586)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 40
    assert m.AverageBMSTemperature == approx(31.0)
    assert m.RemainingCapacity == approx(62.16)
    assert m.TotalCapacity == approx(74)

    m = d.Module[2]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.304,
            3.305,
            3.306,
            3.306,
            3.306,
            3.305,
            3.306,
            3.306,
            3.307,
            3.308,
            3.307,
            3.307,
            3.307,
            3.306,
            3.306,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([28.0, 28.0, 28.0, 28.0])
    assert m.Current == approx(-7.3)
    assert m.Voltage == approx(49.592)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 113
    assert m.AverageBMSTemperature == approx(31.0)
    assert m.RemainingCapacity == approx(59.2)
    assert m.TotalCapacity == approx(74)

    m = d.Module[3]
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.305,
            3.308,
            3.307,
            3.306,
            3.306,
            3.307,
            3.305,
            3.304,
            3.306,
            3.306,
            3.306,
            3.307,
            3.308,
            3.306,
            3.306,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([28.0, 28.0, 28.0, 27.0])
    assert m.Current == approx(-6.9)
    assert m.Voltage == approx(49.593)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 107
    assert m.AverageBMSTemperature == approx(30.0)
    assert m.RemainingCapacity == approx(60.68)
    assert m.TotalCapacity == approx(74)

    assert d.TotalPower == approx(-1041.3981)
    assert d.StateOfCharge == approx(0.8225)


def test_mixed_us3000_us2000_status_info_parsing_1():

    p = Pylontech(
        [
            b"~2002460010F011020F0CCD0CCE0CCC0CCE0CCB0CCC0CCD0CCC0CCD0CCB0CCC0CCD0CCD0CCE0CCC050BE10BCD0BCD0BD70BCDFFC3BFFDFFFF04FFFF0234007F300121100F0CCA0CCA0CCB0CCC0CCA0CCC0CCB0CCB0CCB0CCB0CCB0CCA0CCC0CCC0CCB050BEB0BCD0BCD0BCD0BC3FFD1BFE5FFFF04FFFF0292005FB400C350C4A7\r"
        ]
    )

    d = p.get_values()
    print(d)

    assert d.NumberOfModules == 2
    m = d.Module[0]  # US3000
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.277,
            3.278,
            3.276,
            3.278,
            3.275,
            3.276,
            3.277,
            3.276,
            3.277,
            3.275,
            3.276,
            3.277,
            3.277,
            3.278,
            3.276,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([29.0, 29.0, 30.0, 29.0])
    assert m.Current == approx(-6.1)
    assert m.Voltage == approx(49.149)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 564
    assert m.AverageBMSTemperature == approx(31.0)
    assert m.RemainingCapacity == approx(32.56)
    assert m.TotalCapacity == approx(74)

    m = d.Module[1]  # US2000
    assert m.NumberOfCells == 15
    assert m.CellVoltages == approx(
        [
            3.274,
            3.274,
            3.275,
            3.276,
            3.274,
            3.276,
            3.275,
            3.275,
            3.275,
            3.275,
            3.275,
            3.274,
            3.276,
            3.276,
            3.275,
        ]
    )
    assert m.NumberOfTemperatures == 5
    assert m.GroupedCellsTemperatures == approx([29.0, 29.0, 29.0, 28.0])
    assert m.Current == approx(-4.7)
    assert m.Voltage == approx(49.125)
    assert m.Power == m.Current * m.Voltage
    assert m.CycleNumber == 658
    assert m.AverageBMSTemperature == approx(32.0)
    assert m.RemainingCapacity == approx(24.5)
    assert m.TotalCapacity == approx(50)

    assert d.TotalPower == approx(-530.6964)
    assert d.StateOfCharge == approx(0.460161)


def test_up2500_1module_status_info_parsing_1():
    p = Pylontech(
        [
            b"~20024600D05E1002080D020D020D020D030D000D010D010D03050B7D0B690B690B690B73FFFA680EFFFF04FFFF00000174E401B198E906\r"
        ]
    )

    d = p.get_values_single(2)
    assert d.NumberOfModule == 2
    assert d.NumberOfCells == 8
    assert d.CellVoltages == approx(
        [3.33, 3.33, 3.33, 3.331, 3.328, 3.329, 3.329, 3.331]
    )
    assert d.NumberOfTemperatures == 5
    assert d.GroupedCellsTemperatures == approx([19.0, 19.0, 19.0, 20.0])
    assert d.Current == approx(-0.6)
    assert d.Voltage == approx(26.638)
    assert d.Power == d.Current * d.Voltage
    assert d.CycleNumber == 0
    assert d.AverageBMSTemperature == approx(21.0)
    assert d.RemainingCapacity == approx(95.460)
    assert d.TotalCapacity == approx(111)
    assert d.TotalPower == d.Power
    assert d.StateOfCharge == approx(0.86)


def test_up2500_management_info():
    p = Pylontech([b"~20024600B014026EF05AA0022BFDD5C0F915\r"])

    d = p.get_management_info(2)

    assert d.ChargeVoltageLimit == 28.4
    assert d.DischargeVoltageLimit == 23.2
    assert d.ChargeCurrentLimit == 55.5
    assert d.DischargeCurrentLimit == -55.5
    assert d.status.ChargeEnable
    assert d.status.DischargeEnable
    assert not d.status.ChargeImmediately2
    assert not d.status.ChargeImmediately1
    assert not d.status.FullChargeRequest
    assert not d.status.ShouldCharge
