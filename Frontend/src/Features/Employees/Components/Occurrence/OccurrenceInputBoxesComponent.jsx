import style from "../../../../styles/components/employees.module.css";
import Select from "react-select";
import { useEffect, useState } from "react";
import api from "../../../../api";
import ReadOnlyEmployeeData from "../EmployeeCore/ReadOnlyEmployeeDataComponent";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { MdEdit, MdEditOff } from "react-icons/md";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { useMatch } from "react-router-dom";

export default function OccurrenceInputBoxes(props) {
  const [levelStep, setLevelStep] = useState([]);
  const [grades, setGrades] = useState([]);
  const [events, setEvents] = useState([]);
  const [editStatus, setEditStatus] = useState(false);
  const isEditPage = useMatch(
    "/home/employees/:serviceId/occurrence/edit/:occurrenceId",
  );

  const [displayPercentageDropdown, setDisplayPercentageDropdown] =
    useState(false);
  const [salaryPercentageAdjustments, setSalaryPercentageAdjustments] =
    useState([]);
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  }, [response]);

  useEffect(() => {
    if (!displayPercentageDropdown) {
      // Remove percentageAdjustment key-value pair from the formData if the percentage dropdown is not displayed
      props.setFormData(({ percentageAdjustment, ...prev }) => prev);
    }
  }, [displayPercentageDropdown]);

  useEffect(() => {
    const selectedEvent = props.formData.event?.label;

    if (selectedEvent !== "Salary Adjustment") return;
    editStatus
      ? setDisplayPercentageDropdown(false)
      : setDisplayPercentageDropdown(true);
  }, [props.formData.event?.label]);

  useEffect(() => {
    const showPercentageDropdown = () => {
      const selectedEvent = props.formData.event?.label;
      if (selectedEvent !== "Salary Adjustment") return;
      editStatus
        ? setDisplayPercentageDropdown(false)
        : setDisplayPercentageDropdown(true);
    };
    showPercentageDropdown();
  }, [editStatus]);

  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const res = await api.get("api/occurrence/data/options/");
        setGrades(res.data.grades || []);
        setLevelStep(res.data.level_step || []);
        setEvents(res.data.event || []);
        setSalaryPercentageAdjustments(
          res.data.salary_adjustment_percentage || [],
        );
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
    ["Grade", "text", "dropdown"],
    ["Authority", "text", "input"],
    ["LevelStep", "text", "dropdown"],
    ["Monthly Salary", "text", "input"],
    ["Annual Salary", "text", "input"],
    ["Event", "text", "dropdown"],
    ["Percentage", "text", "dropdown"],
    ["WEF Date", "date", "input"],
    ["Reason", "text", "input"],
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
      case "Grade":
        return grades.map((grade) => ({
          value: grade.id,
          label: grade.grade_name,
        }));
      case "LevelStep":
        return levelStep.map((levStep) => ({
          value: levStep.id,
          label: levStep.level_step,
        }));
      case "Event":
        return events.map((event) => ({
          value: event.id,
          label: event.event_name,
        }));
      case "Percentage":
        return salaryPercentageAdjustments.map((salary) => ({
          value: salary.id,
          label: salary.percentage_adjustment,
        }));
      default:
        return [];
    }
  };

  const assignReadOnly = (label) => {
    if (editStatus && role !== "VIEWER") {
      return false;
    }

    return (
      ["Monthly Salary", "Annual Salary"].includes(label) || role === "VIEWER"
    );
  };

  const verifyLevelStepToAssignSalary = async (label, levelStep) => {
    if (label !== "LevelStep") return;

    try {
      const res = await api.get(
        `api/occurrence/level-step/${levelStep}/annual-salary/`,
      );
      props.setFormData((prev) => ({
        ...prev,
        monthlySalary: res.data.monthly_salary,
        annualSalary: res.data.annual_salary,
      }));
    } catch (error) {
      props.setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };

  const verifyEventToDisplayPercentageDropdown = (label, eventName) => {
    if (label !== "Event") return;

    if (eventName !== "Salary Adjustment") {
      setDisplayPercentageDropdown(false);
      return;
    }

    editStatus
      ? setDisplayPercentageDropdown(false)
      : setDisplayPercentageDropdown(true);
  };

  const createDropdown = (label) => {
    const options = createOptions(label);
    return (
      <Select
        isDisabled={assignReadOnly(label)}
        styles={customSelectStyles}
        options={options}
        placeholder={`Select ${label}`}
        value={props.formData[labelKey(label)]}
        onChange={(selected) => {
          verifyLevelStepToAssignSalary(label, selected.value);
          verifyEventToDisplayPercentageDropdown(label, selected.label);
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
      case "Grade":
        return "grade";
      case "Authority":
        return "authority";
      case "LevelStep":
        return "levelStep";
      case "Monthly Salary":
        return "monthlySalary";
      case "Annual Salary":
        return "annualSalary";
      case "Event":
        return "event";
      case "Percentage":
        return "percentageAdjustment";
      case "WEF Date":
        return "wefDate";
      case "Reason":
        return "reason";
      default:
        return label.toLowerCase();
    }
  };

  const fields = labelsAndInputType.map(([label, type, state]) => {
    if (label === "Percentage" && !displayPercentageDropdown) return;

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
                readOnly={assignReadOnly(label)}
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
          {["Monthly Salary", "Annual Salary"].includes(label) && (
            <>
              <MdEdit
                className={`${style.editIcon}
                 ${editStatus || props.loadingData ? style.displayNone : ""}
                 ${role === "VIEWER" && style.displayNone}
                `}
                onClick={() => {
                  setEditStatus((prev) => !prev);
                }}
              />
              <MdEditOff
                className={`
                  ${style.editIcon} 
                  ${props.loadingData && style.displayNone}
                  ${editStatus ? "" : style.displayNone} 
                  ${role === "VIEWER" && style.displayNone}
                  `}
                onClick={() => {
                  setEditStatus((prev) => !prev);
                }}
              />
            </>
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
