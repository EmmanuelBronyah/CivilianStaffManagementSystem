import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext } from "react-router-dom";
import { useState, useEffect } from "react";
import OccurrenceInputBoxes from "./OccurrenceInputBoxesComponent";
import ClipLoader from "react-spinners/ClipLoader";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";

const OccurrenceFormApply = () => {
  const [formData, setFormData] = useState({});
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { setResponse } = useOutletContext();
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  const applyOccurrence = () => {
    const requiredKeys = [
      "grade",
      "authority",
      "levelStep",
      "monthlySalary",
      "annualSalary",
      "event",
      "wefDate",
      "reason",
    ];
    const keys = [];

    for (const [key, value] of Object.entries(formData)) {
      if (["grade", "levelStep", "event"].includes(key)) {
        const { value: id, label: fieldName } = value;

        if (!id || !fieldName) {
          setResponse({
            message: `Select option for ${key}`,
            type: "error",
            id: Date.now(),
          });
          return;
        }
      }

      keys.push(key);
    }
    const missingKeys = requiredKeys.filter((key) => !keys.includes(key));

    if (missingKeys.length) {
      setResponse({
        message: "All fields are required",
        type: "error",
        id: Date.now(),
      });
      return;
    }
    // Save occurrence data in local storage
    localStorage.setItem("occurrenceData", JSON.stringify(formData));

    navigate("/home/employees/apply/occurrence");
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.occurrenceForm}>
          <p>Occurrence Form</p>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <OccurrenceInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            <button
              className={!role || role === "VIEWER" ? style.displayNone : ""}
              onClick={applyOccurrence}
            >
              Continue
            </button>
            <button
              className={`${style.cancelButton} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
              onClick={() => navigate(`/home/employees`)}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OccurrenceFormApply;
