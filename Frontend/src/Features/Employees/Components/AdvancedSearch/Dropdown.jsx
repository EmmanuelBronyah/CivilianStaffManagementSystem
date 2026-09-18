import Select from "react-select";
import {
  childrenLabels,
  courseLabels,
  employeeLabels,
  identityLabels,
  nextOfKinLabels,
  occurrenceLabels,
  previousGovernmentServiceLabels,
  serviceWithForcesLabels,
  spouseLabels,
  terminationOfAppointmentLabels,
  absencesLabels,
} from "./constants";

export default function Dropdown(props) {
  const customSelectStyles = {
    control: (base) => ({
      ...base,
      height: "calc(2.5rem + 1vh)",
      minHeight: "calc(2.5rem + 1vh)",
      borderRadius: "2rem",
      border: "1px solid var(--userComponent-input-borderColor)",
      fontWeight: "bold",
      fontSize: "1.05rem",
      backgroundColor: "var(--userComponent-input-backgroundColor)",
      color: "var(--userComponent-input-color)",
      paddingLeft: "0.5rem",
      boxShadow: "none",

      display: "flex",
      alignItems: "center",

      "&:hover": {
        border: "1px solid var(--userComponent-input-borderColor)",
      },
    }),

    valueContainer: (base) => ({
      ...base,
      height: "100%",
      display: "flex",
      alignItems: "center",
      paddingLeft: "0.5rem",
    }),

    indicatorsContainer: (base) => ({
      ...base,
      height: "100%",
      display: "flex",
      alignItems: "center",
    }),

    singleValue: (base) => ({
      ...base,
      color: "var(--userComponent-input-color)",
      margin: 0,
    }),

    placeholder: (base) => ({
      ...base,
      color: "var(--userComponent-input-color)",
      margin: 0,
    }),

    menu: (base) => ({
      ...base,
      backgroundColor: "var(--userComponent-input-backgroundColor)",
    }),

    option: (base, state) => ({
      ...base,
      backgroundColor: state.isFocused
        ? "var(--userComponent-input-backgroundColor)"
        : "white",

      color: "var(--userComponent-input-color)",
      fontWeight: "bold",

      cursor: "pointer",
    }),
  };

  const createOptions = (record) => {
    let value = 0;

    switch (record) {
      case "Employee":
        return employeeLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Occurrence":
        return occurrenceLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Children":
        return childrenLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Spouse":
        return spouseLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Absence":
        return absencesLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Identity":
        return identityLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Termination of Appointment":
        return terminationOfAppointmentLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Service With Forces":
        return serviceWithForcesLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Emergency | Next of Kin":
        return nextOfKinLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Course":
        return courseLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      case "Previous Government Service":
        return previousGovernmentServiceLabels.map(([label]) => {
          value = value + 1;
          return { value: value, label: label };
        });
      default:
        break;
    }
  };

  if (props.record) {
    const options = createOptions(props.record);

    return (
      <Select
        styles={customSelectStyles}
        options={options}
        value={props.dropdownData}
        onChange={(selected) => props.setDropdownData(selected)}
      />
    );
  }

  return <Select styles={customSelectStyles} />;
}
