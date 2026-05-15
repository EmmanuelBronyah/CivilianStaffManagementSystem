import style from "../../../../styles/components/employees.module.css";
import Select from "react-select";
import { useEffect, useState } from "react";
import api from "../../../../api";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdEdit, MdEditOff } from "react-icons/md";
import { useMatch } from "react-router-dom";

export default function ServiceWithForcesInputBoxes(props) {
  const [units, setUnits] = useState([]);
  const [militaryRanks, setMilitaryRanks] = useState([]);
  const isEditPage = useMatch(
    "/home/employees/:serviceId/serviceWithForces/edit/:serviceWithForcesId",
  );

  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const res = await api.get(
          "api/service-with-forces/list-ranks-and-units/",
        );
        setMilitaryRanks(res.data.military_ranks || []);
        setUnits(res.data.units || []);
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
    ["Service Date", "date", "input"],
    ["Last Unit", "text", "dropdown"],
    ["Service Number", "text", "input"],
    ["Military Rank", "text", "dropdown"],
  ];

  const customSelectStyles = {
    control: (base) => ({
      ...base,
      height: "calc(2.5rem + 1vh)",
      width: "92.8%",
      marginTop: "0.28rem",
      borderRadius: "2rem",
      border: "1px solid var(--employeeComponent-input-borderColor)",
      fontWeight: "bold",
      fontSize: "1.05rem",
      backgroundColor: "var(--employeeComponent-input-backgroundColor)",
      color: "var(--employeeComponent-input-color)",
      paddingLeft: "1rem",
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
      case "Last Unit":
        return units.map((unit) => ({
          value: unit.id,
          label: unit.unit_name,
        }));
      case "Military Rank":
        return militaryRanks.map((militaryRank) => ({
          value: militaryRank.id,
          label: militaryRank.rank,
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
        onChange={(selected) => {
          props.setFormData((prev) => ({
            ...prev,
            [labelKey(label)]: selected,
          }));
        }}
      />
    );
  };

  const labelKey = (label) => {
    switch (label) {
      case "Military Rank":
        return "militaryRank";
      case "Service Date":
        return "serviceDate";
      case "Service Number":
        return "serviceId";
      case "Last Unit":
        return "lastUnit";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map(([label, type, state]) => {
    return (
      <div key={label}>
        {props.loadingData ? (
          <BaseSkeleton height={35} width={150} />
        ) : (
          <label>{label}</label>
        )}
        <div className={style.occurrenceInputContainer}>
          {state === "input" ? (
            props.loadingData ? (
              <BaseSkeleton height={45} />
            ) : (
              <input
                className={style.primaryPageInputs}
                type={type}
                value={props.formData[labelKey(label)]}
                onChange={(e) => {
                  props.setFormData((prev) => ({
                    ...prev,
                    [labelKey(label)]: e.target.value,
                  }));
                }}
              />
            )
          ) : props.loadingData ? (
            <BaseSkeleton height={45} />
          ) : (
            createDropdown(label)
          )}
        </div>
      </div>
    );
  });

  return (
    <div className={style.occurrenceInputs}>
      {fields}
      {isEditPage && (
        <ReadOnlyEmployeeData
          formData={props.formData}
          loading={props.loadingData}
        />
      )}
    </div>
  );
}
