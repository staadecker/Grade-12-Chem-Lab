import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib as mpl
import numpy as np
import csv

PARTA_CAT = "\n\nPart A - Variable oxidizer"
PARTB_CAT = "Part B - Constant oxidizer, variable catalyst"

mpl.rc('font', family='georgia')


class Database:
    def __init__(self):
        self.time = {}
        self.value = {}

        self.database = None

    def add_row(self, x_value, y_value, trial):
        if trial not in self.time:
            self.time[trial] = [x_value]
            self.value[trial] = [y_value]
        else:
            self.time[trial].append(x_value)
            self.value[trial].append(y_value)


def parse_data_from_csv():
    with open('Culminating Lab Spreadsheet - Data for Python.csv') as data_file:
        reader = csv.reader(data_file, delimiter=",")

        mass_oxidizer = Database()
        mass_catalyst = Database()
        energy_oxidizer = Database()
        energy_catalyst = Database()
        percent_mass_oxidizer = Database()
        percent_mass_catalyst = Database()
        for row_index, row in enumerate(reader):
            if row_index == 0:
                continue

            (part, trial, time, mass, energy, percent_mass) = row

            if mass != "":
                if part == "Variable oxidizer":
                    mass_oxidizer.add_row(float(time), float(mass), trial)
                    percent_mass_oxidizer.add_row(float(time), float(percent_mass[:-1]), trial)
                else:
                    mass_catalyst.add_row(float(time), float(mass), trial)
                    percent_mass_catalyst.add_row(float(time), float(percent_mass[:-1]), trial)

            if energy != "":
                if part == "Variable oxidizer":
                    energy_oxidizer.add_row(float(time), float(energy), trial)
                else:
                    energy_catalyst.add_row(float(time), float(energy), trial)

        return mass_oxidizer, mass_catalyst, energy_oxidizer, energy_catalyst, percent_mass_oxidizer, percent_mass_catalyst


def graph(axis, database: Database, title=None, y_axis_label=None, percent=False, trend=True):
    for trial in database.time.keys():
        x = np.array(database.time[trial])
        y = np.array(database.value[trial])
        if trend:
            color = next(plt.gca()._get_lines.prop_cycler)['color']

            equation = np.poly1d(np.polyfit(x, y, 8))

            axis.plot(x, y, ".", label=trial, color=color)
            axis.plot(x, equation(x), color=color, alpha=0.5)
        else:
            axis.plot(x, y, label=trial, marker=".")

    axis.legend()

    plt.gca().set_xlabel("Time elapsed since ignition (s)")

    if y_axis_label is not None:
        axis.set_ylabel(y_axis_label)

    if title is not None:
        axis.set_title(title)

    if percent:
        axis.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter())


def prepare_sub_plot(title):
    fig, axes = plt.subplots(2, 1, sharex="col")
    fig.set_size_inches(8, 10)
    fig.tight_layout()
    fig.suptitle(title, fontsize="x-large")

    return axes


def main():
    (mass_oxidizer, mass_catalyst, energy_oxidizer, energy_catalyst, percent_mass_oxidizer,
     percent_mass_catalyst) = parse_data_from_csv()

    axes = prepare_sub_plot("Figure II - Gas produced as time passes for each trial")

    graph(axes[0], mass_oxidizer, title=PARTA_CAT,
          y_axis_label="Mass of gas produced (g)")
    graph(axes[1], mass_catalyst, title=PARTB_CAT,
          y_axis_label="Mass of gas produced (g)")

    plt.show()
    # plt.close()
    # plt.savefig("mass_of_reactants_changed_to_gas")

    axes = prepare_sub_plot("Figure III - Heat change in the water as time passes for each trial")
    graph(axes[0], energy_oxidizer, title=PARTA_CAT,
          y_axis_label="Energy absorbed by pop can (J)", trend=False)
    graph(axes[1], energy_catalyst, title=PARTB_CAT,
          y_axis_label="Energy absorbed by water (J)", trend=False)
    plt.show()

    axes = prepare_sub_plot("Figure IV - Percent of combustion completed as time passes")
    graph(axes[0], percent_mass_oxidizer, title=PARTA_CAT, y_axis_label="Percent", percent=True)
    graph(axes[1], percent_mass_catalyst, title=PARTB_CAT, y_axis_label="Percent", percent=True)
    plt.show()


if __name__ == "__main__":
    main()
