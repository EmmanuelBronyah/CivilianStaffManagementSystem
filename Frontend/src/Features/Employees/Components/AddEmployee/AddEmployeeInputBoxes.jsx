import style from "../../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import { useEffect, useState } from "react";
import api from "../../../../api";
import ReadOnlyUserData from "../../../Users/Components/AddReadOnlyUserData";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { adminAndStandardUserCanEdit } from "../../utils/assignReadOnly";

export default function AddEmployeeInputBoxes(props) {
  const [units, setUnits] = useState([]);
  const [gender, setGender] = useState([]);
  const [grades, setGrades] = useState([]);
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const res = await api.get("api/employees/options/add/");
        setUnits(res.data.units || []);
        setGender(res.data.gender || []);
        setGrades(res.data.grades || []);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchDropdownData();
  }, []);

  const labelsAndInputType = [
    ["Service ID", "text", "input"],
    ["Last Name", "text", "input"],
    ["Other Names", "text", "input"],
    ["SSNIT Number", "text", "input"],
    ["Gender", "text", "dropdown"],
    ["Date of Birth", "date", "input"],
    ["Appointment Date", "date", "input"],
    ["Unit", "text", "dropdown"],
    ["Grade", "text", "dropdown"],
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
      case "Gender":
        return gender.map((gender) => ({
          value: gender.id,
          label: gender.sex,
        }));
      case "Unit":
        return units.map((unit) => ({
          value: unit.id,
          label: unit.unit_name,
        }));
      case "Grade":
        return grades.map((grade) => ({
          value: grade.id,
          label: grade.grade_name,
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
        value={props.formData[labelKey(label)]}
        isDisabled={role ? adminAndStandardUserCanEdit(role) : true}
        readOnly={role ? adminAndStandardUserCanEdit(role) : true}
        onChange={(selected) =>
          props.setFormData((prev) => ({
            ...prev,
            [labelKey(label)]: selected,
          }))
        }
      />
    );
  };

  const labelKey = (label) => {
    switch (label) {
      case "Service ID":
        return "serviceId";
      case "Last Name":
        return "lastName";
      case "Other Names":
        return "otherNames";
      case "Date of Birth":
        return "dob";
      case "Gender":
        return "gender";
      case "Unit":
        return "unit";
      case "Appointment Date":
        return "appointmentDate";
      case "SSNIT Number":
        return "ssnitNumber";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map(([label, type, state]) => {
    return (
      <div key={label} className={style.labelInputContainer}>
        {props.loading ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}

        {state === "input" ? (
          props.loading ? (
            <BaseSkeleton height={40} />
          ) : (
            <input
              type={type}
              value={props.formData[labelKey(label)]}
              disabled={role ? adminAndStandardUserCanEdit(role) : true}
              readOnly={role ? adminAndStandardUserCanEdit(role) : true}
              onChange={(e) =>
                props.setFormData((prev) => ({
                  ...prev,
                  [labelKey(label)]: e.target.value,
                }))
              }
            />
          )
        ) : props.loading ? (
          <BaseSkeleton height={40} />
        ) : (
          createDropdown(label)
        )}
      </div>
    );
  });

  return <div className={style.addUserInputs}>{fields}</div>;
}
