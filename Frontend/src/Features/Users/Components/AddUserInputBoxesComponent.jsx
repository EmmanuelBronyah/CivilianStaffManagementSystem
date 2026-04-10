import style from "../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import { useEffect, useState } from "react";
import api from "../../../api";

export default function AddUserInputBoxes({ formData, setFormData }) {
  const [divisions, setDivisions] = useState([]);
  const [grades, setGrades] = useState([]);
  const roles = [
    { id: 1, name: "ADMINISTRATOR" },
    { id: 2, name: "STANDARD USER" },
    { id: 3, name: "VIEWER" },
  ];

  useEffect(() => {
    const fetchDivisionsAndGrades = async () => {
      try {
        const res = await api.get("api/employees/divisions-grades/");
        setDivisions(res.data.divisions || []);
        setGrades(res.data.grades || []);
      } catch (error) {
        console.error(error.response || error);
      }
    };
    fetchDivisionsAndGrades();
  }, []);

  const labelsAndInputType = [
    ["Full Name", "text", "input"],
    ["Username", "text", "input"],
    ["Email Address", "email", "input"],
    ["Role", "text", "dropdown"],
    ["Password", "password", "input"],
    ["Confirm Password", "password", "input"],
    ["Grade", "text", "dropdown"],
    ["Division", "text", "dropdown"],
  ];

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

  const createOptions = (label) => {
    switch (label) {
      case "Role":
        return roles.map((role) => ({ value: role.id, label: role.name }));
      case "Grade":
        return grades.map((grade) => ({
          value: grade.id,
          label: grade.grade_name,
        }));
      case "Division":
        return divisions.map((division) => ({
          value: division.id,
          label: division.division_name,
        }));
      default:
        return [];
    }
  };

  const createDropdown = (label) => {
    const options = createOptions(label);
    return (
      <Select
        styles={customSelectStyles}
        options={options}
        placeholder={`Select ${label}`}
        value={formData[labelKey(label)]}
        onChange={(selected) =>
          setFormData((prev) => ({ ...prev, [labelKey(label)]: selected }))
        }
      />
    );
  };

  const labelKey = (label) => {
    switch (label) {
      case "Full Name":
        return "fullName";
      case "Username":
        return "username";
      case "Email Address":
        return "email";
      case "Password":
        return "password";
      case "Confirm Password":
        return "confirmPassword";
      case "Role":
        return "role";
      case "Grade":
        return "grade";
      case "Division":
        return "division";
      default:
        return label.toLowerCase();
    }
  };

  return (
    <div className={style.addUserInputs}>
      {labelsAndInputType.map(([label, type, state]) => (
        <div key={label} className={style.labelInputContainer}>
          <label>{label}</label>
          {state === "input" ? (
            <input
              type={type}
              value={formData[labelKey(label)]}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  [labelKey(label)]: e.target.value,
                }))
              }
            />
          ) : (
            createDropdown(label)
          )}
        </div>
      ))}
    </div>
  );
}
