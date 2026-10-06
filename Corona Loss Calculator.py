import math


class CoronaLossCalculator:
    def __init__(self, voltage, frequency, conductor_radius,
                 conductor_spacing, air_density=1.0):
        self.voltage = voltage
        self.frequency = frequency
        self.conductor_radius = conductor_radius
        self.conductor_spacing = conductor_spacing
        self.air_density = air_density

    def calculate_disruptive_voltage(self):
        # Peek's formula
        # Vd = 21.1 * m0 * delta * r * ln(D/r)
        # Voltage is calculated per conductor in kV

        m0 = 0.85  # surface irregularity factor for stranded conductor

        vd = (
            21.1
            * m0
            * self.air_density
            * self.conductor_radius
            * math.log(
                self.conductor_spacing / self.conductor_radius
            )
        )

        return vd

    def calculate_corona_loss(self):
        # Convert line voltage to phase voltage
        phase_voltage = self.voltage / math.sqrt(3)

        disruptive_voltage = self.calculate_disruptive_voltage()

        if phase_voltage <= disruptive_voltage:
            return 0.0, disruptive_voltage

        # Peek's simplified corona loss formula
        corona_loss = (
            241
            * (self.frequency + 25)
            / self.air_density
            * math.sqrt(
                self.conductor_radius / self.conductor_spacing
            )
            * (phase_voltage - disruptive_voltage) ** 2
            * 1e-5
        )

        return corona_loss, disruptive_voltage

    def display_result(self):

        corona_loss, disruptive_voltage = (
            self.calculate_corona_loss()
        )

        phase_voltage = self.voltage / math.sqrt(3)

        print("\n----- CORONA LOSS CALCULATOR -----")

        print(f"Line Voltage              : {self.voltage:.2f} kV")
        print(f"Phase Voltage             : {phase_voltage:.2f} kV")
        print(f"Frequency                 : {self.frequency:.2f} Hz")
        print(
            f"Conductor Radius         : "
            f"{self.conductor_radius:.2f} cm"
        )
        print(
            f"Conductor Spacing        : "
            f"{self.conductor_spacing:.2f} cm"
        )
        print(f"Air Density Factor        : {self.air_density:.2f}")

        print(
            f"\nDisruptive Voltage       : "
            f"{disruptive_voltage:.2f} kV"
        )

        print(
            f"Corona Power Loss        : "
            f"{corona_loss:.4f} kW/km"
        )

        if corona_loss == 0:
            print("\nCorona Status             : NO CORONA")
        elif corona_loss < 1:
            print("\nCorona Status             : LOW CORONA LOSS")
        elif corona_loss < 5:
            print("\nCorona Status             : MODERATE CORONA LOSS")
        else:
            print("\nCorona Status             : HIGH CORONA LOSS")


def main():

    print("======================================")
    print("       CORONA LOSS CALCULATOR")
    print("======================================")

    try:
        voltage = float(
            input("\nEnter transmission line voltage (kV): ")
        )

        frequency = float(
            input("Enter frequency (Hz): ")
        )

        radius = float(
            input("Enter conductor radius (cm): ")
        )

        spacing = float(
            input("Enter conductor spacing (cm): ")
        )

        air_density = float(
            input("Enter air density factor (default 1.0): ")
        )

        if (
            voltage <= 0
            or frequency <= 0
            or radius <= 0
            or spacing <= 0
            or air_density <= 0
        ):
            print("\nPlease enter positive values.")
            return

        if spacing <= radius:
            print("\nConductor spacing must be greater than radius.")
            return

        calculator = CoronaLossCalculator(
            voltage,
            frequency,
            radius,
            spacing,
            air_density
        )

        calculator.display_result()

    except ValueError:
        print("\nInvalid input! Please enter numerical values.")


if __name__ == "__main__":
    main()
