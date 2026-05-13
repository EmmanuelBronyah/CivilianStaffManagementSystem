import style from "../../../../styles/components/userscomponent.module.css";
import Select from "react-select";
import { useEffect, useState } from "react";
import api from "../../../../api";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useMatch } from "react-router-dom";

export default function ChildrenInputBoxes({
  loadingData,
  formData,
  setFormData,
  setResponse,
}) {
  const [gender, setGender] = useState([]);
  const isUpdatePage = useMatch(
    "/home/employees/:serviceId/children/edit/:childId",
  );

  useEffect(() => {
    const fetchGender = async () => {
      try {
        const res = await api.get("api/employees/genders/");
        setGender(res.data);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchGender();
  }, []);

  const labelsAndInputType = [
    ["Child Name", "text", "input"],
    ["Date Of Birth", "date", "input"],
    ["Gender", "text", "dropdown"],
    ["Other Parent", "text", "input"],
    ["Authority", "text", "input"],
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
      case "Child Name":
        return "childName";
      case "Date Of Birth":
        return "dob";
      case "Gender":
        return "gender";
      case "Other Parent":
        return "otherParent";
      case "Authority":
        return "authority";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map(([label, type, state]) => {
    return (
      <div key={label} className={style.labelInputContainer}>
        {loadingData ? (
          <BaseSkeleton height={30} width={150} />
        ) : (
          <label>{label}</label>
        )}

        {state === "input" ? (
          loadingData ? (
            <BaseSkeleton height={40} />
          ) : (
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
          )
        ) : loadingData ? (
          <BaseSkeleton height={40} />
        ) : (
          createDropdown(label)
        )}
      </div>
    );
  });

  return (
    <div className={style.addUserInputs}>
      {fields}
      {isUpdatePage && (
        <ReadOnlyEmployeeData loading={loadingData} formData={formData} />
      )}
    </div>
  );
}
