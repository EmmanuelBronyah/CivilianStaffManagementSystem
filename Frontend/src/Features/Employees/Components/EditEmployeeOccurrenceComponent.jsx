import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import OccurrenceInputBoxes from "./OccurrenceInputBoxesComponent";
import api from "../../../api";
import { useState, useEffect } from "react";
import getResponseMessages from "../../../utils/extractResponseMessage";

export default function EditEmployeeOccurrence(props) {
  const [initialData, setInitialData] = useState({});
  const [formData, setFormData] = useState({});

  const { theme } = useTheme();

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  useEffect(() => {
    const fetchOccurrence = async () => {
      try {
        const res = await api.get(`api/occurrence/${props.occurrenceId}/`);
        setInitialData({
          grade: {
            value: res.data.grade,
            label: res.data.grade_display,
          },
          authority: res.data.authority,
          levelStep: {
            value: res.data.level_step,
            label: res.data.level_step_display,
          },
          monthlySalary: res.data.monthly_salary,
          annualSalary: res.data.annual_salary,
          event: {
            value: res.data.event,
            label: res.data.event_display,
          },
          wefDate: res.data.wef_date,
          reason: res.data.reason,
          createdAt: res.data.date_added,
          createdBy: res.data.created_by_display,
          updatedAt: res.data.date_modified,
          updatedBy: res.data.updated_by_display,
        });
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchOccurrence();
  }, []);

  const updateOccurrence = async () => {
    console.log("form data -> ", formData);
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          <button
            className={style.addOccurrence}
            onClick={() => props.setCurrentOccurrencePage("List Occurrence")}
          >
            All Occurrences
          </button>
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <OccurrenceInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={props.setResponse}
        />
        <div className={style.editOccurrenceButtons}>
          <button onClick={updateOccurrence}>Save Changes</button>
          <button className={style.cancelButton}>Cancel</button>
        </div>
      </div>
    </div>
  );
}
