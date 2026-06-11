import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import OccurrenceInputBoxes from "./OccurrenceInputBoxesComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";

export default function AddOccurrence() {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [loadingDropdownData, setLoadingDropdownData] = useState(true);
  const { theme } = useTheme();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { setResponse } = useOutletContext();
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  const addOccurrence = async () => {
    setLoading(true);

    const payload = {
      employee: serviceId,
      grade: formData.grade.value,
      authority: formData.authority,
      level_step: formData.levelStep.value,
      monthly_salary: formData.monthlySalary,
      annual_salary: formData.annualSalary,
      event: formData.event.value,
      percentage_adjustment: formData?.percentageAdjustment?.label || null,
      wef_date: formData.wefDate || null,
      reason: formData.reason,
    };
    try {
      const res = await api.post("api/occurrence/create/", payload);
      setFormData({
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
      });
      setResponse({
        message: "Occurrence saved",
        id: Date.now(),
      });
      setLoading(false);
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
      setLoading(false);
    }
  };

  return (
    <div
      className={`${style.editEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loadingDropdownData ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button
              className={style.addOccurrence}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/occurrence`)
              }
            >
              All Occurrences
            </button>
          )}
        </div>
      </div>
      <div className={style.inputAndButtonsSection}>
        <OccurrenceInputBoxes
          formData={formData}
          setFormData={setFormData}
          setResponse={setResponse}
          loadingDropdownData={loadingDropdownData}
          setLoadingDropdownData={setLoadingDropdownData}
        />
        <div className={style.addOccurrenceButtons}>
          <div className={style.addCancelButtons}>
            {loadingDropdownData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button
                className={!role || role === "VIEWER" ? style.displayNone : ""}
                onClick={addOccurrence}
              >
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save Occurrence"
                )}
              </button>
            )}

            {loadingDropdownData ? (
              <BaseSkeleton width={120} height={38} />
            ) : (
              <button
                className={`${style.cancelButton} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
                onClick={() =>
                  navigate(`/home/employees/${serviceId}/occurrence`)
                }
              >
                Cancel
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
