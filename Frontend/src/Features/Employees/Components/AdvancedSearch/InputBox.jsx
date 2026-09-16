import style from "../../../../styles/components/advancedsearch.module.css";
import { inputRecordData, allLabelKeys } from "./constants";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import api from "../../../../api";
import Select from "react-select";
import {
  dropdownDataAPIEndpoints,
  dropdownConfig,
  rangeDropdownOptions,
} from "./constants";

export default function InputBox(props) {
  const [dropdownData, setDropdownData] = useState({});
  const { setResponse } = useOutletContext();

  useEffect(() => {
    const fetchAllDropdownData = async () => {
      try {
        const res = await api.get(dropdownDataAPIEndpoints[props.record]);
        setDropdownData(res.data);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };

    fetchAllDropdownData();
  }, [props.record]);

  const inputData = inputRecordData[props.record].find(
    ([label]) => props.label === label,
  );
  const [, inputType, inputStructure] = inputData || [];

  const customSelectStyles = {
    control: (base) => ({
      ...base,
      height: "calc(2.5rem + 1vh)",
      minHeight: "calc(2.5rem + 1vh)",
      width: "100%",
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
    const config = dropdownConfig[label];

    if (!config) {
      return [];
    }

    const { dataKey, valueKey, labelKey } = config;
    const data = dropdownData[dataKey] || [];

    return data.map((item) => ({
      value: item[valueKey],
      label: item[labelKey],
    }));
  };

  const createDropdown = (label) => {
    const options = createOptions(label);

    return (
      <Select
        styles={customSelectStyles}
        options={options}
        value={
          props.formData?.[props.record]?.[allLabelKeys[props.label]] || ""
        }
        onChange={(selected) =>
          props.setFormData((prev) => ({
            ...prev,
            [props.record]: {
              ...prev[props.record],
              [allLabelKeys[props.label]]: selected,
            },
          }))
        }
      />
    );
  };

  const createRangeDropdown = () => {
    return (
      <Select
        styles={customSelectStyles}
        options={rangeDropdownOptions}
        value={props.rangeOption}
        onChange={(selected) => props.setRangeOption(selected)}
      />
    );
  };

  const isRangeField = (label) =>
    label.toLowerCase().includes("date") ||
    label.toLowerCase().includes("age") ||
    label.toLowerCase().includes("salary") ||
    label.toLowerCase().includes("probation");

  return (
    <div className={style.inputContainer}>
      <div>
        <label>{props.label}</label>
      </div>
      {inputStructure === "dropdown" ? (
        createDropdown(props.label)
      ) : isRangeField(props.label) ? (
        createRangeDropdown()
      ) : (
        <input
          className={inputType === "checkbox" ? style.checkbox : ""}
          placeholder={props.label === "Duration" ? "Number of years..." : ""}
          type={inputType}
          {...(inputType === "checkbox"
            ? {
                checked:
                  props.formData?.[props.record]?.[allLabelKeys[props.label]] ||
                  false,
              }
            : {
                value:
                  props.formData?.[props.record]?.[allLabelKeys[props.label]] ??
                  "",
              })}
          onChange={(e) => {
            props.setFormData((prev) => ({
              ...prev,
              [props.record]: {
                ...prev[props.record],
                [allLabelKeys[props.label]]:
                  inputType === "checkbox" ? e.target.checked : e.target.value,
              },
            }));
          }}
        />
      )}
    </div>
  );
}
