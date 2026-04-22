import { useEffect, useState } from "react";
import style from "../../../styles/components/employees.module.css";
import Select from "react-select";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import useFetchUserRole from "../../hooks/fetchUserRoleHook";
import isReadOnly from "../utils/assignReadOnly";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";

export default function PrimaryComponentInputBoxes(props) {
  const [units, setUnits] = useState([]);
  const [grades, setGrades] = useState([]);
  const [gender, setGender] = useState([]);
  const [region, setRegion] = useState([]);
  const [maritalStatus, setMaritalStatus] = useState([]);
  const [religion, setReligion] = useState([]);
  const [structure, setStructure] = useState([]);
  const [bloodGroup, setBloodGroup] = useState([]);
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  useEffect(() => {
    const fetchAllDropdownData = async () => {
      try {
        const res = await api.get("api/employees/staff/options/");
        props.setLoadingData(false);
        setUnits(res.data.units || []);
        setGrades(res.data.grades || []);
        setGender(res.data.gender || []);
        setRegion(res.data.region || []);
        setMaritalStatus(res.data.marital_status || []);
        setReligion(res.data.religion || []);
        setStructure(res.data.structure || []);
        setBloodGroup(res.data.blood_group || []);
      } catch (error) {
        props.setLoadingData(false);
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };

    fetchAllDropdownData();
  }, []);

  const labelsAndInputType = [
    ["Service ID", "text", "input"],
    ["Last Name", "text", "input"],
    ["Other Names", "text", "input"],

    ["SSNIT Number", "text", "input"],
    ["Category", "text", "input"],
    ["Appointment Date", "date", "input"],

    ["Confirmation Date", "date", "input"],
    ["Probation", "text", "input"],
    ["Entry Qualification", "text", "input"],

    ["Unit", "text", "dropdown"],
    ["Grade", "text", "dropdown"],
    ["Station", "text", "input"],

    ["Date of Birth", "date", "input"],
    ["Age", "text", "input"],
    ["Gender", "text", "dropdown"],

    ["Hometown", "text", "input"],
    ["Region", "text", "dropdown"],
    ["Nationality", "text", "input"],

    ["Address", "text", "input"],
    ["Email", "email", "input"],
    ["Marital Status", "text", "dropdown"],

    ["Religion", "text", "dropdown"],
    ["Structure", "text", "dropdown"],
    ["Blood Group", "text", "dropdown"],

    ["Disable", "checkbox", "input"],
  ];

  const customSelectStyles = {
    control: (base) => ({
      ...base,
      height: "calc(2.5rem + 1vh)",
      minHeight: "calc(2.5rem + 1vh)",
      width: "95%",
      marginTop: "0.28rem",
      borderRadius: "2rem",
      border: "1px solid var(--employeeComponent-input-borderColor)",
      fontWeight: "bold",
      fontSize: "1.05rem",
      backgroundColor: "var(--employeeComponent-input-backgroundColor)",
      color: "var(--employeeComponent-input-color)",
      paddingLeft: "0.5rem",
      boxShadow: "none",

      display: "flex",
      alignItems: "center",

      "&:hover": {
        border: "1px solid var(--employeeComponent-input-borderColor)",
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
      color: "var(--employeeComponent-input-color)",
      margin: 0,
    }),

    placeholder: (base) => ({
      ...base,
      color: "var(--employeeComponent-input-color)",
      margin: 0,
    }),

    menu: (base) => ({
      ...base,
      backgroundColor: "var(--employeeComponent-input-backgroundColor)",
    }),

    option: (base, state) => ({
      ...base,
      backgroundColor: state.isFocused
        ? "var(--employeeComponent-input-backgroundColor)"
        : "white",

      color: "var(--employeeComponent-input-color)",
      fontWeight: "bold",

      cursor: "pointer",
    }),
  };

  const createOptions = (label) => {
    switch (label) {
      case "Unit":
        return units.map((unit) => ({ value: unit.id, label: unit.unit_name }));
      case "Grade":
        return grades.map((grade) => ({
          value: grade.id,
          label: grade.grade_name,
        }));
      case "Gender":
        return gender.map((gender) => ({
          value: gender.id,
          label: gender.sex,
        }));
      case "Region":
        return region.map((region) => ({
          value: region.id,
          label: region.region_name,
        }));
      case "Marital Status":
        return maritalStatus.map((maritalStatus) => ({
          value: maritalStatus.id,
          label: maritalStatus.marital_status_name,
        }));
      case "Religion":
        return religion.map((religion) => ({
          value: religion.id,
          label: religion.religion_name,
        }));
      case "Structure":
        return structure.map((structure) => ({
          value: structure.id,
          label: structure.structure_name,
        }));
      case "Blood Group":
        return bloodGroup.map((bloodGroup) => ({
          value: bloodGroup.id,
          label: bloodGroup.blood_group_name,
        }));
      default:
        return [];
    }
  };

  const labelKey = (label) => {
    switch (label) {
      case "Service ID":
        return "serviceId";
      case "Last Name":
        return "lastName";
      case "Other Names":
        return "otherNames";
      case "SSNIT Number":
        return "socialSecurity";
      case "Category":
        return "category";
      case "Appointment Date":
        return "appointmentDate";
      case "Confirmation Date":
        return "confirmationDate";
      case "Probation":
        return "probation";
      case "Entry Qualification":
        return "entryQualification";
      case "Unit":
        return "unit";
      case "Grade":
        return "grade";
      case "Station":
        return "station";
      case "Date of Birth":
        return "dob";
      case "Age":
        return "age";
      case "Gender":
        return "gender";
      case "Hometown":
        return "hometown";
      case "Region":
        return "region";
      case "Nationality":
        return "nationality";
      case "Address":
        return "address";
      case "Email":
        return "email";
      case "Marital Status":
        return "maritalStatus";
      case "Religion":
        return "religion";
      case "Structure":
        return "structure";
      case "Blood Group":
        return "bloodGroup";
      case "Disable":
        return "disable";
      default:
        return label.toLowerCase();
    }
  };

  const createDropdown = (label, role) => {
    const options = createOptions(label);
    return (
      <Select
        isDisabled={role && isReadOnly(label, role)} // Disable dropdown due to user's role
        styles={customSelectStyles}
        options={options}
        placeholder={`Select ${label}`}
        value={props.formData[labelKey(label)]}
        onChange={(selected) =>
          props.setFormData((prev) => ({
            ...prev,
            [labelKey(label)]: selected,
          }))
        }
      />
    );
  };

  const fields = labelsAndInputType.map(([label, type, state]) => {
    return (
      <div key={label}>
        {props.loadingData ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}
        <div>
          {state === "input" ? (
            props.loadingData ? (
              <BaseSkeleton height={40} />
            ) : (
              <input
                disabled={role && isReadOnly(label, role)} // Disable checkbox due to user's role
                readOnly={role && isReadOnly(label, role)} // Disable text input due to user's role
                className={`${style.primaryPageInputs} ${
                  type === "checkbox" && style.checkbox
                }`}
                type={type}
                {...(type === "checkbox"
                  ? { checked: props.formData[labelKey(label)] }
                  : { value: props.formData[labelKey(label)] })}
                onChange={(e) =>
                  props.setFormData((prev) => ({
                    ...prev,
                    [labelKey(label)]:
                      type === "checkbox" ? e.target.checked : e.target.value,
                  }))
                }
              />
            )
          ) : props.loadingData ? (
            <BaseSkeleton height={40} />
          ) : (
            createDropdown(label, role)
          )}
        </div>
      </div>
    );
  });

  return fields;
}
